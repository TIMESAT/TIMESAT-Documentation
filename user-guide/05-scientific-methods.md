# 5 Scientific methods and seasonal interpretation

[Previous](04-input-data.md) · [Contents](table-of-contents.md) · [Next](06-parameters-and-configuration.md)

This chapter explains quality-guided fitting and seasonal interpretation for the reference versions. Scientific background is provided by the [references in appendix D](appendix-d-references.md); method availability and processing boundaries are stated below.

## 5.1 Processing sequence and observation weights

TIMESAT derives seasonal information from fitted trajectories. The ordinary processing sequence includes value-range and missing-value handling, removal of zero-weight observations, checks for usable variation, optional outlier filtering, baseline estimation, availability analysis, optional baseline gap filling, temporal extension, fitting and seasonal-metric extraction.

Quality information assigns relative influence to observations. A zero weight excludes a value from the retained fitting observations. Positive weights allow differing influence; they are not automatically calibrated inverse variances or probabilities that a measurement is correct. A sensor's class definitions and the scientific objective determine whether a proposed weighting scheme is appropriate. There is no universal cloud/quality mapping suitable for every input product.

A series can fail processing even when several values are present. The code checks retained data and variation, including adjacent changes; a constant sequence does not become a meaningful vegetation season because a smoother can be evaluated. Inspect missing/constant series and output quality rather than interpreting every output slot as a detected season.

## 5.2 Range policies and baseline estimation

`p_ylu` supplies lower and upper bounds in the units passed to Core. Each class can independently choose how to handle values beyond each bound:

| Mode | Treatment |
| --- | --- |
| 0 | Keep the stored value but set its weight to zero; it is excluded from subsequent retained observations |
| 1 | Clip to the boundary and retain its weight |
| 2 | Clip to the boundary and multiply its weight by `rangedownweight` |

Invalidating a water/cloud artefact and clipping a physically plausible low vegetation value are different scientific decisions. Report the chosen policy. Loader defaults are not product-specific recommendations.

The preprocessing **baseline** is estimated from retained observations with positive weights across the record. With `p_low_percentile <= 0`, the minimum is used. Within the documented interval 0–1, a positive value selects a low order statistic; for example, 0.05 represents a 5% setting, not 5. Observations below the estimated baseline are removed before ordinary fitting. The exact discrete estimate depends on record length and retained observations.

This record-level baseline supports fitting and optional gap handling. It differs from the per-season baseline reported as `MINV`, which is the average of the left and right seasonal minima. Keep both meanings distinct in methods descriptions.

## 5.3 Outliers, availability and gaps

Optional outlier detection fits an initial smoothing spline and examines absolute residuals. A retained point is rejected when its residual meets both global and local median-based cutoffs. The outlier routine uses a factor of six and a local half-window of 45 synthetic days. It is not the old manual's neighbour-based median filter, and its parameters are not the same as the separate user-controlled availability window.

`p_davailwin` is the half-width used to count retained observations around a fitted date. A value of 45 means approximately ±45 synthetic days within the covered extent, rather than a total 45-day interval. These counts support fitted-series QA and optional gap handling.

With `p_fillbase=1`, baseline-valued, unit-weight control observations are inserted in periods identified as having no observations by this availability analysis. This supplies modelling support rather than new measurements. It can be unsuitable for a gap that spans real green vegetation. Compare sensitivity and report its use.

Core also extends boundary support by copying portions of the first/last years into an extended modelling interval. This assumes useful seasonal context and is distinct from supplying independent buffer-year observations. Duplicated support is not evidence of measured vegetation behaviour outside the observed record. A single-year analysis particularly needs caution about incomplete or boundary-crossing seasons. Do not import a universal historical rule that an n-year record always yields exactly n-minus-one seasons.

## 5.4 Double logistic fitting

Double logistic fitting represents green-up and decline with paired logistic transitions. A useful form for understanding the seasonal shape is

$$
f(t)=b+\sum_k A_k\left[
\frac{1}{1+\exp((a_k-t)/s_k)}-
\frac{1}{1+\exp((c_k-t)/d_k)}\right].
$$

Here `b` represents a baseline, `A` an amplitude contribution, `a`/`c` transition locations, and `s`/`d` transition scales. This is an explanatory parameterization, not the JSON interface: users configure processing/season definitions rather than entering these coefficients directly. The implementation estimates constrained model parameters from dated observations and seasonal context.

