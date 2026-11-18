# Appendix C Advanced interfaces

[Previous](appendix-b-legacy.md) · [Contents](table-of-contents.md) · [Next](appendix-d-references.md)

These interfaces are for Python/workflow integrators. They do not add terminal subcommands or alter GUI -> CLI -> Core. Record the exact CLI version because helper signatures and array contracts are more detailed than a settings file.

## C.1 Python pipeline entry

The terminal command ultimately calls `timesat_cli.processing.run(settings_path)`. A Python integration can use the same configuration path and processing layer:

```python
import os
os.environ["OMP_NUM_THREADS"] = "1"

from timesat_cli.processing import run
run("path/to/settings.json")
```

Set relevant thread environment before importing/loading numerical processing, use a complete validated JSON, and select a new output directory. The Python call does not by itself supply the CLI argument parser's checks or a complete provenance record. It retains the same overwrite, raster-input and output-convention responsibilities as terminal processing. This entry is source-verified; the tutorial's terminal execution exercises this pipeline.

## C.2 Helper inventory and arrays

| Module/helper | Role and contract boundary |
| --- | --- |
| `config.load_config` / `load_config_data` | Parse file/dictionary into normalized settings; scientific domains still need checking |
| `readers.read_file_lists` | Parse raster/list/stack input dates and QA alignment, then sort/deduplicate |
| `readers.open_image_data` | Read a requested spatial block and selected bands; calibration is applied later by batch processing |
| `qa.assign_qa_weight` | Map raw labels to weights; identify whether an array is raw QA or already mapped |
| `csvutils.read_table_data` | Read a DataFrame's first date column and remaining series into arrays for interactive helpers |
| `single_pixel.extract_single_pixel` | Extract a 1×1 spatial series from time-last arrays |
| `single_pixel.run_single_pixel` | Accept the complete single-series parameter/array set and invoke Core |
| `vpp.vpp_to_table` | Presentation-oriented date/value formatting and four-significant-digit table output |
| `vpp_layout` helpers | Named metric selection and date/integral conversion for raster output |

The single-series helper uses arrays with shape `(rows, columns, time)`, normally `(1,1,n_observations)`, a matched numeric QA cube and a `YYYYDOY` vector. Many class parameters are supplied as arrays with 255 slots, and start/end cutoffs use two columns. Dtypes and layout must satisfy the selected compiled interface. The helper currently forces one class; supplying a land-cover scalar does not turn it into a multiclass raster processor.

Use the installed version's function signature/docstring for an integration, rather than inventing a short call omitting required arrays. Pass raw QA when the helper performs mapping; repeated mapping is not generally equivalent to a single mapping. Prefer the JSON pipeline for routine raster work. The numerical service comparison in chapter 11 explicitly constructed the complete matched parameter set and checked its results against batch output.

## C.3 Remote object-store inputs

The CLI has an S3-compatible access path that reads a local dotenv configuration selected by `input.s3env`. Expected environment names include `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, optional `AWS_SESSION_TOKEN`, `S3_BUCKET` and `ENDPOINT_URL`. Store credentials through your approved local mechanism; do not put secret values or a credential file into shared documentation, scientific JSON examples, logs or public issue reports.

Object access uses presigned HTTPS URLs constructed through boto3, with a default 3600-second lifetime. Endpoint access, object keys, expiry during long jobs and interactions with temporal-stack band references require deployment-specific verification. Land-cover handling and local lists/settings must also be checked; this facility is not a general remote dataset discovery or authentication service.

Cloud access was not exercised in the recorded validation. This section describes the access facility and constraints; it does not supply a tested cloud deployment recipe. Validate a small approved object with a complete environment record before production use. Local processing remains the reproducible reference in chapter 11.

## C.4 Integration responsibilities

Keep a boundary between acquisition, calibration, scientific fitting and product conversion. Record each transformation and compare corresponding arrays at explicit units/precision. Directly importing a Core extension in a developer experiment does not make that experiment an ordinary GUI or terminal workflow. Keep experimental methods, forecasts and unstable helper contracts clearly separate from the documented reference procedures.

Local execution checks and untested areas are recorded in [validation](validation.md).
