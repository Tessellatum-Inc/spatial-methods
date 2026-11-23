#!/usr/bin/env python3
"""Screen Sentinel-1 backscatter over eroded ESA WorldCover built-up interiors.

WorldCover is a 2021 thematic reference, not a 2026 truth layer. The resulting
built-up mask is a candidate stable-reference stratum and must not be treated as
ground truth or used for automatic radiometric normalization.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path

import numpy as np
import rasterio
from rasterio.enums import Resampling
from rasterio.features import geometry_mask
from rasterio.warp import reproject
from rasterio.windows import from_bounds
from shapely.geometry import shape

WORLDCOVER_URL = (
    "https://esa-worldcover.s3.eu-central-1.amazonaws.com/v200/2021/map/"
    "ESA_WorldCover_10m_2021_v200_S03E036_Map.tif"
)
WORLDCOVER_CLASS_BUILT_UP = 50


def erode_binary(mask: np.ndarray, iterations: int = 2) -> np.ndarray:
    """Erode a boolean mask with a 3x3 square kernel, without SciPy."""
    result = np.asarray(mask, dtype=bool).copy()
    if result.ndim != 2 or iterations < 0:
        raise ValueError("mask must be 2D and iterations must be non-negative")
    for _ in range(iterations):
        padded = np.pad(result, 1, mode="constant", constant_values=False)
        h, w = result.shape
        result = np.logical_and.reduce([
            padded[dy:dy + h, dx:dx + w]
            for dy in range(3) for dx in range(3)
        ])
    return result


def read_worldcover_on_grid(reference_path: Path, url: str = WORLDCOVER_URL) -> tuple[np.ndarray, dict]:
    """Read only the reference raster window from the public WorldCover COG."""
    with rasterio.Env(GDAL_DISABLE_READDIR_ON_OPEN="EMPTY_DIR", GDAL_HTTP_MULTIRANGE="YES"):
        with rasterio.open(reference_path) as ref, rasterio.open(url) as src:
            if ref.crs is None or src.crs is None:
                raise ValueError("Reference and WorldCover rasters must define a CRS")
            window = from_bounds(*ref.bounds, transform=src.transform)
            window = window.round_offsets().round_lengths()
            source = src.read(1, window=window, boundless=True, fill_value=0)
            source_transform = src.window_transform(window)
            destination = np.zeros((ref.height, ref.width), dtype=np.uint8)
            reproject(
                source=source,
                destination=destination,
                src_transform=source_transform,
                src_crs=src.crs,
                src_nodata=src.nodata if src.nodata is not None else 0,
                dst_transform=ref.transform,
                dst_crs=ref.crs,
                dst_nodata=0,
                resampling=Resampling.nearest,
            )
            provenance = {
                "product": "ESA WorldCover 10 m 2021 v200",
                "url": url,
                "class_code": WORLDCOVER_CLASS_BUILT_UP,
                "class_name": "Built-up",
                "native_crs": src.crs.to_string(),
                "native_resolution_degrees": [abs(src.transform.a), abs(src.transform.e)],
                "license": "Creative Commons Attribution 4.0 International",
                "attribution": "© ESA WorldCover project 2021 / Contains modified Copernicus Sentinel data (2021) processed by ESA WorldCover consortium",
            }
    return destination, provenance


def county_mask_from_geojson(path: Path, transform, shape_: tuple[int, int]) -> np.ndarray:
    document = json.loads(path.read_text(encoding="utf-8"))
    features = document.get("features", [])
    if not features:
        raise ValueError(f"No features in county boundary: {path}")
    geometries = [shape(feature["geometry"]) for feature in features]
    return geometry_mask(geometries, out_shape=shape_, transform=transform, invert=True, all_touched=False)


def distribution(values: np.ndarray) -> dict:
    values = values[np.isfinite(values) & (values > 0)]
    if not values.size:
        return {"valid_pixels": 0}
    db = 10.0 * np.log10(values.astype(np.float64))
    q = np.percentile(db, [5, 25, 50, 75, 95])
    return {
        "valid_pixels": int(values.size),
        "mean_db": float(db.mean()),
        "p05_db": float(q[0]),
        "p25_db": float(q[1]),
        "median_db": float(q[2]),
        "p75_db": float(q[3]),
        "p95_db": float(q[4]),
    }


def screen(raster_paths: list[Path], boundary_path: Path, output_path: Path,
           worldcover_url: str = WORLDCOVER_URL) -> dict:
    if len(raster_paths) < 2:
        raise ValueError("At least two temporal rasters are required")
    first = raster_paths[0]
    with rasterio.open(first) as ds:
        grid = (ds.crs, ds.transform, ds.width, ds.height)
        worldcover, provenance = read_worldcover_on_grid(first, worldcover_url)
        county = county_mask_from_geojson(boundary_path, ds.transform, (ds.height, ds.width))
    built_up = (worldcover == WORLDCOVER_CLASS_BUILT_UP) & county
    interior = erode_binary(built_up, iterations=2)
    if int(interior.sum()) < 1000:
        raise ValueError(
            f"Too few eroded built-up reference pixels ({int(interior.sum())}); "
            "inspect tile alignment, class coverage and erosion settings."
        )

    scenes = []
    reference_stats = None
    for path in raster_paths:
        with rasterio.open(path) as ds:
            if (ds.crs, ds.transform, ds.width, ds.height) != grid:
                raise ValueError(f"Grid mismatch in {path}")
            vv, vh = ds.read(1), ds.read(2)
            valid = (ds.read(3) > 0.5) & np.isfinite(vv) & np.isfinite(vh)
        mask = interior & valid
        vv_stats, vh_stats = distribution(vv[mask]), distribution(vh[mask])
        record = {
            "file": path.name,
            "acquisition_datetime_utc": path.name.split("_")[-2] if "_" in path.name else None,
            "reference_pixel_count": int(mask.sum()),
            "reference_valid_fraction": float(mask.sum() / max(1, interior.sum())),
            "VV": vv_stats,
            "VH": vh_stats,
        }
        if reference_stats is None:
            reference_stats = {"VV": vv_stats, "VH": vh_stats}
        else:
            for pol in ("VV", "VH"):
                base = reference_stats[pol].get("median_db")
                current = record[pol].get("median_db")
                record[pol]["median_db_difference_from_first"] = (
                    float(current - base) if base is not None and current is not None else None
                )
        scenes.append(record)

    report = {
        "schema": "tessellatum.sentinel1.reference-area-screen.v1",
        "created_at_utc": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "status": "candidate_reference_stratum_screening_only",
        "analysis_ready": False,
        "reference_stratum": {
            **provenance,
            "mask_method": "WorldCover class 50, intersected with Nairobi County pixel-centre mask, then eroded by two 3x3 iterations on the Sentinel-1 output grid",
            "county_boundary_file": boundary_path.name,
            "built_up_pixels_before_erosion": int(built_up.sum()),
            "interior_pixels_after_erosion": int(interior.sum()),
            "interior_fraction_of_county_pixels": float(interior.sum() / max(1, county.sum())),
            "erosion_distance_approximation": "Two output-grid pixels; spatial distance varies with latitude and grid geometry.",
        },
        "scenes": scenes,
        "limitations": [
            "WorldCover 2021 is several years older than the 2026 SAR acquisitions; class 50 does not prove the same surfaces remained unchanged.",
            "Built-up pixels can change through construction, demolition, surface wetness, roofing and urban activity.",
            "Erosion reduces mixed boundary pixels but does not identify invariant radar scatterers.",
            "Backscatter statistics are descriptive and are not calibration validation or permission to normalize.",
            "The output grid is a requested resampling grid, not a claim of native 10 m Sentinel-1 resolution.",
            "No independent geodetic tie points, precise-orbit validation or terrain-corrected gamma0 assessment is performed.",
        ],
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rasters", nargs="+", type=Path, required=True)
    parser.add_argument("--boundary", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    report = screen(args.rasters, args.boundary, args.output)
    print(
        f"Wrote {args.output}; built-up pixels={report['reference_stratum']['built_up_pixels_before_erosion']}; "
        f"interior pixels={report['reference_stratum']['interior_pixels_after_erosion']}; "
        "analysis_ready=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
