# Synthetic User Guide example

The scripts are original documentation support code and include no application source, real satellite data or credentials. See [chapter 11](../user-guide/11-worked-examples.md) for procedures and expected results.

The supporting files are the [data generator](generate_example.py),
[output checker](check_outputs.py) and [figure helper](plot_example.py).

Run from the documentation repository root in the pinned CLI/Core environment:

```sh
python examples/generate_example.py timesat-example
python -m timesat_cli run timesat-example/settings.json --threads 1
python examples/check_outputs.py timesat-example/settings.json
```

`generate_example.py` requires NumPy/rasterio and refuses a nonempty destination. Generated paths are absolute; select a new destination after relocation. `check_outputs.py` is specific to this three-year 4×4 dataset and six selected metrics. It reads outputs without changing them and checks inventory, geospatial metadata, dtypes/NoData, finite values and seasonal variation. It does not validate biological accuracy.

Five generated configurations cover regular 16-day output, daily output, month days 1/11/21, two class profiles and excluded-observation QA. Each writes to its own output folder. A repeated processing run can overwrite files in that folder; use a new configuration/output directory to preserve prior results.

The synthetic CRS/transform do not identify a real site. Keep generated observations and run outputs in a separate analysis directory; generated datasets are not bundled with this documentation.

The full environment and bounded checks are recorded in [validation](../user-guide/validation.md). Keep generated datasets and outputs outside this repository when preserving a clean checkout; substitute the chosen path consistently in the commands.
