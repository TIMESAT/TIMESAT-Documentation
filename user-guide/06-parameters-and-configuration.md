# 6 Parameters and configuration

[Previous](05-scientific-methods.md) · [Contents](table-of-contents.md) · [Next](07-outputs-and-quality.md)

This is the shared parameter reference for GUI and CLI. Tables give **CLI 1.9.2 loader defaults**, not sensor recommendations or guarantees that GUI save/load preserves every field. GUI labels and restrictions are included where verified. Scientific meanings are explained in [chapter 5](05-scientific-methods.md); command syntax is in [chapter 10](10-raster-processing.md).

## 6.1 Structure and naming

Current CLI configuration is JSON with required `input`, `output` and `general` objects. `general.classes` must be a nonempty list. Optional `metadata` stores provenance but does not control computation. JSON uses double quotes, lowercase `true`/`false`, no comments and no trailing commas. Backslashes in Windows JSON paths must be escaped; forward slashes avoid that problem.

```json
{
  "input": {"image_file_list": "timesat-example/vi_stack.tif"},
  "output": {"outputfolder": "timesat-example/outputs", "time_step_days": 16},
  "general": {"p_a": [[1, 1]], "classes": [{"landuse": 1}]}
}
```

Replace the paths with real inputs. This compact example illustrates structure; use the complete generated configuration in chapter 11 for a verified runnable example. A stack needs dated bands. A list field can identify a temporal stack despite its name.

## 6.2 Input and output fields

| Input field | Type; default | Meaning |
| --- | --- | --- |
| `image_file_list` | string; empty | Required actual data input for a run: image-list TXT or temporal GeoTIFF stack |
| `quality_file_list` | string; empty | Optional QA list/stack; supply explicit weighting rules |
| `tv_list` | string; empty | Optional one-date-per-observation list for CLI parsing |
| `lc_file` | string; empty | Optional land-cover raster for multiclass profiles |
| `s3env` | string; empty | Local dotenv configuration path for advanced object-store access; see appendix C |

| Output field | Type; default | Meaning |
| --- | --- | --- |
| `outputfolder` | string; empty | Root for `ST`/`VPP`; set a deliberate output directory |
| `outputvariables` | integer; 1 | 1 enables seasonal metrics/QA; use 0 for fitted-series-only processing |
| `time_sampling` | string; `regular` | `regular` or `monthly` for fitted-series sampling |
| `time_step_days` | integer; 1 | Positive synthetic-day interval for regular output; use at least 1 in normal work |
| `monthly_days` | integer list; `[1,11,21]` | Unique month days 1–31; sorted by loader; invalid dates within individual months are omitted |
| `drop_first_year`, `drop_last_year` | booleans; false | Independently remove first/last fitted-series output years; do not remove fitting observations |
| `p_st_timestep` | integer; 1 | Legacy interval input; prefer explicit modern sampling fields |
| `p_nodata` | number; -9999 | Numeric output missing sentinel; must be representable by selected output dtype |
| `p_hrvppformat` | integer; 1 | Enables Core date formatting and CLI HRVPP-style date/integral conversion; see chapter 7 |
| `vpp_dtype` | string; `float32` | Seasonal raster dtype; allowed: uint8/uint16/int16/uint32/int32/float32/float64 |
| `yfit_prefix`, `vpp_prefix` | strings; `TIMESAT` | Fitted-series/seasonal filename prefixes |
| `vpp_variables` | list; all thirteen | Select/reorder/rename seasonal layers; keep at least one enabled when VPP output is enabled |

## 6.3 General and class fields

| General field | Default | Meaning / documented range |
| --- | --- | --- |
| `imwindow` | `[0,0,0,0]` | Full raster; otherwise `[x_offset,y_offset,width,height]`, zero-based offsets |
| `p_band_id` | 1 | One-based input band for image-list observations; encoded temporal-stack bands take precedence |
| `scale`, `offset` | 1, 0 | Calibration before Core; coordinate with valid range and absolute thresholds |
| `p_ylu` | `[0,10000]` | Lower/upper bounds after calibration; GUI **Data Range** |
| `p_a` | `[]` | QA rules; empty rules yield zero weights and are unsuitable for an ordinary fit |
| `p_ignoreday` | 366 | Leap-year ordinal omitted from the synthetic calendar; ordinary monthly workflow uses this default |
| `p_davailwin` | 45 | Availability half-window in synthetic days; GUI **Availability Window** |
| `p_outlier` | 0 | 1 enables outlier detection; GUI checkbox |
| `p_printflag` | 0 | 0 quiet scientific processing; 1 enables diagnostic messages; legacy 0–3 file-debug descriptions do not apply |
| `max_memory_gb` | 10 | Approximate block-planning budget, not a hard bound on process memory |
| `p_nclasses` | number of classes | Optional; must equal the list length when present |
| `classes` | required | List of class objects; use unique byte-representable IDs and at most 255 configured profiles |

Class defaults and parameters:

