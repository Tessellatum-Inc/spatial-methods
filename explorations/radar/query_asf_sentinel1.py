#!/usr/bin/env python3
"""Query ASF for Sentinel-1 scenes intersecting the Nairobi study window.

This tool performs catalogue discovery only. It does not download scene assets,
prove full AOI coverage, or establish scientific suitability.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sys
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

API_URL = "https://api.daac.asf.alaska.edu/services/search/param"
AOI_WKT = (
    "polygon((36.65 -1.45,37.05 -1.45,37.05 -1.15,"
    "36.65 -1.15,36.65 -1.45))"
)
DEFAULT_START = "2026-10-01T00:00:00Z"
DEFAULT_END = "2026-11-21T23:59:59Z"


def build_query(start: str, end: str, polarization: str, max_results: int) -> dict[str, str]:
    """Return the explicit ASF query parameters used for this investigation."""
    if not start or not end:
        raise ValueError("Both --start and --end are required.")
    if max_results < 1:
        raise ValueError("--max-results must be at least 1.")
    if polarization not in {"VV+VH", "VV"}:
        raise ValueError("Polarization must be VV+VH or the separately documented VV fallback.")
    try:
        start_dt = datetime.fromisoformat(start.replace("Z", "+00:00"))
        end_dt = datetime.fromisoformat(end.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError("Start and end must be ISO 8601 timestamps with UTC offsets.") from exc
    if start_dt.tzinfo is None or end_dt.tzinfo is None:
        raise ValueError("Start and end timestamps must include an explicit UTC offset.")
    if start_dt.utcoffset().total_seconds() != 0 or end_dt.utcoffset().total_seconds() != 0:
        raise ValueError("This investigation requires UTC timestamps (Z or +00:00).")
    if start_dt > end_dt:
        raise ValueError("Start timestamp must not be later than end timestamp.")
    return {
        "dataset": "SENTINEL-1",
        "beamMode": "IW",
        "processingLevel": "GRD_HD",
        "polarization": polarization,
        "start": start,
        "end": end,
        "intersectsWith": AOI_WKT,
        "output": "geojson",
        "maxResults": str(max_results),
    }


def retrieve(url: str, timeout: int) -> bytes:
    request = Request(
        url,
        headers={
            "Accept": "application/geo+json, application/json",
            "User-Agent": "Tessellatum-Spatial-Methods/1.0 (reproducible research)",
        },
    )
    with urlopen(request, timeout=timeout) as response:
        return response.read()


def parse_feature_collection(raw: bytes) -> dict:
    try:
        payload = json.loads(raw)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError("ASF response was not valid UTF-8 JSON.") from exc

    if not isinstance(payload, dict):
        raise ValueError("ASF response JSON must be an object.")
    if payload.get("type") != "FeatureCollection":
        detail = payload.get("message") or payload.get("error") or payload
        raise ValueError(f"ASF did not return a GeoJSON FeatureCollection: {detail}")
    features = payload.get("features")
    if not isinstance(features, list):
        raise ValueError("GeoJSON FeatureCollection has no valid 'features' array.")
    for index, feature in enumerate(features):
        if not isinstance(feature, dict) or feature.get("type") != "Feature":
            raise ValueError(f"Feature at index {index} is not a GeoJSON Feature.")
        properties = feature.get("properties")
        geometry = feature.get("geometry")
        if not isinstance(properties, dict):
            raise ValueError(f"Feature at index {index} has no valid properties object.")
        if not isinstance(geometry, dict):
            raise ValueError(f"Feature at index {index} has no usable scene footprint geometry.")
        if geometry.get("type") not in {"Polygon", "MultiPolygon"}:
            raise ValueError(
                f"Feature at index {index} has unsupported footprint geometry "
                f"{geometry.get(chr(116)+chr(121)+chr(112)+chr(101))!r}."
            )
        if not isinstance(geometry.get("coordinates"), list) or not geometry["coordinates"]:
            raise ValueError(f"Feature at index {index} has empty footprint coordinates.")
    return payload


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--start", default=DEFAULT_START, help="Acquisition start in UTC.")
    parser.add_argument("--end", default=DEFAULT_END, help="Acquisition end in UTC.")
    parser.add_argument(
        "--polarization", default="VV+VH",
        help="ASF polarisation filter; use VV for a separately documented fallback.",
    )
    parser.add_argument("--max-results", type=int, default=30)
    parser.add_argument("--timeout", type=int, default=90)
    parser.add_argument("--output-dir", type=Path, default=Path("data/asf/nairobi"))
    args = parser.parse_args(argv)

    if args.timeout < 1:
        parser.error("--timeout must be at least 1 second.")

    try:
        params = build_query(args.start, args.end, args.polarization, args.max_results)
    except ValueError as exc:
        parser.error(str(exc))

    query_url = f"{API_URL}?{urlencode(params)}"
    try:
        raw = retrieve(query_url, args.timeout)
        collection = parse_feature_collection(raw)
    except HTTPError as exc:
        print(f"ASF HTTP error {exc.code}: {exc.reason}", file=sys.stderr)
        return 2
    except (URLError, TimeoutError, OSError) as exc:
        print(f"Could not retrieve ASF catalogue response: {exc}", file=sys.stderr)
        return 2
    except ValueError as exc:
        print(f"Invalid ASF catalogue response: {exc}", file=sys.stderr)
        return 3

    args.output_dir.mkdir(parents=True, exist_ok=True)
    retrieved = datetime.now(timezone.utc)
    retrieved_at = retrieved.isoformat(timespec="microseconds").replace("+00:00", "Z")
    stamp = retrieved.strftime("%Y%m%dT%H%M%S%fZ")
    stem = f"asf_sentinel1_nairobi_{stamp}"
    geojson_path = args.output_dir / f"{stem}.geojson"
    metadata_path = args.output_dir / f"{stem}.metadata.json"

    # Preserve the exact response bytes; the digest permits later integrity checks.
    geojson_path.write_bytes(raw)
    metadata = {
        "source": API_URL,
        "query_url": query_url,
        "query_parameters": params,
        "retrieved_at_utc": retrieved_at,
        "response_file": geojson_path.name,
        "response_sha256": hashlib.sha256(raw).hexdigest(),
        "feature_count": len(collection["features"]),
        "status": "catalogue_response_saved",
        "interpretation_limit": (
            "Intersection results do not establish full AOI coverage, asset access, "
            "product suitability, or scientific validity."
        ),
    }
    metadata_path.write_text(
        json.dumps(metadata, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    print(f"Saved {len(collection['features'])} catalogue features.")
    print(f"GeoJSON: {geojson_path}")
    print(f"Metadata: {metadata_path}")
    print(f"SHA-256: {metadata['response_sha256']}")
    print("Next: inspect full footprints and product metadata; do not infer full coverage from intersection.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
