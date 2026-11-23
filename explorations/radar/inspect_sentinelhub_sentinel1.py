#!/usr/bin/env python3
"""Quality-check a Sentinel Hub Sentinel-1 VV/VH GeoTIFF and make a quicklook."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path

import numpy as np
import rasterio
from PIL import Image


def _finite_stats(values: np.ndarray) -> dict:
    finite = values[np.isfinite(values)]
    if finite.size == 0:
        return {"count": 0, "min": None, "max": None, "mean": None,
                "median": None, "p01": None, "p05": None, "p95": None, "p99": None}
    percentiles = np.percentile(finite, [1, 5, 95, 99])
    return {
        "count": int(finite.size),
        "min": float(np.min(finite)),
        "max": float(np.max(finite)),
        "mean": float(np.mean(finite)),
        "median": float(np.median(finite)),
        "p01": float(percentiles[0]),
        "p05": float(percentiles[1]),
        "p95": float(percentiles[2]),
        "p99": float(percentiles[3]),
    }


def inspect_raster(input_path: Path, output_dir: Path) -> tuple[Path, Path, dict]:
    output_dir.mkdir(parents=True, exist_ok=True)
    with rasterio.open(input_path) as ds:
        if ds.count != 3:
            raise ValueError(f"Expected 3 bands (VV, VH, dataMask); found {ds.count}.")
        if ds.width < 1 or ds.height < 1:
            raise ValueError("Raster dimensions must be positive.")
        vv = ds.read(1).astype(np.float32, copy=False)
        vh = ds.read(2).astype(np.float32, copy=False)
        data_mask = ds.read(3).astype(np.float32, copy=False)
        if not np.isfinite(data_mask).all():
            raise ValueError("dataMask contains non-finite values.")
        unique_mask = np.unique(data_mask)
        if not np.isin(unique_mask, [0.0, 1.0]).all():
            raise ValueError("dataMask must contain only 0 and 1.")
        valid = data_mask > 0.5
        if not valid.any():
            raise ValueError("Raster contains no valid data pixels.")
        valid_vv = vv[valid]
        valid_vh = vh[valid]
        if not np.isfinite(valid_vv).all() or not np.isfinite(valid_vh).all():
            raise ValueError("VV/VH contain non-finite values inside dataMask-valid pixels.")
        if np.any(valid_vv < 0) or np.any(valid_vh < 0):
            raise ValueError("Linear-power VV/VH values must not be negative.")

        vv_stats = _finite_stats(valid_vv)
        vh_stats = _finite_stats(valid_vh)
        coverage = float(valid.mean())
        center_lat = (ds.bounds.top + ds.bounds.bottom) / 2
        pixel_width_deg = abs(float(ds.transform.a))
        pixel_height_deg = abs(float(ds.transform.e))
        pixel_width_m = pixel_width_deg * 111320.0 * math.cos(math.radians(center_lat))
        pixel_height_m = pixel_height_deg * 110574.0
        crs = ds.crs.to_string() if ds.crs else None
        bounds = {
            "left": float(ds.bounds.left), "bottom": float(ds.bounds.bottom),
            "right": float(ds.bounds.right), "top": float(ds.bounds.top),
        }
        width, height = ds.width, ds.height

    # A log-scaled VV/VH composite is for inspection only, not quantitative analysis.
    def stretch(values: np.ndarray) -> np.ndarray:
        logged = np.full(values.shape, np.nan, dtype=np.float32)
        logged[valid] = np.log10(np.maximum(values[valid], 1e-8))
        sample = logged[valid]
        low, high = np.percentile(sample, [2, 98])
        if high <= low:
            return np.zeros(values.shape, dtype=np.float32)
        result = np.zeros(values.shape, dtype=np.float32)
        result[valid] = np.clip((sample - low) / (high - low), 0, 1)
        return result

    red = stretch(vv)
    green = stretch(vh)
    blue = np.sqrt(red * green)
    rgb = np.stack([red, green, blue], axis=-1)
    rgb[~valid] = 0
    quicklook = (np.clip(rgb, 0, 1) * 255).astype(np.uint8)
    quicklook_path = output_dir / f"{input_path.stem}.quicklook.png"
    Image.fromarray(quicklook, mode="RGB").save(quicklook_path)

    digest = hashlib.sha256(input_path.read_bytes()).hexdigest()
    status = "pass" if coverage >= 0.90 else "partial_coverage"
    report = {
        "created_at_utc": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "input_file": input_path.name,
        "input_sha256": digest,
        "format": "GeoTIFF",
        "crs": crs,
        "width": width,
        "height": height,
        "band_order": ["VV", "VH", "dataMask"],
        "data_mask": {
            "valid_pixels": int(valid.sum()),
            "total_pixels": int(valid.size),
            "valid_fraction": coverage,
            "valid_percent": round(coverage * 100, 4),
            "unique_values": [float(x) for x in unique_mask],
        },
        "pixel_spacing_approx": {
            "longitude_degrees": pixel_width_deg,
            "latitude_degrees": pixel_height_deg,
            "east_west_metres_at_raster_centre": pixel_width_m,
            "north_south_metres_at_raster_centre": pixel_height_m,
            "note": "Approximate geographic-grid spacing at raster centre; not a native-resolution claim.",
        },
        "bounds": bounds,
        "backscatter": {
            "coefficient": "GAMMA0_ELLIPSOID",
            "units": "LINEAR_POWER",
            "VV": vv_stats,
            "VH": vh_stats,
        },
        "quicklook": {
            "file": quicklook_path.name,
            "channels": {"red": "log-stretched VV", "green": "log-stretched VH",
                         "blue": "sqrt(VV_stretch * VH_stretch)"},
            "note": "Visualization only; not suitable for quantitative measurements.",
        },
        "quality_status": status,
        "quality_notes": (
            ["Less than 90% of the requested rectangular extent has valid scene pixels. "
             "Treat this as a partial-coverage scene and intersect the data mask with the study AOI."]
            if status == "partial_coverage" else []
        ),
    }
    report_path = output_dir / f"{input_path.stem}.qa.json"
    report_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    return quicklook_path, report_path, report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="Input three-band Sentinel-1 GeoTIFF.")
    parser.add_argument("--output-dir", type=Path, default=None)
    args = parser.parse_args()
    if not args.input.is_file():
        parser.error(f"Input raster does not exist: {args.input}")
    output_dir = args.output_dir or args.input.parent
    try:
        quicklook, report_path, report = inspect_raster(args.input, output_dir)
    except (ValueError, rasterio.errors.RasterioError) as exc:
        parser.exit(2, f"Raster QA failed: {exc}\n")
    print(f"Raster QA: {report['quality_status']}")
    print(f"Valid data coverage: {report['data_mask']['valid_percent']:.2f}%")
    print(f"Approximate pixel spacing: {report['pixel_spacing_approx']['east_west_metres_at_raster_centre']:.2f} m x "
          f"{report['pixel_spacing_approx']['north_south_metres_at_raster_centre']:.2f} m")
    print(f"Quicklook: {quicklook}")
    print(f"QA report: {report_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