| Class field | Default | Meaning and GUI correspondence |
| --- | --- | --- |
| `landuse` | required in each class | Land-cover identifier; one configured class applies to all pixels |
| `p_fitmethod` | 2 | 1 DL, 2 SP for ordinary workflows; **Fitting Method** |
| `p_smooth` | 1000 | SP stiffness; GUI **Smoothing parameter**, ordinary UI range 1–10000 |
| `p_nenvi` | 1 | Total fitting passes; normal 1–3; GUI additional-pass labels no/1/2 |
| `p_wfactnum` | 1 | Positive adaptation strength; normal GUI 1–10; keep nonzero |
| `p_startmethod` | 1 | Threshold method; use the compatibility matrix in section 5.7 |
| `p_startcutoff` | `[0.25,0.15]` | Start/end fractions for methods 1/3 or increments in data units for method 2 |
| `p_low_percentile` | 0 | Record baseline setting in 0–1; 0 selects minimum; GUI **Base Level** |
| `p_fillbase` | 0 | 1 inserts baseline controls where availability is zero |
| `p_seasonmethod` | 1 | 1 irregular, 2 regular; GUI **Seasonal Method** |
| `p_seapar` | 1 | Season-structure control in 0–1; meaning depends on season method |
| `lowrangemode`, `highrangemode` | 0, 0 | Range modes 0 invalidate, 1 clip, 2 clip/downweight |
| `rangedownweight` | 0.5 | Weight multiplier for mode 2; use a scientifically justified nonnegative value |

Range keys with `p_` prefixes are accepted as compatibility aliases. Prefer the names above consistently; do not supply conflicting aliases. GUI controls can clamp/normalize values and export only their supported subset. For exact reproducibility, record the effective exported values rather than assuming the widget's initial appearance equals the CLI defaults.

## 6.4 QA, calibration and method dependencies

Equality rules have two columns:

```json
"p_a": [[0, 0], [1, 1]]
```

This maps label 0 to zero weight and label 1 to unit weight. Inclusive ranges have three columns:

```json
"p_a": [[0, 10, 0], [11, 20, 0.5], [21, 31, 1]]
```

These are illustrative labels, not a sensor recommendation. Later matching rules overwrite earlier matches, and unmatched labels get zero weight. Inspect overlaps and boundaries. For synthesized unit QA when no QA input exists, an explicit `[[1,1]]` rule preserves unit weights. The tutorial uses known binary rules. For fractional/categorical mappings, verify the effective preview and batch weights before quantitative comparisons; the binary example does not establish equivalence for arbitrary mappings. See [preview/batch comparisons](12-troubleshooting.md#124-previewbatch-comparisons).

Changing scale/offset changes the numeric data presented to fitting and thresholds. Changing `p_seasonmethod` changes the interpretation of `p_seapar` and the available threshold combinations. Changing `p_fitmethod` to DL does not make `p_smooth` a DL stiffness control. Treat these dependencies as part of parameter selection, not just file syntax.

## 6.5 Calendar and output sampling

Core represents years using a 365-day synthetic timeline. In leap years, `p_ignoreday` chooses an omitted ordinal. Default 366 omits December 31 and retains February 29; it does not remove February 29. Thus a synthetic year contains 365 dates even for a leap year.

Regular output samples indices beginning with the first synthetic day and then every positive `time_step_days` across the complete record; an interval need not restart exactly on January 1 of every year. Monthly mode selects the requested month days on the implementation's default leap policy. Avoid combining nondefault ignored days with monthly mode without checking exact output dates.

```json
"output": {
  "outputfolder": "outputs_monthly",
  "time_sampling": "monthly",
  "monthly_days": [1, 11, 21],
  "drop_first_year": false,
  "drop_last_year": true
}
```

Output sampling selects fitted dates; it does not composite input observations. Year dropping removes fitted-series/QA output dates, not observations used in fitting or a corresponding VPP year inventory. Explicit modern sampling fields take precedence over legacy `p_st_timestep`. With only the legacy value -1, the loader supplies the historical monthly `[1,11,21]` schedule and both year drops. Supply modern fields together for new work and inspect effective values.

## 6.6 Layer selection and validation boundaries

```json
"vpp_variables": [
  {"source": "SOSD"},
  {"source": "TPROD", "name": "total_index_integral"},
  {"source": "SPROD", "enabled": false}
]
```

`source` identifies the scientific metric; `name` changes its output filename label, not its definition or units. `enabled` defaults to true; `name` defaults to the source name. String entries are also accepted. Source names must match the current metric inventory. Avoid separators or ambiguous names in output aliases.

The loader validates structure, types and selected enumerations; it is not a full scientific-domain validator. Independently check meaningful thresholds, positive adaptation strength, class uniqueness/count, valid windows, available storage and representable dtype/NoData. A configuration that loads successfully has not thereby passed a numerical or scientific evaluation.

## 6.7 Settings preservation and migration

GUI **Save Settings...** is a parameter-preset operation for its supported subset. It is not a lossless advanced-CLI editor or a complete project archive. Current loading takes the first class; paths, metadata, modern sampling/drop flags, advanced range policy and dtype do not all survive GUI load/save. Preserve an authoritative CLI JSON before experimenting in the GUI. Input selections for a GUI batch job are supplied from the loaded session when its run configuration is built.

Use `migrate-config` for the implemented older JSON layout containing `settings` and `classN` objects. Preserve the old file, write to a new destination, compare every migrated value, and rerun a small controlled dataset. Migration does not establish import support for old `.set` files or identical results from a historical TIMESAT version.


