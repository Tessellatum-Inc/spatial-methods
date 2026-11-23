#!/usr/bin/env python3
"""Screen cross-date consistency of Sentinel-1 local incidence-angle rasters.

This compares geometry diagnostics on a common pixel grid. It is not a
geolocation, co-registration, terrain-correction, or radiometric QA test.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path

import numpy as np
import rasterio


def compare_angle_rasters(paths: list[Path]) -> dict:
    if len(paths) < 2:
        raise ValueError("At least two local-incidence-angle rasters are required.")
    scenes = []
    grid = None
    for path in sorted(paths):
        with rasterio.open(path) as ds:
            signature = (ds.crs, ds.transform, ds.width, ds.height, ds.count)
            if ds.count != 2:
                raise ValueError(f"{path} must contain angle and dataMask bands.")
            if grid is None:
                grid = signature
            elif signature != grid:
                raise ValueError("Local-incidence-angle rasters do not share an identical grid.")
            angle = ds.read(1).astype(np.float32)
            valid = (ds.read(2) > 0.5) & np.isfinite(angle) & (angle >= 0) & (angle <= 180)
        scenes.append((path.name, angle, valid))

    baseline_name, baseline, baseline_valid = scenes[0]
    comparisons = []
    for name, angle, valid in scenes[1:]:
        common = baseline_valid & valid
        if not common.any():
            raise ValueError(f"No common valid angle pixels for {name}.")
        delta = np.abs(angle[common] - baseline[common]).astype(np.float64)
        comparisons.append({
            "baseline_file": baseline_name,
            "comparison_file": name,
            "common_valid_pixels": int(common.sum()),
            "common_valid_fraction": float(common.mean()),
            "absolute_delta_degrees": {
                "median": float(np.median(delta)),
                "p95": float(np.percentile(delta, 95)),
                "p99": float(np.percentile(delta, 99)),
                "maximum": float(delta.max()),
                "fraction_above_0_1_degree": float(np.mean(delta > 0.1)),
            },
        })
    return {
        "schema": "tessellatum.sentinel1.local-incidence-angle-consistency.v1",
        "created_at_utc": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "scene_count": len(scenes),
        "baseline_file": baseline_name,
        "comparisons": comparisons,
        "status": "geometry_consistency_screen_only",
        "analysis_ready": False,
        "limitations": [
            "Near-identical incidence-angle surfaces do not prove sub-pixel co-registration or geolocation accuracy.",
            "This screen does not evaluate DEM slope/aspect, layover, radar shadow, radiometric terrain correction, or stable tie points.",
            "The first chronologically sorted raster is the comparison baseline; no normalization is applied.",
        ],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rasters", nargs="+", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    report = compare_angle_rasters(args.rasters)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(f"Compared {len(report['comparisons'])} incidence-angle surfaces; analysis_ready=false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
