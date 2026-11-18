"""Generate original synthetic inputs for chapter 11; never overwrite a dataset.

Requirements: numpy and rasterio. No satellite or private data are included.
"""
from __future__ import annotations

import argparse
import copy
import csv
import datetime as dt
import json
from pathlib import Path

import numpy as np
import rasterio
from rasterio.transform import from_origin


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path, help="New or empty example directory")
    root = parser.parse_args().directory.expanduser().resolve()
    if root.exists() and any(root.iterdir()):
        raise SystemExit("Choose a new or empty directory; existing data are preserved.")
    root.mkdir(parents=True, exist_ok=True)
    dates = [dt.date(year, 1, 1) + dt.timedelta(days=d - 1)
             for year in (2021, 2022, 2023) for d in range(1, 362, 10)]
    doy = np.array([d.timetuple().tm_yday for d in dates], dtype=float)
    shifts = np.tile(np.array([0., 0., 20., 20.]), (4, 1))
    t = doy[:, None, None]
    values = (.15 + .65 * (1 / (1 + np.exp(-(t - 100 - shifts) / 12))
                           - 1 / (1 + np.exp(-(t - 270 - shifts) / 18))))
    values = values.astype("float32")
    qa = np.ones(values.shape, dtype="uint8")
    qa_gap = qa.copy()
    qa_gap[(doy >= 140) & (doy <= 170)] = 0
    profile = dict(driver="GTiff", width=4, height=4, count=len(dates),
                   crs="EPSG:32633", transform=from_origin(500000, 6200000, 10, 10))
    for filename, array in [("vi_stack.tif", values), ("qa_stack.tif", qa),
                            ("qa_gap_stack.tif", qa_gap)]:
        with rasterio.open(root / filename, "w", dtype=array.dtype,
                           nodata=-9999 if array.dtype.kind == "f" else 255, **profile) as ds:
            ds.write(array)
            for i, date in enumerate(dates, 1):
                ds.set_band_description(i, date.strftime("%Y%m%d"))
    lc = np.tile(np.array([1, 1, 2, 2], dtype="uint8"), (4, 1))
    lc_profile = dict(profile, count=1)
    with rasterio.open(root / "landcover.tif", "w", dtype="uint8", nodata=255,
                       **lc_profile) as ds:
        ds.write(lc, 1)
    with (root / "series.csv").open("w", encoding="utf-8", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(["date", "series_a", "series_b"])
        writer.writerows((date.isoformat(), float(values[i, 0, 0]),
                          float(values[i, 0, 2])) for i, date in enumerate(dates))
    class1 = dict(landuse=1, p_fitmethod=2, p_smooth=1000, p_nenvi=1,
                  p_wfactnum=1, p_startmethod=1, p_startcutoff=[.25, .15],
                  p_low_percentile=.05, p_fillbase=0, p_seasonmethod=1,
                  p_seapar=1, lowrangemode=0, highrangemode=0, rangedownweight=.5)
    config = {
        "input": {"image_file_list": (root / "vi_stack.tif").as_posix(),
                  "quality_file_list": (root / "qa_stack.tif").as_posix()},
        "output": {"outputfolder": (root / "outputs").as_posix(), "outputvariables": 1,
                   "time_sampling": "regular", "time_step_days": 16,
                   "drop_first_year": False, "drop_last_year": False,
                   "p_nodata": -9999, "p_hrvppformat": 1, "vpp_dtype": "float32",
                   "vpp_variables": ["SOSD", "EOSD", "MAXD", "AMPL", "TPROD", "SPROD"]},
        "general": {"p_a": [[0, 0], [1, 1]], "p_ylu": [0, 1.2],
                    "p_ignoreday": 366, "p_band_id": 1, "scale": 1, "offset": 0,
                    "p_outlier": 0, "p_davailwin": 45, "max_memory_gb": 1,
                    "classes": [class1]},
        "metadata": {"provenance": "Original synthetic User Guide example",
                     "years": [2021, 2022, 2023], "observations": len(dates),
                     "units": "dimensionless synthetic index; no real site"},
    }
    cases = {"settings": config}
    daily = copy.deepcopy(config)
    daily["output"].update(time_step_days=1, outputfolder=(root / "outputs_daily").as_posix())
    cases["settings_daily"] = daily
    monthly = copy.deepcopy(config)
    monthly["output"].update(time_sampling="monthly", monthly_days=[1, 11, 21],
                              outputfolder=(root / "outputs_monthly").as_posix())
    cases["settings_monthly"] = monthly
    multiclass = copy.deepcopy(config)
    multiclass["input"]["lc_file"] = (root / "landcover.tif").as_posix()
    multiclass["general"]["classes"].append(dict(class1, landuse=2, p_fitmethod=1))
    multiclass["output"]["outputfolder"] = (root / "outputs_multiclass").as_posix()
    cases["settings_multiclass"] = multiclass
    gap = copy.deepcopy(config)
    gap["input"]["quality_file_list"] = (root / "qa_gap_stack.tif").as_posix()
    gap["output"]["outputfolder"] = (root / "outputs_qa_gap").as_posix()
    cases["settings_qa_gap"] = gap
    for name, cfg in cases.items():
        Path(cfg["output"]["outputfolder"]).mkdir()
        (root / (name + ".json")).write_text(json.dumps(cfg, indent=2) + "\n", encoding="utf-8")
    (root / "README.txt").write_text(
        "Synthetic TIMESAT User Guide example. No real satellite observations.\n"
        "4 x 4 pixels; 111 observations; 2021-2023; two seasonal timing profiles.\n"
        "The CRS/transform are synthetic metadata, not a real study site.\n"
        "Generated paths are absolute. Regenerate after relocating this dataset.\n",
        encoding="utf-8")
    print(f"Created {root}: {len(dates)} dates, 4 x 4 pixels, five configurations.")


if __name__ == "__main__":
    main()
