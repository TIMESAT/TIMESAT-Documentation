"""Expose only approved canonical sources to MkDocs, without moving or editing them."""

from pathlib import Path

from mkdocs.exceptions import PluginError
from mkdocs.plugins import event_priority
from mkdocs.structure.files import File

ROOT = Path(__file__).resolve().parents[1]

# Explicit publication boundary: adding a file to the checkout does not publish it.
PUBLIC_FILES = (
    "README.md",
    "user-guide/table-of-contents.md",
    "user-guide/01-introduction.md",
    "user-guide/02-software-overview.md",
    "user-guide/03-installation.md",
    "user-guide/04-input-data.md",
    "user-guide/05-scientific-methods.md",
    "user-guide/06-parameters-and-configuration.md",
    "user-guide/07-outputs-and-quality.md",
    "user-guide/08-exploration.md",
    "user-guide/09-raster-processing.md",
    "user-guide/10-raster-processing.md",
    "user-guide/11-worked-examples.md",
    "user-guide/12-troubleshooting.md",
    "user-guide/13-reproducibility.md",
    "user-guide/appendix-a-glossary.md",
    "user-guide/appendix-b-legacy.md",
    "user-guide/appendix-c-advanced-interfaces.md",
    "user-guide/appendix-d-references.md",
    "user-guide/validation.md",
    "examples/README.md",
    "examples/generate_example.py",
    "examples/check_outputs.py",
    "examples/plot_example.py",
    "assets/README.md",
    "assets/synthetic-timeseries.png",
)

WEBSITE_FILES = (
    "stylesheets/extra.css",
    "javascripts/mathjax.js",
    "javascripts/vendor/mathjax-tex-svg-3.2.2.js",
    "javascripts/vendor/mathjax-LICENSE.txt",
    "javascripts/vendor/mermaid-11.12.1.min.js",
    "javascripts/vendor/mermaid-LICENSE.txt",
    "javascripts/vendor/material-LICENSE.txt",
    "javascripts/vendor/THIRD-PARTY-NOTICES.md",
)


def checked_source(relative):
    """Reject missing files, symlinks and sources outside this repository."""
    path = ROOT / relative
    if not path.is_file() or not path.resolve().is_relative_to(ROOT):
        raise PluginError(f"Missing or outside-repository website source: {relative}")
    if any(part.is_symlink() for part in (path, *path.parents) if part != ROOT.parent):
        raise PluginError(f"Symlink is not an approved website source: {relative}")
    return path


@event_priority(100)
def on_files(files, config):
    """Use MkDocs virtual files so root Markdown remains the sole editable source."""
    # MkDocs has already added its installed theme assets at this event. Only
    # physical files from docs_dir are subject to our authored-asset allowlist.
    docs_dir = Path(config.docs_dir)
    found = {
        path.relative_to(docs_dir).as_posix()
        for path in docs_dir.rglob("*") if path.is_file()
    }
    if found != set(WEBSITE_FILES):
        unexpected = sorted(found - set(WEBSITE_FILES))
        missing = sorted(set(WEBSITE_FILES) - found)
        raise PluginError(f"Website asset allowlist mismatch: extra={unexpected}, missing={missing}")
    for relative in WEBSITE_FILES:
        checked_source("website/" + relative)
    for relative in PUBLIC_FILES:
        path = checked_source(relative)
        files.append(File.generated(config, relative, abs_src_path=str(path)))
    return files
