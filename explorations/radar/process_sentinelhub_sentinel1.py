#!/usr/bin/env python3
"""Request a small Sentinel-1 GRD VV/VH GeoTIFF for the latest Nairobi scene.

This uses Sentinel Hub's Process API, not the OData SAFE archive endpoint.
The request selects the latest catalogue feature in the search interval and
constrains processing to that feature's acquisition timestamp.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timedelta, timezone
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import sys
import time
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from shapely.geometry import box, shape

PROCESS_URL = "https://sh.dataspace.copernicus.eu/process/v1"
NAIROBI_BBOX = [36.65, -1.45, 37.05, -1.15]
WIDTH = 2048
HEIGHT = 1536
EVALSCRIPT = """//VERSION=3
function setup() {
  return {
    input: [{
      bands: ["VV", "VH", "dataMask"],
      units: ["LINEAR_POWER", "LINEAR_POWER", "DN"]
    }],
    output: { bands: 3, sampleType: "FLOAT32" }
  };
}
function evaluatePixel(sample) {
  return [sample.VV, sample.VH, sample.dataMask];
}
"""

# Import the already-tested OAuth and Catalog client without duplicating auth logic.
_MODULE_PATH = Path(__file__).with_name("query_sentinelhub_sentinel1.py")
_SPEC = importlib.util.spec_from_file_location("query_sentinelhub_sentinel1", _MODULE_PATH)
if _SPEC is None or _SPEC.loader is None:
    raise RuntimeError("Could not load the Sentinel Hub catalogue client.")
_CATALOG = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(_CATALOG)


def default_interval() -> tuple[str, str]:
    end = datetime.now(timezone.utc)
    start = end - timedelta(days=30)
    fmt = lambda value: value.isoformat(timespec="seconds").replace("+00:00", "Z")
    return fmt(start), fmt(end)


def feature_coverage(feature: dict) -> tuple[bool, float]:
    """Return whether a STAC footprint covers the search rectangle and its area fraction."""
    geometry_json = feature.get("geometry")
    if not isinstance(geometry_json, dict):
        return False, 0.0
    try:
        footprint = shape(geometry_json)
        aoi = box(*NAIROBI_BBOX)
        if footprint.is_empty or not footprint.is_valid:
            return False, 0.0
        fraction = float(footprint.intersection(aoi).area / aoi.area)
        return bool(footprint.covers(aoi)), min(1.0, max(0.0, fraction))
    except (TypeError, ValueError):
        return False, 0.0


def select_latest_feature(collection: dict, allow_partial: bool = False) -> dict:
    """Select the latest full-coverage feature; partial coverage requires explicit opt-in."""
    features = collection.get("features")
    if not isinstance(features, list) or not features:
        raise ValueError("No Sentinel-1 GRD catalogue features intersect the Nairobi AOI.")
    full_coverage = []
    partial_coverage = []
    for feature in features:
        if not isinstance(feature, dict):
            continue
        properties = feature.get("properties")
        stamp = properties.get("datetime") if isinstance(properties, dict) else None
        if not isinstance(stamp, str):
            continue
        try:
            acquired = datetime.fromisoformat(stamp.replace("Z", "+00:00"))
        except ValueError:
            continue
        if acquired.tzinfo is None:
            continue
        covers, fraction = feature_coverage(feature)
        if fraction <= 0:
            continue
        record = (acquired.astimezone(timezone.utc), feature)
        (full_coverage if covers else partial_coverage).append(record)
    if full_coverage:
        return max(full_coverage, key=lambda pair: pair[0])[1]
    if allow_partial and partial_coverage:
        return max(partial_coverage, key=lambda pair: pair[0])[1]
    if partial_coverage:
        raise ValueError("No catalogue footprint fully covers the Nairobi search rectangle. "
                         "Use --allow-partial-coverage only when a partial scene is acceptable.")
    raise ValueError("Catalogue features had no valid footprints or acquisition timestamps.")


def build_process_payload(feature: dict, width: int = WIDTH, height: int = HEIGHT) -> dict:
    if not 1 <= width <= 2500 or not 1 <= height <= 2500:
        raise ValueError("Output width and height must each be between 1 and 2500.")
    properties = feature.get("properties", {})
    stamp = properties.get("datetime")
    if not isinstance(stamp, str):
        raise ValueError("Selected catalogue feature has no acquisition datetime.")
    try:
        acquired = datetime.fromisoformat(stamp.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError("Selected feature has an invalid acquisition datetime.") from exc
    if acquired.tzinfo is None:
        raise ValueError("Selected feature acquisition datetime must include a timezone.")
    acquired = acquired.astimezone(timezone.utc)
    start = (acquired - timedelta(seconds=1)).isoformat(timespec="milliseconds").replace("+00:00", "Z")
    end = (acquired + timedelta(seconds=1)).isoformat(timespec="milliseconds").replace("+00:00", "Z")
    return {
        "input": {
            "bounds": {
                "bbox": NAIROBI_BBOX,
                "properties": {"crs": "http://www.opengis.net/def/crs/OGC/1.3/CRS84"},
            },
            "data": [{
                "type": "sentinel-1-grd",
                "dataFilter": {
                    "timeRange": {"from": start, "to": end},
                    "mosaickingOrder": "mostRecent",
                },
                "processing": {
                    "orthorectify": True,
                    "backCoeff": "GAMMA0_ELLIPSOID",
                },
            }],
        },
        "output": {
            "width": width,
            "height": height,
            "responses": [{"identifier": "default", "format": {"type": "image/tiff"}}],
        },
        "evalscript": EVALSCRIPT,
    }


def request_geotiff(access_token: str, payload: dict, timeout: int = 180) -> bytes:
    if not access_token:
        raise ValueError("An access token is required.")
    request = Request(
        PROCESS_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
            "Accept": "image/tiff",
        },
        method="POST",
    )
    # Retry transient provider/network failures, but fail immediately on
    # non-retryable client/authentication errors (e.g. 400/401/403).
    retry_delays = (2, 5, 10)
    for attempt in range(len(retry_delays) + 1):
        try:
            with urlopen(request, timeout=timeout) as response:
                content_type = response.headers.get("Content-Type", "").lower()
                body = response.read()
            break
        except HTTPError as exc:
            if exc.code in {429, 500, 502, 503, 504} and attempt < len(retry_delays):
                time.sleep(retry_delays[attempt])
                continue
            # Do not expose provider response bodies, headers, request bodies, or credentials.
            raise RuntimeError(f"Sentinel Hub Process API failed with HTTP {exc.code}.") from None
        except (URLError, TimeoutError, OSError) as exc:
            if attempt < len(retry_delays):
                time.sleep(retry_delays[attempt])
                continue
            raise RuntimeError(
                f"Sentinel Hub Process API request could not complete ({type(exc).__name__})."
            ) from None
    if "image/tiff" not in content_type and "application/octet-stream" not in content_type:
        raise RuntimeError("Sentinel Hub Process API did not return a GeoTIFF response.")
    if len(body) < 8 or body[:4] not in (b"II*\x00", b"MM\x00*"):
        raise RuntimeError("Sentinel Hub response did not contain a valid TIFF header.")
    return body


def main(argv: list[str] | None = None) -> int:
    default_start, default_end = default_interval()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--start", default=default_start, help="Inclusive ISO 8601 catalogue start.")
    parser.add_argument("--end", default=default_end, help="Exclusive ISO 8601 catalogue end.")
    parser.add_argument("--limit", type=int, default=100)
    parser.add_argument("--timeout", type=int, default=180)
    parser.add_argument("--allow-partial-coverage", action="store_true", help="Allow a partial scene if no full-coverage scene exists.")
    parser.add_argument("--output-dir", type=Path, default=Path("data/sentinelhub/nairobi"))
    args = parser.parse_args(argv)
    try:
        query = _CATALOG.build_search_payload(args.start, args.end, args.limit)
        token = _CATALOG.request_access_token(
            os.environ.get("SENTINEL_HUB_CLIENT_ID", ""),
            os.environ.get("SENTINEL_HUB_CLIENT_SECRET", ""),
            timeout=min(args.timeout, 30),
        )
        catalogue = _CATALOG.search_catalog(token, query, timeout=min(args.timeout, 60))
        feature = select_latest_feature(catalogue, allow_partial=args.allow_partial_coverage)
        payload = build_process_payload(feature)
        raster = request_geotiff(token, payload, timeout=args.timeout)
    except (ValueError, RuntimeError) as exc:
        print(str(exc), file=sys.stderr)
        return 2

    retrieved = datetime.now(timezone.utc)
    stamp = retrieved.strftime("%Y%m%dT%H%M%SZ")
    args.output_dir.mkdir(parents=True, exist_ok=True)
    raster_path = args.output_dir / f"sentinel1_nairobi_{stamp}_vv-vh.tif"
    metadata_path = args.output_dir / f"sentinel1_nairobi_{stamp}_vv-vh.metadata.json"
    raster_path.write_bytes(raster)
    props = feature.get("properties", {})
    footprint_covers, footprint_fraction = feature_coverage(feature)
    metadata = {
        "service": "Copernicus Data Space Ecosystem Sentinel Hub Process API",
        "process_endpoint": PROCESS_URL,
        "catalog_collection": "sentinel-1-grd",
        "catalog_item_id": feature.get("id"),
        "acquisition_datetime": props.get("datetime"),
        "catalogue_footprint": {"covers_search_rectangle": footprint_covers, "intersection_fraction": footprint_fraction},
        "retrieved_at_utc": retrieved.isoformat().replace("+00:00", "Z"),
        "bbox_crs84": NAIROBI_BBOX,
        "output": {
            "file": raster_path.name,
            "format": "GeoTIFF",
            "width": payload["output"]["width"],
            "height": payload["output"]["height"],
            "bands": ["VV", "VH", "dataMask"],
            "backscatter_coefficient": "GAMMA0_ELLIPSOID",
            "polarization_units": "LINEAR_POWER",
            "orthorectified": True,
            "sample_type": "FLOAT32",
        },
        "bytes": len(raster),
        "sha256": hashlib.sha256(raster).hexdigest(),
        "limitations": [
            "This is a Sentinel Hub processed subset, not the original SAFE archive.",
            "The output grid is 2048 by 1536 over the configured Nairobi bounding box; it is not a claim of 10 m native resolution.",
            "The bounding box includes areas outside the Nairobi urban footprint.",
            "VV/VH values are linear gamma0 ellipsoid backscatter; dataMask identifies valid data pixels.",
            "A single acquisition is a scene-level sample, not a validated time series or change-detection result."
        ],
    }
    metadata_path.write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
    print("Sentinel Hub OAuth: authenticated.")
    print(f"Selected catalogue item: {metadata['catalog_item_id']}")
    print(f"Acquisition UTC: {metadata['acquisition_datetime']}")
    print(f"GeoTIFF bytes: {len(raster)}")
    print(f"GeoTIFF: {raster_path}")
    print(f"Metadata: {metadata_path}")
    print(f"Raster SHA-256: {metadata['sha256']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
