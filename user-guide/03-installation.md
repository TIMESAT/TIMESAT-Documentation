# 3 Installation and release identification

[Previous](02-software-overview.md) · [Contents](table-of-contents.md) · [Next](04-input-data.md)

**Reference versions: Core 4.4.1, CLI 1.9.2, GUI 1.6.2**

## 3.1 Choosing an environment

Use the official desktop distribution for interactive GUI work. Use an isolated Python environment for terminal processing and the supplied synthetic examples. Both follow GUI -> CLI -> Core; terminal users enter at CLI. The reference combination has been confirmed compatible by the project owner. Record the actual components used for each analysis, especially when comparing a bundled desktop application with a separately installed CLI.

Source repositories are development resources. Ordinary users do not need to clone source repositories or build Fortran to use a supported precompiled release. Keep scientific input/output directories separate from application installation folders.

## 3.2 Desktop application

1. Open the [official GUI 1.6.2 release](https://github.com/TIMESAT/TIMESAT-GUI/releases/tag/v1.6.2).
2. Select the archive for your operating system: Windows ZIP, macOS ZIP or Linux tar.gz. Preserve the archive filename and release identifier in the analysis record.
3. Extract the complete archive into an application directory. Preserve its directory structure, bundled libraries and accompanying CLI executable.
4. Start the TIMESAT application supplied in that directory. Confirm the displayed version in the application title or **Help > About TIMESAT**.
5. Begin with the small [chapter 11 dataset](11-worked-examples.md) before loading a large raster stack.

The desktop bundle supplies its own runtime components. MATLAB Runtime is not part of this installation procedure. Do not replace a bundled CLI with an unrelated executable merely because their filenames match. Record an operating-system launch error exactly and consult [chapter 12](12-troubleshooting.md); the release archive does not establish universal support for every OS revision, CPU architecture or security policy.

## 3.3 Terminal installation

The published Core 4.4.1 wheel inventory covers CPython 3.10–3.12 on Windows x86-64, Linux x86-64 and macOS ARM64. Choose a Python/platform combination with an available wheel. A general package description of cross-platform support is not a promise of a wheel for another architecture. This review's numerical examples were run with Python 3.12 on Windows; other platform procedures require their own environment record.

Create an isolated environment. For example, with Conda available:

```sh
conda create -n timesat4 python=3.12
conda activate timesat4
python -m pip install "timesat==4.4.1" "timesat-cli==1.9.2"
```

Alternatively, use a virtual environment created with a supported Python:

```sh
python -m venv .venv-timesat4
```

Activate it using the appropriate shell command:

| Shell | Activation |
| --- | --- |
| Windows PowerShell | `.\.venv-timesat4\Scripts\Activate.ps1` |
| Windows Command Prompt | `.venv-timesat4\Scripts\activate.bat` |
| POSIX shell | `. .venv-timesat4/bin/activate` |

Then run the pinned installation command above inside that environment. These are installation recipes. The checked environment used the pinned published packages with existing dependencies; a clean installation on every listed platform has not been tested. See [validation](validation.md) for the environment and scope.

## 3.4 Startup checks

```sh
python -c "import importlib.metadata as m; print('Core',m.version('timesat')); print('CLI',m.version('timesat-cli'))"
python -m timesat_cli run --help
python -c "import timesat; print('Core entry available:', hasattr(timesat,'tsfprocess'))"
```

The expected component versions are 4.4.1 and 1.9.2, and the Core entry check should print `True`. Use `run --help` for run options; the CLI also supports `migrate-config`. An import check establishes that libraries load, not that a scientific analysis is correct. Run and inspect the example next.

## 3.5 Environment and licence record

Record OS/architecture, Python, Core, CLI, GUI where used, NumPy, rasterio and relevant dependencies. Preserve a dependency listing with the analysis, for example using `python -m pip freeze`. Keep the original application archive/digest or package records for reproducibility.

Core and GUI have component-specific proprietary research/teaching terms; CLI has an MIT licence. Read the licence delivered with each component and its notices. An MIT-licensed CLI does not change Core or GUI terms. [Appendix D](appendix-d-references.md) identifies the authoritative files and citation sources without replacing their terms.

Checked environments and limitations are recorded in [validation](validation.md).
