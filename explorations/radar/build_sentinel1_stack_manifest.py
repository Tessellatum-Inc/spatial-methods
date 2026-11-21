#!/usr/bin/env python3
"""Build a cautious, reproducible candidate manifest from the Nairobi S1 inventory.

This is catalogue-level selection only. It does not make products analysis-ready.
"""
from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sys
import uuid

DEFAULT_INPUT = Path("explorations/radar/nairobi-sentinel-1-catalogue-inventory.csv")
DEFAULT_OUTPUT = Path("explorations/radar/nairobi-sentinel-1-stack-manifest.json")
REQUIRED_COLUMNS = {
    "product_id", "product_name", "sensing_start_utc", "orbit_direction",
    "relative_orbit", "platform", "polarisation_channels", "product_composition",
    "slice_number", "total_slices", "online", "covers_study_aoi",
}


def parse_bool(value: str, field: str, row_number: int) -> bool:
    normalized = value.strip().lower()
    if normalized not in {"true", "false"}:
        raise ValueError(f"Row {row_number}: {field} must be True or False.")
    return normalized == "true"


def load_inventory(path: Path) -> tuple[list[dict], str]:
    raw = path.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    try:
        text = raw.decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        raise ValueError("Inventory must be UTF-8 CSV.") from exc
    reader = csv.DictReader(text.splitlines())
    if reader.fieldnames is None:
        raise ValueError("Inventory CSV has no header.")
    missing = REQUIRED_COLUMNS.difference(reader.fieldnames)
    if missing:
        raise ValueError(f"Inventory is missing required columns: {', '.join(sorted(missing))}")

    rows = []
    seen_ids = set()
    for row_number, row in enumerate(reader, start=2):
        product_id = (row.get("product_id") or "").strip()
        try:
            parsed_id = str(uuid.UUID(product_id))
        except (ValueError, AttributeError) as exc:
            raise ValueError(f"Row {row_number}: product_id must be a UUID.") from exc
        if parsed_id != product_id.lower():
            raise ValueError(f"Row {row_number}: product_id must use canonical UUID format.")
        if product_id in seen_ids:
            raise ValueError(f"Row {row_number}: duplicate product_id {product_id}.")
        seen_ids.add(product_id)

        try:
            acquired = datetime.fromisoformat(
                row["sensing_start_utc"].replace("Z", "+00:00")
            )
        except (ValueError, AttributeError) as exc:
            raise ValueError(f"Row {row_number}: invalid sensing_start_utc.") from exc
        if acquired.tzinfo is None or acquired.utcoffset() is None:
            raise ValueError(f"Row {row_number}: sensing_start_utc needs a timezone.")
        if acquired.utcoffset().total_seconds() != 0:
            raise ValueError(f"Row {row_number}: sensing_start_utc must be UTC.")

        for field in ("relative_orbit", "slice_number", "total_slices"):
            try:
                row[field] = int(row[field])
            except (ValueError, TypeError):
                raise ValueError(f"Row {row_number}: {field} must be an integer.")
            if row[field] < 1:
                raise ValueError(f"Row {row_number}: {field} must be positive.")

        row["online"] = parse_bool(row["online"], "online", row_number)
        row["covers_study_aoi"] = parse_bool(
            row["covers_study_aoi"], "covers_study_aoi", row_number
        )
        row["_acquired"] = acquired.astimezone(timezone.utc)
        rows.append(row)
    if not rows:
        raise ValueError("Inventory contains no product rows.")
    return rows, digest


