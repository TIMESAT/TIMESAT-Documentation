"""Validate built routes, anchors, approved downloads and publication boundaries.

Run after `python -m mkdocs build --strict`. Uses only the Python standard library.
"""

import argparse
import hashlib
import json
import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit

from site_hooks import PUBLIC_FILES, ROOT, WEBSITE_FILES

SITE = ROOT / "site"
BASE = "https://timesat.github.io/TIMESAT-Documentation/"
PREFIX = urlsplit(BASE).path


class Page(HTMLParser):
    def __init__(self, text):
        super().__init__(convert_charrefs=True)
        self.ids = set()
        self.links = []
        self.tags = {}
        self.code_blocks = []
        self._pre = None
        self.math_blocks = 0
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.tags[tag] = self.tags.get(tag, 0) + 1
        if tag == "pre":
            self._pre = []
        if tag == "div" and "arithmatex" in attrs.get("class", "").split():
            self.math_blocks += 1
        if "id" in attrs:
            self.ids.add(attrs["id"])
        for attr in ("href", "src", "poster"):
            if attrs.get(attr):
                self.links.append(attrs[attr])

    def handle_data(self, text):
        if self._pre is not None:
            self._pre.append(text)

    def handle_endtag(self, tag):
        if tag == "pre" and self._pre is not None:
            self.code_blocks.append("".join(self._pre).strip("\n"))
            self._pre = None


def destination(relative):
    path = Path(relative)
    if path.suffix != ".md":
        return relative
    return (path.parent / "index.html").as_posix() if path.name == "README.md" else (
        path.with_suffix("") / "index.html"
    ).as_posix()


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--source-baseline", type=Path,
        help="Optionally compare sources with an explicitly chosen JSON hash snapshot",
    )
    args = parser.parse_args()
    assert (SITE / "index.html").is_file(), "Build the website first"
    pages = {
        p.relative_to(SITE).as_posix(): Page(p.read_text(encoding="utf-8"))
        for p in SITE.rglob("*.html")
    }
    failures = []
    links = anchors = 0
    for relative, page in pages.items():
        page_url = BASE + (relative[:-10] if relative.endswith("index.html") else relative)
        for link in page.links:
            url = urlsplit(urljoin(page_url, link))
            if url.scheme == "file":
                failures.append(f"{relative}: local filesystem URL")
            if url.scheme not in ("http", "https") or url.netloc != urlsplit(BASE).netloc:
                continue
            if not url.path.startswith(PREFIX):
                failures.append(f"{relative}: link escapes project-site prefix: {link}")
                continue
            target = unquote(url.path[len(PREFIX):])
            if not target or target.endswith("/"):
                target += "index.html"
            resolved = (SITE / target).resolve()
            links += 1
            if not resolved.is_relative_to(SITE.resolve()) or not resolved.is_file():
                failures.append(f"{relative}: missing local target: {link}")
            elif url.fragment and target in pages:
                anchors += 1
                if unquote(url.fragment) not in pages[target].ids:
                    failures.append(f"{relative}: missing anchor: {link}")

    code_blocks = tables = math_blocks = 0
    for relative in PUBLIC_FILES:
        out = SITE / destination(relative)
        if not out.is_file():
            failures.append(f"Missing canonical page/asset: {relative}")
        elif not relative.endswith(".md") and sha(out) != sha(ROOT / relative):
            failures.append(f"Modified download/figure: {relative}")
        elif relative.endswith(".md"):
            source = (ROOT / relative).read_text(encoding="utf-8")
            page = pages[destination(relative)]
            fenced = re.findall(r"^```[^\n]*\n(.*?)^```[ \t]*$", source, re.MULTILINE | re.DOTALL)
            if [block.strip("\n") for block in fenced] != page.code_blocks:
                failures.append(f"Rendered code block differs from Markdown: {relative}")
            table_count = len(re.findall(r"^\|(?:\s*:?-{3,}:?\s*\|)+\s*$", source, re.MULTILINE))
            if table_count != page.tags.get("table", 0):
                failures.append(f"Rendered table count differs from Markdown: {relative}")
            math_count = len(re.findall(r"^\$\$\s*$", source, re.MULTILINE)) // 2
            if math_count != page.math_blocks:
                failures.append(f"Rendered display-equation count differs from Markdown: {relative}")
            code_blocks += len(fenced)
            tables += table_count
            math_blocks += math_count
    for relative in WEBSITE_FILES:
        out = SITE / destination(relative)
        if not out.is_file():
            failures.append(f"Missing website asset: {relative}")

    index = json.loads((SITE / "search/search_index.json").read_text(encoding="utf-8"))
    search_locations = {doc["location"].split("#")[0] for doc in index["docs"]}
    for relative in (*PUBLIC_FILES, *WEBSITE_FILES):
        if relative.endswith(".md"):
            route = destination(relative).removesuffix("index.html")
            if route not in search_locations:
                failures.append(f"Page absent from search: {relative}")

    private = re.compile(
        r"TIMESAT-Workspace|TIMESAT-GUI-Source|documentation/planning|"
        r"OneDrive\s*-\s*Lund|[A-Z]:[\\/]Users[\\/]|"
        r"(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{30,}|"
        r"AKIA[0-9A-Z]{16}|-----BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY-----)",
        re.IGNORECASE,
    )
    forbidden_parts = {".git", ".github", ".venv-site", ".website-review", "__pycache__"}
    scanned = 0
    for file in SITE.rglob("*"):
        if not file.is_file():
            continue
        rel = file.relative_to(SITE)
        if forbidden_parts.intersection(rel.parts) or file.suffix in {".yml", ".yaml", ".env", ".docx", ".pdf", ".pyc"}:
            failures.append(f"Unexpected non-public build file: {rel.as_posix()}")
        if file.suffix in {".html", ".js", ".json", ".map", ".css", ".txt", ".py", ".xml"}:
            scanned += 1
            if private.search(file.read_text(encoding="utf-8")):
                # Report the filename, never a possible secret's contents.
                failures.append(f"Publication-safety pattern in {rel.as_posix()}")

    # The original website-preparation snapshot is historical. Approved later
    # editorial changes must not fail because that ignored local file exists.
    baseline = args.source_baseline
    preserved = None
    if baseline is not None:
        original = json.loads(baseline.read_text(encoding="utf-8"))
        preserved = sum((ROOT / f).is_file() and sha(ROOT / f) == h for f, h in original.items())
        if preserved != len(original):
            failures.append("Sources differ from the explicitly requested hash baseline")

    summary = {
        "html_pages_including_404": len(pages),
        "local_links_and_resources_checked": links,
        "anchor_targets_checked": anchors,
        "indexed_sections": len(index["docs"]),
        "publication_safety_text_files_scanned": scanned,
        "original_files_preserved": preserved,
        "code_blocks_preserved": code_blocks,
        "tables_rendered": tables,
        "display_equations_rendered": math_blocks,
        "failures": failures,
    }
    print(json.dumps(summary, indent=2))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
