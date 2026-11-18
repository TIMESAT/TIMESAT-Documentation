# Appendix A Glossary and notation

[Previous](13-reproducibility.md) · [Contents](table-of-contents.md) · [Next](appendix-b-legacy.md)

| Term | Meaning in this guide |
| --- | --- |
| Amplitude | Fitted seasonal maximum minus the mean of side minima; AMPL |
| Availability window | Synthetic-day half-window around an output date used to count retained observations |
| Baseline, preprocessing | Record-level low value estimated before fitting using `p_low_percentile` |
| Baseline, seasonal | Mean of the left and right seasonal minima; MINV |
| Batch processing | Processing many raster series through the CLI pipeline, initiated by terminal or GUI |
| Buffer observations | Independently supplied observations before/after the target period; distinct from copied boundary support |
| Calibration | Conversion from stored values to the numeric variable supplied to Core using scale/offset |
| Class profile | Scientific settings assigned to a configured land-cover identifier |
| CLI | Command-line interface; also the TIMESAT Python processing-service layer used by GUI |
| Core | TIMESAT 4 numerical Fortran implementation exposed through Python |
| CRS | Coordinate reference system; meaningful spatial alignment also requires matching transforms/grid origins |
| DL | Double logistic fitting; ordinary Core method 1 |
| DOY | Day of year; distinguish Gregorian ordinal, synthetic day and layer-relative event position |
| Effective configuration | The parsed/normalized settings actually used by a processing path |
| Envelope adaptation | Additional fitting passes that reduce influence of observations below an earlier fitted curve |
| EOS / SOS | End/start of season under the chosen operational threshold definition |
| GeoTIFF | TIFF raster with geospatial metadata; a stack can store observation dates in band descriptions |
| GUI | Graphical user interface; native Qt desktop application |
| HRVPP-style format | The implemented output convention affecting event date encoding and integral scaling; not a universal certification of a product |
| Integral | Daily accumulation over an implemented seasonal interval; distinguish total and baseline-subtracted sums |
| JSON | Configuration document format used by current CLI; comments are not part of JSON syntax |
| Land-cover identifier | Code matched to a class profile in multiclass processing |
| Mask / NoData | Indication of excluded/missing raster values; explicit handling through data/quality policies must be checked |
| Observation | A dated input value before modelling, not a fitted value evaluated between observation times |
| Phenology | Timing of biological events; satellite seasonal metrics require an explicit interpretation/validation relationship |
| QA | Quality information; distinguish raw labels, mapped weights, fitted-series codes and seasonal codes |
| ROI | Region of interest; current GUI summaries describe raw spatial values rather than fitted regional phenology |
| Season slot | Allocated output position for a year/season, which may contain no accepted season |
| Seasonality | Temporal pattern described by the observations/fitted trajectory |
| SP | Smoothing spline; ordinary Core method 2 |
| ST | Folder identifier for fitted time-series outputs and associated QA |
| Synthetic calendar | Core's 365-day-per-year time representation with a specified ignored leap-day ordinal |
| Temporal stack | Raster with separate bands representing successive observation times of one variable |
| VPP | Identifier used for the seasonal-parameter family; current GUI calls these Vegetation Phenology Parameters |
| Weight | Nonnegative fitting influence assigned from observation quality and subsequent processing policies |

Notation: `t` denotes time, `y` an observation, `f(t)` a fitted trajectory, `U` the calibrated variable's units, and `D` a synthetic day. Parameter names in backticks denote exact JSON/software identifiers. GUI labels are written in bold. All dates in examples specify their format rather than relying on local month/day conventions.
