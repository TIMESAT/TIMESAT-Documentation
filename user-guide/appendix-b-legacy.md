# Appendix B Current and legacy workflows

[Previous](appendix-a-glossary.md) · [Contents](table-of-contents.md) · [Next](appendix-c-advanced-interfaces.md)

The older manuals preserve important scientific background and historical reproducibility information. Use them to understand a historical analysis together with its actual software version. Do not translate an old instruction into a current command by changing the program name alone.

| Historical material | Current guide treatment |
| --- | --- |
| MATLAB/MCR installers, MATLAB menus and TSM tools | Official Qt desktop release and separate Python CLI installation; no MATLAB Runtime instruction |
| GUI directly launching standalone Fortran executables | GUI -> CLI processing services/program -> Core |
| TSF_process and binary post-processing executables | Current CLI `run` pipeline writes raster products directly |
| Row-numbered `.set` settings | Grouped JSON with input/output/general/classes; the current migration command is for an older JSON schema |
| `.tts`, `.tpa` and `.ndx` output instructions | GeoTIFF ST/VPP/QA and current interactive CSV/figure exports |
| Count header at the beginning of an image list | One path per line in current lists; no count header |
| Mandatory GeoTIFF-to-ENVI conversion tool | Current documented workflows accept GeoTIFF lists/stacks; old conversion steps are not prerequisites |
| Method codes for SG, asymmetric Gaussian and DL | Ordinary current dispatch is 1 DL, 2 SP; special codes require their own contract |
| Savitzky–Golay half-window described under spline smoothing | Current SP stiffness is a different control |
| Four universally usable start/end methods | Current season/threshold compatibility matrix in section 5.7 |
| A fixed absolute y threshold for method 2 | Current code uses a side-minimum plus absolute increment, with fallback |
| Exponential coarse-season parameter formula | Current irregular-season mapping is bounded linear interpolation, 1000–50000 |
| “Middle of season” as mean of 80% crossing times | Current MAXD is the seasonal maximum position |
| Exactly n-minus-one seasons from n input years | Current extension/allocation/acceptance must be interpreted from data and QA, not a universal historical count |
| Universal three-class QA rule limit | Current equality/range rule list with later-match precedence and unmatched-zero behaviour |

For a historical result, retain its original settings, inputs, calendar, product units and software. Reproducing that historical environment is distinct from rerunning a translated configuration in Core 4.4.1. Compare matched observations and definitions before attributing a difference to a scientific change.

The underlying scientific ideas retained in this guide include quality-guided fitting, careful envelope adaptation, data-dependent method selection, distinct baseline concepts, operational seasonal thresholds and inspection of representative series. Exact old formulas, defaults, licences, compiler/platform statements and output numbering require version-specific checking.
