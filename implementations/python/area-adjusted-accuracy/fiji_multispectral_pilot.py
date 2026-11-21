#!/usr/bin/env python3
"""Run a bounded, blind five-point Sentinel-2 multispectral feasibility pilot.

This runner retrieves only point-centred windows from public Earth Search assets.
It writes metadata and numeric summaries, not class predictions or review labels.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from datetime import datetime
from collections import Counter
from pathlib import Path
from typing import Any

import numpy as np

from multispectral_metrics import (
    apply_valid_mask,
    index_stack,
    scl_valid_mask,
    scl_quality_summary,
    summarize_window,
)
from multispectral_raster import BAND_ALIASES, BAND_GRID, read_multispectral_windows
from stac_imagery_review import (
    EARTH_SEARCH,
    EARTH_COLLECTIONS,
    item_cloud,
    acquisition,
    search_catalogue,
)

PILOT_BANDS = tuple(BAND_ALIASES)


def _safe_float(value: Any, default: float = 100.0) -> float:
    try:
        result = float(value)
        return result if np.isfinite(result) else default
    except (TypeError, ValueError):
        return default


def _acquisition_key(item: dict[str, Any]) -> tuple[str, str]:
    """Normalize cross-catalogue records for one platform acquisition to seconds."""
    stamp = acquisition(item)
    if not stamp:
        return ("item", str(item.get("id", "")))
    try:
        normalized = datetime.fromisoformat(
            stamp.replace("Z", "+00:00")
        ).replace(microsecond=0).isoformat()
    except ValueError:
        normalized = stamp
    platform = str(item.get("properties", {}).get("platform", ""))
    return (platform, normalized)


def _asset_access_score(item: dict[str, Any]) -> tuple[int, int, int]:
    """Prefer representations with usable public band assets over private S3 aliases."""
    https = 0
    public_cogs = 0
    restricted_s3 = 0
    for asset in item.get("assets", {}).values():
        href = str(asset.get("href", ""))
        if href.startswith(("https://", "http://")):
            https += 1
        elif href.startswith("s3://sentinel-cogs/"):
            public_cogs += 1
        elif href.startswith("s3://"):
            restricted_s3 += 1
    return (https + public_cogs, https, -restricted_s3)


def deduplicate_acquisitions(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Keep the most publicly readable STAC representation per platform acquisition.

    Different catalogues can describe the same overpass but expose different
    asset URLs. Prefer the representation with the most HTTP(S) or known-public
    sentinel-cogs assets so deduplication does not discard the usable copy.
    """
    unique_by_key: dict[tuple[str, str], dict[str, Any]] = {}
    for item in items:
        key = _acquisition_key(item)
        current = unique_by_key.get(key)
        if current is None or _asset_access_score(item) > _asset_access_score(current):
            unique_by_key[key] = item
    return list(unique_by_key.values())


def _index_summaries(bands: dict[str, np.ndarray]) -> dict[str, dict[str, Any]]:
    """Summarize only indices whose inputs are present and grid-compatible."""
    summaries: dict[str, dict[str, Any]] = {}
    if "B04" in bands and "B08" in bands:
        try:
            ndvi = index_stack({"B04": bands["B04"], "B08": bands["B08"]}).get("NDVI")
            if ndvi is not None:
                summaries["NDVI_10m_unmasked"] = summarize_window(ndvi)
        except (ValueError, TypeError):
            pass
    if "B05" in bands and "B8A" in bands:
        try:
            ndre = index_stack({"B05": bands["B05"], "B8A": bands["B8A"]}).get("NDRE")
            if ndre is not None:
                summaries["NDRE_20m_unmasked"] = summarize_window(ndre)
                if "SCL" in bands:
                    ndre_scl = apply_valid_mask(ndre, scl_valid_mask(bands["SCL"]))
                    summaries["NDRE_20m_scl_valid"] = summarize_window(ndre_scl)
                else:
                    summaries["NDRE_20m_scl_valid"] = {"status": "not_available_no_scl"}
        except (ValueError, TypeError):
            pass
    return summaries


