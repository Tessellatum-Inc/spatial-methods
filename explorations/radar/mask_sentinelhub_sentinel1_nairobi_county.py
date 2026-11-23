#!/usr/bin/env python3
"""Fetch a Nairobi County boundary and mask a Sentinel-1 VV/VH GeoTIFF to it.

The source is the WWF-Kenya ArcGIS service, which attributes the county layer
to Survey of Kenya and says it was shared by the Ministry of Lands, Directorate
of Physical Planning. This is an exploratory research boundary, not a legal
survey/cadastral boundary.
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

LAYER_URL = (
    "https://wwfke-giscoe.wwfkenya.org/arcgis/rest/services/"
    "Basedata_Kenya/KenyaCountyBoundary/FeatureServer/0"
)
QUERY_URL = LAYER_URL + "/query"
SOURCE_DESCRIPTION = (
    "WWF-Kenya ArcGIS FeatureServer; county boundaries attributed to "
    "Survey of Kenya (SOK), shared by Ministry of Lands - Directorate of "
    "Physical Planning (MOL-DPP); service copyright Ministry of Lands, WWF-Kenya"
)
NODATA = -9999.0


def fetch_nairobi_boundary(timeout: int = 60) -> tuple[dict, dict]:
    """Fetch exactly one Nairobi feature as GeoJSON; reject ambiguous responses."""
    params = urlencode({
        "where": "county='Nairobi'",
        "outFields": "county,area_km2,objectid",
        "returnGeometry": "true",
        "outSR": "4326",
        "f": "geojson",
    })
    request = Request(
        QUERY_URL + "?" + params,
        headers={"Accept": "application/geo+json, application/json"},
    )
    try:
        with urlopen(request, timeout=timeout) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except HTTPError as exc:
        raise RuntimeError(f"County boundary service returned HTTP {exc.code}.") from None
    except (URLError, TimeoutError, OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"Could not retrieve county boundary ({type(exc).__name__}).") from None

    if not isinstance(payload, dict) or payload.get("type") != "FeatureCollection":
        raise RuntimeError("County boundary service did not return a GeoJSON FeatureCollection.")
    features = payload.get("features")
    if not isinstance(features, list) or len(features) != 1:
        raise RuntimeError(f"Expected exactly one Nairobi county feature; received {len(features) if isinstance(features, list) else 'invalid feature list'}.")
    feature = features[0]
    properties = feature.get("properties") or {}
    if str(properties.get("county", "")).strip().casefold() != "nairobi":
        raise RuntimeError("Boundary service response did not identify the county as Nairobi.")
    geometry = feature.get("geometry")
    if not isinstance(geometry, dict):
        raise RuntimeError("Nairobi county feature has no polygon geometry.")
    polygon = make_valid(shape(geometry))
    if polygon.is_empty or polygon.geom_type not in ("Polygon", "MultiPolygon"):
        raise RuntimeError("Nairobi county boundary is empty or not polygonal.")
    feature["geometry"] = mapping(polygon)
    return feature, {
        "service_layer": LAYER_URL,
        "query_url": QUERY_URL + "?" + params,
        "description": SOURCE_DESCRIPTION,
        "feature_properties": properties,
        "retrieved_at_utc": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "geometry_crs": "EPSG:4326",
        "limitations": [
            "Exploratory administrative boundary; not a legal survey or cadastral boundary.",
            "Boundary provenance is attributed by the service to Survey of Kenya and Ministry of Lands, and shared with WWF-Kenya.",
            "Boundary is retrieved live at processing time; retain the saved GeoJSON to reproduce this exact run."
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
                boundary_source=LAYER_URL,
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
