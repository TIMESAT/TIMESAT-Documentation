# Documentation website preparation and validation

**Date:** 18 November 2026  
**Scope:** website preparation and public-draft validation; deployment is controlled by the workflow and repository settings.

## Result

The existing [User Guide](README.md) is configured as a Material for MkDocs
website. Navigation follows the approved [table of contents](user-guide/table-of-contents.md):
four parts, thirteen chapters and four appendices, followed by supporting
validation, tutorials, figure provenance and website runtime notices.

Initial website preparation left all **26 migrated files byte-for-byte unchanged**.
Subsequent approved editorial updates clarified authorship and contribution roles
and labelled the guide **Public Draft (Under Review)**. Scientific explanations,
equations, configuration examples, tutorial scripts and the scientific figure
were preserved. The software reference versions and GUI → CLI → Core architecture
remain as stated in the guide; no application source was changed.

The build uses **Python 3.12, MkDocs 1.6.1, Material for MkDocs 9.8.1,
PyMdown Extensions 13.1, Markdown 3.11.3 and Pygments 2.21.0** in an isolated
documentation environment. All build dependencies are pinned separately from
TIMESAT's application dependencies.

## Files added

Initial website preparation added twenty-one source/configuration files and
preserved pre-existing migration work. Later approved publication preparation
updated the draft labels, attribution and website checks without rewriting the
scientific chapters.
Publication preparation also added Git attributes to preserve existing Markdown
formatting and byte-identical third-party distributions across platforms.

| Files | Purpose |
| --- | --- |
| [mkdocs.yml](mkdocs.yml) | Theme, search, extensions, strict checks and complete chapter navigation |
| [.gitignore](.gitignore) | Excludes environment, generated output, caches and local review artifacts |
| [.gitattributes](.gitattributes) | Consistent authored-text line endings and preserved upstream distribution bytes/whitespace |
| [requirements-website.txt](requirements-website.txt) | Pinned website build dependencies |
| [requirements-website-review.txt](requirements-website-review.txt) | Optional browser-validation dependencies |
| [scripts/site_hooks.py](scripts/site_hooks.py) | Explicit publication allowlist; reads canonical Markdown through virtual files |
| [scripts/check_site.py](scripts/check_site.py) | Rendered links/anchors, source preservation, search, formatting and safety checks |
| [scripts/check_browser.py](scripts/check_browser.py) | Reproducible local responsive/browser checks |
| [website/stylesheets/extra.css](website/stylesheets/extra.css) | Text branding, responsive equations and readable light/dark presentation |
| [website/javascripts/mathjax.js](website/javascripts/mathjax.js) | Equation-renderer configuration |
| [overrides/main.html](overrides/main.html) | Loads the pinned local diagram renderer before Material |
| [overrides/partials/logo.html](overrides/partials/logo.html) | Uses the project name without asserting an official logo |
| [overrides/partials/source.html](overrides/partials/source.html) | Plain repository link without live GitHub-statistics requests |
| [MathJax runtime](website/javascripts/vendor/mathjax-tex-svg-3.2.2.js) and [licence](website/javascripts/vendor/mathjax-LICENSE.txt) | Unmodified MathJax 3.2.2 SVG distribution and Apache 2.0 terms |
| [Mermaid runtime](website/javascripts/vendor/mermaid-11.12.1.min.js) and [licence](website/javascripts/vendor/mermaid-LICENSE.txt) | Unmodified Mermaid 11.12.1 distribution and MIT terms |
| [Material licence](website/javascripts/vendor/material-LICENSE.txt) | Retained theme redistribution notice |
| [Runtime notices](website/javascripts/vendor/THIRD-PARTY-NOTICES.md) | Distribution provenance, versions, licence scope and runtime hashes |
| [.github/workflows/documentation-pages.yml](.github/workflows/documentation-pages.yml) | Automatic main-branch deployment with a repository switch and optional manual runs |
| [WEBSITE.md](WEBSITE.md) | Local setup, website structure, maintenance and future deployment instructions |
| [WEBSITE-VALIDATION.md](WEBSITE-VALIDATION.md) | This results report |

The generated `site/`, `.venv-site/` and `.website-review/` directories are
ignored. They contain output/tools/evidence, not another editable manual.
No root documentation `LICENSE` was added.

## Build and structural validation

The following commands completed successfully:

```sh
python -m mkdocs build --strict
python scripts/check_site.py
```

| Check | Result |
| --- | --- |
| Strict MkDocs build | PASS; no navigation/link/anchor warnings |
| Generated HTML | 23 content pages plus one 404 page |
| Local links and resource references | 1,611 checked; no missing target |
| Anchor references | 565 checked; no missing anchor |
| Full-text search | All content pages indexed; 140 page/section entries |
| Source preservation | Initial 26-file preservation checked; later approved attribution/status edits distinguished from scientific content |
| Fenced code | All 31 blocks preserved in rendered text, including the diagram source before browser rendering |
| Tables | All 25 Markdown tables rendered, including the approved contribution table |
| Display equation | One preserved equation rendered through Arithmatex and MathJax |
| Scripts and scientific PNG downloads | Byte-identical to canonical files |
| Publication-safety patterns | 78 generated text assets checked; no flagged private path/source/credential pattern |
| Dependency consistency | `pip check` passed |
| Python tooling syntax | All three website scripts parsed successfully |
| Git whitespace and staged changes | `git diff --check` passed; nothing staged |
| Ignore rules | Environment, generated output and review directories correctly ignored |