def build_manifest(rows: list[dict], source_sha256: str) -> dict:
    criteria = {
        "product_family": "Sentinel-1 IW GRD",
        "platform": "C",
        "orbit_direction": "DESCENDING",
        "relative_orbit": 79,
        "polarisation_channels": "VV&VH",
        "online": True,
        "covers_study_aoi": True,
    }
    eligible = []
    excluded = []
    for row in rows:
        reasons = []
        if not row["product_name"].startswith("S1C_IW_GRDH_"):
            reasons.append("not Sentinel-1C IW GRD")
        if row["platform"] != criteria["platform"]:
            reasons.append("platform differs from Sentinel-1C")
        if row["orbit_direction"] != criteria["orbit_direction"]:
            reasons.append("orbit direction differs")
        if row["relative_orbit"] != criteria["relative_orbit"]:
            reasons.append("relative orbit differs")
        if row["polarisation_channels"] != criteria["polarisation_channels"]:
            reasons.append("dual VV/VH metadata requirement not met")
        if not row["online"]:
            reasons.append("catalogue does not report product online")
        if not row["covers_study_aoi"]:
            reasons.append("catalogue footprint audit does not cover study AOI")
        if row["product_composition"].lower() != "slice":
            reasons.append("product composition is not a slice")
        item = {
            "product_id": row["product_id"],
            "product_name": row["product_name"],
            "sensing_start_utc": row["sensing_start_utc"],
            "platform": row["platform"],
            "orbit_direction": row["orbit_direction"],
            "relative_orbit": row["relative_orbit"],
            "polarisation_channels": row["polarisation_channels"],
            "slice_number": row["slice_number"],
            "total_slices": row["total_slices"],
            "online": row["online"],
            "covers_study_aoi": row["covers_study_aoi"],
            "location_formats": row.get("location_formats", ""),
            "download_links": [
                link for link in (row.get("download_links") or "").split(";") if link
            ],
            "catalogue_selection_status": "candidate" if not reasons else "excluded",
            "exclusion_reasons": reasons,
            "analysis_ready": False,
            "analysis_readiness_note": (
                "Catalogue metadata only; download, SAFE, channel, processing and QA gates remain."
            ),
        }
        if not reasons:
            eligible.append(item)
        else:
            excluded.append(item)

    eligible.sort(key=lambda item: item["sensing_start_utc"])
    intervals_days = []
    for previous, current in zip(eligible, eligible[1:]):
        before = datetime.fromisoformat(previous["sensing_start_utc"].replace("Z", "+00:00"))
        after = datetime.fromisoformat(current["sensing_start_utc"].replace("Z", "+00:00"))
        intervals_days.append((after - before).total_seconds() / 86400)

    return {
        "manifest_schema": "tessellatum.sentinel1.stack-manifest.v1",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z"),
        "source_inventory": str(DEFAULT_INPUT.as_posix()),
        "source_inventory_sha256": source_sha256,
        "study_area": "Nairobi rectangular discovery AOI; see scene record for coordinates and limitations",
        "selection_criteria": criteria,
        "candidate_count": len(eligible),
        "inventory_row_count": len(rows),
        "candidate_acquisition_intervals_days": intervals_days,
        "stack_status": "catalogue_candidates_only" if eligible else "no_matching_candidates",
        "processing_status": "not_started",
        "analysis_ready": False,
        "critical_limitations": [
            "Catalogue coverage audit applies to the defined rectangular AOI, not an official Nairobi boundary.",
            "Each candidate is a slice product; the slice is not the complete datatake.",
            "Catalogue channel metadata does not replace inspection of SAFE measurement files.",
            "No candidate is analysis-ready until download, archive, metadata, processing and QA gates pass.",
            "Common orbit and nominal 12-day cadence do not prove radiometric or temporal interchangeability.",
        ],
        "candidates": eligible,
        "excluded_inventory_records": excluded,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args(argv)
    try:
        rows, digest = load_inventory(args.input)
        manifest = build_manifest(rows, digest)
    except (OSError, ValueError) as exc:
        print(f"Cannot build Sentinel-1 stack manifest: {exc}", file=sys.stderr)
        return 2
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Inventory rows: {manifest['inventory_row_count']}")
    print(f"Catalogue candidates: {manifest['candidate_count']}")
    print(f"Manifest: {args.output}")
    print("Status: catalogue candidates only; no product is analysis-ready.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
