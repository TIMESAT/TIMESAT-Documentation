# Building and maintaining the documentation website

The website uses MkDocs 1.6.1 and Material for MkDocs 9.8.1. Its content is the
existing, authoritative Markdown in this repository. Website preparation does
not constitute approval of a final scientific edition or activation of Pages.

## Sources and navigation

```text
README.md                         Guide home; also the repository entry point
user-guide/                       13 chapters, 4 appendices, contents, validation
examples/                         Original tutorial scripts and instructions
assets/                           Approved illustration and provenance
mkdocs.yml                        Website configuration and approved chapter order
requirements-website.txt          Pinned build dependencies
requirements-website-review.txt   Optional browser-check dependencies
scripts/site_hooks.py             Explicit list of canonical published files
scripts/check_site.py             Generated links, anchors, search and safety checks
scripts/check_browser.py          Local desktop/mobile Chromium checks
website/                         Website CSS and pinned, licensed browser runtimes
overrides/                       Small Material template customizations
.github/workflows/                Manual, guarded Pages deployment preparation
site/                            Generated output; ignored, never edited
```

MkDocs reads the canonical chapter files through its virtual-file API. It does
not copy them into a second editable `docs/` tree. Existing Markdown links and
headings remain intact; MkDocs turns them into website URLs during rendering.
The repository's root README becomes the website home page. Navigation follows
the approved four parts, thirteen chapters and four appendices, followed by
validation, examples, provenance and website runtime notices.

Only the explicit files in `scripts/site_hooks.py` can enter the site from this
repository, alongside the installed theme's assets. The build refuses unknown
files inside `website/`. Build instructions, workflow files, review artifacts,
the virtual environment and repository metadata do not enter the website or its
search index. Review an asset and its rights before adding it to the allowlist.

## Local setup and preview

Use Python **3.12** in a separate virtual environment. The website does not need
TIMESAT Core, CLI or GUI installed. Run these commands at this repository's root.

Windows PowerShell:

```powershell
py -3.12 -m venv .venv-site
.venv-site/Scripts/python.exe -m pip install -r requirements-website.txt
.venv-site/Scripts/python.exe -m mkdocs serve --dev-addr 127.0.0.1:8000
```

macOS/Linux:

```sh
python3.12 -m venv .venv-site
.venv-site/bin/python -m pip install -r requirements-website.txt
.venv-site/bin/python -m mkdocs serve --dev-addr 127.0.0.1:8000
```

Open the local address printed by MkDocs. The configured project-site prefix is
`/TIMESAT-Documentation/`. The preview is bound to loopback, not a public host.
Stop it with Ctrl+C. The preview watches the canonical Markdown directories as
well as the website configuration and assets. It is an HTTP preview; opening
generated HTML directly with `file://` does not provide the search worker's
normal serving environment.

## Build and validate

Use the virtual environment's Python (Windows commands shown):

```powershell
.venv-site/Scripts/python.exe -m mkdocs build --strict
.venv-site/Scripts/python.exe scripts/check_site.py
```

On macOS/Linux substitute `.venv-site/bin/python`. `site/` is generated and may
be replaced by the next build; keep source edits in the canonical Markdown,
configuration or website assets. Do not commit the environment, output or review
artifacts. The strict build treats broken Markdown links/anchors and missing
navigation targets as errors. The additional checker inspects rendered local
references, project-site paths, indexed chapters and likely confidential content.
Automated pattern checks supplement human publication review.

The source-preservation comparison used during initial website preparation is
optional for later editorial work. To check against a particular JSON file of
source-file SHA-256 hashes, add `--source-baseline path/to/snapshot.json` to
`scripts/check_site.py`. Choose a snapshot appropriate to the task; the original
website snapshot predates approved authorship and public-draft updates.

Optional browser checks:

```powershell
.venv-site/Scripts/python.exe -m pip install -r requirements-website-review.txt
$env:PLAYWRIGHT_BROWSERS_PATH = Join-Path (Get-Location) '.website-review/browsers'
.venv-site/Scripts/python.exe -m playwright install chromium
.venv-site/Scripts/python.exe scripts/check_browser.py
```

```sh
.venv-site/bin/python -m pip install -r requirements-website-review.txt
export PLAYWRIGHT_BROWSERS_PATH="$PWD/.website-review/browsers"
.venv-site/bin/python -m playwright install chromium
.venv-site/bin/python scripts/check_browser.py
```

