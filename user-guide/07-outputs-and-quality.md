# 7 Outputs and quality information

[Previous](06-parameters-and-configuration.md) · [Contents](table-of-contents.md) · [Next](08-exploration.md)

## 7.1 Output inventory

CLI writes fitted-series products to `ST/` and seasonal products to `VPP/` below `output.outputfolder`. With default prefixes:

```text
ST/TIMESAT_20230101.tif
ST/TIMESAT_20230101_QA.tif
VPP/TIMESAT_SOSD_2023_season_1.tif
VPP/TIMESAT_QA_2023_season_1.tif
```

Fitted dates depend on the schedule. Seasonal files have up to two allocated slots per input year, not a guarantee of two detected seasons. Output selection can write fewer than all thirteen metrics. With `outputvariables=0`, the ordinary fitted-series/QA workflow remains but seasonal files are not requested.

The Core also returns arrays used internally, including season counts and coarse seasonal fits. Not every Core array is exported as an ordinary batch raster. Read each exported product's documented meaning rather than inferring an additional file from a Python return value.

## 7.2 Seasonal metric dictionary

Let `U` denote units of the values actually supplied to Core, and `D` a synthetic day. Definitions below describe the scientific quantities before any documented HRVPP integral scaling. Dates have encoding conventions rather than a single numeric day unit.

| Name | Meaning | Unit / interpretation |
| --- | --- | --- |
| SOSD | Start-of-season position at the selected rising-side threshold | Date/time convention in section 7.3 |
| SOSV | Fitted value at SOS | U |
| LSLOPE | Rising rate between fitted 20% and 80% transitions | U/D; denominator stabilization is implemented |
| EOSD | End-of-season position at the selected declining-side threshold | Date/time convention in section 7.3 |
| EOSV | Fitted value at EOS | U |
| RSLOPE | Declining rate based on the right-side 20%/80% transitions | U/D; the ordinary descending branch reports a positive decline magnitude |
| LENGTH | EOS position minus SOS position | D, potentially fractional |
| MINV | Mean of left and right seasonal minima | U; not necessarily the record-level preprocessing baseline |
| MAXD | Time of the seasonal maximum | Peak date, not the historical mean of 80% crossing times |
| MAXV | Fitted seasonal maximum | U |
| AMPL | MAXV minus MINV | U |
| TPROD | Total seasonal fitted-value sum | Accumulation over daily samples; conceptual U·D before output scaling |
| SPROD | Seasonal sum above MINV | Conceptual U·D before output scaling |

For the integrals, Core sums daily values from the floor of SOS through the ceiling of EOS, inclusively. SPROD subtracts the seasonal baseline for each included day. These are the implemented discrete sums, not an exact analytic integral with fractional endpoint weighting. Negative values/baselines require interpretation appropriate to the variable. The names do not convert a vegetation-index accumulation into carbon uptake or biomass production.

In irregular-season allocation, the peak position determines the output year. Seasons can cross calendar-year boundaries; SOS/EOS can therefore fall outside the nominal year of a product. More candidate peaks may be found than there are output slots, and selection/consistency checks can reject seasons. Use QA and NoData, not file existence, to identify accepted measurements.

## 7.3 Date and scale conventions

Core's synthetic timeline counts 365 days per year. With HRVPP formatting enabled, valid event positions are encoded by Core as full-year `YYYYDOY` values. CLI then writes layer-relative day positions:

```text
relative day = source DOY + (source year − output layer year) × 365
```

For a 2023 layer, a date in the previous year can have a negative relative position and a following-year date can exceed 365. Preserve fractional numeric values where present, but do not infer subdaily biological precision from a floating-point encoding. GUI table dates are presented as calendar strings through the CLI table formatter. With HRVPP formatting disabled, raw synthetic event positions are retained; these are not automatically Gregorian `YYYYMMDD` dates.

