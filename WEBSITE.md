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
.github/workflows/                Automatic main-branch Pages deployment and manual runs
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

- Text branding is **TIMESAT 4 User Guide**, with a blue-and-gold palette informed
  by the established TIMESAT wordmark. A white masthead, fine gold rules and
  serif reading typography give the guide a traditional handbook presentation.
  No logo artwork has been copied or newly designed.
  The theme's generic favicon and interface controls are theme resources.
- Locally available fonts, local full-text search, highlighted/copyable code, scrollable
  tables, responsive navigation and accessible heading links are enabled.
- Contents and organization links are provided in the fixed masthead. The home
  page has no footer navigation, and no page repeats the organization link in
  its footer. The documentation-source link is a separate destination.
- The single masthead provides **Contents** and **TIMESAT GitHub** without a
  second navigation bar. Small screens use labelled list/GitHub icons; the source
  link remains available in the chapter drawer. Existing chapter-opening links
  and previous/next footer navigation on reading pages are retained. The header
  override derives from the pinned Material template; review it when upgrading
  the theme.
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

## GitHub Pages deployment

The project-site address is `https://timesat.github.io/TIMESAT-Documentation/`.
No custom domain or `gh-pages` branch is used.

Every **push to `main`** runs the strict build and generated-site checks, then
automatically deploys the validated result when repository variable
`PAGES_DEPLOYMENT_ENABLED` equals the literal string `true`. Failed builds or
checks prevent deployment. Pull requests, other branches, tags and releases do
not trigger automatic publication.

`workflow_dispatch` remains available for manual runs. Its deployment input
defaults to **false**, allowing build-only checks. A manual deployment requires
selecting `main`, enabling the deployment input and keeping the same repository
switch enabled. Artifact upload and deployment share these conditions.

One-time repository configuration:

1. In **Settings → Pages → Build and deployment**, select **GitHub Actions** as
   the source, using the existing workflow.
2. Ensure repository/organization Actions policies permit the pinned official
   GitHub actions. The build needs `contents: read`; the deployment job alone
   receives `pages: write` and `id-token: write`. No personal access token is
   required and the workflow does not request repository write access.
3. Configure the **github-pages** environment's allowed deployment branch as
   `main`. Any existing environment approval rules still apply to automatic
   deployments; a required reviewer must approve the run before it proceeds.
4. When ready to enable publication, create the repository **Actions
   variable** `PAGES_DEPLOYMENT_ENABLED=true` under **Settings → Secrets and
   variables → Actions → Variables**. It is a switch, not a secret.

For routine updates, review the Markdown changes, commit and push them to
`main`, then check **Actions → Documentation Pages** for successful `build` and
`deploy` jobs. No manual workflow run is needed. Verify the resulting Pages URL,
search, equation, diagram, downloads and mobile navigation as appropriate.

If the switch is enabled after a push whose deployment was skipped, run the
workflow manually from `main` with deployment enabled, or make the next approved
push. Removing the variable or setting it to `false` pauses future deployments
while retaining build/check runs. Taking an already published site offline is a
separate Pages administration action.

`configure-pages` has automatic enablement disabled, so a workflow run will not
silently turn Pages on. It must already have been configured by an administrator.
The pinned action commit IDs were resolved from the official action repositories.
Remote execution and deployment results are available in GitHub Actions.

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