The allowlist prevents repository metadata, tooling, environment files and
unselected content from entering the website. Theme assets are supplied by the
pinned theme package. The three published Python downloads are existing
tutorial helpers, not application implementation files. The checks do not
constitute a universal secret detector; the source selection and actual output
were also reviewed.

## Browser and visual validation

The built site was served through a temporary loopback HTTP server under the
actual project-site prefix `/TIMESAT-Documentation/`. All external browser
requests were blocked during the tests.

**Browser:** Chromium 159.0.8154.6 on Windows.  
**Layouts:** 1440 × 1000 desktop, 390 × 844 mobile-width and 360 × 800 small mobile-width.

- All 23 content pages passed at all three widths: **69 page/layout checks**.
- No whole-page horizontal overflow, HTTP resource error, JavaScript error or
  external request was observed in the final complete run.
- The responsive navigation drawer, nested Part I navigation and installation
  chapter link were exercised, together with the desktop sidebar.
- A typed full-text query, `double logistic`, returned the scientific-methods
  chapter in each layout through the actual search worker.
- Highlighted code rendered and the copy control copied the exact command text.
- The original architecture block rendered as GUI → CLI → Core, with terminal
  entry at CLI. Material's renderer uses a closed shadow root; both successful
  replacement/rendering and the actual diagram screenshot were checked.
- The equation produced a full-size SVG with valid glyphs. Oversized equations
  and tables could scroll horizontally inside their containers on mobile.
- The approved scientific image loaded with its intrinsic dimensions and scaled
  to the available width. Its axes, legend and caption were visually reviewed.
- Dark mode and its diagram were checked. The final text-link contrast measured
  **12.65:1**, exceeding the browser check's minimum ratio of 4.5:1.

Visual review caught a narrow-screen MathJax SVG sizing interaction with the
theme's generic SVG rule. Website CSS now preserves the equation's intrinsic
size and scrolls the containing region instead of shrinking it to an unreadable
point. Dark-mode link colors were also adjusted for legibility. Neither change
alters scientific Markdown. The full browser run was repeated after the final
presentation changes.

Screenshots, build logs, original-file hashes and machine-readable results are
kept locally in ignored `.website-review/`. They are not included in the site.
This is Chromium responsive-layout testing, not a claim of testing physical
phones, Safari, Firefox or every assistive technology. External scholarly
citation reachability was not re-certified by the local checker.

## Publication and rights review

- Scientific explanations, citations and reference-version statements are
  preserved. Authorship/contribution statements are approved, and the edition
  is labelled **TIMESAT 4 User Guide — Public Draft (Under Review)**.
- The existing illustration's [provenance](assets/README.md) was consulted. No
  historical artwork, application screenshot, new project logo or restricted
  dataset was introduced.
- Text branding and bundled theme controls are used. MathJax and Mermaid are
  version-pinned, served locally and accompanied by their redistribution terms;
  the MathJax package contained no separate NOTICE file. Bundled Mermaid
  dependency notices remain in the unmodified distribution.
- System fonts and local search are used. Live GitHub statistics, Google Fonts,
  analytics and external JavaScript CDN requests are unnecessary for the tested
  website. Following an external scholarly/repository link is a separate user
  action.
- These website software licences do not assign ownership of the User Guide or
  grant a new licence for its text. No documentation reuse licence is assigned.
  Public-draft publication does not imply final scientific sign-off.

No confirmed website build, navigation, responsive-rendering or disclosure
blocker remains in the tested scope. Website readiness is separate from final
scientific approval and permission to publish the guide.

## Deployment preparation and remaining checks

The workflow runs automatically on pushes to **main** and retains a manual
dispatch trigger. Automatic deployment requires repository variable
**PAGES_DEPLOYMENT_ENABLED=true**. Manual runs additionally require the deployment
input to be enabled; that input defaults to **false**. Artifact upload and
deployment use the same main-branch/event/switch conditions. It uses read-only checkout
credentials, pinned official GitHub actions, and grants `pages: write` and
`id-token: write` only to the deployment job. A `github-pages` environment is
declared, with automatic Pages enablement disabled.

The workflow's YAML, automatic/manual triggers, input default, branch/variable
gates, permission split, environment and five action commit pins were checked
locally. The commits were resolved from the official action repositories.
Server-side execution and deployment results are recorded in GitHub Actions.

The workflow does not automatically enable Pages or change repository variables
or environment policies. It creates no GitHub Release. Once the administrator's
one-time Pages setup and deployment switch are enabled, pushes to `main` trigger
automatic publication after successful validation.

After approval to activate Pages, follow [WEBSITE.md](WEBSITE.md): select
**GitHub Actions** in repository Pages settings,
configure the `github-pages` environment, enable the repository variable only
when ready, and push approved updates to `main`. Review the successful run and
the published URL, downloads, search and rendering after deployment.

One scheduled maintenance decision remains: Material's current upstream package
notice announces end of life on **5 May 2027**. The requested stack is retained;
review its maintenance plan before that date. See the
[upstream notice](https://pypi.org/project/mkdocs-material/).
