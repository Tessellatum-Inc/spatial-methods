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
    """Fetch STAC search pages, honoring GET/POST next-link instructions.

    Pagination links are treated as untrusted input: only HTTPS links to the
    configured STAC host are followed.
    """
    url = f"{STAC_ROOT}/search"
    params = {"bbox": ",".join(map(str, bbox)),
              "datetime": f"{start}/{end}", "limit": 100}
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
            body = {**params, **body}
        next_request = (method, body, next_link.get("headers") or {})
        params = None
    return items, pages
