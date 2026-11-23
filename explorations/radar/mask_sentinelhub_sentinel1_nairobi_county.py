#!/usr/bin/env python3
"""Fetch a pinned geoBoundaries Kenya ADM1 boundary and mask Sentinel-1 data to Nairobi.

The selected gbOpen boundary is sourced from RCMRD GeoPortal / Africa GeoPortal.
The upstream GeoJSON is pinned by commit and verified with its Git LFS SHA-256.
This is an exploratory reference boundary, not a legal survey/cadastral boundary.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

import numpy as np
import rasterio
from rasterio.features import geometry_mask
from rasterio.mask import mask
from shapely.geometry import mapping, shape
from shapely.validation import make_valid

# geoBoundaries gbOpen Kenya ADM1, pinned to the upstream Git LFS object.
# API metadata snapshot: https://www.geoboundaries.org/api/current/gbOpen/KEN/ADM1/
BOUNDARY_ID = "KEN-ADM1-32016919"
BOUNDARY_YEAR = "2020"
BOUNDARY_SOURCE = "RCMRD GeoPortal, Africa GeoPortal"
BOUNDARY_LICENSE = "Public Domain"
BOUNDARY_LICENSE_SOURCE = "https://rcmrd.africageoportal.com/datasets/africageoportal"
BOUNDARY_BUILD_DATE = "Dec 12, 2023"
BOUNDARY_SOURCE_UPDATE_DATE = "Thu Jan 19 07:31:04 2023"
BOUNDARY_FEATURE_COUNT = 47
BOUNDARY_LFS_SHA256 = "a3e073594494eb740e42fadec63acda982f6a745bb64ee4aa152453ccc46f94e"
BOUNDARY_SIZE_BYTES = 7956137
BOUNDARY_URL = (
    "https://media.githubusercontent.com/media/wmgeolab/geoBoundaries/"
    "9469f09/releaseData/gbOpen/KEN/ADM1/geoBoundaries-KEN-ADM1.geojson"
)
BOUNDARY_METADATA_URL = "https://www.geoboundaries.org/api/current/gbOpen/KEN/ADM1/"
LAYER_URL = BOUNDARY_URL
NODATA = -9999.0



def fetch_nairobi_boundary(timeout: int = 120) -> tuple[dict, dict]:
    """Download a pinned Kenya ADM1 source and select exactly one Nairobi feature."""
    request = Request(BOUNDARY_URL, headers={"Accept": "application/geo+json, application/json"})
    try:
        with urlopen(request, timeout=timeout) as response:
            raw = response.read()
        if len(raw) != BOUNDARY_SIZE_BYTES:
            raise RuntimeError(
                f"geoBoundaries file size mismatch: expected {BOUNDARY_SIZE_BYTES}, received {len(raw)}."
            )
        digest = hashlib.sha256(raw).hexdigest()
        if digest != BOUNDARY_LFS_SHA256:
            raise RuntimeError(
                "Pinned geoBoundaries file checksum mismatch; refusing unverified boundary geometry."
            )
        payload = json.loads(raw.decode("utf-8"))
    except HTTPError as exc:
        raise RuntimeError(f"geoBoundaries download returned HTTP {exc.code}.") from None
    except (URLError, TimeoutError, OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"Could not retrieve geoBoundaries boundary ({type(exc).__name__}).") from None

    if not isinstance(payload, dict) or payload.get("type") != "FeatureCollection":
        raise RuntimeError("geoBoundaries source did not return a GeoJSON FeatureCollection.")
    features = payload.get("features")
    if not isinstance(features, list) or len(features) != BOUNDARY_FEATURE_COUNT:
        received = len(features) if isinstance(features, list) else "invalid"
        raise RuntimeError(
            f"Expected {BOUNDARY_FEATURE_COUNT} Kenya ADM1 features; received {received}."
        )

    matches = []
    for candidate in features:
        properties = (candidate or {}).get("properties") or {}
        labels = (
            properties.get("shapeName"), properties.get("shapeNameAlt"),
            properties.get("name"), properties.get("NAME_1"),
            properties.get("county"), properties.get("County"),
        )
        normalized = {
            " ".join(str(value or "").strip().casefold().split())
            for value in labels
        }
        if "nairobi" in normalized or "nairobi city" in normalized:
            matches.append(candidate)
    if len(matches) != 1:
        labels = sorted({
            str(((item or {}).get("properties") or {}).get("shapeName", ""))
            for item in features
        })
        raise RuntimeError(
            "Expected exactly one Nairobi county feature in the pinned geoBoundaries dataset; "
            f"received {len(matches)}. ADM1 labels: {labels[:60]}"
        )

    feature = matches[0]
    geometry = feature.get("geometry")
    if not isinstance(geometry, dict):
        raise RuntimeError("Nairobi county feature has no polygon geometry.")
    polygon = make_valid(shape(geometry))
    if polygon.is_empty or polygon.geom_type not in ("Polygon", "MultiPolygon"):
        raise RuntimeError("Nairobi county boundary is empty or not polygonal.")
    feature["geometry"] = mapping(polygon)

    return feature, {
        "provider": "geoBoundaries",
        "product": "gbOpen",
        "boundary_id": BOUNDARY_ID,
        "boundary_name": "Kenya",
        "administrative_level": "ADM1 (counties)",
        "represented_year": BOUNDARY_YEAR,
        "feature_count": BOUNDARY_FEATURE_COUNT,
        "source": BOUNDARY_SOURCE,
        "license": BOUNDARY_LICENSE,
        "license_source": BOUNDARY_LICENSE_SOURCE,
        "metadata_url": BOUNDARY_METADATA_URL,
        "download_url": BOUNDARY_URL,
        "upstream_git_commit": "9469f09",
        "upstream_lfs_sha256": BOUNDARY_LFS_SHA256,
        "downloaded_file_sha256": digest,
        "downloaded_file_size_bytes": len(raw),
        "source_data_update_date": BOUNDARY_SOURCE_UPDATE_DATE,
        "build_date": BOUNDARY_BUILD_DATE,
        "feature_properties": feature.get("properties") or {},
        "retrieved_at_utc": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "geometry_crs": "EPSG:4326",
        "limitations": [
            "Open reference administrative boundary; not a legal survey or cadastral boundary.",
            "Source metadata identifies RCMRD GeoPortal and Africa GeoPortal; represented year is 2020.",
            "Full source dataset is pinned by upstream commit and verified against its Git LFS SHA-256.",
        ],
    }


def mask_raster_to_county(input_path: Path, output_dir: Path) -> tuple[Path, Path, Path, dict]:
    """Create a cropped county GeoTIFF with VV/VH nodata outside valid county pixels."""
    if not input_path.is_file():
        raise ValueError(f"Input raster does not exist: {input_path}")
    output_dir.mkdir(parents=True, exist_ok=True)
    feature, provenance = fetch_nairobi_boundary()
    polygon = shape(feature["geometry"])
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    boundary_path = output_dir / f"nairobi_county_boundary_{stamp}.geojson"
    boundary_path.write_text(json.dumps({
        "type": "FeatureCollection",
        "name": "Nairobi County exploratory boundary",
        "crs": {"type": "name", "properties": {"name": "urn:ogc:def:crs:EPSG::4326"}},
        "features": [feature],
    }, indent=2) + "\n", encoding="utf-8")

    with rasterio.open(input_path) as src:
        if src.count != 3:
            raise ValueError(f"Expected 3 bands (VV, VH, dataMask); found {src.count}.")
        if src.crs is None:
            raise ValueError("Input raster has no CRS.")
        raster_geom = polygon
        if src.crs.to_string() != "EPSG:4326":
            from rasterio.warp import transform_geom
            raster_geom_json = transform_geom("EPSG:4326", src.crs, mapping(polygon))
        else:
            raster_geom_json = mapping(polygon)
        try:
            clipped, transform = mask(
                src, [raster_geom_json], crop=True, filled=True, nodata=NODATA,
                all_touched=False,
            )
        except ValueError as exc:
            raise ValueError("Nairobi county boundary does not overlap the input raster.") from exc
        if clipped.shape[1] == 0 or clipped.shape[2] == 0:
            raise ValueError("County mask produced an empty raster.")
        inside = geometry_mask(
            [raster_geom_json],
            out_shape=(clipped.shape[1], clipped.shape[2]),
            transform=transform,
            invert=True,
            all_touched=False,
        )
        original_valid = clipped[2] > 0.5
        valid_county = inside & original_valid
        county_pixel_count = int(inside.sum())
        valid_count = int(valid_county.sum())
        if county_pixel_count == 0:
            raise ValueError("No raster pixels fall inside the Nairobi county polygon.")
        clipped[2] = valid_county.astype(np.float32)
        clipped[0][~valid_county] = NODATA
        clipped[1][~valid_county] = NODATA
        profile = src.profile.copy()
        profile.update(
            driver="GTiff", height=clipped.shape[1], width=clipped.shape[2],
            transform=transform, count=3, dtype="float32", nodata=NODATA,
            compress="deflate", predictor=3,
        )
        raster_crs = src.crs.to_string()
        with rasterio.open(output_dir / f"sentinel1_nairobi_county_{stamp}.tif", "w", **profile) as dst:
            dst.write(clipped.astype(np.float32))
            dst.set_band_description(1, "VV gamma0 ellipsoid backscatter (linear power)")
            dst.set_band_description(2, "VH gamma0 ellipsoid backscatter (linear power)")
            dst.set_band_description(3, "dataMask: 1 = valid county pixel, 0 = outside county or no scene data")
            dst.update_tags(
                boundary_source="geoBoundaries gbOpen KEN ADM1",\n                boundary_download_url=BOUNDARY_URL,\n                boundary_id=BOUNDARY_ID,
                boundary_feature_name="Nairobi",
                boundary_crs="EPSG:4326",
                processing_note="County crop; invalid/outside VV and VH set to -9999; dataMask set to 0.",
            )
        output_path = output_dir / f"sentinel1_nairobi_county_{stamp}.tif"

    county_fraction = valid_count / county_pixel_count
    report = {
        "created_at_utc": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "input_file": input_path.name,
        "input_sha256": hashlib.sha256(input_path.read_bytes()).hexdigest(),
        "output_file": output_path.name,
        "output_sha256": hashlib.sha256(output_path.read_bytes()).hexdigest(),
        "crs": raster_crs,
        "band_order": ["VV", "VH", "dataMask"],
        "boundary_file": boundary_path.name,
        "boundary_provenance": provenance,
        "county_pixel_coverage": {
            "valid_pixels_inside_county": valid_count,
            "total_pixels_inside_county": county_pixel_count,
            "valid_fraction": county_fraction,
            "valid_percent": round(county_fraction * 100, 4),
            "pixel_rule": "Pixel centre inside polygon (all_touched=False); valid where source dataMask equals 1.",
        },
        "nodata": NODATA,
        "quality_status": "pass" if county_fraction >= 0.90 else "partial_county_coverage",
        "limitations": [
            "Raster is cropped to the county polygon's rectangular envelope; pixels outside the county are masked.",
            "Coverage percentage is calculated only over pixel centres inside the county polygon.",
            "This output remains a single acquisition and is not a validated change-detection product.",
        ],
    }
    report_path = output_dir / f"sentinel1_nairobi_county_{stamp}.qa.json"
    report_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    return output_path, boundary_path, report_path, report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="Input three-band Sentinel-1 GeoTIFF.")
    parser.add_argument("--output-dir", type=Path, default=None)
    args = parser.parse_args()
    output_dir = args.output_dir or args.input.parent
    try:
        output, boundary, report_path, report = mask_raster_to_county(args.input, output_dir)
    except (ValueError, RuntimeError) as exc:
        parser.exit(2, f"County masking failed: {exc}\n")
    print(f"County raster: {output}")
    print(f"Boundary GeoJSON: {boundary}")
    print(f"County valid-data coverage: {report['county_pixel_coverage']['valid_percent']:.2f}%")
    print(f"County QA: {report_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
