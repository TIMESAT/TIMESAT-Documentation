"""Create Figure 11.1 from the generated example using CLI fitting services."""
from __future__ import annotations

import argparse
import datetime as dt
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
from timesat_cli.config import build_param_array, load_config
from timesat_cli.readers import open_image_data, read_file_lists
from timesat_cli.single_pixel import run_single_pixel


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("settings", type=Path)
    parser.add_argument("image", type=Path, help="New PNG destination; must not exist")
    options = parser.parse_args()
    if options.image.exists():
        raise SystemExit("Choose a new image path; the existing figure is preserved.")
    s = load_config(str(options.settings)).settings
    tv, images, quality, years, first, _ = read_file_lists(
        s.tv_list, s.image_file_list, s.quality_file_list)
    y, w, lc = open_image_data(0, 0, 1, 1, images, quality, None, "float32", 1)
    fields = ["p_fitmethod", "p_smooth", "p_nenvi", "p_wfactnum", "p_startmethod",
              "p_low_percentile", "p_fillbase", "p_seasonmethod", "p_seapar",
              "p_lowrangemode", "p_highrangemode", "p_rangedownweight"]
    floats = {"p_smooth", "p_wfactnum", "p_low_percentile", "p_seapar", "p_rangedownweight"}
    arrays = {key: build_param_array(s, key, "float64" if key in floats else "int32",
                                    fill_value=.5 if key == "p_rangedownweight" else 0)
              for key in fields}
    arrays["p_startcutoff"] = build_param_array(
        s, "p_startcutoff", "float64", shape=(2,), fortran_2d=True)
    args = dict(raw_y=y, raw_w=w, raw_lc=lc, tv_yyyydoy=tv, yrstart=first,
                nyear=years, npt=len(tv), p_outststep=1, p_ignoreday=s.p_ignoreday,
                p_ylu=s.p_ylu, p_a=s.p_a, p_printflag=0, p_nodata=s.p_nodata,
                p_davailwin=s.p_davailwin, p_outlier=s.p_outlier,
                p_hrvppformat=s.p_hrvppformat, **arrays)
    sp = run_single_pixel(**args)
    args["p_fitmethod"] = np.ones(255, dtype="int32")
    dl = run_single_pixel(**args)
    observations = [dt.datetime.strptime(str(int(v)), "%Y%j") for v in tv]
    fig, ax = plt.subplots(figsize=(9.2, 3.6), layout="constrained")
    ax.scatter(observations, y[0, 0], s=14, color="#323a46", label="Synthetic observations", zorder=3)
    ax.plot(sp[6], sp[3][0, 0], color="#176b9b", lw=1.8, label="Smoothing spline")
    ax.plot(dl[6], dl[3][0, 0], color="#b55e24", lw=1.6, ls="--", label="Double logistic")
    ax.set(xlabel="Observation / fitted date", ylabel="Synthetic index (dimensionless)", ylim=(.08, .88))
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=6))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
    ax.grid(alpha=.2)
    ax.legend(loc="upper right", fontsize=8, ncol=3, frameon=False)
    fig.savefig(options.image, dpi=180)
    plt.close(fig)


if __name__ == "__main__":
    main()
