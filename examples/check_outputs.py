"""Check the generated chapter 11 example's files, metadata and basic signal.

This checks execution and data contracts, not biological/scientific validation.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import rasterio


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("settings", type=Path, help="One generated settings JSON")
    config = json.loads(parser.parse_args().settings.read_text(encoding="utf-8"))
    output = config["output"]
    folder = Path(output["outputfolder"])
    n_dates = 108 if output["time_sampling"] == "monthly" else len(
        range(0, 3 * 365, output["time_step_days"]))
    st = sorted((folder / "ST").glob("*.tif"))
    vpp = sorted((folder / "VPP").glob("*.tif"))
    assert len(st) == 2 * n_dates, (len(st), 2 * n_dates)
    assert len(vpp) == 42, (len(vpp), 42)
    with rasterio.open(config["input"]["image_file_list"]) as source:
        crs, transform = source.crs, source.transform
    finite_values = []
    qa_codes = set()
    for path in st + vpp:
        with rasterio.open(path) as ds:
            assert (ds.width, ds.height, ds.count) == (4, 4, 1), path.name
            assert ds.crs == crs and ds.transform == transform, path.name
            values = ds.read(1, masked=True).compressed()
            assert np.isfinite(values).all(), path.name
            if "_QA" in path.name:
                assert ds.dtypes[0] == "uint8" and ds.nodata == 0, path.name
                qa_codes.update(map(int, values))
            else:
                assert ds.dtypes[0] == "float32" and ds.nodata == -9999, path.name
                if path.parent.name == "ST":
                    finite_values.extend(values.tolist())
    assert finite_values and max(finite_values) - min(finite_values) > .2
    assert qa_codes and qa_codes <= set(range(1, 11)), qa_codes
    report = {"status": "PASS", "st_files": len(st), "vpp_files": len(vpp),
              "qa_codes_present": sorted(qa_codes),
              "fitted_range": [min(finite_values), max(finite_values)],
              "scope": "Files, metadata, finite values and seasonal variation only"}
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