DL can describe a smooth seasonal rise and fall using a small set of shape parameters. Complex shoulders, management events or multiple overlapping seasonal signals still need inspection. A good-looking sigmoid is not proof that its transition is a specified biological event. The robust seasonal modelling background is discussed by [Jönsson et al. (2018)](https://doi.org/10.3390/rs10040635); method-specific implementation is defined by the selected Core release.

## 5.5 Smoothing splines and upper-envelope adaptation

A smoothing spline balances agreement with weighted observations against curve roughness. In conceptual notation, a cubic spline minimizes a weighted residual criterion plus a penalty on its second derivative. The smoothing parameter controls the balance: weaker penalization permits more local variation, while stronger penalization suppresses it. The weight convention and numeric stiffness parameter are those of Core's spline implementation; weights should not be interpreted as statistical measurement variances without an explicit model.

For SP, `p_smooth` is the fitting stiffness control. A larger value generally produces a smoother trajectory; it is not a DL fit-strength parameter or a Savitzky–Golay half-window. Data units, observation density and weighting affect a sensible setting. Inspect several representative series and assess sensitivity instead of selecting a parameter from a different product without checking.

Upper-envelope adaptation iteratively reduces the influence of observations below an earlier fit. Its rationale is useful where relevant contamination is predominantly negative. It can also emphasize isolated high values or suppress valid low observations; it should not be applied mechanically to every variable.

`p_nenvi=1` means one fit with no extra envelope pass; 2 and 3 give one and two additional passes. GUI labels **no**, **1**, **2** refer to the number of additional passes. `p_wfactnum` controls adaptation through a reciprocal factor in Core. A value of 1 gives no extra downweighting strength; the GUI's normal strength range is 1–10. Keep it positive and report it with the iteration count.

## 5.6 Regular and irregular season structure

Season structure supplies coarse temporal context for fitting and event extraction. It is not the same as an output sampling interval.

| Setting | Meaning of `p_seapar` |
| --- | --- |
| `p_seasonmethod=1`, irregular | Controls the coarse-season spline stiffness. Core uses bounded linear interpolation: `1000 + 49000 × p_seapar`, limited to 1000–50000 |
| `p_seasonmethod=2`, regular | Controls the primary/secondary seasonal structure in the sinusoidal coarse fit; the interpretation concerns seasonal amplitude relationships rather than spline stiffness |

For irregular seasons, a lower coarse stiffness can retain more peaks; increasing it can merge small fluctuations into a simpler seasonal structure. For regular seasons, inspect the coarse structure and the single/dual-season behaviour rather than transferring an irregular-season tuning interpretation. Neither a coarse peak nor an allocated output slot guarantees an accepted season.

## 5.7 Start/end definitions and supported combinations

Start of season (SOS) and end of season (EOS) are operational thresholds on fitted curves. A threshold fraction requires the amplitude definition; a threshold in variable units requires the baseline/offset convention.

| `p_startmethod` | Current meaning | Irregular seasons | Regular seasons |
| --- | --- | --- | --- |
| 1 | A fraction of seasonal amplitude above the relevant left/right minimum | Implemented | Implemented |
| 2 | An absolute **increment above** the relevant left/right minimum, with fallback when the target is not attainable | Implemented | Implemented |
| 3 | Record-relative amplitude based on robust peak/base summaries, with fallback logic | Implemented | Outside the documented standard combinations |
| 4 | GUI's STL/Loess label | Active trend decomposition for this threshold has not been established; exclude from standard procedures | Outside the documented standard combinations |

Method 2 is not simply a fixed absolute y-value independent of the local minimum. The two elements of `p_startcutoff` define start and end separately. Method 1 uses side-specific minima and the implemented seasonal amplitude; it does not require equal start/end values. Fallbacks can change which threshold is actually used; inspect seasonal QA and retain the requested configuration.

Guide workflows use DL/SP (`p_fitmethod` 1/2). Legacy SG/asymmetric Gaussian/STL processing must not be inferred from old method-number tables; use the supported combinations above for the reference procedures.

## 5.8 Selection and validation

Choose methods by the variable's seasonal structure, sampling, contamination and research objective. Test representative good, sparse, low-amplitude, multiple-season and boundary series. Compare alternate smoothing, weighting and thresholds, and evaluate independently where suitable reference data exist. Report excluded cases and the definition of success. The comparative study by [Cai et al. (2017)](https://doi.org/10.3390/rs9121271) provides methodological context; it does not establish a universal best setting or validate every current product/workflow.

Distinguish evaluating a complete historical record from evaluating a record truncated at a decision date. Including later observations makes a comparison retrospective; output-year trimming does not remove those later observations from fitting. Boundary copying and a temporal-context experiment are not evidence of general forecasting skill.
