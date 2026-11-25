#!/usr/bin/env python3
"""Discover OpenAerialMap STAC imagery candidates intersecting Nairobi R130.

Metadata discovery only: no imagery downloads, visual interpretation, licence
validation, positional-accuracy assessment, or reference-label production.
"""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse, urlunsplit

import requests
from shapely.geometry import box, shape

STAC_ROOT = "https://api.imagery.hotosm.org/stac"
R130_BBOX = [36.65, -1.45, 37.05, -1.15]
START = "2026-10-01T00:00:00Z"
END = "2026-11-24T23:59:59Z"
TIMEOUT = 45
MAX_METADATA_BYTES = 1_000_000
METADATA_HOSTS = {"oin-hotosm-prod.s3.us-east-1.amazonaws.com"}


def validate_asset_href(href: str) -> bool:
    """Only report HTTPS asset URLs; never fetch them in this discovery tool."""
    parsed = urlparse(href)
    return parsed.scheme == "https" and bool(parsed.netloc)


def search_items(session=requests, bbox=R130_BBOX, start=START, end=END):
    """Fetch STAC search pages, honoring GET/POST next-link instructions.

    Pagination links are untrusted input: only HTTPS links to the configured
    STAC host are followed.
    """
    url = f"{STAC_ROOT}/search"
    params = {"bbox": ",".join(map(str, bbox)),
              "datetime": f"{start}/{end}", "limit": 100}
    initial_params = dict(params)
    items, pages = [], []
    root_host = urlparse(STAC_ROOT).netloc
    next_request = None
    while url:
        if next_request is None:
            response = session.get(url, params=params, timeout=TIMEOUT)
        else:
            method, body, headers = next_request
            if method == "GET":
                response = session.get(url, params=body or None,
                                       headers=headers or None, timeout=TIMEOUT)
            elif method == "POST":
                response = session.post(url, json=body or {},
                                        headers=headers or None, timeout=TIMEOUT)
            else:
                raise ValueError(f"Unsupported STAC pagination method: {method}")
        response.raise_for_status()
        page = response.json()
        pages.append({"url": response.url, "returned": len(page.get("features", []))})
        items.extend(page.get("features", []))
        next_link = next((x for x in page.get("links", [])
                          if x.get("rel") == "next"), None)
        if not next_link:
            url, next_request = None, None
            continue
        url = next_link.get("href", "")
        parsed = urlparse(url)
        if parsed.scheme != "https" or parsed.netloc != root_host:
            raise ValueError("Refusing STAC next link outside configured HTTPS host")
        method = (next_link.get("method") or "GET").upper()
        body = next_link.get("body") or {}
        if next_link.get("merge"):
            body = {**initial_params, **body}
        next_request = (method, body, next_link.get("headers") or {})
        params = None
    return items, pages


def fetch_source_metadata(href: str, session=requests):
    """Fetch only the small OAM metadata JSON from the known asset host.

    Never fetch the large visual/COG asset here. Redirects and non-allowlisted
    hosts are refused; response size is capped before JSON parsing.
    """
    parsed = urlparse(href)
    if parsed.scheme != "https" or parsed.netloc not in METADATA_HOSTS:
        return {"status": "blocked_untrusted_metadata_host"}
    try:
        response = session.get(href, timeout=TIMEOUT, stream=True,
                               allow_redirects=False)
        if response.status_code != 200:
            return {"status": "http_error", "http_status": response.status_code}
        declared = response.headers.get("Content-Length")
        if declared and int(declared) > MAX_METADATA_BYTES:
            return {"status": "too_large", "declared_bytes": int(declared)}
        chunks = []
        total = 0
        for chunk in response.iter_content(chunk_size=65536):
            if not chunk:
                continue
            total += len(chunk)
            if total > MAX_METADATA_BYTES:
                return {"status": "too_large", "received_bytes_at_least": total}
            chunks.append(chunk)
        payload = json.loads(b"".join(chunks).decode("utf-8"))
        if not isinstance(payload, dict):
            return {"status": "invalid_json_shape"}
        return {"status": "ok", "bytes": total, "metadata": payload}
    except (requests.RequestException, ValueError, UnicodeDecodeError) as exc:
        return {"status": "fetch_error", "error_type": type(exc).__name__}


