#!/usr/bin/env python3
"""Screen Sentinel-1 rasters for relative pixel-grid alignment.

This is a diagnostic phase-correlation screen, not a substitute for tie-point
registration, geolocation validation, or radiometric calibration.
"""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import sys
import numpy as np
import rasterio


def _read_log_vv(path: Path):
    with rasterio.open(path) as ds:
        if ds.count < 3:
            raise ValueError(f"{path}: expected VV, VH and dataMask bands.")
        vv = ds.read(1).astype(np.float32)
        valid = (ds.read(3) > 0.5) & np.isfinite(vv) & (vv > 0)
        if not valid.any():
            raise ValueError(f"{path}: no valid positive VV pixels.")
        image = np.zeros(vv.shape, dtype=np.float32)
        image[valid] = np.log10(vv[valid])
        grid = {"crs": ds.crs.to_string() if ds.crs else None,
                "width": ds.width, "height": ds.height,
                "transform": list(ds.transform)[:6],
                "bounds": [float(v) for v in ds.bounds]}
    return image, valid, grid


def phase_correlation(reference, moving, valid):
    """Estimate translation of moving relative to reference in pixel units."""
    if reference.shape != moving.shape or reference.shape != valid.shape:
        raise ValueError("Phase-correlation arrays must have identical shapes.")
    if min(reference.shape) < 16 or int(valid.sum()) < 256:
        raise ValueError("Insufficient common pixels for phase-correlation screening.")
    ref = np.zeros(reference.shape, dtype=np.float64)
    mov = np.zeros(moving.shape, dtype=np.float64)
    ref[valid] = reference[valid] - reference[valid].mean()
    mov[valid] = moving[valid] - moving[valid].mean()
    window = np.outer(np.hanning(reference.shape[0]), np.hanning(reference.shape[1]))
    ref *= window
    mov *= window
    cross = np.fft.fft2(ref) * np.conj(np.fft.fft2(mov))
    cross /= np.maximum(np.abs(cross), 1e-12)
    corr = np.abs(np.fft.ifft2(cross))
    py, px = np.unravel_index(np.argmax(corr), corr.shape)

    def subpixel(values, index):
        n = len(values)
        before, centre, after = values[(index-1) % n], values[index], values[(index+1) % n]
        denom = before - 2.0 * centre + after
        return float(0.5 * (before-after) / denom) if abs(denom) >= 1e-12 else 0.0

    dy = float(py if py <= reference.shape[0]//2 else py-reference.shape[0]) + subpixel(corr[:, px], py)
    dx = float(px if px <= reference.shape[1]//2 else px-reference.shape[1]) + subpixel(corr[py, :], px)
    sidelobes = corr.copy()
    sidelobes[max(0,py-2):min(corr.shape[0],py+3), max(0,px-2):min(corr.shape[1],px+3)] = 0
    background = float(sidelobes.mean())
    return {"estimated_shift_pixels": {"x": dx, "y": dy},
            "shift_magnitude_pixels": float(np.hypot(dx,dy)),
            "peak_to_mean_sidelobe_ratio": float(corr[py,px]/background) if background > 0 else None,
            "common_valid_fraction": float(valid.mean()),
            "common_valid_pixels": int(valid.sum())}


def compare(reference_path: Path, moving_path: Path):
    ref, rv, rg = _read_log_vv(reference_path)
    mov, mv, mg = _read_log_vv(moving_path)
    if rg != mg:
        raise ValueError(f"Raster grids differ: {reference_path.name} vs {moving_path.name}.")
    result = phase_correlation(ref, mov, rv & mv)
    result.update({"reference_file": reference_path.name, "moving_file": moving_path.name,
                   "grid": rg, "method": "global phase correlation on log10(linear VV)"})
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rasters", nargs="+", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    if len(args.rasters) < 2:
        parser.error("At least two rasters are required.")
    if any(not p.is_file() for p in args.rasters):
        parser.error("Every input raster must exist.")
    try:
        comparisons = [compare(args.rasters[0], p) for p in args.rasters[1:]]
    except (ValueError, OSError, rasterio.errors.RasterioError) as exc:
        print(f"Registration screening failed: {exc}", file=sys.stderr)
        return 2
    magnitudes = [x["shift_magnitude_pixels"] for x in comparisons]
    report = {"schema": "tessellatum.sentinel1.registration-screen.v1",
              "created_at_utc": datetime.now(timezone.utc).isoformat().replace("+00:00","Z"),
              "reference_file": args.rasters[0].name, "comparison_count": len(comparisons),
              "comparisons": comparisons,
              "maximum_estimated_global_shift_pixels": max(magnitudes),
              "status": "screening_only_not_registration_validation", "analysis_ready": False,
              "limitations": [
                  "Phase correlation is a global image-content translation diagnostic, not geometric registration.",
                  "Temporal surface change, speckle, terrain effects and scene seams can influence the estimated shift.",
                  "No local tie-point, orbit, DEM, geolocation-error or radiometric calibration assessment is performed.",
                  "A small estimated shift is not proof of sub-pixel co-registration."
              ]}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2)+"\n", encoding="utf-8")
    print(f"Registration screening: {report['status']}")
    print(f"Maximum estimated global shift: {report['maximum_estimated_global_shift_pixels']:.4f} pixels")
    print(f"Report: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
