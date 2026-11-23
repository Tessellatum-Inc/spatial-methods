#!/usr/bin/env python3
"""Screen a JRC Global Surface Water occurrence stratum against Sentinel-1.

The water mask is a candidate stable-reference stratum, not ground truth.
The source is accessed as a remote GeoTIFF and only the Nairobi output window
is warped/read; the global/tile raster is never downloaded as a whole file.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import importlib.util
import json
from pathlib import Path

import numpy as np
import rasterio
from rasterio.features import geometry_mask
from rasterio.enums import Resampling
from rasterio.vrt import WarpedVRT
from shapely.geometry import shape

ROOT = Path(__file__).resolve().parents[2]
RADAR = Path(__file__).resolve().parent

SOURCE_TILE = "30E_0N"
SOURCE_URL = (
    "https://s3.waw4-1.cloudferro.com/swift/v1/global-surface-water/"
    "download2024/Aggregated/VER1-5/occurrence/"
    "occurrence_30E_0N_v1_5_2024.tif"
)
THRESHOLDS = (90, 95, 99, 100)
CORE_THRESHOLD = 95
EROSION_ITERATIONS = 2


def erode_mask(mask: np.ndarray, iterations: int = 2) -> np.ndarray:
    """Binary 3x3 erosion with false outside the raster boundary."""
    result = np.asarray(mask, dtype=bool).copy()
    if result.ndim != 2:
        raise ValueError("Mask must be a 2D array.")
    if iterations < 0:
        raise ValueError("Erosion iterations cannot be negative.")
    for _ in range(iterations):
        height, width = result.shape
        padded = np.pad(result, 1, mode="constant", constant_values=False)
        eroded = np.ones_like(result, dtype=bool)
        for row in range(3):
            for col in range(3):
                eroded &= padded[row:row + height, col:col + width]
        result = eroded
    return result


def build_occurrence_masks(occurrence: np.ndarray, valid: np.ndarray,
                           threshold: int = CORE_THRESHOLD,
                           erosion_iterations: int = EROSION_ITERATIONS) -> tuple[np.ndarray, np.ndarray]:
    values = np.asarray(occurrence)
    valid_mask = np.asarray(valid, dtype=bool)
    if values.ndim != 2 or values.shape != valid_mask.shape:
        raise ValueError("Occurrence and validity arrays must be matching 2D arrays.")
    if not 1 <= threshold <= 100:
        raise ValueError("Occurrence threshold must be between 1 and 100.")
    if np.any((values[valid_mask] < 0) | (values[valid_mask] > 100)):
        raise ValueError("Valid occurrence values must be in the 0–100 range.")
    candidate = valid_mask & (values >= threshold) & (values != 255)
    core = erode_mask(candidate, erosion_iterations)
    return candidate, core


def _geometries(path: Path) -> list:
    document = json.loads(path.read_text(encoding="utf-8"))
    kind = document.get("type")
    if kind == "FeatureCollection":
        geometries = [shape(feature["geometry"]) for feature in document.get("features", [])
                      if feature.get("geometry")]
    elif kind == "Feature":
        geometries = [shape(document["geometry"])]
    else:
        geometries = [shape(document)]
    if not geometries:
        raise ValueError("County boundary contains no geometries.")
    return geometries


def _db_stats(values: np.ndarray) -> dict | None:
    selected = np.asarray(values, dtype=np.float64)
    selected = selected[np.isfinite(selected) & (selected > 0)]
    if selected.size == 0:
        return None
    db = 10.0 * np.log10(selected)
    q = np.percentile(db, [5, 50, 95])
    return {
        "positive_pixels": int(selected.size),
        "p05_db": float(q[0]),
        "median_db": float(q[1]),
        "p95_db": float(q[2]),
    }


def process(stack_metadata: Path, boundary_path: Path, output_dir: Path,
            occurrence_url: str = SOURCE_URL) -> dict:
    stack = json.loads(stack_metadata.read_text(encoding="utf-8"))
    scenes = stack.get("scenes")
    if not isinstance(scenes, list) or len(scenes) < 2:
        raise ValueError("Stack metadata must contain at least two scenes.")
    reference_scene = scenes[0]
    reference_path = Path("data/sentinelhub/nairobi/stack") / reference_scene["output"]["file"]
    with rasterio.open(reference_path) as reference:
        target_crs = reference.crs
        target_transform = reference.transform
        width, height = reference.width, reference.height
        target_bounds = reference.bounds
        reference_valid = reference.read(3) > 0.5

    county = geometry_mask(
        [geom.__geo_interface__ for geom in _geometries(boundary_path)],
        out_shape=(height, width), transform=target_transform,
        invert=True, all_touched=False,
    )
    target_valid = county & reference_valid

    # Remote range access: refuse strip-organized TIFFs to avoid accidentally
    # transferring a very large 10-degree source tile.
    remote_path = occurrence_url if occurrence_url.startswith("/vsi") else f"/vsicurl/{occurrence_url}"
    with rasterio.Env(
        GDAL_DISABLE_READDIR_ON_OPEN="EMPTY_DIR",
        CPL_VSIL_CURL_ALLOWED_EXTENSIONS=".tif",
        GDAL_HTTP_MULTIRANGE="YES",
    ):
        with rasterio.open(remote_path) as source:
            if source.count != 1:
                raise ValueError("JRC occurrence source must contain exactly one band.")
            if not source.is_tiled:
                raise RuntimeError(
                    "JRC occurrence GeoTIFF is not tiled; refusing a potentially full-tile download."
                )
            if source.crs is None:
                raise ValueError("JRC occurrence source has no CRS.")
            if (source.bounds.left > target_bounds.left or source.bounds.bottom > target_bounds.bottom
                    or source.bounds.right < target_bounds.right or source.bounds.top < target_bounds.top):
                raise ValueError("JRC occurrence tile does not cover the Sentinel-1 target grid.")
            with WarpedVRT(
                source, crs=target_crs, transform=target_transform,
                width=width, height=height, resampling=Resampling.nearest,
                src_nodata=source.nodata if source.nodata is not None else 255,
                nodata=255,
                dtype="uint8",
            ) as warped:
                occurrence = warped.read(1)

            source_info = {
                "url": occurrence_url,
                "tile": SOURCE_TILE if occurrence_url == SOURCE_URL else "custom",
                "crs": source.crs.to_string(),
                "bounds": [float(v) for v in source.bounds],
                "width": int(source.width),
                "height": int(source.height),
                "dtype": source.dtypes[0],
                "nodata": source.nodata if source.nodata is not None else 255,
                "tiled": bool(source.is_tiled),
                "block_shapes": [list(v) for v in source.block_shapes],
            }

    valid_occurrence = target_valid & (occurrence != 255) & (occurrence <= 100)
    if not valid_occurrence.any():
        raise ValueError("No valid JRC occurrence pixels overlap Nairobi County and the Sentinel-1 grid.")

    threshold_sensitivity = []
    masks = {}
    for threshold in THRESHOLDS:
        candidate, core = build_occurrence_masks(
            occurrence, valid_occurrence, threshold, EROSION_ITERATIONS
        )
        masks[threshold] = (candidate, core)
        threshold_sensitivity.append({
            "occurrence_threshold_percent": threshold,
            "candidate_pixels": int(candidate.sum()),
            "candidate_fraction_of_valid_county_pixels": float(candidate.sum() / valid_occurrence.sum()),
            "eroded_core_pixels": int(core.sum()),
            "eroded_core_fraction_of_valid_county_pixels": float(core.sum() / valid_occurrence.sum()),
            "erosion_iterations": EROSION_ITERATIONS,
        })

    candidate, core = masks[CORE_THRESHOLD]
    occurrence_out = np.where(valid_occurrence, occurrence, 255).astype(np.uint8)
    candidate_out = np.where(valid_occurrence, candidate.astype(np.uint8), 255).astype(np.uint8)
    core_out = np.where(valid_occurrence, core.astype(np.uint8), 255).astype(np.uint8)
    output_dir.mkdir(parents=True, exist_ok=True)
    mask_path = output_dir / "sentinel1_nairobi_jrc_gsw_v1_5_water_reference.tif"
    profile = {
        "driver": "GTiff", "width": width, "height": height, "count": 3,
        "dtype": "uint8", "crs": target_crs, "transform": target_transform,
        "nodata": 255, "compress": "deflate", "predictor": 2,
        "tiled": True, "blockxsize": 256, "blockysize": 256,
    }
    with rasterio.open(mask_path, "w", **profile) as dst:
        dst.write(occurrence_out, 1)
        dst.write(candidate_out, 2)
        dst.write(core_out, 3)
        dst.set_band_description(1, "JRC occurrence 1984-2024 percent")
        dst.set_band_description(2, f"Occurrence >= {CORE_THRESHOLD}% candidate")
        dst.set_band_description(3, f"Occurrence >= {CORE_THRESHOLD}% eroded core ({EROSION_ITERATIONS} iterations)")

    per_scene = []
    for scene in scenes:
        stamp = scene["catalog_item_datetime_utc"].replace(":", "").replace("-", "")
        stamp = stamp.replace("T", "T")
        ell_path = Path("data/sentinelhub/nairobi/stack") / scene["output"]["file"]
        rtc_path = Path("data/sentinelhub/nairobi/stack/terrain_aux") / (
            f"sentinel1_nairobi_{stamp}_gamma0-terrain-rtc.tif"
        )
        with rasterio.open(ell_path) as ell, rasterio.open(rtc_path) as rtc:
            if (ell.crs != target_crs or ell.transform != target_transform
                    or rtc.crs != target_crs or rtc.transform != target_transform
                    or (ell.width, ell.height) != (width, height)
                    or (rtc.width, rtc.height) != (width, height)):
                raise ValueError("A scene does not match the target reference grid.")
            ell_data = ell.read([1, 2, 3])
            rtc_data = rtc.read([1, 2, 6])
        common = (core & (ell_data[2] > 0.5) & (rtc_data[2] > 0.5)
                  & np.isfinite(ell_data).all(axis=0) & np.isfinite(rtc_data).all(axis=0))
        stats = {"core_pixels": int(common.sum()), "polarizations": {}}
        for band, name in ((0, "VV"), (1, "VH")):
            stats["polarizations"][name] = {
                "ellipsoid": _db_stats(ell_data[band][common]),
                "terrain_corrected": _db_stats(rtc_data[band][common]),
            }
        per_scene.append({
            "acquisition_datetime_utc": scene["catalog_item_datetime_utc"],
            "reference_water_core_statistics": stats,
        })

    report = {
        "schema": "tessellatum.sentinel1.jrc-gsw-water-reference-screen.v1",
        "created_at_utc": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "status": "candidate_reference_stratum_screening_only",
        "analysis_ready": False,
        "source": {
            "dataset": "JRC Global Surface Water v1.5",
            "product": "Water Occurrence 1984–2024",
            "temporal_basis": "Landsat Collection 1 (1984–2021) and Collection 2 (2022–2024)",
            "occurrence_definition": "Monthly-weighted frequency of valid observations classified as water, expressed as percent",
            "tile": SOURCE_TILE if occurrence_url == SOURCE_URL else "custom",
            "url": occurrence_url,
            "license": "Copernicus Programme; free of charge, with acknowledgement",
            "attribution": "Source: EC JRC/Google",
            "citation": "Pekel et al. (2016), High-resolution mapping of global surface water and its long-term changes, Nature 540, 418–422, doi:10.1038/nature20584",
            "source_grid": source_info,
        },
        "target_grid": {
            "crs": target_crs.to_string(),
            "width": width, "height": height,
            "transform": list(target_transform)[:6],
            "county_valid_pixels": int(valid_occurrence.sum()),
        },
        "threshold_sensitivity": threshold_sensitivity,
        "core_threshold_percent": CORE_THRESHOLD,
        "mask_file": mask_path.name,
        "mask_bands": {
            "1": "Occurrence percent (255 nodata/outside county)",
            "2": f"Candidate water pixels, occurrence >= {CORE_THRESHOLD}%",
            "3": f"Eroded candidate core, {EROSION_ITERATIONS} iterations of 3x3 erosion",
        },
        "scenes": per_scene,
        "limitations": [
            "This is a candidate persistent-water reference stratum, not independent ground truth or a validated invariant surface.",
            "JRC v1.5 combines Landsat Collection 1 (1984–2021) and Collection 2 (2022–2024); the publisher documents residual co-registration offsets at the collection transition, sometimes reaching or exceeding one 30 m pixel.",
            "Two-pixel erosion reduces boundary mixing but cannot remove all source geolocation, classification, or temporal-change uncertainty.",
            "Landsat optical water classification and Sentinel-1 SAR backscatter have different observation physics and spatial supports.",
            "Occurrence threshold sensitivity is reported; no normalization, exclusion of the source stack, or change detection is performed.",
        ],
    }
    report_path = output_dir / "sentinel1_nairobi_jrc_gsw_v1_5_water_reference_screen.json"
    report_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--stack-metadata", type=Path, default=Path("data/sentinelhub/nairobi/stack/sentinel1_nairobi_temporal_stack.metadata.json"))
    parser.add_argument("--boundary", type=Path, default=None)
    parser.add_argument("--output-dir", type=Path, default=Path("data/sentinelhub/nairobi/stack/reference_aux"))
    parser.add_argument("--occurrence-url", default=SOURCE_URL)
    args = parser.parse_args(argv)
    boundary = args.boundary
    if boundary is None:
        candidates = sorted(Path("data/sentinelhub/nairobi/stack").glob("nairobi_county_boundary_*.geojson"))
        if not candidates:
            parser.error("No Nairobi County boundary GeoJSON found; supply --boundary.")
        boundary = candidates[-1]
    try:
        report = process(args.stack_metadata, boundary, args.output_dir, args.occurrence_url)
    except (OSError, ValueError, RuntimeError) as exc:
        parser.exit(2, f"JRC water reference screen failed: {exc}\n")
    print(
        f"JRC water reference: {report['threshold_sensitivity'][1]['eroded_core_pixels']} "
        "eroded core pixels at 95% occurrence; analysis_ready=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