def run_pilot(input_csv: Path, output_dir: Path, *, point_limit: int = 5,
              item_limit: int = 3, window_pixels: int = 16) -> dict[str, Any]:
    if point_limit < 1 or item_limit < 1:
        raise ValueError("point_limit and item_limit must be positive")
    with input_csv.open(newline="", encoding="utf-8-sig") as stream:
        reader = csv.DictReader(stream)
        points = list(reader)
        fields = set(reader.fieldnames or [])
    required = {"sample_id", "longitude", "latitude"}
    if not points or not required.issubset(fields):
        raise ValueError(f"Input CSV must contain rows and columns: {sorted(required)}")
    points = points[:point_limit]
    output_dir.mkdir(parents=True, exist_ok=True)

    rows: list[dict[str, Any]] = []
    errors: list[dict[str, str]] = []
    candidate_items_found = 0
    unique_acquisitions_found = 0
    duplicate_acquisitions_skipped = 0
    for point in points:
        sample_id = str(point["sample_id"]).strip()
        lon, lat = float(point["longitude"]), float(point["latitude"])
        if not (-180 <= lon <= 180 and -90 <= lat <= 90):
            errors.append({"sample_id": sample_id, "error": "Invalid WGS84 coordinates"})
            continue

        items, search_errors = search_catalogue(
            EARTH_SEARCH, EARTH_COLLECTIONS, lon, lat
        )
        for message in search_errors:
            errors.append({"sample_id": sample_id, "error": message})
        candidate_items_found += len(items)
        items.sort(key=lambda item: (item_cloud(item), acquisition(item)))
        unique_items = deduplicate_acquisitions(items)
        unique_acquisitions_found += len(unique_items)
        duplicate_acquisitions_skipped += len(items) - len(unique_items)
        if not unique_items:
            rows.append({
                "sample_id": sample_id, "item_id": "", "datetime": "",
                "cloud_cover_percent": "", "status": "no_items",
                "bands_read": "", "missing_bands": json.dumps(list(PILOT_BANDS)),
                "indices": "{}", "band_summaries": "{}",
                "notes": "No Earth Search items returned; this does not prove no imagery exists.",
            })
            continue

        for rank, item in enumerate(unique_items[:item_limit], start=1):
            base: dict[str, Any] = {
                "sample_id": sample_id,
                "item_id": item.get("id", ""),
                "collection": item.get("collection", ""),
                "datetime": acquisition(item),
                "cloud_cover_percent": item_cloud(item),
                "platform": item.get("properties", {}).get("platform", ""),
                "status": "read_failed",
                "bands_read": "",
                "missing_bands": "",
                "native_grids": "",
                "indices": "{}",
                "band_summaries": "{}",
                "provenance": "{}",
                "notes": "",
            }
            try:
                result = read_multispectral_windows(
                    item, lon, lat, bands=PILOT_BANDS,
                    window_pixels=window_pixels,
                )
                band_summaries = {
                    band: summarize_window(array)
                    for band, array in result["bands"].items()
                }
                index_summaries = _index_summaries(result["bands"])
                if "SCL" in result["bands"]:
                    index_summaries["SCL_QA_20m"] = scl_quality_summary(result["bands"]["SCL"])
                # Hash a canonical summary/provenance payload; no raster pixels
                # or signed asset query parameters are written to the report.
                provenance = {
                    "item_id": result["item_id"],
                    "collection": result["collection"],
                    "datetime": result["datetime"],
                    "longitude": lon,
                    "latitude": lat,
                    "window_pixels": window_pixels,
                    "bands": {
                        band: {
                            key: value for key, value in meta.items()
                            if key != "href"
                        }
                        for band, meta in result["band_metadata"].items()
                    },
                }
                payload = json.dumps(
                    {"provenance": provenance, "bands": band_summaries,
                     "indices": index_summaries},
                    sort_keys=True, default=str,
                ).encode("utf-8")
                core_bands = {"B02", "B03", "B04", "B08"}
                core_complete = core_bands.issubset(result["bands"])
                base.update({
                    "status": (
                        "core_bands_read" if core_complete
                        else "partial_bands_read" if result["bands"]
                        else "no_assets_read"
                    ),
                    "bands_read": json.dumps(sorted(result["bands"])),
                    "missing_bands": json.dumps(result["missing_bands"]),
                    "native_grids": json.dumps(result["native_grids"]),
                    "indices": json.dumps(index_summaries, sort_keys=True),
                    "band_summaries": json.dumps(band_summaries, sort_keys=True),
                    "provenance": json.dumps(provenance, sort_keys=True, default=str),
                    "sha256": hashlib.sha256(payload).hexdigest(),
                    "notes": (
                        "Indices are calculated only within matching native-grid groups. "
                        "No class labels or predictions are produced."
                    ),
                })
            except Exception as exc:
                base["notes"] = f"{type(exc).__name__}: {exc}"
            rows.append(base)

    provenance_path = output_dir / "fiji-multispectral-pilot.csv"
    fields_out = [
        "sample_id", "item_id", "collection", "datetime",
        "cloud_cover_percent", "platform", "status", "bands_read",
        "missing_bands", "native_grids", "indices", "band_summaries",
        "provenance", "sha256", "notes",
    ]
    with provenance_path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields_out)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields_out})

    errors_path = output_dir / "fiji-multispectral-search-errors.csv"
    if errors:
        with errors_path.open("w", newline="", encoding="utf-8") as stream:
            writer = csv.DictWriter(stream, fieldnames=["sample_id", "error"])
            writer.writeheader()
            writer.writerows(errors)
    else:
        errors_path.unlink(missing_ok=True)

    statuses = Counter(row["status"] for row in rows)
    points_with_core_read = {
        row["sample_id"] for row in rows
        if row["status"] == "core_bands_read"
    }
    return {
        "points_requested": len(points),
        "candidate_items_found": candidate_items_found,
        "unique_acquisitions_found": unique_acquisitions_found,
        "duplicate_acquisitions_skipped": duplicate_acquisitions_skipped,
        "candidate_rows": len(rows),
        "points_with_core_10m_bands": len(points_with_core_read),
        "statuses": dict(statuses),
        "search_errors": len(errors),
        "provenance_csv": str(provenance_path),
        "errors_csv": str(errors_path) if errors else None,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input",
        default="data/fiji-worldcover-legend-adjudication-blind-review.csv",
    )
    parser.add_argument("--output-dir", default="/tmp/fiji-multispectral-pilot")
    parser.add_argument("--points", type=int, default=5)
    parser.add_argument("--items-per-point", type=int, default=3)
    parser.add_argument("--window-pixels", type=int, default=32)
    args = parser.parse_args()
    result = run_pilot(
        Path(args.input), Path(args.output_dir),
        point_limit=args.points, item_limit=args.items_per_point,
        window_pixels=args.window_pixels,
    )
    print(json.dumps(result, indent=2))
    # A green run means all requested blind points had at least one candidate
    # with the four co-registered 10 m visible/NIR bands. Partial evidence is
    # still retained as an artifact for diagnosis.
    return 0 if result["points_with_core_10m_bands"] == result["points_requested"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
