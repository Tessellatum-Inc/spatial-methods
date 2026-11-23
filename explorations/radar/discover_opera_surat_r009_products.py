#!/usr/bin/env python3
"""Discover independent OPERA RTC-S1 products for the four Surat R009 acquisitions.

Catalogue intersection is discovery only. It does not establish exact source-scene
identity, complete target coverage, pixel co-registration, or radiometric equivalence.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timedelta, timezone
import hashlib
import json
from pathlib import Path
import re
import sys
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

API_URL = "https://api.daac.asf.alaska.edu/services/search/param"
BBOX = (150.244625, -27.273849, 150.500114, -27.070649)
WKT = (
    "polygon((150.244625 -27.273849, 150.500114 -27.273849, "
    "150.500114 -27.070649, 150.244625 -27.070649, "
    "150.244625 -27.273849))"
)
ACQUISITIONS = {
    "2025-12-19": "2025-12-19T08:41:12Z",
    "2025-12-31": "2025-12-31T08:41:11Z",
    "2026-01-12": "2026-01-12T08:41:10Z",
    "2026-01-24": "2026-01-24T08:41:08Z",
}
TIME_TOLERANCE_SECONDS = 300


def build_query(start: str, end: str, max_results: int = 500) -> dict[str, str]:
    """Build a documented ASF OPERA RTC search query."""
    if max_results < 1:
        raise ValueError("max_results must be positive")
    for value in (start, end):
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        if parsed.tzinfo is None or parsed.utcoffset() != timedelta(0):
            raise ValueError("timestamps must include UTC timezone")
    if datetime.fromisoformat(start.replace("Z", "+00:00")) > datetime.fromisoformat(end.replace("Z", "+00:00")):
        raise ValueError("start must not be after end")
    return {
        "dataset": "OPERA-S1",
        "processingLevel": "RTC",
        "intersectsWith": WKT,
        "start": start,
        "end": end,
        "output": "geojson",
        "maxResults": str(max_results),
    }


def build_static_query(max_results: int = 500) -> dict[str, str]:
    """Search the documented 2014-04-03 acquisition date for static layers."""
    if max_results < 1:
        raise ValueError("max_results must be positive")
    return {
        "dataset": "OPERA-S1",
        "processingLevel": "RTC-STATIC",
        "intersectsWith": WKT,
        "start": "2014-04-03T00:00:00Z",
        "end": "2014-04-04T00:00:00Z",
        "output": "geojson",
        "maxResults": str(max_results),
    }


def parse_collection(raw: bytes) -> dict:
    payload = json.loads(raw)
    if not isinstance(payload, dict) or payload.get("type") != "FeatureCollection":
        raise ValueError("ASF response is not a GeoJSON FeatureCollection")
    features = payload.get("features")
    if not isinstance(features, list):
        raise ValueError("ASF GeoJSON has no features array")
    for i, feature in enumerate(features):
        if not isinstance(feature, dict) or not isinstance(feature.get("properties"), dict):
            raise ValueError(f"Invalid feature or properties at index {i}")
        if not isinstance(feature.get("geometry"), dict):
            raise ValueError(f"Missing geometry at feature {i}")
    return payload


def retrieve(params: dict[str, str], timeout: int) -> tuple[bytes, str]:
    url = f"{API_URL}?{urlencode(params)}"
    request = Request(url, headers={
        "Accept": "application/geo+json, application/json",
        "User-Agent": "Tessellatum-Spatial-Methods/1.0 (reproducible research)",
    })
    with urlopen(request, timeout=timeout) as response:
        return response.read(), url


def value(properties: dict, *keys):
    for key in keys:
        found = properties.get(key)
        if found not in (None, ""):
            return found
    return None


def acquisition_datetime(properties: dict) -> datetime | None:
    raw = value(properties, "startTime", "starttime", "acquisitionDate", "sceneDate")
    if raw:
        try:
            parsed = datetime.fromisoformat(str(raw).replace("Z", "+00:00"))
            if parsed.tzinfo is None:
                parsed = parsed.replace(tzinfo=timezone.utc)
            return parsed.astimezone(timezone.utc)
        except ValueError:
            pass
    # Product/granule names commonly embed the source acquisition timestamp.
    text = " ".join(str(value(properties, k) or "") for k in
                    ("fileID", "fileName", "granuleName", "sceneName", "productName"))
    match = re.search(r"(20\d{6})T(\d{6})", text)
    if match:
        return datetime.strptime("".join(match.groups()), "%Y%m%d%H%M%S").replace(tzinfo=timezone.utc)
    return None


def summarize(collection: dict) -> dict:
    rows = []
    for feature in collection["features"]:
        props = feature["properties"]
        acquired = acquisition_datetime(props)
        date_key = acquired.strftime("%Y-%m-%d") if acquired else None
        target = ACQUISITIONS.get(date_key)
        difference = None
        if target and acquired:
            expected = datetime.fromisoformat(target.replace("Z", "+00:00"))
            difference = abs((acquired - expected).total_seconds())
        rows.append({
            "acquisition_datetime_utc": acquired.isoformat().replace("+00:00", "Z") if acquired else None,
            "seconds_from_expected_scene_time": difference,
            "within_source_time_tolerance": bool(difference is not None and difference <= TIME_TOLERANCE_SECONDS),
            "file_id": value(props, "fileID", "fileId", "granuleName", "sceneName"),
            "product_name": value(props, "fileName", "productName", "granuleName"),
            "burst_id": value(props, "operaBurstID", "operaBurstId", "burstID"),
            "polarization": value(props, "polarization", "polarisation"),
            "platform": value(props, "platform", "platformName"),
            "flight_direction": value(props, "flightDirection", "orbitDirection"),
            "properties": props,
            "geometry": feature["geometry"],
        })
    matched = [x for x in rows if x["within_source_time_tolerance"]]
    return {
        "schema": "tessellatum.opera-surat-r009-catalogue-discovery.v1",
        "source": API_URL,
        "query_aoi_bbox_wgs84": list(BBOX),
        "query_feature_count": len(rows),
        "time_tolerance_seconds": TIME_TOLERANCE_SECONDS,
        "expected_source_acquisitions": ACQUISITIONS,
        "time_matched_feature_count": len(matched),
        "matched_features": matched,
        "all_features": rows,
        "interpretation_limits": [
            "ASF catalogue intersection does not establish full AOI or reflector coverage.",
            "Time matching is a candidate screen; verify Sentinel-1 source granule and burst IDs against the original acquisition metadata.",
            "OPERA RTC-S1 is burst-based SLC processing with 30 m gamma0 power outputs, unlike the Sentinel Hub GRD workflow.",
            "Do not compare raw pixels until product geometry, radiometry, polarization, masks, effective resolution and temporal source identity are reconciled.",
            "This discovery step does not establish radiometric equivalence or validate the proposed equation.",
        ],
    }


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=Path("data/asf/surat_r009_opera"))
    parser.add_argument("--timeout", type=int, default=120)
    parser.add_argument("--max-results", type=int, default=500)
    args = parser.parse_args(argv)
    if args.timeout < 1:
        parser.error("--timeout must be positive")

    all_features = []
    queries = []
    for date, timestamp in ACQUISITIONS.items():
        center = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
        start = (center - timedelta(seconds=TIME_TOLERANCE_SECONDS)).isoformat().replace("+00:00", "Z")
        end = (center + timedelta(seconds=TIME_TOLERANCE_SECONDS)).isoformat().replace("+00:00", "Z")
        params = build_query(start, end, args.max_results)
        try:
            raw, query_url = retrieve(params, args.timeout)
            collection = parse_collection(raw)
        except HTTPError as exc:
            print(f"ASF HTTP error {exc.code}: {exc.reason}", file=sys.stderr)
            return 2
        except (URLError, TimeoutError, OSError, ValueError, json.JSONDecodeError) as exc:
            print(f"ASF catalogue query failed for {date}: {exc}", file=sys.stderr)
            return 3
        queries.append({
            "expected_date": date,
            "query_url": query_url,
            "feature_count": len(collection["features"]),
            "response_sha256": hashlib.sha256(raw).hexdigest(),
        })
        all_features.extend(collection["features"])

    # De-duplicate repeated catalogue rows by product identifier and burst name.
    unique = {}
    for feature in all_features:
        props = feature["properties"]
        key = value(props, "fileID", "fileId", "granuleName", "sceneName")
        if not key:
            key = json.dumps(feature, sort_keys=True)
        unique[key] = feature
    collection = {"type": "FeatureCollection", "features": list(unique.values())}
    report = summarize(collection)
    static_params = build_static_query()
    try:
        static_raw, static_url = retrieve(static_params, args.timeout)
        static_collection = parse_collection(static_raw)
    except HTTPError as exc:
        print(f"ASF RTC-STATIC HTTP error {exc.code}: {exc.reason}", file=sys.stderr)
        return 2
    except (URLError, TimeoutError, OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"ASF RTC-STATIC catalogue query failed: {exc}", file=sys.stderr)
        return 3
    wanted_bursts = {"T009-019159-IW3", "T009-019160-IW3", "T009_019159_IW3", "T009_019160_IW3"}
    static_features = []
    for x in static_collection["features"]:
        props = x["properties"]
        burst = value(props, "operaBurstID", "operaBurstId")
        if burst in wanted_bursts or any(burst and burst.replace("-", "_") == wanted.replace("-", "_") for wanted in wanted_bursts):
            static_features.append(x)
    report["static_layer_query"] = {
        "query_url": static_url,
        "response_sha256": hashlib.sha256(static_raw).hexdigest(),
        "catalogue_feature_count": len(static_collection["features"]),
        "matched_burst_ids": sorted({value(x["properties"], "operaBurstID", "operaBurstId") for x in static_features}),
        "feature_count": len(static_features),
        "features": [{
            "file_id": value(x["properties"], "fileID", "fileId", "sceneName"),
            "product_name": value(x["properties"], "fileName", "sceneName"),
            "burst_id": value(x["properties"], "operaBurstID", "operaBurstId"),
            "properties": x["properties"],
            "geometry": x["geometry"],
        } for x in static_features],
    }
    report["queries"] = queries
    args.output_dir.mkdir(parents=True, exist_ok=True)
    path = args.output_dir / "surat_r009_opera_rtc_catalogue_discovery.json"
    path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Queries: {len(queries)}; unique catalogue products: {len(unique)}")
    print(f"Time-matched products within +/-{TIME_TOLERANCE_SECONDS}s: {report['time_matched_feature_count']}")
    for row in report["matched_features"][:20]:
        print(f"{row['acquisition_datetime_utc']} | {row['burst_id']} | {row['polarization']} | {row['file_id']}")
    print(f"Report: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
