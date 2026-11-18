# 12 Troubleshooting and known limitations

[Previous](11-worked-examples.md) · [Contents](table-of-contents.md) · [Next](13-reproducibility.md)

Work from the first meaningful error in the run log. Preserve the original inputs, effective settings and partial outputs before experimenting. Start by reproducing the issue with a small known dataset in the same environment; successful startup alone does not exercise scientific processing.

## 12.1 Installation and component discovery

| Symptom | Checks and response |
| --- | --- |
| Core import/DLL failure | Confirm supported Python/architecture and actual installed versions. Keep desktop bundle libraries together. Verify a Core wheel exists for that environment; preserve the complete loader error. |
| `timesat-cli` command not found | Activate the intended environment and try `python -m timesat_cli run --help`. Record which Python is being used. |
| GUI cannot find its CLI | Restore/preserve the complete official archive layout and bundled CLI. Do not substitute a random executable or a legacy TSF program. |
| Spreadsheet loading fails | Check workbook format and reader-engine availability. Export an unambiguous date-plus-numeric-series CSV to separate engine issues from data issues. |

## 12.2 Input and configuration errors

| Symptom | Checks and response |
| --- | --- |
| Input path missing | Check absolute/relative path bases, permissions and relocation of generated data. A settings file's directory is not a universal base for all CLI paths. |
| Date extraction fails | Use a supported filename pattern or dated band descriptions; avoid generic `Band 1` and multiple unrelated date strings. Check explicit time-list length. |
| Data/QA counts or coverage differ | Match observation dates and source selection, not just nominal product range. Resolve missing QA before a run. |
| Invalid grouped schema | Supply required input/output/general objects and nonempty classes. Use JSON booleans/quoting, check lengths and preserve the rejected file. |
| “Nothing to do” | Set `output.outputfolder`; confirm that meaningful output was requested and written. |
| Output dtype/NoData error | Use a representable sentinel/type combination. Default -9999 cannot be represented by an unsigned scientific output type. |

## 12.3 Unexpected fits and missing seasons

Inspect dates, units, scale/offset and retained quality weights first. Empty rules or unmatched QA labels can remove all observations. A narrow range can reject real values; a wide one can retain corrupt data. Inspect missing/constant/low-variation series before adjusting model flexibility.

For oscillatory SP fits, compare smoothing, quality weighting and high outliers. For an overly simple trajectory, check coarse-season structure and excessive stiffness. Inspect amplitude and threshold attainability where seasons are absent. Use the supported season/threshold combinations, and check QA/fallback/NoData rather than counting files as seasons.

For boundary-year anomalies, inspect actual temporal coverage and copied support. Independent buffer observations differ from internal extension. Do not add arbitrary repeated years to force an expected count of seasons without recording the assumption.

## 12.4 Preview/batch comparisons

Corresponding results should be consistent for the compatible reference components under matching inputs, effective parameters and output conventions. Compare in this order:

1. Identify the exact raster pixel/grid or table series and source dates, including duplicates, input extent and observation exclusions.
2. Compare the values reaching Core: band, scale/offset, NaNs, ranges and QA-to-weight mapping.
3. Compare effective fitting/class parameters, season/threshold settings, baseline, availability and gap filling. Recheck method after coarse overlays.
4. Compare output sampling/calendar and requested years; select common dates for a scientific-value comparison.
5. Apply the documented date/integral conversions and account for table display rounding. Compare raw numerical outputs at an explicit tolerance.

Product-specific QA mapping, calibration/band selection, output scheduling and the selected fitting method need explicit checks in a preview/batch comparison. The generated binary-QA, identity-calibration example is a verified matched case; it does not establish every product-specific mapping or configuration. Use the effective values and dates rather than assuming that similar-looking controls guarantee equivalent inputs. See [validation](validation.md) for the tested scope.

If a comparison still disagrees, retain both complete configurations and inputs, parsed dates, pixel/series identity and the exact output conversion used. Identify whether the difference is already present in input values, effective settings or output representation, and prepare a minimal reproducible report. Compatibility confirmation does not remove the need to diagnose a specific configuration problem.

## 12.5 Settings, resources and interrupted jobs

Advanced settings changed after GUI save/load may lie outside its preserved subset. Keep the original CLI JSON and compare saved values. Input selections and metadata are not guaranteed to form a complete saved project.

For memory problems, reduce loaded data/extent, inspect effective block budget, thread count and storage. The GUI memory field and CLI planner field need checking; the planner is not a hard process memory ceiling. A smaller output interval can create many more files and arrays.

Stop or a process failure can leave partially written outputs. Inspect the exit code, log and inventory; isolate that run and use a new directory for a deliberate retry. The reference workflow has no general checkpoint/resume facility. Missing coverage must not be filled by copying arbitrary files from a different run.

## 12.6 A reproducible issue report

Prepare component versions/artifact names, OS/architecture/Python, relevant dependencies and threads, effective JSON, minimal redistributable inputs, exact command or GUI action sequence, expected/actual results and the first relevant log/error. State pixel/date/metric and units for numerical issues. Include whether the synthetic tutorial passes.

Remove credentials, signed URLs, restricted data and sensitive paths from material shared publicly. This does not mean removing scientific provenance from the private analysis record; retain enough non-sensitive detail for another person to reproduce the problem. No automated issue submission or message sending is part of this guide.
