#!/usr/bin/env python3
"""Discover 2021 Sentinel-2 scenes and create point-centred RGB review chips.

Only small raster windows are read. No scene-wide downloads are intended.
Earth Search HTTPS COGs use GDAL range requests. The public sentinel-cogs S3
bucket is accessed anonymously; CDSE S3 assets require generated credentials.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import re
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
# Prefer explicit 10 m assets. Generic Earth Search aliases are fallbacks.
BAND_ALIASES = {
    "blue": ("B02_10m", "blue", "B02", "B02_20m"),
    "green": ("B03_10m", "green", "B03", "B03_20m"),
    "red": ("B04_10m", "red", "B04", "B04_20m"),
}
REQUEST_TIMEOUT = float(os.getenv("STAC_REQUEST_TIMEOUT", "60"))
MAX_PAGES = int(os.getenv("STAC_MAX_PAGES", "10"))

PROVENANCE_FIELDS = (
    "sample_id", "catalogue", "item_id", "collection", "datetime",
    "cloud_cover_percent", "platform", "assets_available", "assets",
    "source_grid", "longitude", "latitude", "status", "chip_file",
    "chip_width", "chip_height", "chip_bytes", "chip_sha256",
    "read_method", "stretch", "notes",
)


def _request_page(method: str, href: str, body: dict[str, Any] | None = None,
                  headers: dict[str, str] | None = None) -> dict[str, Any]:
    method = method.upper()
    if method == "POST":
        response = requests.post(href, json=body or {}, headers=headers,
                                 timeout=REQUEST_TIMEOUT)
    elif method == "GET":
        response = requests.get(href, params=body if body else None,
                                headers=headers, timeout=REQUEST_TIMEOUT)
    else:
        raise ValueError(f"Unsupported STAC pagination method: {method}")
    response.raise_for_status()
    payload = response.json()
    if not isinstance(payload, dict):
        raise ValueError("STAC search response was not a JSON object")
    return payload


def post_search(endpoint: str, collection: str, lon: float, lat: float,
                limit: int = 100, max_pages: int = MAX_PAGES) -> list[dict[str, Any]]:
    """Search one collection and follow STAC next links up to max_pages."""
    if limit < 1 or max_pages < 1:
        raise ValueError("limit and max_pages must be positive")
    body: dict[str, Any] = {
        "collections": [collection],
        "intersects": {"type": "Point", "coordinates": [lon, lat]},
        "datetime": DATE_RANGE,
        "limit": limit,
    }
    payload = _request_page("POST", endpoint, body)
    features: list[dict[str, Any]] = []
    seen: set[str] = set()
    for page_number in range(max_pages):
        for item in payload.get("features", []):
            if not isinstance(item, dict):
                continue
            identity = str(item.get("id") or json.dumps(item, sort_keys=True))
            if identity not in seen:
                seen.add(identity)
                features.append(item)
        next_link = next(
            (link for link in payload.get("links", [])
             if link.get("rel") == "next" and link.get("href")),
            None,
        )
        if not next_link or page_number + 1 >= max_pages:
            break
        payload = _request_page(
            next_link.get("method", "GET"),
            next_link["href"],
            next_link.get("body"),
            next_link.get("headers"),
        )
    return features


def search_catalogue(endpoint: str, collections: tuple[str, ...],
                     lon: float, lat: float) -> tuple[list[dict[str, Any]], list[str]]:
    """Return successful items and collection-specific errors without hiding partial failure."""
    found: dict[str, dict[str, Any]] = {}
    errors: list[str] = []
    for collection in collections:
        try:
            for item in post_search(endpoint, collection, lon, lat):
                identity = str(item.get("id") or json.dumps(item, sort_keys=True))
                found[identity] = item
        except (requests.RequestException, ValueError, KeyError) as exc:
            errors.append(f"{collection}: {type(exc).__name__}: {exc}")
    return list(found.values()), errors


def write_provenance(path: Path, rows: list[dict[str, Any]]) -> None:
    """Write discovery and chip rows using one stable CSV schema."""
    if not rows:
        path.unlink(missing_ok=True)
        return
    with open(path, "w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=PROVENANCE_FIELDS, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in PROVENANCE_FIELDS})

def item_cloud(item: dict[str, Any]) -> float:
    props = item.get("properties", {})
    value = props.get("eo:cloud_cover", props.get("cloudCover", 100))
    try:
        result = float(value)
        return result if np.isfinite(result) and 0 <= result <= 100 else 100.0
    except (TypeError, ValueError):
        return 100.0


def acquisition(item: dict[str, Any]) -> str:
    props = item.get("properties", {})
    return str(props.get("datetime") or props.get("start_datetime") or "")


def asset_for(item: dict[str, Any], band: str) -> tuple[str, str] | None:
    """Prefer directly readable HTTPS assets over S3 aliases when both exist."""
    if band not in BAND_ALIASES:
        raise ValueError(f"Unsupported RGB band: {band}")
    assets = item.get("assets", {})
    # Preserve the configured alias preference (especially explicit 10 m bands),
    # while preferring HTTP(S) over S3 for each matching alias.
    for name in BAND_ALIASES[band]:
        aliases = {name.lower(), f"{name.lower()}-jp2"}
        matches = [
            (key, asset.get("href", ""))
            for key, asset in assets.items()
            if key.lower() in aliases and asset.get("href")
        ]
        if not matches:
            continue
        public = [
            (key, href)
            for key, href in matches
            if href.startswith(("https://", "http://"))
        ]
        if public:
            return public[0]
        return matches[0]
    return None


def rasterio_source(href: str):
    """Return (GDAL path, rasterio.Env); the caller enters Env before opening."""
    import rasterio
    if href.startswith("s3://"):
        parsed = urlparse(href)
        vsi_path = "/vsis3/" + (parsed.netloc + parsed.path).lstrip("/")
        # Earth Search's legacy Sentinel-2 collection exposes the public
        # sentinel-cogs bucket through s3:// URLs. Do not mistake these for
        # Copernicus Data Space S3 assets or require CDSE credentials.
        if parsed.netloc == "sentinel-cogs":
            env = rasterio.Env(
                AWS_NO_SIGN_REQUEST="YES",
                AWS_REGION=os.getenv("AWS_DEFAULT_REGION", "us-west-2"),
            )
            return vsi_path, env

        access = os.getenv("AWS_ACCESS_KEY_ID")
        secret = os.getenv("AWS_SECRET_ACCESS_KEY")
        if not access or not secret:
            raise RuntimeError(
                f"S3 asset bucket '{parsed.netloc}' requires AWS_ACCESS_KEY_ID "
                "and AWS_SECRET_ACCESS_KEY; configure the credentials for that bucket."
            )
        env = rasterio.Env(
            AWS_S3_ENDPOINT=os.getenv("CDSE_S3_ENDPOINT", "eodata.dataspace.copernicus.eu"),
            AWS_HTTPS="YES",
            AWS_VIRTUAL_HOSTING="FALSE",
            AWS_REGION=os.getenv("AWS_DEFAULT_REGION", "default"),
            AWS_ACCESS_KEY_ID=access,
            AWS_SECRET_ACCESS_KEY=secret,
        )
        return vsi_path, env
    if href.startswith(("https://", "http://")):
        return href, rasterio.Env()
    raise ValueError(f"Unsupported asset href scheme: {href}")


def render_chip(item: dict[str, Any], lon: float, lat: float,
                output: Path, chip_pixels: int = 256) -> dict[str, Any]:
    import rasterio
    from rasterio.warp import transform as transform_coordinates
    from rasterio.windows import Window
    from PIL import Image

    selected = {band: asset_for(item, band) for band in ("red", "green", "blue")}
    if any(value is None for value in selected.values()):
        raise RuntimeError("Item does not expose all three RGB band assets")

    arrays: list[tuple[np.ndarray, np.ndarray]] = []
    grid_signature = None
    asset_names: dict[str, str] = {}
    source_metadata: dict[str, Any] = {}
    for band in ("red", "green", "blue"):
        asset_name, href = selected[band]  # type: ignore[misc]
        raster_path, env = rasterio_source(href)
        with env:
            with rasterio.open(raster_path) as src:
                if src.crs is None:
                    raise RuntimeError(f"{asset_name} asset has no CRS")
                x, y = transform_coordinates("EPSG:4326", src.crs, [lon], [lat])
                row, col = src.index(x[0], y[0])
                if not (0 <= row < src.height and 0 <= col < src.width):
                    raise RuntimeError(f"Sample point falls outside {asset_name} raster bounds")
                half = chip_pixels // 2
                window = Window(col - half, row - half, chip_pixels, chip_pixels)
                signature = (src.crs.to_string(), src.transform, src.width, src.height)
                if grid_signature is None:
                    grid_signature = signature
                elif signature != grid_signature:
                    raise RuntimeError(
                        "RGB assets are not on the same grid; refusing to create a misaligned chip"
                    )
                data = src.read(1, window=window, boundless=True, fill_value=0)
                mask = src.read_masks(1, window=window, boundless=True)
                arrays.append((data, mask))
                asset_names[band] = asset_name
                source_metadata[band] = {
                    "crs": src.crs.to_string(),
                    "resolution": [abs(src.transform.a), abs(src.transform.e)],
                    "nodata": src.nodata,
                }

    rgb = []
    for data, mask in arrays:
        valid = data[(mask > 0) & (data > 0)]
        if valid.size == 0:
            rgb.append(np.zeros(data.shape, dtype=np.uint8))
            continue
        low, high = np.percentile(valid, [2, 98])
        if high <= low:
            high = low + 1
        stretched = np.clip((data.astype(np.float32) - low) * 255.0 / (high - low), 0, 255)
        stretched[mask == 0] = 0
        rgb.append(stretched.astype(np.uint8))

    if not (rgb[0].shape == rgb[1].shape == rgb[2].shape):
        raise RuntimeError("RGB band arrays have different dimensions")
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
        "source_grid": json.dumps(source_metadata, sort_keys=True),
        "chip_file": str(output),
        "chip_width": image.shape[1],
        "chip_height": image.shape[0],
        "chip_bytes": output.stat().st_size,
        "chip_sha256": digest,
        "read_method": "GDAL window read; HTTP range/S3 requests; exact transferred bytes not exposed",
        "longitude": lon,
        "latitude": lat,
        "stretch": "independent per-band 2nd-98th percentile; nodata masked to black",
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
    if args.limit_per_point < 1:
        parser.error("--limit-per-point must be positive")

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    provenance_path = output_dir / "stac-imagery-provenance.csv"
    errors_path = output_dir / "stac-search-errors.csv"
    rows: list[dict[str, Any]] = []
    errors: list[dict[str, str]] = []

    with open(args.input, newline="", encoding="utf-8-sig") as stream:
        reader = csv.DictReader(stream)
        points = list(reader)
        input_fields = set(reader.fieldnames or [])
    required = {"sample_id", "longitude", "latitude"}
    if not points or not required.issubset(input_fields):
        parser.error(f"Input CSV must contain rows and columns: {', '.join(sorted(required))}")
    sample_ids = [str(point.get("sample_id", "")).strip() for point in points]
    if any(not value for value in sample_ids):
        parser.error("Every input row must have a non-empty sample_id")
    if len(sample_ids) != len(set(sample_ids)):
        parser.error("Input sample_id values must be unique")
    safe_ids = [re.sub(r"[^A-Za-z0-9_.-]", "_", value) for value in sample_ids]
    if len(safe_ids) != len(set(safe_ids)):
        parser.error("Input sample_id values collide after chip filename sanitisation")

    catalogues = []
    if args.catalogues in ("both", "earth-search"):
        catalogues.append(("earth-search", EARTH_SEARCH, EARTH_COLLECTIONS))
    if args.catalogues in ("both", "cdse"):
        catalogues.append(("cdse", CDSE_STAC, CDSE_COLLECTIONS))

    for point in points:
        sample_id = point["sample_id"]
        try:
            lon, lat = float(point["longitude"]), float(point["latitude"])
        except (TypeError, ValueError):
            errors.append({"sample_id": sample_id, "catalogue": "", "error": "Invalid numeric coordinates"})
            continue
        if not (-180 <= lon <= 180 and -90 <= lat <= 90):
            errors.append({"sample_id": sample_id, "catalogue": "", "error": "Invalid WGS84 coordinates"})
            continue

        for label, endpoint, collections in catalogues:
            items, collection_errors = search_catalogue(endpoint, collections, lon, lat)
            for error in collection_errors:
                errors.append({"sample_id": sample_id, "catalogue": label, "error": error})
            items.sort(key=lambda item: (item_cloud(item), acquisition(item)))
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
                    "chip_width": "",
                    "chip_height": "",
                    "chip_bytes": "",
                    "chip_sha256": "",
                    "notes": "",
                }
                if not args.metadata_only:
                    chip = output_dir / f"{re.sub(r'[^A-Za-z0-9_.-]', '_', sample_id)}_{label}_{index+1}.png"
                    try:
                        details = render_chip(item, lon, lat, chip, args.chip_pixels)
                        base.update(details)
                        base["status"] = "chip_created"
                        if not args.keep_chips:
                            chip.unlink(missing_ok=True)
                            base["status"] = "chip_created_then_deleted"
                            base["chip_file"] = ""
                    except Exception as exc:
                        base["status"] = "asset_or_chip_failed"
                        base["notes"] = f"{type(exc).__name__}: {exc}"
                        chip.unlink(missing_ok=True)
                rows.append(base)
            if not items:
                rows.append({
                    "sample_id": sample_id, "catalogue": label, "item_id": "",
                    "collection": "", "datetime": "", "cloud_cover_percent": "",
                    "platform": "", "assets_available": "", "longitude": lon,
                    "latitude": lat,
                    "status": "search_failed" if collection_errors else "no_items",
                    "chip_file": "", "chip_width": "", "chip_height": "",
                    "chip_bytes": "", "chip_sha256": "",
                    "notes": (
                        "Catalogue search failed; no conclusion about imagery coverage is possible."
                        if collection_errors
                        else "No 2021 items returned; this is not proof of no imagery."
                    ),
                })

    write_provenance(provenance_path, rows)

    if errors:
        with open(errors_path, "w", newline="", encoding="utf-8") as stream:
            writer = csv.DictWriter(stream, fieldnames=["sample_id", "catalogue", "error"])
            writer.writeheader()
            writer.writerows(errors)
    elif errors_path.exists():
        errors_path.unlink()

    print(json.dumps({
        "points": len(points),
        "provenance_rows": len(rows),
        "search_errors": len(errors),
        "provenance_csv": str(provenance_path) if rows else None,
        "errors_csv": str(errors_path) if errors else None,
        "chips_retained": bool(args.keep_chips and not args.metadata_only),
        "note": "An empty catalogue result is not proof of no imagery; cross-check both catalogues, especially around the antimeridian.",
    }, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