For `p_hrvppformat=1`, CLI divides TPROD and SPROD by 1000 when writing HRVPP-style raster values; Core returns its daily sums without that division. Keep the **Core quantity**, **raster scale convention** and **displayed number** distinct. Compare raster and Core/interactive values only after expressing them in the same convention, including this factor of 1000. Record the input units and output scale explicitly. A vegetation-index accumulation is not automatically calibrated physical productivity; no physical-productivity unit is inferred from its filename.

## 7.4 Quality dictionaries

Observation QA labels and weights describe inputs. Fitted-series QA describes retained observation availability around an output time. Seasonal QA describes acceptance/fallback/coverage conditions for a season. They are different quantities, and none is a general uncertainty interval.

| Fitted-series QA | Meaning in the reference processing |
| --- | --- |
| 0 | Initial/unprocessed output; also the QA raster NoData value |
| 1 | Outside the availability-covered extent / initial assigned coverage state |
| 2 | Zero retained observations in the availability window |
| 3 | One or two observations |
| 4 | Three to eight observations |
| 5 | More than eight observations |

Counts precede optional inserted baseline controls. A high count can still contain biased or unsuitable observations, and counts depend on the chosen half-window.

| Seasonal QA | Meaning |
| --- | --- |
| 0 | Unprocessed / raster NoData |
| 1 | Initialized or undetermined seasonal slot; do not treat it as an accepted season |
| 2 | Accepted-season branch with poor coverage |
| 3 | Threshold fallback used |
| 4 | More than two observations in declining zone only among the tested coverage combinations |
| 5 | More than two in peak zone |
| 6 | More than two in rising zone |
| 7 | Rising and peak zones covered |
| 8 | Rising and declining zones covered |
| 9 | Peak and declining zones covered |
| 10 | All three zones covered |

Zones use fitted 20%/80% transitions. The branch order and fallback take precedence over a simple ranking. QA 10 is not “100% accurate,” and the other values are not percentages. Inspect missing-slot behaviour with the numeric data mask; use QA together with the actual product's NoData values.

## 7.5 Spatial layout, types and NoData

GeoTIFFs retain the input raster profile/extent; a subarea run writes into the selected window within that profile. Do not assume the file bounds are cropped to the processing window or interpret unwritten regions as valid zero-valued science. Preserve the window/configuration with the run.

Default VPP dtype is float32, and QA uses uint8 with NoData 0. Fitted-series dtype follows input dtype when scale=1 and offset=0; otherwise it is float32. Integer output can truncate fitted fractional values. An unsigned raster type cannot represent the default negative scientific sentinel. Prefer floating-point scientific inputs/outputs for the tutorial and confirm the chosen sentinel/dtype combination for production.

## 7.6 Interactive export and precision

**Save Time Series** produces separate files with `_fit.csv`, `_raw.csv` and `_quality.csv` suffixes. Fitted columns identify selected DL/SP curves; raw and quality files use observation dates. The inspected quality export follows the displayed marker scale: mapped weights multiplied by 8 and clipped to 0–8. It must not be treated as unchanged sensor QA or unscaled fitting weights. Preserve the original QA inputs and mapping rules; do not reconstruct a scientific quality mask from this CSV alone. This export behaviour has not been checked on every official desktop artifact; see [validation](validation.md).

Seasonal tables format values to four significant digits and convert dates for presentation. Export/figure facilities are useful for inspection, but compare numerical arrays or sufficiently precise raster values for reproducibility rather than values transcribed from a formatted table. Save figure captions with variable units, date convention, method and parameter context.

## 7.7 Completion and interpretation checks

Confirm successful exit, expected dates/layers, dimensions/CRS/transform, data types, NoData, QA codes and plausible ranges. Inspect known valid/invalid pixels and the full spatial window. An existing output file is not proof that the run completed: output datasets are created before all blocks are processed, and a rerun can overwrite matching names. Use a fresh output directory for each deliberate experiment and preserve failed-run evidence separately.

The tested numerical comparisons and their scope are recorded in [validation](validation.md).
