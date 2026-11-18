# Website runtime notices

These notices apply to website software, not to the User Guide's scientific
text, project ownership or documentation reuse rights.

- **Material for MkDocs 9.8.1:** the theme, its bundled interface icons and
  browser assets are provided by the installed `mkdocs-material` package under
  its [MIT licence](material-LICENSE.txt). The site keeps the theme's existing
  notices. No theme icon is presented as a TIMESAT logo. System fonts are used;
  no Google Fonts request or new project logo is introduced.
- **MathJax 3.2.2:** the unmodified `es5/tex-svg.js` distribution is included as
  `mathjax-tex-svg-3.2.2.js`, under [Apache 2.0](mathjax-LICENSE.txt).
  Source: [MathJax 3.2.2](https://github.com/mathjax/MathJax/tree/3.2.2).
  SHA-256: `d4295dc33744836935c1399feece5159577b34c5c8ffb9f1c6324cd82e03a882`.
- **Mermaid 11.12.1:** the unmodified `dist/mermaid.min.js` distribution is
  included as `mermaid-11.12.1.min.js`, under its [MIT licence](mermaid-LICENSE.txt).
  Existing bundled dependency notices remain in the JavaScript file.
  Source: [Mermaid 11.12.1](https://github.com/mermaid-js/mermaid/tree/mermaid%4011.12.1).
  SHA-256: `198b19442f86f0b46a17e56d3abf744c3a28a3427e66fa8dada3b589a77babcc`.

The pinned MathJax and Mermaid distributions were obtained from jsDelivr's
version-specific npm package files. They are served locally with the website;
visitors do not need a CDN connection to render the present equation or diagram.

The existing scientific image and editable Mermaid diagram retain the
provenance recorded in the site's **Figure provenance** page (`assets/README.md`
in the repository). No historical manual artwork or additional application
screenshot was introduced.
