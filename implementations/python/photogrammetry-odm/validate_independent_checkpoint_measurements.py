#!/usr/bin/env python3
"""Validate independently remeasured checkpoint image coordinates and provenance.

This validator checks records and source-image identity. It does not prove that
measurements were made independently, that a target was identified correctly,
or that any ground-coordinate reference is accurate.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


REQUIRED_FIELDS = (
    "point_id", "image", "measurement_status", "independent_pixel_x",
    "independent_pixel_y", "measurement_method", "reviewer",
    "measured_at_utc", "source_image_sha256", "measurement_notes",
)
SHA256_RE = re.compile(r"^[0-9a-fA-F]{64}$")
APPROVED_SPLIT_STATUSES = {"approved", "locked", "approved_locked"}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _utc_timestamp(value: str, row_number: int) -> str:
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError(f"Row {row_number}: measured_at_utc must be ISO 8601") from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ValueError(f"Row {row_number}: measured_at_utc must include a UTC offset")
    if parsed.utcoffset().total_seconds() != 0:
        raise ValueError(f"Row {row_number}: measured_at_utc must be recorded in UTC")
    return parsed.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def _manifest_images(manifest: dict[str, Any]) -> dict[str, str]:
    files = manifest.get("files")
    if not isinstance(files, list):
        raise ValueError("Acquisition manifest must contain a files list")
    images: dict[str, str] = {}
    for item in files:
        if not isinstance(item, dict):
            continue
        path = str(item.get("path", ""))
        digest = str(item.get("sha256", "")).lower()
        name = Path(path).name
        if not name.lower().endswith((".jpg", ".jpeg", ".tif", ".tiff", ".png")):
            continue
        if not SHA256_RE.fullmatch(digest):
            raise ValueError(f"Acquisition manifest has an invalid image SHA-256 for {path!r}")
        if name in images and images[name] != digest:
            raise ValueError(f"Acquisition manifest has ambiguous image basename {name!r}")
        images[name] = digest
    if not images:
        raise ValueError("Acquisition manifest contains no supported source images")
    return images


def validate_measurements(
    measurements_csv: str | Path,
    approved_split_json: str | Path,
    acquisition_manifest_json: str | Path,
    visual_summary_json: str | Path,
    output_json: str | Path | None = None,
) -> dict:
    csv_path = Path(measurements_csv).expanduser().resolve()
    split_path = Path(approved_split_json).expanduser().resolve()
    manifest_path = Path(acquisition_manifest_json).expanduser().resolve()
    summary_path = Path(visual_summary_json).expanduser().resolve()

    split = json.loads(split_path.read_text(encoding="utf-8"))
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    summary = json.loads(summary_path.read_text(encoding="utf-8"))

    if split.get("status") not in APPROVED_SPLIT_STATUSES:
        raise ValueError("Split must have an explicitly approved/locked status; proposed splits are rejected")
    selection = split.get("selection")
    if not isinstance(selection, dict):
        raise ValueError("Approved split must contain selection.checkpoint_points")
    checkpoint_ids = {str(value) for value in selection.get("checkpoint_points", [])}
    control_ids = {str(value) for value in selection.get("control_points", [])}
    if not checkpoint_ids:
        raise ValueError("Approved split contains no checkpoint point IDs")
    if checkpoint_ids & control_ids:
        raise ValueError("Approved split assigns one or more points as both controls and checkpoints")

    dataset = split.get("dataset", {})
    manifest_revision = manifest.get("resolved_revision")
    manifest_path_value = manifest.get("selected_path")
    if dataset.get("resolved_revision") != manifest_revision:
        raise ValueError("Approved split source revision does not match acquisition manifest")
    if dataset.get("selected_path") != manifest_path_value:
        raise ValueError("Approved split dataset path does not match acquisition manifest")
    manifest_hash = sha256_file(manifest_path)
    declared_manifest_hash = dataset.get("acquisition_manifest_sha256")
    if declared_manifest_hash and declared_manifest_hash != manifest_hash:
        raise ValueError("Approved split acquisition-manifest hash does not match supplied manifest")

    if summary.get("source_revision") != manifest_revision:
        raise ValueError("Visual-review summary source revision does not match acquisition manifest")
    if summary.get("selected_dataset_path") != manifest_path_value:
        raise ValueError("Visual-review summary dataset path does not match acquisition manifest")
    source_observations = summary.get("source_observations")
    if not isinstance(source_observations, list):
        raise ValueError("Visual-review summary must include source_observations")
    allowed_pairs = {
        (str(item.get("point_id", "")), Path(str(item.get("image_name", ""))).name)
        for item in source_observations
    }
    allowed_pairs = {pair for pair in allowed_pairs if all(pair)}
    if not allowed_pairs:
        raise ValueError("Visual-review summary contains no usable source observation keys")

    source_images = _manifest_images(manifest)
    with csv_path.open("r", newline="", encoding="utf-8-sig") as stream:
        reader = csv.DictReader(stream)
        fields = reader.fieldnames or []
        missing = [field for field in REQUIRED_FIELDS if field not in fields]
        if missing:
            raise ValueError("Measurement CSV is missing columns: " + ", ".join(missing))
        rows = list(reader)
    if not rows:
        raise ValueError("Measurement CSV contains no records")

    seen: set[tuple[str, str]] = set()
    measured_points: set[str] = set()
    row_statuses: Counter[str] = Counter()
    reviewer_names: set[str] = set()
    normalized_rows = []
    for row_number, row in enumerate(rows, 2):
        blanks = [field for field in REQUIRED_FIELDS if not (row.get(field) or "").strip()]
        # Coordinates and notes may be blank for a measured row; an
        # unmeasurable row must provide a reason below.
        blanks = [field for field in blanks if field not in {
            "independent_pixel_x", "independent_pixel_y", "measurement_notes"
        }]
        if blanks:
            raise ValueError(f"Row {row_number}: blank required values: " + ", ".join(blanks))
        point_id = row["point_id"].strip()
        image_name = Path(row["image"].strip()).name
        pair = (point_id, image_name)
        if pair in seen:
            raise ValueError(f"Row {row_number}: duplicate point/image measurement {point_id}/{image_name}")
        seen.add(pair)
        if point_id not in checkpoint_ids:
            if point_id in control_ids:
                raise ValueError(f"Row {row_number}: control point {point_id} is not an independent checkpoint")
            raise ValueError(f"Row {row_number}: point {point_id} is not in the approved checkpoint set")
        if pair not in allowed_pairs:
            raise ValueError(f"Row {row_number}: point/image pair is absent from source observation index")
        if image_name not in source_images:
            raise ValueError(f"Row {row_number}: source image {image_name!r} is absent from acquisition manifest")
        digest = row["source_image_sha256"].strip().lower()
        if not SHA256_RE.fullmatch(digest):
            raise ValueError(f"Row {row_number}: source_image_sha256 must be 64 hexadecimal characters")
        if digest != source_images[image_name]:
            raise ValueError(f"Row {row_number}: source image SHA-256 does not match acquisition manifest")
        status = row["measurement_status"].strip().lower()
        if status not in {"measured", "unmeasurable"}:
            raise ValueError(f"Row {row_number}: measurement_status must be measured or unmeasurable")
        x_text = row["independent_pixel_x"].strip()
        y_text = row["independent_pixel_y"].strip()
        if status == "measured":
            if not x_text or not y_text:
                raise ValueError(f"Row {row_number}: measured records require both pixel coordinates")
            try:
                x, y = float(x_text), float(y_text)
            except ValueError as exc:
                raise ValueError(f"Row {row_number}: pixel coordinates must be numeric") from exc
            if not all(math.isfinite(v) and v >= 0 for v in (x, y)):
                raise ValueError(f"Row {row_number}: pixel coordinates must be finite and non-negative")
            measured_points.add(point_id)
        elif x_text or y_text:
            raise ValueError(f"Row {row_number}: unmeasurable records must leave both pixel coordinates blank")
        elif not row["measurement_notes"].strip():
            raise ValueError(f"Row {row_number}: unmeasurable records require a reason in measurement_notes")
        _utc_timestamp(row["measured_at_utc"].strip(), row_number)
        reviewer_names.add(row["reviewer"].strip())
        row_statuses[status] += 1
        normalized_rows.append({
            "point_id": point_id, "image": image_name, "measurement_status": status,
            "independent_pixel_x": float(x_text) if x_text else None,
            "independent_pixel_y": float(y_text) if y_text else None,
            "reviewer": row["reviewer"].strip(),
        })

    missing_points = sorted(checkpoint_ids - measured_points)
    if missing_points:
        raise ValueError(
            "Every approved checkpoint must have at least one measured image observation; missing: "
            + ", ".join(missing_points)
        )
    expected_checkpoint_pairs = {
        pair for pair in allowed_pairs if pair[0] in checkpoint_ids
    }
    missing_pairs = sorted(expected_checkpoint_pairs - seen)
    if missing_pairs:
        rendered = ", ".join(f"{point}/{image}" for point, image in missing_pairs)
        raise ValueError(
            "Measurement register must account for every checkpoint source observation "
            "(measured or explicitly unmeasurable); missing: " + rendered
        )

    report = {
        "schema_version": "1.0",
        "status": "record_structure_and_provenance_validated",
        "validated_at_utc": datetime.now(timezone.utc).isoformat(),
        "dataset_revision": manifest_revision,
        "selected_dataset_path": manifest_path_value,
        "approved_split_sha256": sha256_file(split_path),
        "acquisition_manifest_sha256": manifest_hash,
        "visual_review_summary_sha256": sha256_file(summary_path),
        "measurement_csv_sha256": sha256_file(csv_path),
        "approved_checkpoint_count": len(checkpoint_ids),
        "checkpoint_count_with_measured_observations": len(measured_points),
        "measurement_row_count": len(rows),
        "measurement_status_counts": dict(sorted(row_statuses.items())),
        "reviewer_names": sorted(reviewer_names),
        "independent_measurement_independence_proven": False,
        "target_identity_proven": False,
        "accuracy_assessment_performed": False,
        "limitations": [
            "This validator checks record structure, point membership, source-image hashes and observation-key membership only.",
            "It does not prove that the reviewer measured independently or avoided consulting publisher measurements.",
            "It does not prove physical target identity, centring quality, measurement precision or reviewer competence.",
            "It does not establish ground-coordinate reference quality, CRS compatibility or photogrammetric accuracy.",
            "A structurally valid record is not human approval or an accuracy acceptance decision.",
        ],
    }
    if output_json is not None:
        out = Path(output_json).expanduser().resolve()
        if out in {csv_path, split_path, manifest_path, summary_path}:
            raise ValueError("Validation output must not overwrite an input evidence file")
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate independent checkpoint image-measurement records and provenance."
    )
    parser.add_argument("measurements_csv", type=Path)
    parser.add_argument("approved_split_json", type=Path)
    parser.add_argument("acquisition_manifest_json", type=Path)
    parser.add_argument("visual_summary_json", type=Path)
    parser.add_argument("--json-out", type=Path)
    args = parser.parse_args(argv)
    try:
        report = validate_measurements(
            args.measurements_csv, args.approved_split_json,
            args.acquisition_manifest_json, args.visual_summary_json,
            args.json_out,
        )
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        parser.error(str(exc))
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
