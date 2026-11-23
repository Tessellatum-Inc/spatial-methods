#!/usr/bin/env python3
"""Probe anonymous HTTPS access to representative OPERA RTC and RTC-STATIC assets."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


def probe(url: str, timeout: int = 30) -> dict:
    request = Request(url, method="GET", headers={
        "Range": "bytes=0-15",
        "User-Agent": "Tessellatum-Spatial-Methods/1.0",
    })
    try:
        with urlopen(request, timeout=timeout) as response:
            sample = response.read(16)
            return {
                "url": url,
                "status": response.status,
                "content_type": response.headers.get("Content-Type"),
                "content_range": response.headers.get("Content-Range"),
                "sample_bytes": len(sample),
                "accessible_without_auth": response.status in (200, 206),
            }
    except HTTPError as exc:
        return {
            "url": url,
            "status": exc.code,
            "reason": str(exc.reason),
            "accessible_without_auth": False,
        }
    except (URLError, TimeoutError, OSError) as exc:
        return {
            "url": url,
            "status": None,
            "reason": str(exc),
            "accessible_without_auth": False,
        }


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", type=Path, default=Path(
        "data/asf/surat_r009_opera/surat_r009_opera_rtc_catalogue_discovery.json"
    ))
    parser.add_argument("--output", type=Path, default=Path(
        "data/asf/surat_r009_opera/anonymous_access_probe.json"
    ))
    args = parser.parse_args(argv)
    report = json.loads(args.report.read_text(encoding="utf-8"))
    dynamic = report["matched_features"]
    static = report["static_layer_query"]["features"]
    dynamic_url = next(
        u for u in dynamic[0]["properties"].get("additionalUrls", [])
        if u.endswith("_VV.tif")
    )
    static_url = next(
        u for u in static[0]["properties"].get("additionalUrls", [])
        if u.endswith("_rtc_anf_gamma0_to_beta0.tif")
    )
    results = [probe(dynamic_url), probe(static_url)]
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
    for item in results:
        print(f"{item['status']} {item['url']} accessible_without_auth={item['accessible_without_auth']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
