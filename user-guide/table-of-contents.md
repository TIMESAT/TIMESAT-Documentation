# Table of contents

[Guide home](../README.md)

**Public Draft (Under Review) · 18 November 2026**

All thirteen chapters and four appendices are available in this review draft. Shared scientific definitions and product conventions are maintained once and referenced from GUI and CLI procedures. [Validation](validation.md) identifies the environments and workflows actually checked; available text does not imply that every configuration or platform has been tested.

## Part I Getting oriented

<a id="chapter-1"></a>

### [1 Introduction](01-introduction.md)

- [1.1 Purpose of TIMESAT](01-introduction.md#11-purpose-of-timesat)
- [1.2 Intended readers](01-introduction.md#12-intended-readers)
- [1.3 Scope and reference versions](01-introduction.md#13-scope-and-reference-versions)
- [1.4 Scientific interpretation](01-introduction.md#14-scientific-interpretation)
- [1.5 Using this guide](01-introduction.md#15-using-this-guide)

<a id="chapter-2"></a>

### [2 Software Overview](02-software-overview.md)

- [2.1 Software components](02-software-overview.md#21-software-components)
- [2.2 Processing architecture](02-software-overview.md#22-processing-architecture)
- [2.3 Available workflows](02-software-overview.md#23-available-workflows)
- [2.4 Fitting methods and output families](02-software-overview.md#24-fitting-methods-and-output-families)
- [2.5 Workflow boundaries](02-software-overview.md#25-workflow-boundaries)

<a id="chapter-3"></a>

### [3 Installation and release identification](03-installation.md)

- [3.1 Choosing an environment](03-installation.md#31-choosing-an-environment)
- [3.2 Desktop application](03-installation.md#32-desktop-application)
- [3.3 Terminal installation](03-installation.md#33-terminal-installation)
- [3.4 Startup checks](03-installation.md#34-startup-checks)
- [3.5 Environment and licence record](03-installation.md#35-environment-and-licence-record)

## Part II Shared scientific and data reference

<a id="chapter-4"></a>

### [4 Preparing input data](04-input-data.md)

- [4.1 Observations, dates and calibration](04-input-data.md#41-observations-dates-and-calibration)
- [4.2 Tables for GUI exploration](04-input-data.md#42-tables-for-gui-exploration)
- [4.3 Raster lists](04-input-data.md#43-raster-lists)
- [4.4 Temporal GeoTIFF stacks](04-input-data.md#44-temporal-geotiff-stacks)
- [4.5 Quality and land-cover inputs](04-input-data.md#45-quality-and-land-cover-inputs)
- [4.6 Spatial and missing-data checks](04-input-data.md#46-spatial-and-missing-data-checks)

<a id="chapter-5"></a>

### [5 Scientific methods and seasonal interpretation](05-scientific-methods.md)

- [5.1 Processing sequence and observation weights](05-scientific-methods.md#51-processing-sequence-and-observation-weights)
- [5.2 Range policies and baseline estimation](05-scientific-methods.md#52-range-policies-and-baseline-estimation)
- [5.3 Outliers, availability and gaps](05-scientific-methods.md#53-outliers-availability-and-gaps)
- [5.4 Double logistic fitting](05-scientific-methods.md#54-double-logistic-fitting)
- [5.5 Smoothing splines and upper-envelope adaptation](05-scientific-methods.md#55-smoothing-splines-and-upper-envelope-adaptation)
- [5.6 Regular and irregular season structure](05-scientific-methods.md#56-regular-and-irregular-season-structure)
- [5.7 Start/end definitions and supported combinations](05-scientific-methods.md#57-startend-definitions-and-supported-combinations)
- [5.8 Selection and validation](05-scientific-methods.md#58-selection-and-validation)

<a id="chapter-6"></a>

### [6 Parameters and configuration](06-parameters-and-configuration.md)

- [6.1 Structure and naming](06-parameters-and-configuration.md#61-structure-and-naming)
- [6.2 Input and output fields](06-parameters-and-configuration.md#62-input-and-output-fields)
- [6.3 General and class fields](06-parameters-and-configuration.md#63-general-and-class-fields)
- [6.4 QA, calibration and method dependencies](06-parameters-and-configuration.md#64-qa-calibration-and-method-dependencies)
- [6.5 Calendar and output sampling](06-parameters-and-configuration.md#65-calendar-and-output-sampling)
- [6.6 Layer selection and validation boundaries](06-parameters-and-configuration.md#66-layer-selection-and-validation-boundaries)
- [6.7 Settings preservation and migration](06-parameters-and-configuration.md#67-settings-preservation-and-migration)

<a id="chapter-7"></a>

### [7 Outputs and quality information](07-outputs-and-quality.md)

- [7.1 Output inventory](07-outputs-and-quality.md#71-output-inventory)
- [7.2 Seasonal metric dictionary](07-outputs-and-quality.md#72-seasonal-metric-dictionary)
- [7.3 Date and scale conventions](07-outputs-and-quality.md#73-date-and-scale-conventions)
- [7.4 Quality dictionaries](07-outputs-and-quality.md#74-quality-dictionaries)
- [7.5 Spatial layout, types and NoData](07-outputs-and-quality.md#75-spatial-layout-types-and-nodata)
- [7.6 Interactive export and precision](07-outputs-and-quality.md#76-interactive-export-and-precision)
- [7.7 Completion and interpretation checks](07-outputs-and-quality.md#77-completion-and-interpretation-checks)

## Part III Using TIMESAT

<a id="chapter-8"></a>

### [8 Exploring data with the GUI](08-exploration.md)

- [8.1 Interface orientation and loading](08-exploration.md#81-interface-orientation-and-loading)
- [8.2 Table series and raster pixels](08-exploration.md#82-table-series-and-raster-pixels)
- [8.3 Region summaries](08-exploration.md#83-region-summaries)
- [8.4 Comparing fits and seasonal metrics](08-exploration.md#84-comparing-fits-and-seasonal-metrics)
- [8.5 Saving and exporting](08-exploration.md#85-saving-and-exporting)
- [8.6 Before continuing to batch processing](08-exploration.md#86-before-continuing-to-batch-processing)

<a id="chapter-9"></a>

### [9 Running raster processing from the GUI](09-raster-processing.md)

- [9.1 Prerequisites](09-raster-processing.md#91-prerequisites)
- [9.2 Outputs and run settings](09-raster-processing.md#92-outputs-and-run-settings)
- [9.3 Full data and subareas](09-raster-processing.md#93-full-data-and-subareas)
- [9.4 Execution, records and logs](09-raster-processing.md#94-execution-records-and-logs)
- [9.5 Threads, memory and stopping](09-raster-processing.md#95-threads-memory-and-stopping)
- [9.6 Checking results](09-raster-processing.md#96-checking-results)

<a id="chapter-10"></a>

### [10 Running raster processing with the CLI](10-raster-processing.md)

- [10.1 Commands](10-raster-processing.md#101-commands)
- [10.2 Configuration and standard input](10-raster-processing.md#102-configuration-and-standard-input)
- [10.3 Classes and spatial windows](10-raster-processing.md#103-classes-and-spatial-windows)
- [10.4 Resource planning](10-raster-processing.md#104-resource-planning)
- [10.5 Logs, failures and reruns](10-raster-processing.md#105-logs-failures-and-reruns)
- [10.6 Migration and output inspection](10-raster-processing.md#106-migration-and-output-inspection)

## Part IV Examples and responsible use

<a id="chapter-11"></a>

### [11 Worked examples](11-worked-examples.md)

- [11.1 Generate and explore the dataset](11-worked-examples.md#111-generate-and-explore-the-dataset)
- [11.2 Run a small raster](11-worked-examples.md#112-run-a-small-raster)
- [11.3 QA sensitivity](11-worked-examples.md#113-qa-sensitivity)
- [11.4 Output schedules and temporal context](11-worked-examples.md#114-output-schedules-and-temporal-context)
- [11.5 Land-cover profiles](11-worked-examples.md#115-land-cover-profiles)
- [11.6 Repeating and comparing results](11-worked-examples.md#116-repeating-and-comparing-results)

<a id="chapter-12"></a>

### [12 Troubleshooting and known limitations](12-troubleshooting.md)

- [12.1 Installation and component discovery](12-troubleshooting.md#121-installation-and-component-discovery)
- [12.2 Input and configuration errors](12-troubleshooting.md#122-input-and-configuration-errors)
- [12.3 Unexpected fits and missing seasons](12-troubleshooting.md#123-unexpected-fits-and-missing-seasons)
- [12.4 Preview/batch comparisons](12-troubleshooting.md#124-previewbatch-comparisons)
- [12.5 Settings, resources and interrupted jobs](12-troubleshooting.md#125-settings-resources-and-interrupted-jobs)
- [12.6 A reproducible issue report](12-troubleshooting.md#126-a-reproducible-issue-report)

<a id="chapter-13"></a>

### [13 Reproducibility and scientific reporting](13-reproducibility.md)

- [13.1 Preserve the complete analysis](13-reproducibility.md#131-preserve-the-complete-analysis)
- [13.2 Sensitivity and independent evaluation](13-reproducibility.md#132-sensitivity-and-independent-evaluation)
- [13.3 Report definitions and units](13-reproducibility.md#133-report-definitions-and-units)
- [13.4 Citation and attribution](13-reproducibility.md#134-citation-and-attribution)

## Appendices

<a id="appendix-a"></a>

### [Appendix A Glossary and notation](appendix-a-glossary.md)


<a id="appendix-b"></a>

### [Appendix B Current and legacy workflows](appendix-b-legacy.md)


<a id="appendix-c"></a>

### [Appendix C Advanced interfaces](appendix-c-advanced-interfaces.md)

- [C.1 Python pipeline entry](appendix-c-advanced-interfaces.md#c1-python-pipeline-entry)
- [C.2 Helper inventory and arrays](appendix-c-advanced-interfaces.md#c2-helper-inventory-and-arrays)
- [C.3 Remote object-store inputs](appendix-c-advanced-interfaces.md#c3-remote-object-store-inputs)
- [C.4 Integration responsibilities](appendix-c-advanced-interfaces.md#c4-integration-responsibilities)

<a id="appendix-d"></a>

### [Appendix D References and acknowledgements](appendix-d-references.md)

- [D.1 Scientific references](appendix-d-references.md#d1-scientific-references)
- [D.2 Software and release records](appendix-d-references.md#d2-software-and-release-records)
- [D.3 Licences, data and figure provenance](appendix-d-references.md#d3-licences-data-and-figure-provenance)
- [D.4 Acknowledgements](appendix-d-references.md#d4-acknowledgements)

[Guide home](../README.md) · [Validation scope](validation.md)
