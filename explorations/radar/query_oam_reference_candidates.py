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
from urllib.parse import urlparse

import requests
from shapely.geometry import box, shape

STAC_ROOT = "https://api.imagery.hotosm.org/stac"
R130_BBOX = [36.65, -1.45, 37.05, -1.15]
START = "2026-10-01T00:00:00Z"
END = "2026-11-24T23:59:59Z"
TIMEOUT = 45


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


def audit(items, bbox=R130_BBOX):
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
            "asset_keys": sorted(assets),
            "https_asset_hrefs_available": sum(validate_asset_href(href) for href in hrefs),
        })
    return rows


def build_report(items, pages, bbox=R130_BBOX, start=START, end=END):
    rows = audit(items, bbox=bbox)
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
            "Metadata, acquisition dates, platform, GSD, licence and asset availability require source-level confirmation.",
            "HTTPS asset URL presence does not validate the asset or authorize its use.",
            "No imagery was downloaded or visually interpreted; no reference labels or accuracy estimates were produced.",
        ],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--start", default=START)
    parser.add_argument("--end", default=END)
    parser.add_argument("--output", type=Path,
                        default=Path("data/reference/nairobi-r130-oam-stac-audit.json"))
    args = parser.parse_args()
    items, pages = search_items(start=args.start, end=args.end)
    report = build_report(items, pages, start=args.start, end=args.end)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n",
                           encoding="utf-8")
    print(f"Wrote {report['item_count']} STAC items across {len(pages)} pages to {args.output}")


if __name__ == "__main__":
    main()
