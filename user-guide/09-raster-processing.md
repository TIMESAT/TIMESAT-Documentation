# 9 Running raster processing from the GUI

[Previous](08-exploration.md) · [Contents](table-of-contents.md) · [Next](10-raster-processing.md)

## 9.1 Prerequisites

GUI batch processing accepts loaded image-list or temporal-stack raster inputs. It does not process a table through the standard batch service. Complete the input and parameter checks in chapter 8. An input map preview or a table fit is not evidence that the entire raster run configuration is ready.

For a first run, use the small generated dataset and a new output directory. Prepare a record of the input files/date interpretation, calibration, QA mapping, selected method, season/threshold parameters, output schedule and component versions. Preserve a copy of any advanced CLI configuration before loading its subset into the GUI.

## 9.2 Outputs and run settings

1. Select exactly one ordinary fitting method: DL or SP. Clear the other comparison selection.
2. Open **Outputs** and choose an existing directory with **Browse...** under **Output Location**. Use a new directory for a new experiment to avoid overwriting matching output names.
3. Set **Output Time Step** and **NoData Value** deliberately. For a straightforward first GUI/CLI comparison, use daily output (1 day) with the generated daily configuration. When legacy and modern sampling keys coexist, modern fields can take precedence over the legacy interval. Inspect the effective batch settings and actual dates for other intervals; do not rely on the interval control alone for an advanced sampling configuration.
4. Set **YFit Prefix** and **VPP Prefix** if needed. Keep a naming convention that identifies the analysis without implying a different scientific metric.
5. In **VPP Outputs**, select the desired metrics and edit output names only where necessary. **Select All** restores selections and **Reset Names** restores source names. Renaming TPROD does not change its scale/units.
6. Open **Jobs**. Check the thread and resource settings and the readiness message.

The job controls require one selected method and an existing output folder. Additional problems can still be detected when the CLI reads the configuration or inputs. Readiness is a UI prerequisite check, not a scientific validation certificate.

## 9.3 Full data and subareas

Use **Run Full Data** to request the full raster. Use **Run Subarea** for the applicable loaded processing region. Confirm the intended region in the input/summary information before launching; small input datasets can have subarea loading ignored as described in chapter 8.

The GUI translates its user-facing region to CLI zero-based offsets and dimensions. The CLI retains the full raster profile and writes the chosen processing window; output bounds therefore do not prove every pixel was processed. Record the window and inspect values/QA inside and outside it.

For a large study area, first process a bounded representative region and inspect the outputs. Increase the extent only after confirming dates, values, units, quality and product selection.

## 9.4 Execution, records and logs

The GUI starts CLI processing and retains a run record containing grouped settings and, where required, resolved input lists. Preserve that record separately from the scientific output directory. The settings snapshot records the configuration actually submitted for the job.

The **Output Log** reports the job command/context, processing messages and CLI exit status. Preserve the run directory path shown in the log. The GUI's final status should indicate successful completion; a nonzero exit requires investigation even if files already exist. Store the effective settings snapshot with the analysis, since it is more informative than a screenshot of a few controls.

## 9.5 Threads, memory and stopping

Threads control spatial parallel processing. Avoid oversubscribing a workstation that is already running other jobs. The CLI's block planner estimates working arrays from width, input length, requested dates, years and a memory budget; it is not a hard operating-system memory cap. Raster-stack exploration has its own loading demand.

Confirm the effective `max_memory_gb` in the run snapshot before relying on a displayed memory value for a large job. A GUI control value alone does not establish which block-planning value the CLI used.

**Stop** terminates the running job. It does not pause a recoverable checkpoint. Files may be incomplete because datasets are opened before all blocks finish. Preserve the log and isolate the partial output directory. Correct the reason for stopping and rerun deliberately into a fresh directory; do not merge partial products into a complete result by filename alone.

## 9.6 Checking results

Check the exit status, `ST`/`VPP` inventory and dates, spatial metadata/window, NoData, QA and selected metrics. Inspect representative pixels and compare them with preview/terminal values under matching effective settings and the documented output conversions. Check the CSV/table precision limits before declaring a numerical discrepancy.

For the tutorial, daily processing produces 1095 fitted dates over 2021–2023, two ST files per date and 42 seasonal/QA files for the six selected metrics. A production run can differ in years, selected metrics and schedule; calculate its expected inventory from its own configuration. [Chapter 11](11-worked-examples.md) provides the generated inputs and checker.

The scope of completed execution checks is recorded in [validation](validation.md).
