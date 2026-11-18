# Appendix D References and acknowledgements

[Previous](appendix-c-advanced-interfaces.md) · [Contents](table-of-contents.md) · [Guide home](../README.md)

## D.1 Scientific references

The following bibliographic records were checked against publisher or author-institution sources. Earlier papers describe historical methods and scientific foundations; a paper's method inventory does not establish that all of those methods are ordinary options in Core 4.4.1.

1. Jönsson, P., and Eklundh, L. (2002). Seasonality extraction by function fitting to time-series of satellite sensor data. *IEEE Transactions on Geoscience and Remote Sensing*, 40(8), 1824–1832. [DOI: 10.1109/TGRS.2002.802519](https://doi.org/10.1109/TGRS.2002.802519). [Author-institution record](https://lup.lub.lu.se/search/publication/bd9045a5-a020-4969-b038-ae638f29dff8).
2. Jönsson, P., and Eklundh, L. (2004). TIMESAT—a program for analyzing time-series of satellite sensor data. *Computers & Geosciences*, 30(8), 833–845. [DOI: 10.1016/j.cageo.2004.05.006](https://doi.org/10.1016/j.cageo.2004.05.006). [Author-institution record](https://portal.research.lu.se/en/publications/timesat-a-program-for-analyzing-time-series-of-satellite-sensor-d/).
3. Cai, Z., Jönsson, P., Jin, H., and Eklundh, L. (2017). Performance of Smoothing Methods for Reconstructing NDVI Time-Series and Estimating Vegetation Phenology from MODIS Data. *Remote Sensing*, 9(12), 1271. [DOI: 10.3390/rs9121271](https://doi.org/10.3390/rs9121271). [Author-institution record](https://portal.research.lu.se/en/publications/performance-of-smoothing-methods-for-reconstructing-ndvi-time-ser/).
4. Jönsson, P., Cai, Z., Melaas, E., Friedl, M., and Eklundh, L. (2018). A Method for Robust Estimation of Vegetation Seasonality from Landsat and Sentinel-2 Time Series Data. *Remote Sensing*, 10(4), 635. [DOI: 10.3390/rs10040635](https://doi.org/10.3390/rs10040635). [Publisher article](https://www.mdpi.com/2072-4292/10/4/635).

The guide's scientific narrative also draws on earlier TIMESAT 4 manuals attributed to Zhanzhang Cai, Lars Eklundh and Per Jönsson. Scientifically accurate concepts were retained and reconciled with the reference software; historical execution instructions were replaced. Those original manuscripts are not included in this repository.

## D.2 Software and release records

Record the actual software versions alongside scientific citations:

| Component | Reference release and authoritative publication link |
| --- | --- |
| TIMESAT 4 Core | [timesat 4.4.1 on PyPI](https://pypi.org/project/timesat/4.4.1/) |
| TIMESAT CLI | [timesat-cli 1.9.2 on PyPI](https://pypi.org/project/timesat-cli/1.9.2/) and [GitHub release](https://github.com/TIMESAT/TIMESAT-CLI/releases/tag/v1.9.2) |
| TIMESAT GUI | [official GUI v1.6.2 executable release](https://github.com/TIMESAT/TIMESAT-GUI/releases/tag/v1.6.2) |

Cite the actual software release/version records above and use a matching maintainer-supplied software DOI where available. A historical citation pointer should not be assumed to identify another binary. Record the software components and versions actually used, separately from scientific-method citations.

## D.3 Licences, data and figure provenance

Obtain and read the LICENSE/NOTICE files delivered with the Core, CLI and GUI releases listed above and their dependency notices. The public [CLI 1.9.2 licence](https://github.com/TIMESAT/TIMESAT-CLI/blob/258b50565b322d9f5bafd9df9b822c80ca09a847/LICENSE) does not change Core or GUI terms. These are separate component licences; this guide does not replace or expand them. No document reuse licence is assigned by this migration.

Figure 2.1 is an original diagram of the source-verified architecture. Figure 11.1 is an original plot of the generated synthetic dataset and published Core/CLI processing. It contains no real study-site observations or screenshots. Synthetic example source is in [the example directory](../examples/README.md), and [asset provenance](../assets/README.md) records generation. No older restricted/no-derivatives figure was edited or reused.

## D.4 Acknowledgements

Per Jönsson and Lars Eklundh are the original TIMESAT developers and scientific founders. Zhanzhang Cai develops TIMESAT 4 Core, TIMESAT CLI and TIMESAT GUI.

The current User Guide has the following authorship and contribution roles:

| Contributor | Role |
| --- | --- |
| Zhanzhang Cai | Lead author and editor |
| Lars Eklundh | Scientific and technical reviewer |
| Per Jönsson | Scientific guidance |

Preserve applicable third-party notices.

The guide describes the [reference versions](../README.md#reference-versions) and the bounded checks in [validation](validation.md). It does not claim independent biological accuracy or validation of every platform, input product or configuration.
