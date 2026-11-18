"""Exercise the built project site in Chromium, with all external requests blocked.

Optional requirements: requirements-website-review.txt and `playwright install chromium`.
Screenshots and results stay in ignored .website-review/. No remote service is used.
"""

import functools
import json
import sys
import threading
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit

from playwright.sync_api import sync_playwright

from check_site import BASE, PREFIX, destination
from site_hooks import PUBLIC_FILES, ROOT, WEBSITE_FILES


class ProjectHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if not self.path.startswith(PREFIX):
            self.send_error(404)
            return
        self.path = self.path[len(PREFIX) - 1:]
        super().do_GET()

    def log_message(self, *args):
        pass


def main():
    review = ROOT / ".website-review"
    review.mkdir(exist_ok=True)
    handler = functools.partial(ProjectHandler, directory=str(ROOT / "site"))
    server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    origin = f"http://127.0.0.1:{server.server_port}"
    base = origin + PREFIX
    problems, external, checks = [], [], []
    pages = [p for p in (*PUBLIC_FILES, *WEBSITE_FILES) if p.endswith(".md")]
    quick = "--quick" in sys.argv
    viewports = (("mobile", 390, 844), ("small-mobile", 360, 800), ("desktop", 1440, 1000))
    if quick:
        pages = pages[:1]
        viewports = viewports[:1]

    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch()
            for label, width, height in viewports:
                context = browser.new_context(
                    viewport={"width": width, "height": height},
                    color_scheme="light", reduced_motion="reduce",
                    permissions=["clipboard-read", "clipboard-write"],
                )

                def route_request(route):
                    if urlsplit(route.request.url).netloc == urlsplit(origin).netloc:
                        route.continue_()
                    else:
                        external.append(route.request.url)
                        route.abort()

                context.route("**/*", route_request)
                page = context.new_page()
                page.on("pageerror", lambda error: problems.append("JavaScript: " + str(error)))
                page.on("console", lambda message: problems.append("Console: " + message.text) if message.type == "error" else None)
                page.on("response", lambda response: problems.append(f"HTTP {response.status}: {urlsplit(response.url).path}") if response.status >= 400 else None)

                for source in pages:
                    print(f"Checking {label}: {source}", flush=True)
                    path = destination(source).removesuffix("index.html")
                    response = page.goto(base + path, wait_until="networkidle")
                    assert response and response.status == 200, source
                    page.wait_for_selector(".md-content__inner h1")
                    if "05-scientific-methods" in source:
                        page.wait_for_selector("mjx-container[jax='SVG'] svg")
                        page.evaluate("MathJax.startup.promise")
                        box = page.locator("mjx-container[jax='SVG'] svg").bounding_box()
                        assert box and box["width"] > 100 and box["height"] > 20
                        assert page.locator("mjx-merror").count() == 0
                    if "02-software-overview" in source:
                        # Material 9.8 renders Mermaid into a closed shadow root.
                        # The replacement div appears only after render() succeeds.
                        diagram = page.wait_for_selector("div.mermaid")
                        box = diagram.bounding_box()
                        assert box and box["width"] > 100 and box["height"] > 60
                    for image in page.locator(".md-content__inner img").all():
                        assert image.evaluate("e => e.complete && e.naturalWidth > 0"), source
                    dimensions = page.evaluate("({page: document.documentElement.scrollWidth, viewport: innerWidth})")
                    assert dimensions["page"] <= dimensions["viewport"] + 1, (label, source, dimensions)
                    checks.append({"viewport": label, "page": source, "page_overflow": False})

                # Explicit navigation through the responsive drawer/sidebar.
                page.goto(base, wait_until="networkidle")
                if width < 1220:
                    page.locator('label.md-header__button[for="__drawer"]').click()
                    page.screenshot(path=str(review / f"{label}-menu.png"))
                    page.locator('.md-nav--primary label.md-nav__link').filter(has_text="Getting oriented").first.click()
                installation = page.locator('.md-nav--primary a[href*="03-installation"]').first
                installation.click()
                page.wait_for_url("**/user-guide/03-installation/")
                assert "Installation" in page.locator(".md-content__inner h1").inner_text()

                # Search exercises the actual worker and results, not just index existence.
                query = page.locator('[data-md-component="search-query"]')
                toggle = page.locator('label.md-header__button[for="__search"]')
                if toggle.is_visible():
                    toggle.click()
                query.click()
                # Material observes keyup; type as a user rather than only
                # setting the value through Playwright's input-event helper.
                query.press_sequentially("double logistic", delay=20)
                try:
                    page.wait_for_selector('.md-search-result__link[href*="05-scientific-methods"]')
                except Exception:
                    page.screenshot(path=str(review / f"{label}-failed-search.png"))
                    print(json.dumps({
                        "query": query.input_value(),
                        "search_open": page.locator("#__search").is_checked(),
                        "search_text": page.locator(".md-search").inner_text()[:2000],
                        "results": page.locator(".md-search-result__link").evaluate_all("nodes => nodes.map(e => ({href:e.getAttribute('href'), rect:e.getBoundingClientRect().toJSON()}))")
                    }, indent=2), flush=True)
                    raise
                page.screenshot(path=str(review / f"{label}-search.png"))
                page.keyboard.press("Escape")

                page.goto(base + "user-guide/10-raster-processing/", wait_until="networkidle")
                assert page.locator(".highlight span").count() > 0
                button = page.locator('.md-content__inner button[data-md-type="copy"]').first
                button.click()
                copied = page.evaluate("navigator.clipboard.readText()")
                assert copied.strip() == page.locator(".highlight pre code").first.inner_text().strip()

                page.goto(base + "user-guide/02-software-overview/", wait_until="networkidle")
                page.wait_for_selector("div.mermaid")
                page.screenshot(path=str(review / f"{label}-overview.png"))
                page.goto(base + "user-guide/05-scientific-methods/#54-double-logistic-fitting", wait_until="networkidle")
                page.wait_for_selector("mjx-container svg")
                page.evaluate("MathJax.startup.promise")
                box = page.locator("mjx-container svg").bounding_box()
                assert box and box["width"] > 100 and box["height"] > 20
                if width < 600:
                    assert page.locator(".arithmatex").first.evaluate("""e => {
                      if (e.scrollWidth <= e.clientWidth) return true;
                      e.scrollLeft = 32; const moved = e.scrollLeft > 0;
                      e.scrollLeft = 0; return moved;
                    }""")
                page.screenshot(path=str(review / f"{label}-equation.png"))
                page.goto(base + "user-guide/07-outputs-and-quality/#72-seasonal-metric-dictionary", wait_until="networkidle")
                page.screenshot(path=str(review / f"{label}-table.png"))
                if width < 600:
                    assert page.locator(".md-typeset__table").count() > 0
                    assert page.locator(".md-typeset__scrollwrap").first.evaluate("""e => {
                      if (e.scrollWidth <= e.clientWidth) return true;
                      e.scrollLeft = 32; const moved = e.scrollLeft > 0;
                      e.scrollLeft = 0; return moved;
                    }""")
                page.goto(base + "user-guide/11-worked-examples/#116-repeating-and-comparing-results", wait_until="networkidle")
                image = page.locator('img[src*="synthetic-timeseries.png"]')
                image.scroll_into_view_if_needed()
                page.screenshot(path=str(review / f"{label}-figure.png"))

                # A fresh context emulates the OS preference and avoids persisted toggles.
                context.close()

            dark = browser.new_context(viewport={"width": 1440, "height": 1000}, color_scheme="dark")
            dark.route("**/*", lambda route: route.continue_() if urlsplit(route.request.url).netloc == urlsplit(origin).netloc else route.abort())
            page = dark.new_page()
            page.goto(base + "user-guide/02-software-overview/", wait_until="networkidle")
            page.wait_for_selector("div.mermaid")
            assert page.locator("body").get_attribute("data-md-color-scheme") == "slate"
            contrast = page.evaluate("""() => {
              function luminance(rgb) {
                const values = rgb.match(/[\\d.]+/g).slice(0,3).map(v => {
                  v = Number(v)/255; return v <= 0.04045 ? v/12.92 : ((v+0.055)/1.055)**2.4;
                });
                return values[0]*0.2126 + values[1]*0.7152 + values[2]*0.0722;
              }
              const foreground = luminance(getComputedStyle(document.querySelector('.md-content__inner a')).color);
              const background = luminance(getComputedStyle(document.body).backgroundColor);
              return (Math.max(foreground,background)+0.05)/(Math.min(foreground,background)+0.05);
            }""")
            assert contrast >= 4.5, ("Dark-mode text-link contrast", contrast)
            page.screenshot(path=str(review / "desktop-dark.png"))
            dark.close()
            version = browser.version
            browser.close()
    except Exception:
        print(json.dumps({"problems": problems, "external_requests": external}, indent=2), flush=True)
        raise
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)

    result = {
        "browser": "Chromium " + version,
        "mode": "quick mobile smoke test" if quick else "complete",
        "project_prefix": urlsplit(BASE).path,
        "page_viewport_checks": len(checks),
        "viewports": [f"{width}x{height}" for _, width, height in viewports],
        "navigation_search_copy_math_diagram_images": "PASS",
        "dark_text_link_contrast": round(contrast, 2),
        "external_request_attempts": sorted(set(external)),
        "problems": problems,
        "checks": checks,
    }
    name = "browser-smoke.json" if quick else "browser-validation.json"
    (review / name).write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps({k: v for k, v in result.items() if k != "checks"}, indent=2))
    assert not problems and not external, "Review browser-validation.json"


if __name__ == "__main__":
    main()
