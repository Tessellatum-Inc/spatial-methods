#!/usr/bin/env python3
"""Discover 2021 Sentinel-2 scenes and create small point chips from STAC assets.

No scene-wide downloads. Earth Search HTTPS COG assets are read through GDAL
range requests. CDSE S3 assets can be read through GDAL's /vsis3/ driver when
CDSE S3 credentials are configured in the environment.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

import numpy as np
import requests

EARTH_SEARCH = "https://earth-search.aws.element84.com/v1/search"
CDSE_STAC = "https://stac.dataspace.copernicus.eu/v1/search"
EARTH_COLLECTIONS = ("sentinel-2-c1-l2a", "sentinel-2-l2a")
CDSE_COLLECTIONS = ("sentinel-2-l2a",)
DATE_RANGE = "2021-01-01T00:00:00Z/2021-12-31T23:59:59Z"
BAND_ALIASES = {
    "blue": ("blue", "B02", "B02_10m", "B02_20m"),
    "green": ("green", "B03", "B03_10m", "B03_20m"),
    "red": ("red", "B04", "B04_10m", "B04_20m"),
}


def post_search(endpoint: str, collection: str, lon: float, lat: float,
                limit: int = 100) -> list[dict[str, Any]]:
    body = {
        "collections": [collection],
        "intersects": {"type": "Point", "coordinates": [lon, lat]},
        "datetime": DATE_RANGE,
        "limit": limit,
        "sortby": [{"field": "properties.eo:cloud_cover", "direction": "asc"}],
    }
    response = requests.post(endpoint, json=body, timeout=60)
    response.raise_for_status()
    payload = response.json()
    return payload.get("features", [])


def search_catalogue(endpoint: str, collections: tuple[str, ...],
                     lon: float, lat: float) -> list[dict[str, Any]]:
    found: dict[str, dict[str, Any]] = {}
    errors = []
    for collection in collections:
        try:
            for item in post_search(endpoint, collection, lon, lat):
                found[item.get("id", json.dumps(item, sort_keys=True))] = item
        except requests.RequestException as exc:
            errors.append(f"{collection}: {exc}")
    if not found and errors:
        raise RuntimeError("; ".join(errors))
    return list(found.values())


def item_cloud(item: dict[str, Any]) -> float:
    props = item.get("properties", {})
    value = props.get("eo:cloud_cover", props.get("cloudCover", 100))
    try:
        return float(value)
    except (TypeError, ValueError):
        return 100.0


def acquisition(item: dict[str, Any]) -> str:
    props = item.get("properties", {})
    return str(props.get("datetime") or props.get("start_datetime") or "")


def asset_for(item: dict[str, Any], band: str) -> tuple[str, str] | None:
    assets = item.get("assets", {})
    for alias in BAND_ALIASES[band]:
        if alias in assets:
            asset = assets[alias]
            href = asset.get("href")
            if href:
                return alias, href
    # Some catalogues use lowercase band names with resolution suffixes.
    for key, asset in assets.items():
        if key.lower() in {x.lower() for x in BAND_ALIASES[band]} and asset.get("href"):
            return key, asset["href"]
    return None


def open_raster_href(href: str):
    import rasterio
    if href.startswith("s3://"):
        # CDSE S3 endpoint. Credentials must be exported by the user.
        parsed = urlparse(href)
        bucket_key = parsed.netloc + parsed.path
        vsi_path = "/vsis3/" + bucket_key.lstrip("/")
        env = {
            "AWS_S3_ENDPOINT": os.getenv("CDSE_S3_ENDPOINT", "eodata.dataspace.copernicus.eu"),
            "AWS_HTTPS": "YES",
            "AWS_VIRTUAL_HOSTING": "FALSE",
            "AWS_REGION": os.getenv("AWS_DEFAULT_REGION", "default"),
            "AWS_ACCESS_KEY_ID": os.environ["AWS_ACCESS_KEY_ID"],
            "AWS_SECRET_ACCESS_KEY": os.environ["AWS_SECRET_ACCESS_KEY"],
        }
        return rasterio.open(vsi_path), rasterio.Env(**env)
    if href.startswith("https://") or href.startswith("http://"):
        # GDAL /vsicurl/ uses HTTP range requests for COG windows.
        return rasterio.open(href), rasterio.Env()
    raise ValueError(f"Unsupported asset href scheme: {href}")


def render_chip(item: dict[str, Any], lon: float, lat: float,
                output: Path, chip_pixels: int = 256) -> dict[str, Any]:
    import rasterio
    from rasterio.windows import Window
    from PIL import Image

    selected = {band: asset_for(item, band) for band in ("red", "green", "blue")}
    if any(value is None for value in selected.values()):
        raise RuntimeError("Item does not expose all three RGB band assets")

    arrays = []
    dimensions = None
    asset_names = {}
    bytes_note = "HTTP range/S3 window reads; exact transferred bytes are not exposed by rasterio"
    for band in ("red", "green", "blue"):
        asset_name, href = selected[band]
        src, env = open_raster_href(href)
        try:
            with env:
                with src:
                    row, col = src.index(lon, lat)
                    half = chip_pixels // 2
                    window = Window(col - half, row - half, chip_pixels, chip_pixels)
                    data = src.read(1, window=window, boundless=True, fill_value=0)
                    mask = src.read_masks(1, window=window, boundless=True)
                    arrays.append((data, mask))
                    dimensions = list(data.shape)
                    asset_names[band] = asset_name
        except Exception:
            try:
                src.close()
            except Exception:
                pass
            raise

    rgb = []
    for data, mask in arrays:
        valid = data[(mask > 0) & (data > 0)]
        if valid.size == 0:
            rgb.append(np.zeros(data.shape, dtype=np.uint8))
            continue
        lo, hi = np.percentile(valid, [2, 98])
        if hi <= lo:
            hi = lo + 1
        stretched = np.clip((data.astype(np.float32) - lo) * 255.0 / (hi - lo), 0, 255)
        stretched[mask == 0] = 0
        rgb.append(stretched.astype(np.uint8))

    image = np.dstack(rgb)
    output.parent.mkdir(parents=True, exist_ok=True)
    Image.fromarray(image, mode="RGB").save(output, format="PNG", optimize=True)
    digest = hashlib.sha256(output.read_bytes()).hexdigest()
    props = item.get("properties", {})
    return {
        "item_id": item.get("id", ""),
        "collection": item.get("collection", ""),
        "datetime": acquisition(item),
        "cloud_cover_percent": item_cloud(item),
        "platform": props.get("platform", ""),
        "assets": json.dumps(asset_names, sort_keys=True),
        "chip_file": str(output),
        "chip_width": dimensions[1] if dimensions else "",
        "chip_height": dimensions[0] if dimensions else "",
        "chip_bytes": output.stat().st_size,
        "chip_sha256": digest,
        "read_method": bytes_note,
        "longitude": lon,
        "latitude": lat,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, help="Blind review CSV")
    parser.add_argument("--output-dir", default="tmp/fiji-stac-chips")
    parser.add_argument("--catalogues", choices=("both", "earth-search", "cdse"),
                        default="both")
    parser.add_argument("--limit-per-point", type=int, default=3)
    parser.add_argument("--chip-pixels", type=int, default=256)
    parser.add_argument("--metadata-only", action="store_true",
                        help="Discover scenes and write metadata without reading imagery")
    parser.add_argument("--keep-chips", action="store_true",
                        help="Keep PNG chips; otherwise delete them after provenance is written")
    args = parser.parse_args()

    if args.chip_pixels < 32 or args.chip_pixels > 1024:
        parser.error("--chip-pixels must be between 32 and 1024")

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    provenance_path = output_dir / "stac-imagery-provenance.csv"
    errors_path = output_dir / "stac-search-errors.csv"
    rows: list[dict[str, Any]] = []
    errors: list[dict[str, str]] = []

    with open(args.input, newline="", encoding="utf-8-sig") as stream:
        points = list(csv.DictReader(stream))

    for point in points:
        sample_id = point["sample_id"]
        lon, lat = float(point["longitude"]), float(point["latitude"])
        if not (-180 <= lon <= 180 and -90 <= lat <= 90):
            errors.append({"sample_id": sample_id, "catalogue": "", "error": "Invalid WGS84 coordinates"})
            continue

        catalogues = []
        if args.catalogues in ("both", "earth-search"):
            catalogues.append(("earth-search", EARTH_SEARCH, EARTH_COLLECTIONS))
        if args.catalogues in ("both", "cdse"):
            catalogues.append(("cdse", CDSE_STAC, CDSE_COLLECTIONS))

        for label, endpoint, collections in catalogues:
            try:
                items = search_catalogue(endpoint, collections, lon, lat)
                items.sort(key=lambda item: (item_cloud(item), acquisition(item)), reverse=False)
                for index, item in enumerate(items[:args.limit_per_point]):
                    base = {
                        "sample_id": sample_id,
                        "catalogue": label,
                        "item_id": item.get("id", ""),
                        "collection": item.get("collection", ""),
                        "datetime": acquisition(item),
                        "cloud_cover_percent": item_cloud(item),
                        "platform": item.get("properties", {}).get("platform", ""),
                        "assets_available": json.dumps(sorted(item.get("assets", {}).keys())),
                        "longitude": lon,
                        "latitude": lat,
                        "status": "discovered",
                        "chip_file": "",
                        "chip_bytes": "",
                        "chip_sha256": "",
                        "notes": "",
                    }
                    if not args.metadata_only:
                        try:
                            chip = output_dir / f"{re.sub(r'[^A-Za-z0-9_.-]', '_', sample_id)}_{label}_{index+1}.png"
                            details = render_chip(item, lon, lat, chip, args.chip_pixels)
                            base.update(details)
                            base["status"] = "chip_created"
                            if not args.keep_chips:
                                chip.unlink(missing_ok=True)
                                base["status"] = "chip_created_then_deleted"
                                base["chip_file"] = ""
                        except Exception as exc:
                            base["status"] = "asset_or_chip_failed"
                            base["notes"] = str(exc)
                    rows.append(base)
                if not items:
                    rows.append({
                        "sample_id": sample_id, "catalogue": label, "item_id": "",
                        "collection": "", "datetime": "", "cloud_cover_percent": "",
                        "platform": "", "assets_available": "", "longitude": lon,
                        "latitude": lat, "status": "no_items", "chip_file": "",
                        "chip_bytes": "", "chip_sha256": "",
                        "notes": "No 2021 items returned for this point and collection set.",
                    })
            except Exception as exc:
                errors.append({"sample_id": sample_id, "catalogue": label, "error": str(exc)})

    if rows:
        with open(provenance_path, "w", newline="", encoding="utf-8") as stream:
            writer = csv.DictWriter(stream, fieldnames=list(rows[0].keys()))
            writer.writeheader()
            writer.writerows(rows)
    if errors:
        with open(errors_path, "w", newline="", encoding="utf-8") as stream:
            writer = csv.DictWriter(stream, fieldnames=["sample_id", "catalogue", "error"])
            writer.writeheader()
            writer.writerows(errors)

    print(json.dumps({
        "points": len(points),
        "provenance_rows": len(rows),
        "search_errors": len(errors),
        "provenance_csv": str(provenance_path),
        "errors_csv": str(errors_path) if errors else None,
        "chips_retained": bool(args.keep_chips and not args.metadata_only),
        "note": "An empty catalogue result is not proof of no imagery; cross-check the other catalogue, especially around the antimeridian.",
    }, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
