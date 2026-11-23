#!/usr/bin/env python3
"""Validate and lock a completed role-blind image-observation review.

This utility does not read the control/checkpoint split. It locks reviewer
decisions while preserving the role-blind boundary.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path


REQUIRED_FIELDS = (
    "point_id", "image_name", "pixel_x", "pixel_y",
    "target_visible", "target_identity_clear", "marker_centred",
    "blur", "occlusion", "ambiguity", "decision", "rationale",
    "reviewer", "reviewed_at",
)
VALID_DECISIONS = {"accepted", "questioned", "rejected"}
VALID_YES_NO_UNCERTAIN = {"yes", "no", "uncertain"}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _parse_timestamp(value: str, row_number: int) -> None:
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError(f"Row {row_number}: reviewed_at must be ISO 8601") from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ValueError(f"Row {row_number}: reviewed_at must include a timezone offset")


def lock_review(
    decisions_csv: str | Path,
    visual_summary_json: str | Path,
    acquisition_manifest_json: str | Path,
    output_json: str | Path,
) -> dict:
    decisions_path = Path(decisions_csv).expanduser().resolve()
    summary_path = Path(visual_summary_json).expanduser().resolve()
    manifest_path = Path(acquisition_manifest_json).expanduser().resolve()
    output_path = Path(output_json).expanduser().resolve()

    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    expected_count = summary.get("observation_count")
    if not isinstance(expected_count, int) or expected_count < 1:
        raise ValueError("Visual-review summary must declare a positive observation_count")
    if not str(summary.get("status", "")).startswith("role_blind_"):
        raise ValueError("Review summary is not marked as role-blind")
    if summary.get("source_revision") != manifest.get("resolved_revision"):
        raise ValueError("Review summary source revision does not match acquisition manifest")
    if summary.get("selected_dataset_path") != manifest.get("selected_path"):
        raise ValueError("Review summary selected dataset path does not match acquisition manifest")
    source_observations = summary.get("source_observations")
    if not isinstance(source_observations, list) or len(source_observations) != expected_count:
        raise ValueError("Review summary must include the complete source_observations index")
    expected_observations = {}
    for item in source_observations:
        key = (str(item.get("point_id", "")), str(item.get("image_name", "")))
        if not all(key) or key in expected_observations:
            raise ValueError("Source observation index contains blank or duplicate point/image keys")
        expected_observations[key] = (
            float(item["pixel_x"]), float(item["pixel_y"])
        )

    if output_path in {decisions_path, summary_path, manifest_path}:
        raise ValueError("Locked review output must not overwrite an input evidence file")

    with decisions_path.open("r", newline="", encoding="utf-8-sig") as stream:
        reader = csv.DictReader(stream)
        fields = reader.fieldnames or []
        missing = [field for field in REQUIRED_FIELDS if field not in fields]
        if missing:
            raise ValueError("Review worksheet is missing columns: " + ", ".join(missing))
        rows = list(reader)

    if len(rows) != expected_count:
        raise ValueError(
            f"Expected {expected_count} observation decisions; found {len(rows)}"
        )

    seen = set()
    decisions = Counter()
    reviewers = set()
    point_ids = set()
    for row_number, row in enumerate(rows, 2):
        missing_values = [
            field for field in REQUIRED_FIELDS
            if not isinstance(row.get(field), str) or not row[field].strip()
        ]
        if missing_values:
            raise ValueError(
                f"Row {row_number}: blank required values: " + ", ".join(missing_values)
            )
        point_id = row["point_id"].strip()
        image_name = row["image_name"].strip()
        key = (point_id, image_name)
        if key in seen:
            raise ValueError(
                f"Row {row_number}: duplicate observation decision for {point_id}/{image_name}"
            )
        if key not in expected_observations:
            raise ValueError(
                f"Row {row_number}: point/image pair is absent from source observation index"
            )
        seen.add(key)
        try:
            pixel_x, pixel_y = float(row["pixel_x"]), float(row["pixel_y"])
        except ValueError as exc:
            raise ValueError(f"Row {row_number}: pixel coordinates must be numeric") from exc
        if not all(math.isfinite(value) and value >= 0 for value in (pixel_x, pixel_y)):
            raise ValueError(f"Row {row_number}: pixel coordinates must be finite and non-negative")
        expected_x, expected_y = expected_observations[key]
        if abs(pixel_x - expected_x) > 1e-3 or abs(pixel_y - expected_y) > 1e-3:
            raise ValueError(f"Row {row_number}: source pixel coordinates were altered")
        for field in ("target_visible", "target_identity_clear", "marker_centred"):
            if row[field].strip().lower() not in VALID_YES_NO_UNCERTAIN:
                raise ValueError(
                    f"Row {row_number}: {field} must be yes, no or uncertain"
                )
        decision = row["decision"].strip().lower()
        if decision not in VALID_DECISIONS:
            raise ValueError(
                f"Row {row_number}: decision must be accepted, questioned or rejected"
            )
        _parse_timestamp(row["reviewed_at"].strip(), row_number)
        decisions[decision] += 1
        reviewers.add(row["reviewer"].strip())
        point_ids.add(point_id)

    if seen != set(expected_observations):
        raise ValueError("Review worksheet does not cover every source observation")
    reviewer_list = sorted(reviewers)
    if len(reviewer_list) == 1:
        adjudication_status = "single_reviewer_adjudication_locked"
    else:
        adjudication_status = "multi_reviewer_adjudication_locked_not_independent"

    output_path.parent.mkdir(parents=True, exist_ok=True)
    report = {
        "schema_version": "1.0",
        "status": adjudication_status,
        "locked_at_utc": datetime.now(timezone.utc).isoformat(),
        "source_revision": manifest.get("resolved_revision"),
        "selected_dataset_path": manifest.get("selected_path"),
        "observation_count_expected": expected_count,
        "observation_count_reviewed": len(rows),
        "unique_point_count_reviewed": len(point_ids),
        "reviewer_count": len(reviewer_list),
        "reviewers": reviewer_list,
        "decision_counts": dict(sorted(decisions.items())),
        "review_decisions_sha256": sha256_file(decisions_path),
        "visual_review_summary_sha256": sha256_file(summary_path),
        "acquisition_manifest_sha256": sha256_file(manifest_path),
        "source_observation_index_sha256": hashlib.sha256(
            json.dumps(source_observations, sort_keys=True, separators=(",", ":")).encode("utf-8")
        ).hexdigest(),
        "unblinded": False,
        "independent_validation": False,
        "limitations": [
            "This record locks review of source-provided Metashape image picks; it does not establish survey accuracy.",
            "A single reviewer is recorded as single-reviewer adjudication, not independent validation.",
            "Multiple reviewer names do not prove independent review; this tool does not establish reviewer independence.",
            "The control/checkpoint split is not read or disclosed by this utility.",
            "A separate post-lock unblinding and validation process is required before role-specific analysis.",
        ],
    }
    output_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate and lock a completed role-blind observation review worksheet."
    )
    parser.add_argument("decisions_csv", type=Path)
    parser.add_argument("visual_summary_json", type=Path)
    parser.add_argument("acquisition_manifest_json", type=Path)
    parser.add_argument("output_json", type=Path)
    args = parser.parse_args(argv)
    try:
        report = lock_review(
            args.decisions_csv, args.visual_summary_json,
            args.acquisition_manifest_json, args.output_json,
        )
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        parser.error(str(exc))
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