def audit(items, bbox=R130_BBOX, fetch_metadata=False, session=requests):
    """Normalize candidate metadata and screen geometry against discovery bbox."""
    discovery_area = box(*bbox)
    rows = []
    for item in items:
        properties = item.get("properties") or {}
        geometry = item.get("geometry")
        geometry_present = geometry is not None
        intersects = None
        if geometry_present:
            try:
                intersects = bool(shape(geometry).intersects(discovery_area))
            except (TypeError, ValueError):
                intersects = None
        assets = item.get("assets") or {}
        hrefs = [asset.get("href", "") for asset in assets.values()
                 if isinstance(asset, dict)]
        rows.append({
            "id": item.get("id"),
            "collection": item.get("collection"),
            "datetime": properties.get("datetime"),
            "start_datetime": properties.get("start_datetime"),
            "end_datetime": properties.get("end_datetime"),
            "platform": properties.get("platform"),
            "platform_type": properties.get("oam:platform_type"),
            "producer_name": properties.get("oam:producer_name"),
            "gsd": properties.get("gsd"),
            "license": properties.get("license") or item.get("license"),
            "acquisition_time_estimated": properties.get("oam:acquisition_time_estimated"),
            "acquisition_source": properties.get("oam:acquisition_source"),
            "footprint_source": properties.get("oam:footprint_source"),
            "footprint_area": properties.get("oam:footprint_area"),
            "geometry_present": geometry_present,
            "intersects_r130_bbox": intersects,
            "bbox": item.get("bbox"),
            # Preserve source geometry so a later step can intersect the exact
            # item footprint with the frozen R130 mask. This remains unverified
            # catalogue metadata, not a positional-accuracy assessment.
            "geometry": geometry,
            "assets": {
                key: {
                    "href": (urlunsplit((urlparse(asset.get("href", "")).scheme,
                                         urlparse(asset.get("href", "")).netloc,
                                         urlparse(asset.get("href", "")).path, "", ""))
                            if isinstance(asset, dict) and validate_asset_href(asset.get("href", ""))
                            else None),
                    "href_query_redacted": bool(urlparse(asset.get("href", "")).query)
                        if isinstance(asset, dict) else False,
                    "type": asset.get("type"),
                    "roles": asset.get("roles"),
                    "title": asset.get("title"),
                    "file:size": asset.get("file:size"),
                    "raster:bands": asset.get("raster:bands"),
                }
                for key, asset in assets.items() if isinstance(asset, dict)
            },
            "source_metadata": (fetch_source_metadata(assets.get("metadata", {}).get("href", ""), session=session)
                                if fetch_metadata and isinstance(assets.get("metadata"), dict) else None),
            "asset_keys": sorted(assets),
            "https_asset_hrefs_available": sum(validate_asset_href(href) for href in hrefs),
        })
    return rows


def build_report(items, pages, bbox=R130_BBOX, start=START, end=END, fetch_metadata=False):
    rows = audit(items, bbox=bbox, fetch_metadata=fetch_metadata)
    return {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "catalogue": STAC_ROOT,
        "query": {"bbox": bbox, "datetime": [start, end]},
        "pages": pages,
        "item_count": len(rows),
        "items": rows,
        "limitations": [
            "Discovery rectangle is not the frozen exact R130 analysis mask.",
            "Geometry intersection is a screening result, not proof of usable pixel overlap or positional alignment.",
            "Catalogue geometry and metadata are preserved for follow-up but require source/provider confirmation and positional-quality assessment.",
            "Asset URL query strings are redacted; only bounded metadata JSON from the allowlisted OAM S3 host is optionally fetched; the visual COG is never downloaded by this client.",
            "No imagery was downloaded or visually interpreted; no reference labels or accuracy estimates were produced.",
        ],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--start", default=START)
    parser.add_argument("--end", default=END)
    parser.add_argument("--fetch-metadata", action="store_true",
                        help="Fetch bounded metadata JSON from the allowlisted OAM asset host; never fetch the visual COG.")
    parser.add_argument("--output", type=Path,
                        default=Path("data/reference/nairobi-r130-oam-stac-audit.json"))
    args = parser.parse_args()
    items, pages = search_items(start=args.start, end=args.end)
    report = build_report(items, pages, start=args.start, end=args.end,
                          fetch_metadata=args.fetch_metadata)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n",
                           encoding="utf-8")
    print(f"Wrote {report['item_count']} STAC items across {len(pages)} pages to {args.output}")


if __name__ == "__main__":
    main()
