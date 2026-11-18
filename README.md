# TIMESAT 4 User Guide — Public Draft (Under Review)

Official documentation and user guides for TIMESAT 4, CLI, and GUI.

## TIMESAT 4 User Guide

**Public Draft (Under Review) · 18 November 2026**

The TIMESAT 4 User Guide is intended for researchers, students and practitioners
analysing satellite time series and vegetation seasonality. It explains the
scientific interpretation of seasonal metrics and the roles of the graphical
user interface (GUI), command-line interface (CLI) and TIMESAT 4 Core.

The [complete table of contents](user-guide/table-of-contents.md) links all
thirteen chapters and four appendices. Begin with the approved
[Introduction](user-guide/01-introduction.md) and
[Software Overview](user-guide/02-software-overview.md), then continue with
[installation](user-guide/03-installation.md), [input preparation](user-guide/04-input-data.md),
the shared [scientific methods](user-guide/05-scientific-methods.md),
[parameters](user-guide/06-parameters-and-configuration.md) and
[outputs](user-guide/07-outputs-and-quality.md).

Follow [GUI exploration](user-guide/08-exploration.md),
[GUI raster processing](user-guide/09-raster-processing.md) or
[CLI processing](user-guide/10-raster-processing.md), then try the
[worked examples](user-guide/11-worked-examples.md). The guide also supplies
troubleshooting, reproducibility guidance and four reference appendices.

The [validation record](user-guide/validation.md) distinguishes tested examples
from untested platforms, official GUI interactions and advanced configurations.
Public-draft status does not imply independent biological accuracy or validation
of every procedure. Original tutorial code and its usage are in
[examples/](examples/README.md); approved figure provenance is in
[assets/](assets/README.md).

## Reference versions

| Component | Reference version | Publication record |
| --- | --- | --- |
| TIMESAT 4 Core | 4.4.1 | [timesat 4.4.1 on PyPI](https://pypi.org/project/timesat/4.4.1/) |
| TIMESAT CLI | 1.9.2 | [timesat-cli 1.9.2 on PyPI](https://pypi.org/project/timesat-cli/1.9.2/) |
| TIMESAT GUI | 1.6.2 | [Official GUI v1.6.2 release](https://github.com/TIMESAT/TIMESAT-GUI/releases/tag/v1.6.2) |

**These versions form a verified compatible combination.** With matching input
observations, effective processing parameters and output conventions,
corresponding scientific results should be consistent across GUI preview,
GUI batch processing and terminal runs.

These reference versions define the guide's software scope. They do not imply
that every platform, input product or parameter combination has been tested.
The publication records identify individual components; the documentation
edition is separate from the software versions.

## Processing architecture

**TIMESAT GUI -> TIMESAT CLI -> TIMESAT 4 Core**

The GUI supports interactive exploration and desktop raster processing. The CLI
organises processing and connects these workflows to Core's common scientific
calculations. Terminal users enter at the CLI layer. The
[Software Overview](user-guide/02-software-overview.md#22-processing-architecture)
explains this relationship.

## Documentation and attribution

The Markdown chapters in this repository are the authoritative editing source
for the material available here. Shared scientific concepts are described once
and apply to both GUI and CLI workflows. The chapters use that
shared reference without duplicating the scientific explanations.

Per Jönsson and Lars Eklundh are the original TIMESAT developers and scientific
founders. Zhanzhang Cai develops TIMESAT 4 Core, TIMESAT CLI and TIMESAT GUI.

Zhanzhang Cai is the lead author and editor of the current User Guide.
Lars Eklundh provides scientific and technical review, and Per Jönsson provides
scientific guidance.

The scientific explanations build on earlier TIMESAT manuals attributed to
Zhanzhang Cai, Lars Eklundh and Per Jönsson and on the cited scientific
literature. Software components retain their own licence terms; this guide does
not replace or expand them.
