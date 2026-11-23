#!/usr/bin/env python3
"""Compare ellipsoid and terrain-corrected Sentinel-1 backscatter on common valid pixels.

This is a paired processing-branch diagnostic, not a calibration or validation
of radiometric equivalence. Inputs must share an identical raster grid.
"""
from __future__ import annotations

import argparse
from datetime import datetime
import json
from pathlib import Path

import numpy as np
import rasterio


def _quantiles(values: np.ndarray) -> dict:
    q = np.percentile(values, [1, 5, 25, 50, 75, 95, 99])
    return {
        "min": float(np.min(values)), "p01": float(q[0]), "p05": float(q[1]),
        "p25": float(q[2]), "median": float(q[3]), "p75": float(q[4]),
        "p95": float(q[5]), "p99": float(q[6]), "max": float(np.max(values)),
    }


def compare_pair(ellipsoid_path: Path, rtc_path: Path) -> dict:
    with rasterio.open(ellipsoid_path) as ell, rasterio.open(rtc_path) as rtc:
        if ell.count < 3 or rtc.count != 6:
            raise ValueError("Expected ellipsoid VV/VH/dataMask (3 bands) and RTC six-band raster.")
        if (ell.crs != rtc.crs or ell.transform != rtc.transform
                or (ell.width, ell.height) != (rtc.width, rtc.height)):
            raise ValueError("Ellipsoid and RTC rasters do not have identical grids.")
        base = ell.read([1, 2, 3]).astype(np.float32)
        terrain = rtc.read().astype(np.float32)

    common = ((base[2] > 0.5) & (terrain[5] > 0.5)
              & np.isfinite(base).all(axis=0) & np.isfinite(terrain).all(axis=0))
    if not common.any():
        raise ValueError("No common valid pixels between ellipsoid and RTC rasters.")
    result = {
        "ellipsoid_file": ellipsoid_path.name,
        "rtc_file": rtc_path.name,
        "grid": {"width": int(base.shape[2]), "height": int(base.shape[1])},
        "ellipsoid_valid_pixels": int(np.count_nonzero(base[2] > 0.5)),
        "rtc_valid_pixels": int(np.count_nonzero(terrain[5] > 0.5)),
        "common_valid_pixels": int(common.sum()),
        "common_valid_fraction_of_grid": float(common.mean()),
        "rtc_shadow_fraction_of_common_valid_pixels": float(np.mean(terrain[4][common] > 0.5)),
        "scattering_area_quantiles_on_common_valid": _quantiles(terrain[2][common]),
        "polarizations": {},
        "interpretation": (
            "Descriptive paired difference between two processing branches. "
            "Not evidence of radiometric equivalence, calibration accuracy, or suitability for change detection."
        ),
    }
    for index, name in ((0, "VV"), (1, "VH")):
        a, b = base[index][common], terrain[index][common]
        positive = (a > 0) & (b > 0)
        if not positive.any():
            raise ValueError(f"No common positive linear-power pixels for {name}.")
        ell_db = 10.0 * np.log10(a[positive].astype(np.float64))
        rtc_db = 10.0 * np.log10(b[positive].astype(np.float64))
        delta = rtc_db - ell_db
        result["polarizations"][name] = {
            "positive_common_pixels": int(positive.sum()),
            "ellipsoid_median_db": float(np.median(ell_db)),
            "rtc_median_db": float(np.median(rtc_db)),
            "rtc_minus_ellipsoid_db": {
                "mean": float(np.mean(delta)),
                "median": float(np.median(delta)),
                "mean_absolute": float(np.mean(np.abs(delta))),
                "quantiles": _quantiles(delta),
            },
        }
    return result


def run(stack_metadata: Path, ellipsoid_dir: Path, rtc_dir: Path, output: Path) -> dict:
    stack = json.loads(stack_metadata.read_text(encoding="utf-8"))
    scenes = stack.get("scenes")
    if not isinstance(scenes, list) or len(scenes) < 2:
        raise ValueError("Stack metadata must contain at least two scenes.")
    comparisons = []
    failures = []
    for scene in scenes:
        try:
            stamp = datetime.fromisoformat(
                scene["catalog_item_datetime_utc"].replace("Z", "+00:00")
            ).strftime("%Y%m%dT%H%M%SZ")
            ell_path = ellipsoid_dir / scene["output"]["file"]
            rtc_path = rtc_dir / f"sentinel1_nairobi_{stamp}_gamma0-terrain-rtc.tif"
            comparisons.append(compare_pair(ell_path, rtc_path))
        except (KeyError, OSError, ValueError) as exc:
            failures.append({"scene": scene.get("catalog_item_datetime_utc"), "error": str(exc)})
    report = {
        "schema": "tessellatum.sentinel1.ellipsoid-vs-terrain-paired-screen.v1",
        "scene_count": len(scenes),
        "compared_count": len(comparisons),
        "failed_count": len(failures),
        "comparisons": comparisons,
        "failures": failures,
        "status": "paired_diagnostic_only" if not failures and len(comparisons) == len(scenes) else "incomplete_paired_diagnostic",
        "analysis_ready": False,
        "limitations": [
            "Only pixels valid in both processing branches are compared; this can select a non-random subset.",
            "The same requested output grid does not establish pixel-level geometric correspondence.",
            "Terrain correction changes both geometric and radiometric processing; differences must not be interpreted as a simple terrain-only correction.",
            "No automatic normalization, resampling, masking beyond common data validity, or change detection is performed.",
        ],
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    if failures or len(comparisons) != len(scenes):
        raise RuntimeError(f"Paired comparison incomplete: {len(comparisons)}/{len(scenes)} scenes.")
    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--stack-metadata", type=Path, default=Path("data/sentinelhub/nairobi/stack/sentinel1_nairobi_temporal_stack.metadata.json"))
    parser.add_argument("--ellipsoid-dir", type=Path, default=Path("data/sentinelhub/nairobi/stack"))
    parser.add_argument("--rtc-dir", type=Path, default=Path("data/sentinelhub/nairobi/stack/terrain_aux"))
    parser.add_argument("--output", type=Path, default=Path("data/sentinelhub/nairobi/stack/terrain_aux/sentinel1_nairobi_ellipsoid_vs_terrain_paired_screen.json"))
    args = parser.parse_args(argv)
    try:
        report = run(args.stack_metadata, args.ellipsoid_dir, args.rtc_dir, args.output)
    except (OSError, ValueError, RuntimeError) as exc:
        parser.exit(2, f"Paired comparison failed: {exc}\n")
    print(f"Compared {report['compared_count']} scenes; analysis_ready=false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
