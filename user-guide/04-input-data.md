# 4 Preparing input data

[Previous](03-installation.md) · [Contents](table-of-contents.md) · [Next](05-scientific-methods.md)

## 4.1 Observations, dates and calibration

A TIMESAT input series consists of dated values of a defined variable. For raster analysis, each observation image represents that variable over a spatial grid at one date; a pixel's values through those images form its series. State the product/sensor, variable, units, calibration, temporal compositing and quality information before choosing fitting parameters. A dimensionless scaled integer index and its calibrated floating-point representation require different numeric ranges and absolute thresholds.

CLI batch applies:

```text
value supplied to Core = stored raster value × general.scale + general.offset
```

Set `p_ylu` and absolute-increment thresholds in the resulting units. Avoid applying a product scale twice. Display colour stretching changes how a map looks and does not define scientific calibration. Use the same calibrated observations and effective parameters when comparing GUI and terminal results.

Input timestamps need not be evenly spaced. Missing observations can remain absent; do not introduce artificial observations merely to make an evenly spaced input sequence. Missing-value policy, gap filling and output sampling are separate topics in [chapter 5](05-scientific-methods.md).

## 4.2 Tables for GUI exploration

Use a table whose first column contains unambiguous dates and whose remaining columns contain numeric series:

```csv
date,series_a,series_b
2023-01-01,0.15,0.16
2023-01-11,0.16,0.17
2023-01-21,0.17,0.18
```

ISO dates `YYYY-MM-DD` avoid ambiguity between day/month conventions. Give each series a descriptive column heading, keep dates and values aligned, and inspect blanks/non-numeric cells before loading. The active GUI accepts CSV and spreadsheet paths; workbook support depends on available reader engines. CSV is the portable format used in this guide's example. Do not assume that a second worksheet is read as quality data: the current table helper treats columns after the first as value series, not a legacy two-sheet values/QA layout.

The table workflow is interactive. It does not turn the CLI raster `run` command into a CSV batch processor. The generated [synthetic example](11-worked-examples.md) provides a complete table instead of the three illustrative rows above.

## 4.3 Raster lists

Prepare a plain UTF-8 text file with one raster path per line:

```text
/data/vi_20230101.tif
/data/vi_20230111.tif
/data/vi_20230121.tif
```

Use actual paths for your system. Do not place a count, heading or comments at the beginning of a current CLI image list. For terminal runs, absolute paths are the least ambiguous choice: relative input paths are resolved against the process context, so moving a settings file alone does not make all its dependencies portable. The GUI has its own list-relative path handling and creates resolved run lists.

Recognized date patterns include `YYYYMMDD`, `YYYYDOY`, `YYYY-MM-DD`, `YYYY_MM_DD`, and year/day-of-year separated by a hyphen or underscore. Use one unambiguous date per filename; a timestamp in an unrelated directory name can confuse fallback parsing. With CLI, `input.tv_list` can supply a separate date list aligned one-for-one with images. Inspect the actual parsed date sequence.

CLI removes duplicate timestamps by retaining the first corresponding observation and then sorts by time. Resolve duplicates deliberately in data preparation; do not rely on filesystem ordering to select the scientifically preferable observation. Where supplied, QA must follow the same retained observation/date policy.

For image-list input, `general.p_band_id` selects the raster band, with 1 denoting the first band. Explicit stack-band references take precedence in stack processing. The normal GUI image-list exploration path reads band 1; prepare single-band inputs for straightforward GUI/CLI comparisons and investigate other band-selection requirements before a production comparison.

## 4.4 Temporal GeoTIFF stacks

A stack uses one band per observation time. Give each band a description containing its observation date, preferably `YYYYMMDD`. Band descriptions such as `Band 1` do not supply dates. CLI can also use its separate time list, and its stack reader has a `BAND_NAME` tag fallback; the GUI's date extraction uses band descriptions. A stack prepared for both interfaces should therefore have dated descriptions.

The stack must represent one variable on one spatial grid. A multiband spectral image is not automatically a temporal stack. The [example generator](../examples/generate_example.py) writes dated band descriptions, spatial metadata and a three-year series in a small GeoTIFF.

## 4.5 Quality and land-cover inputs

Quality rasters contain labels that must be translated to fitting weights using `general.p_a`. Equal-value and inclusive-interval rules are supported; see [section 6.4](06-parameters-and-configuration.md#64-qa-calibration-and-method-dependencies). Preserve the quality product's exact definition/version. A cloud-category number is not intrinsically a weight.

Supply either a QA image list or a dated QA stack matching the data. CLI aligns supplied QA by parsed timestamps and raises an error if data dates lack QA coverage. It does not infer missing QA from neighbouring dates. When no QA raster is supplied, the reader provides unit-valued QA; specify an explicit rule mapping that value to a unit weight. An empty rule list gives zero weights, not an automatic unweighted fit.

A land-cover raster selects class-dependent profiles in multiclass runs. Use integer codes that correspond to `general.classes[*].landuse`. A single configured class is applied to all pixels; with multiple classes, unmatched pixels are not processed as an implicit default class. Keep class IDs within the representable byte range and the configuration within the 255-slot implementation limit. Define the processing classes deliberately rather than relying on rounded floating-point class values.

## 4.6 Spatial and missing-data checks

Check that all data, QA and land-cover rasters share dimensions, coordinate reference system (CRS), pixel size, transform, orientation and pixel alignment. Reproject/resample inputs beforehand where necessary, using scientifically appropriate methods for continuous variables and categorical labels. The processing path does not constitute an automatic co-registration/reprojection service.

Identify NoData sentinels, masks and physical valid ranges explicitly. A raster's mask/NoData metadata alone is not a guarantee that each excluded value reaches Core with zero weight. Use QA and range policies that correctly exclude invalid observations, and inspect a small known region. Floating-point NaNs are handled in preprocessing, but their existence does not replace an input-quality audit.

Keep original data and a provenance manifest. Start with a small, spatially representative subset; verify dates, calibration, weights and fits before processing the full extent.
