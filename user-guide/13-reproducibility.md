# 13 Reproducibility and scientific reporting

[Previous](12-troubleshooting.md) · [Contents](table-of-contents.md) · [Next: Glossary](appendix-a-glossary.md)

## 13.1 Preserve the complete analysis

A reproducible TIMESAT analysis identifies the software components, inputs and effective settings that produced its results. Preserve immutable source/product identifiers or checksums where possible, while respecting data licences and access restrictions.

| Record | Include |
| --- | --- |
| Software | Core/CLI/GUI versions, artifact/package records, relevant source commits for development runs, OS/architecture, Python/dependencies and threads |
| Observations | Sensor/product/version, variable/units, source dates, compositing, footprint/grid, band and duplicate/missing-date decisions |
| Calibration/quality | Scale/offset, NoData/masks, range policies, QA product definitions and complete mapping rules |
| Scientific settings | Method, smoothing, envelope passes/strength, baseline, outliers, gap filling, class profiles, season structure and thresholds |
| Temporal/output settings | Calendar/ignored day, observation extent and buffer context, output schedule/year drops, metric selection, scale/encoding, dtype and precision |
| Execution/results | Effective JSON/run snapshot, command or GUI sequence, log/exit status, processing window, complete outputs and inspection checks |

Save a record of GUI settings and the actual run snapshot. A figure or a screenshot of selected controls alone cannot recover all of these fields. Preserve original configurations before migration or GUI subset loading. Keep different experiments in clearly identified output directories.

## 13.2 Sensitivity and independent evaluation

Vary one analysis choice at a time when the objective is to attribute its effect. Sampling, retained weights, baseline and threshold changes can all shift derived dates. Compare appropriate dates/pixels and record both missing results and accepted results. A smaller apparent error among the accepted cases may conceal a larger rejection rate.

Choose evaluation data and metrics that address the intended scientific claim. Reference observations should have known spatial/temporal support and their own uncertainties; satellite-pixel seasonality need not equal a point-scale biological event. Distinguish parameter tuning data from independent evaluation and report the definition of SOS/EOS used by both sources.

Synthetic examples verify controlled processing relationships. They do not measure field accuracy, uncertainty calibration, sensor transferability, operational reliability or general forecasting skill. For an information-at-time evaluation, exclude unavailable future observations explicitly and distinguish retrospective estimates from genuinely time-limited inputs.

## 13.3 Report definitions and units

A methods section should name TIMESAT components/versions, input variable/product and date extent, calibration/quality mapping, fitting method/settings, seasonal definition and event thresholds, calendar/boundary policy, output sampling and product conversion. State how missing seasons and QA were handled. Include units for values, slopes and accumulations, and explicitly identify any factor such as CLI's HRVPP integral division by 1000.

A concise report might say: “The analysis used TIMESAT Core 4.4.1 through CLI 1.9.2, with the input index calibrated to [units]. We used [DL/SP], [effective parameters], [QA rules] and [season/threshold definition]. Fitted output was sampled [schedule] on the documented 365-day calendar. We retained [quality/missing-data rule] and reported metrics in [encoding/units].” Fill the bracketed fields with the actual analysis; this is a reporting template, not a scientifically recommended configuration.

For GUI-derived analyses, add GUI 1.6.2 and preserve the effective batch configuration or interactive parameter/input record. Report matched output conventions for interface comparisons and explicit numerical tolerances. Do not claim byte-identical files merely from agreement of scientific values.

## 13.4 Citation and attribution

Cite software and scientific methodology separately. Identify the component versions and concrete release records listed in [appendix D](appendix-d-references.md). Where maintainers provide a matching software DOI, include it; do not silently attach an unrelated historical record to another binary. Preserve variable/date/units definitions and the effective configuration with the analysis.

Preserve author acknowledgements and figure/data attribution. Figure 11.1 is original and generated from the supplied synthetic-example code; its [asset record](../assets/README.md) describes provenance and reproduction. No historical restricted figure is reproduced here. Software components retain their own licence terms, which are not changed by this guide.