On Linux, Playwright may additionally need its documented operating-system
browser prerequisites. The checker starts and stops a temporary loopback server
itself and tests the project prefix, all content pages at three widths, search,
navigation, code copying, equation/diagram rendering and image loading. It blocks
external browser requests. Screenshots and results are kept in ignored
`.website-review/`, outside the website output.

## Presentation, privacy and rights

- Text branding is **TIMESAT 4 User Guide**, with green navigation and a light/
  dark theme. No official TIMESAT logo has been asserted or newly designed.
  The theme's generic favicon and interface controls are theme resources.
- System fonts, local full-text search, highlighted/copyable code, scrollable
  tables, responsive navigation and accessible heading links are enabled.
- The existing equation uses PyMdown Arithmatex and locally served MathJax SVG
  output. The original Mermaid architecture block renders through the locally
  served Mermaid runtime. Scientific Markdown and diagram source are unchanged.
- MathJax 3.2.2 and Mermaid 11.12.1 are pinned and bundled with their licences;
  the theme's licence and bundled notices are retained. See
  [runtime notices](website/javascripts/vendor/THIRD-PARTY-NOTICES.md).
  These software licences do not establish a licence for the guide's text.
- The existing figure's approved provenance remains in [assets/README.md](assets/README.md).
  No new screenshot, legacy artwork or restricted dataset was added.
- No analytics, Google Fonts, external JavaScript CDN, GUI application source,
  local settings or credentials are needed by the generated site.

## GitHub Pages deployment: prepared, not activated

The intended project-site address is
`https://timesat.github.io/TIMESAT-Documentation/`. This is a configuration target,
not a claim that the site is live. No custom domain or `gh-pages` branch is used.

The workflow has **only `workflow_dispatch`**, with deployment **false** by
default. There is no push, release or pull-request deployment trigger. A manual
build without deployment does not upload a Pages artifact. Deployment also
requires the `main` branch and repository variable
`PAGES_DEPLOYMENT_ENABLED` to equal the literal string `true`.

No remote settings or variables were changed during website preparation.
After explicit publication approval, a repository administrator can:

1. Review the complete scientific/publication content and the proposed files,
   then separately authorize committing and pushing them to `main`.
2. In **Settings → Pages → Build and deployment**, select **GitHub Actions** as
   the source. Do not select a publishing branch.
3. Ensure repository/organization Actions policies permit the pinned official
   GitHub actions. The build needs `contents: read`; the deployment job alone
   receives `pages: write` and `id-token: write`. No personal access token is
   required and the workflow does not request repository write access.
4. Configure the **github-pages** environment's allowed deployment branch as
   `main`, and require a reviewer where the repository's plan/policy permits.
5. Only when ready to enable publication, create the repository **Actions
   variable** `PAGES_DEPLOYMENT_ENABLED=true` under **Settings → Secrets and
   variables → Actions → Variables**. It is a switch, not a secret.
6. In **Actions → Documentation Pages**, choose **Run workflow**, select `main`
   and deliberately enable the deployment input. Review/approve the environment
   gate if configured. The strict build and generated-site checker must pass
   before the artifact can be deployed.
7. Verify the resulting Pages URL, search, equation, diagram, downloads and
   mobile navigation. For later changes, repeat the manual review/deployment
   procedure. Removing the variable blocks future workflow deployments; taking
   an already published site offline is a separate Pages administration action.

`configure-pages` has automatic enablement disabled, so a workflow run will not
silently turn Pages on. It must already have been configured by an administrator.
The pinned action commit IDs were resolved from the official action repositories.
The GitHub workflow itself has not been run as part of local validation.

## Maintenance

Keep the Markdown as the single source and run both build/check commands after
changes. Review runtime licence notices and hashes when updating vendored assets;
re-test the equation, architecture diagram and browser network behaviour.
Update the complete requirements set deliberately, rather than upgrading a
shared application environment.

Material's current release information states that critical/security fixes
continue until **5 May 2027**, its announced end-of-life date. The requested
MkDocs/Material stack is used here; schedule a maintenance review before that
date. See the [upstream package notice](https://pypi.org/project/mkdocs-material/)
and [Material documentation](https://squidfunk.github.io/mkdocs-material/).

Implementation references: [MkDocs hooks](https://www.mkdocs.org/user-guide/configuration/#hooks),
[virtual files](https://www.mkdocs.org/dev-guide/api/#mkdocs.structure.files.File.generated),
[Material mathematics](https://squidfunk.github.io/mkdocs-material/reference/math/),
[Material diagrams](https://squidfunk.github.io/mkdocs-material/reference/diagrams/),
and [GitHub custom Pages workflows](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages).
