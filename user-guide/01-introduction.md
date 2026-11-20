# 1 Introduction

[Guide home](../README.md) · [Contents](table-of-contents.md) · [Next: Software Overview](02-software-overview.md)

**18 November 2026**

## 1.1 Purpose of TIMESAT

TIMESAT analyses time series of satellite observations, with a particular focus
on vegetation indices and seasonal vegetation development. It fits functions to
dated observations and extracts seasonal metrics from the fitted trajectories.
These metrics describe features such as seasonal transitions, the seasonal
maximum, amplitude and season length. For raster inputs, the analysis produces
spatially distributed descriptions of seasonal variation.

The fitted trajectory and the rules used to extract its metrics are part of the
analysis. Interpret results together with the input variable, observation
quality, temporal coverage and selected parameters. This guide provides a
shared scientific reference for making and reporting those choices through
either the GUI or the CLI.

An early description of TIMESAT and seasonal-parameter extraction is given by
[Jönsson and Eklundh (2004), *TIMESAT—a program for analyzing time-series of
satellite sensor data*](https://portal.research.lu.se/en/publications/timesat-a-program-for-analyzing-time-series-of-satellite-sensor-d/).

## 1.2 Intended readers

The guide is intended for researchers, students and practitioners investigating
vegetation seasonality with satellite time series. It supports two principal
ways of working:

- **Interactive analysis with the graphical user interface (GUI):** inspect
  observations, compare fitted curves and examine seasonal metrics for selected
  series or raster pixels, then configure raster batch processing where needed.
- **Batch analysis with the command-line interface (CLI):** supply a
  configuration and raster inputs from a terminal or an automated workflow.

Readers should understand the variable being analysed, including its units,
calibration and quality information. Raster processing also requires attention
to spatial alignment and observation dates. Programming knowledge is not needed
for the scientific concepts or ordinary GUI exploration; terminal workflows
require familiarity with paths, files and configuration documents.

## 1.3 Scope and reference versions

The processing architecture is:

**TIMESAT GUI -> TIMESAT CLI -> TIMESAT 4 Core.**

The [reference versions](../README.md#reference-versions) are Core 4.4.1,
CLI 1.9.2 and GUI 1.6.2. They form a verified compatible combination. GUI preview,
GUI batch processing and terminal runs use the same scientific processing chain.
With matching input observations, effective processing parameters and output
conventions, their corresponding scientific results should be consistent.

Earlier TIMESAT manuals include scientific explanations alongside MATLAB
interfaces, TSM/TSF programs and historical settings or output formats. This
guide preserves scientifically accurate concepts while addressing the current
GUI and CLI workflows. Historical execution instructions are not procedures
for these interfaces.

## 1.4 Scientific interpretation

Phenology concerns the timing of biological events. A transition extracted from
a fitted vegetation-index trajectory is an operationally defined feature of
that signal. Its relationship to a particular biological event depends on the
observed variable, vegetation and event definition. Here, **seasonality** means
the temporal pattern represented by observations and their fitted trajectory;
**seasonal metrics** are quantities extracted using specified rules.

For example, a start-of-season date must be reported with its defining method
and threshold. Seasonal amplitude describes a difference in fitted values,
while a seasonal integral accumulates fitted values over a defined interval.
Interpretation depends on the input units, baseline and output transformations.
Use the same units and scaling conventions when comparing corresponding
results. An integral of a vegetation index does not automatically represent
calibrated physical productivity.

Observation quality indicators, fitting weights and output quality codes have
different roles. A fitting weight controls an observation's influence on the
fit. Output quality codes describe particular conditions assessed by the
software. They are not general statistical uncertainty estimates or independent
validation of a seasonal date.

A reproducible analysis records input provenance, software versions, effective
configuration, temporal conventions and output interpretation. Scientific
evaluation additionally requires evidence appropriate to the research question.
A visually plausible fitted curve alone does not establish the accuracy of a
biological event estimate. For an example of evaluating reconstructed satellite
series and phenological estimates against independent observations, see
[Cai et al. (2017), *Performance of Smoothing Methods for Reconstructing NDVI
Time-Series and Estimating Vegetation Phenology from MODIS Data*](https://portal.research.lu.se/en/publications/performance-of-smoothing-methods-for-reconstructing-ndvi-time-ser/).
The methods examined in that study do not define the current software's method
inventory.

## 1.5 Using this guide

Continue with the [Software Overview](02-software-overview.md) for component
roles, interactive exploration and raster batch processing. The
[contents](table-of-contents.md) separates shared scientific/data references
from interface-specific procedures in the proposed complete guide.

The complete guide now includes [installation](03-installation.md), shared
parameter and product references, detailed GUI/CLI procedures,
[worked examples](11-worked-examples.md) and appendices. Use the
[contents](table-of-contents.md) to continue from these opening chapters to the
relevant procedure or reference.

---

[Guide home](../README.md) · [Contents](table-of-contents.md) · [Next: Software Overview](02-software-overview.md)
