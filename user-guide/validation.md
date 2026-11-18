# Validation of this review edition

**Reference validation record · 18 November 2026**

## Environment and scope

The examples were checked on Windows x86-64, Python 3.12.12, published Core 4.4.1 and CLI 1.9.2, NumPy 2.4.1, rasterio 1.5.0 and pandas 2.3.3, using one thread. Core/CLI were loaded from isolated review storage. The existing older development environment was not upgraded. Input data are original artificial signals, not observations of a real site.

## Observed results

| Check | Result |
| --- | --- |
| Regular 16-day SP example | PASS; 138 fitted-series/QA files and 42 seasonal/QA files |
| Monthly 1/11/21 schedule | PASS; 216 fitted-series/QA files and 42 seasonal/QA files |
| Two-class SP/DL example | PASS; 138 fitted-series/QA files and 42 seasonal/QA files |
| Binary QA-gap example | PASS; 138 fitted-series/QA files and 42 seasonal/QA files |
| Daily example | PASS; 2190 fitted-series/QA files and 42 seasonal/QA files |
| Same-pixel CLI single-series service versus raster batch | Maximum absolute fitted-value difference 0 |
| GUI-source preview service versus daily raster batch | 1095 dates; maximum absolute fitted-value difference 0 |
| AMPL comparison | Maximum absolute difference 0 |
| TPROD after documented /1000 raster conversion | Maximum absolute difference approximately 6.8×10⁻⁹ |
| SPROD after documented /1000 raster conversion | Maximum absolute difference approximately 3.0×10⁻⁹ |
| Run help, stdin snapshot/raster execution, legacy JSON migration/load | PASS |
| Nonempty dataset destination | Generator correctly refused to overwrite it |
| Default leap-calendar and output-year dropping checks | PASS |
| Editable illustration generation | PASS |

The output checker inspects inventory, dimensions, CRS/transform, dtypes, NoData, finite unmasked values, QA ranges and seasonal variation. Numerical fits were checked at absolute tolerance 10⁻⁶; transformed metrics used absolute 10⁻⁶ and relative 10⁻⁵. These bounds describe this fixture, not a universal software tolerance or biological accuracy claim.

## Migration execution check

The migrated generator, all five raster cases, output checks and plotting helper
were also rerun from this documentation repository's root using the environment
above. All passed. Generated datasets, images and raster outputs were kept in
separate review storage outside the repository. This distribution check confirms
the migrated example paths and helper execution; it does not extend the scope
of the earlier GUI-service comparison to end-user desktop interactions.

## What these checks do not establish

The GUI comparison exercised source services matching the v1.6.2 application implementation with the pinned published CLI/Core. It did not exhaustively test every frozen end-user executable or every UI action. The checks do not establish clean installation on all platforms, arbitrary fractional-QA mappings, nonidentity calibration, all calendar/method combinations, cloud reliability, interruption recovery or independent biological accuracy.

The confirmed compatible reference combination and the output-consistency requirement remain in force. Use [chapter 12](12-troubleshooting.md#124-previewbatch-comparisons) when investigating configuration-specific questions. Reproduce the included examples using the commands in the guide and [examples/README.md](../examples/README.md).
