# 10 Running raster processing with the CLI

[Previous](09-raster-processing.md) · [Contents](table-of-contents.md) · [Next](11-worked-examples.md)

## 10.1 Commands

In the selected Python environment, run:

```sh
python -m timesat_cli run path/to/settings.json --threads 1
```

The installed console entry is equivalent:

```sh
timesat-cli run path/to/settings.json --threads 1
```

Omitting `run` is accepted, but the explicit subcommand is clearer in recorded procedures. Use `python -m timesat_cli run --help` for run options. The reference CLI has two subcommands: `run` and `migrate-config`; there is no standard terminal CSV/table batch subcommand.

| Run argument | Meaning |
| --- | --- |
| `settings_json` | Required grouped JSON path, or `-` for standard input |
| `-t`, `--threads` | Nonnegative integer; 0 uses detected CPU count; default leaves the option unset |
| `--run-dir` | Directory for the stdin settings snapshot; does not replace `output.outputfolder` |

Very large thread requests are rejected relative to detected CPU count. One thread is used in the tutorial for a simple reproducibility record; it is not an optimal setting for every machine.

## 10.2 Configuration and standard input

Use absolute input paths or a recorded working directory. The [generator](../examples/generate_example.py) writes complete paths for its synthetic inputs and creates output directories.

Standard-input examples differ by shell:

**PowerShell**

```powershell
Get-Content ./timesat-example/settings.json -Raw | python -m timesat_cli run - --run-dir ./run-record --threads 1
```

**POSIX shell or Windows Command Prompt**

```sh
python -m timesat_cli run - --run-dir run-record --threads 1 < timesat-example/settings.json
```

For stdin, the CLI writes `settings.json` under the selected run directory before processing. If no run directory is supplied, it creates a temporary one. For a file-based run, archive the supplied file yourself; `--run-dir` is not a general automatic provenance system or a redirect for scientific outputs. Use an unused run-record directory for a new experiment.

## 10.3 Classes and spatial windows

One class profile supplies its parameters for every pixel. For multiclass processing, supply an aligned land-cover raster and explicit profiles:

```json
"general": {
  "classes": [
    {"landuse": 1, "p_fitmethod": 2, "p_smooth": 1000},
    {"landuse": 2, "p_fitmethod": 1}
  ]
}
```

This is a configuration fragment; retain the other required fields and suitable QA/range settings. Match IDs to actual land cover. Unmatched IDs do not select a catch-all class. Different profiles can be scientifically justified for differing vegetation structure, but class labels do not themselves prove optimal parameter choices.

`general.imwindow=[0,0,0,0]` requests the full image. A nonzero window is `[x_offset,y_offset,width,height]`; offsets are zero-based and dimensions must be positive and lie within the raster. For example, `[100,200,50,40]` selects 50 columns and 40 rows beginning at that offset. Output rasters keep the full input profile; retain the window record with the files.

## 10.4 Resource planning

`max_memory_gb` influences the number of rows processed per spatial block. Memory demand grows with input observations, output dates, record years and raster width. Daily output can substantially increase layer count and bookkeeping even when input sampling is sparse. A smaller block budget can reduce array pressure but cannot eliminate every file-handle, cache or stack-loading constraint.

Keep an initial run small. Record threads and resource settings when comparing performance. Separate throughput measurements from scientific correctness, and do not extrapolate a tiny 4×4 tutorial timing to a regional dataset.

## 10.5 Logs, failures and reruns

The process reports input counts/date extent, selected products, block progress and writing activity. Preserve stdout/stderr in a local run log. Example redirection:

```sh
python -m timesat_cli run timesat-example/settings.json --threads 1 > run.log 2>&1
```

Check the exit status immediately after the command: `$LASTEXITCODE` in PowerShell, `$?` in a POSIX shell, or `%ERRORLEVEL%` in Command Prompt. Zero indicates successful program completion, not scientific validation. An empty `outputfolder` can result in “Nothing to do”; supply a deliberate output location and check inventory.

Output datasets with matching names are opened for writing. A repeated command can overwrite previous results; a failure can leave partial files. Preserve inputs/configuration/logs, select a new output directory for a rerun and compare complete results deliberately. There is no documented resume command.

## 10.6 Migration and output inspection

```sh
python -m timesat_cli migrate-config old_settings.json grouped_settings.json
```

Keep the old file and use a new destination. Review paths, class count, all scientific fields, sampling/drop rules and output conventions in the migrated file. This operation supports the implemented older JSON layout, not arbitrary historical `.set` files. Test a small input before adopting a migrated setup.

Inspect outputs using [chapter 7](07-outputs-and-quality.md). For the supplied example, run:

```sh
python examples/check_outputs.py timesat-example/settings.json
```

The checker is deliberately specific to that generated dataset. It checks file counts, spatial metadata, finite scientific values, data types and basic seasonal variation; it is not a generic production-data validator or independent biological validation.

The checked commands, examples and their limits are recorded in [validation](validation.md).
