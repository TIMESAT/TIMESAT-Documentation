# User Guide asset provenance

## Figure 2.1

The architecture diagram is original Mermaid text in [chapter 2](../user-guide/02-software-overview.md). It represents GUI -> CLI -> Core and terminal entry at CLI. Its source and accessible description remain editable in Markdown. It reproduces no application code or historical figure.

## Figure 11.1

`synthetic-timeseries.png` is an original illustration generated during the initial complete-guide preparation, 2026-11-17/18. Input: the first pixel from `generate_example.py`'s three-year 4×4 artificial dataset, not real satellite observations. Processing: published Core 4.4.1 and CLI 1.9.2, SP/DL, daily sampling, single class, the settings recorded by the generator. Axes identify dates and dimensionless synthetic index values.

The figure was visually checked for complete axes, readable labels/legend and unclipped curves. It contains no personal paths, credentials, screenshots or restricted imagery. Its editable generation source is [plot_example.py](../examples/plot_example.py). To reproduce it with a generated dataset and a new image filename:

```sh
python examples/plot_example.py timesat-example/settings.json reproduced-timeseries.png
```

The plotting helper uses CLI services and requires Matplotlib in addition to the CLI environment. It is specific to the supplied synthetic example with identity calibration, first-band data and the generated class profile. It refuses to overwrite an existing destination. It is not a general production API wrapper or scientific validation harness.

No image from the original Word/PDF manuals was modified or reused. The old phenology diagram's stated reuse conditions remain relevant to any later proposed reuse; no permission is inferred from its presence in an existing draft.
