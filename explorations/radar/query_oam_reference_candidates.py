#!/usr/bin/env python3
"""Discover OpenAerialMap STAC imagery candidates intersecting Nairobi R130.

This is a discovery/metadata audit only. It does not download imagery or
establish positional accuracy, licence validity, or reference-label quality.
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
    url = f"{STAC_ROOT}/search"
    params = {"bbox": ",".join(map(str, bbox)),
              "datetime": f"{start}/{end}", "limit": 100}
    items, pages = [], []
    while url:
        response = session.get(url, params=params, timeout=TIMEOUT)
        response.raise_for_status()
        page = response.json()
        pages.append({"url": response.url, "returned": len(page.get("features", []))})
        items.extend(page.get("features", []))
        next_link = next((x for x in page.get("links", []) if x.get("rel") == "next"), None)
        url = next_link.get("href") if next_link else None
        params = None
    return items, pages


def audit(items, bbox=R130_BBOX):
    aoi = box(*bbox)
    rows = []
    for item in items:
        geom = item.get("geometry")
        intersection_fraction = None
        if geom:
            footprint = shape(geom)
            if not footprint.is_empty and footprint.is_valid:
                intersection_fraction = float(footprint.intersection(aoi).area / aoi.area)
        props = item.get("properties") or {}
        assets = item.get("assets") or {}
        hrefs = [a.get("href", "") for a in assets.values()]
        rows.append({
            "id": item.get("id"),
            "collection": item.get("collection"),
            "datetime": props.get("datetime"),
            "start_datetime": props.get("start_datetime"),
            "end_datetime": props.get("end_datetime"),
            "title": props.get("title") or props.get("oam:imagery_title"),
            "platform": props.get("platform") or props.get("oam:platform"),
            "platform_type": props.get("oam:platform_type"),
            "gsd": props.get("gsd"),
            "license": item.get("license") or props.get("license"),
            "bbox": item.get("bbox"),
            "r130_bbox_intersection_fraction": intersection_fraction,
            "asset_keys": sorted(assets),
            "https_asset_hrefs_available": sum(validate_asset_href(x) for x in hrefs),
            "geometry_present": bool(geom),
        })
    return rows


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path,
                        default=Path("data/reference/nairobi-r130-oam-stac-audit.json"))
    parser.add_argument("--start", default=START)
    parser.add_argument("--end", default=END)
    args = parser.parse_args()
    items, pages = search_items(start=args.start, end=args.end)
    report = {
        "schema": "tessellatum.nairobi-r130.oam-stac-audit.v1",
        "retrieved_at": datetime.now(timezone.utc).isoformat(),
        "stac_root": STAC_ROOT,
        "bbox_crs84": R130_BBOX,
        "datetime_interval": [args.start, args.end],
        "pages": pages,
        "item_count": len(items),
        "items": audit(items),
        "limitations": [
            "STAC bbox search is a candidate screen; inspect full item geometry.",
            "No imagery asset is downloaded or visually interpreted.",
            "Reported GSD, acquisition time and licence require item/source verification.",
            "R130 rectangular search AOI is not the final analysis mask.",
            "No reference labels or empirical accuracy estimates are produced."
        ]
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n")
    print(f"Items: {len(items)}; pages: {len(pages)}; report: {args.output}")


if __name__ == "__main__":
    main()
