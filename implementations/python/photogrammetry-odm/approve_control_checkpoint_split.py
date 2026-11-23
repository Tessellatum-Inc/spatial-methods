#!/usr/bin/env python3
"""Create a formally approved control/checkpoint split from human sign-off.

The utility verifies evidence and explicit approval inputs. It does not make
the suitability decision, assess geometry itself, or infer reviewer approval.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path


APPROVED_REVIEW_STATUSES = {
    "single_reviewer_adjudication_locked",
    "multi_reviewer_adjudication_locked_not_independent",
}
REQUIRED_APPROVAL_FIELDS = (
    "decision", "approver", "approved_at_utc", "review_lock_sha256",
    "review_decisions_sha256", "geometry_assessment", "coverage_assessment",
    "control_checkpoint_separation_confirmed", "checkpoint_withholding_confirmed",
    "coordinate_reference_review_status", "approval_rationale",
)
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def parse_utc(value: str) -> str:
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError("approved_at_utc must be ISO 8601") from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ValueError("approved_at_utc must include a timezone offset")
    if parsed.utcoffset().total_seconds() != 0:
        raise ValueError("approved_at_utc must be UTC")
    return parsed.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def approve_split(
    proposed_split_json: str | Path,
    review_decisions_csv: str | Path,
    locked_review_json: str | Path,
    approval_json: str | Path,
    output_json: str | Path,
) -> dict:
    proposed_path = Path(proposed_split_json).expanduser().resolve()
    decisions_path = Path(review_decisions_csv).expanduser().resolve()
    lock_path = Path(locked_review_json).expanduser().resolve()
    approval_path = Path(approval_json).expanduser().resolve()
    output_path = Path(output_json).expanduser().resolve()
    if output_path in {proposed_path, decisions_path, lock_path, approval_path}:
        raise ValueError("Approved split output must not overwrite an input evidence file")

    proposed = json.loads(proposed_path.read_text(encoding="utf-8"))
    lock = json.loads(lock_path.read_text(encoding="utf-8"))
    approval = json.loads(approval_path.read_text(encoding="utf-8"))

    if proposed.get("status") != "proposed_not_locked":
        raise ValueError("Input partition must be the original proposed_not_locked split")
    if lock.get("status") not in APPROVED_REVIEW_STATUSES:
        raise ValueError("A valid locked role-blind review record is required")
    if lock.get("unblinded") is not False:
        raise ValueError("Review lock must remain unblinded:false")
    if lock.get("source_revision") != proposed.get("dataset", {}).get("resolved_revision"):
        raise ValueError("Review lock and proposed split refer to different source revisions")
    if lock.get("selected_dataset_path") != proposed.get("dataset", {}).get("selected_path"):
        raise ValueError("Review lock and proposed split refer to different dataset paths")

    lock_hash = sha256_file(lock_path)
    decisions_hash = sha256_file(decisions_path)
    if lock.get("review_decisions_sha256") != decisions_hash:
        raise ValueError("Review decision CSV hash does not match the locked review record")
    if lock.get("acquisition_manifest_sha256") != proposed.get("dataset", {}).get("acquisition_manifest_sha256"):
        raise ValueError("Locked review and proposed split acquisition-manifest hashes differ")

    missing = [field for field in REQUIRED_APPROVAL_FIELDS if field not in approval]
    if missing:
        raise ValueError("Human approval record is missing fields: " + ", ".join(missing))
    if approval["decision"] != "approve":
        raise ValueError("Human approval decision must explicitly be 'approve'")
    for field in ("approver", "approval_rationale"):
        if not str(approval[field]).strip():
            raise ValueError(f"Human approval field {field} must be non-empty")
    approved_at = parse_utc(str(approval["approved_at_utc"]))
    if approval["review_lock_sha256"] != lock_hash:
        raise ValueError("Human approval record references a different review lock")
    if approval["review_decisions_sha256"] != decisions_hash:
        raise ValueError("Human approval record references a different review worksheet")
    for field in ("geometry_assessment", "coverage_assessment"):
        if approval[field] != "acceptable":
            raise ValueError(f"{field} must be explicitly assessed as acceptable")
    for field in ("control_checkpoint_separation_confirmed", "checkpoint_withholding_confirmed"):
        if approval[field] is not True:
            raise ValueError(f"{field} must be explicitly true")
    if approval["coordinate_reference_review_status"] not in {
        "horizontal_and_vertical_semantics_documented_pending_processing_verification",
        "resolved_for_rehearsal",
    }:
        raise ValueError("Coordinate-reference review status must be an allowed explicit disposition")

    selection = proposed.get("selection", {})
    controls = {str(value) for value in selection.get("control_points", [])}
    checkpoints = {str(value) for value in selection.get("checkpoint_points", [])}
    excluded = {str(value) for value in selection.get("excluded_low_observation_points", {})}
    if not controls or not checkpoints:
        raise ValueError("Proposed split must contain controls and checkpoints")
    if controls & checkpoints or controls & excluded or checkpoints & excluded:
        raise ValueError("Control, checkpoint and excluded point sets must be disjoint")

    with decisions_path.open("r", newline="", encoding="utf-8-sig") as stream:
        reader = csv.DictReader(stream)
        required = {"point_id", "image_name", "decision"}
        if not required.issubset(reader.fieldnames or []):
            raise ValueError("Review decision CSV is missing point_id, image_name or decision")
        rows = list(reader)
    expected_count = lock.get("observation_count_expected")
    if len(rows) != expected_count or lock.get("observation_count_reviewed") != expected_count:
        raise ValueError("Review worksheet row count does not match the complete locked review")
    decisions_by_point = defaultdict(Counter)
    seen = set()
    for row_number, row in enumerate(rows, 2):
        point_id = str(row["point_id"]).strip()
        image_name = str(row["image_name"]).strip()
        key = (point_id, image_name)
        if not point_id or not image_name or key in seen:
            raise ValueError(f"Review worksheet row {row_number} has a blank or duplicate observation key")
        seen.add(key)
        decision = str(row["decision"]).strip().lower()
        if decision not in {"accepted", "questioned", "rejected"}:
            raise ValueError(f"Review worksheet row {row_number} has an invalid decision")
        decisions_by_point[point_id][decision] += 1

    if len(seen) != expected_count:
        raise ValueError("Review worksheet does not contain unique complete observation keys")
    for role, point_ids in (("control", controls), ("checkpoint", checkpoints)):
        for point_id in sorted(point_ids):
            counts = decisions_by_point.get(point_id, Counter())
            if not counts:
                raise ValueError(f"{role.title()} point {point_id} has no reviewed image observations")
            if counts["questioned"] or counts["rejected"]:
                raise ValueError(
                    f"{role.title()} point {point_id} has questioned/rejected observations; "
                    "revise or exclude it before approval"
                )
            if counts["accepted"] != sum(counts.values()):
                raise ValueError(f"{role.title()} point {point_id} is not fully accepted")

    result = dict(proposed)
    result["status"] = "approved_locked"
    result["approval"] = {
        "decision": "approve",
        "approver": str(approval["approver"]).strip(),
        "approved_at_utc": approved_at,
        "approval_rationale": str(approval["approval_rationale"]).strip(),
        "geometry_assessment": approval["geometry_assessment"],
        "coverage_assessment": approval["coverage_assessment"],
        "control_checkpoint_separation_confirmed": True,
        "checkpoint_withholding_confirmed": True,
        "coordinate_reference_review_status": approval["coordinate_reference_review_status"],
        "review_lock_sha256": lock_hash,
        "review_decisions_sha256": decisions_hash,
        "proposed_split_sha256": sha256_file(proposed_path),
        "accepted_observation_counts_by_role": {
            "control": {point: sum(decisions_by_point[point].values()) for point in sorted(controls)},
            "checkpoint": {point: sum(decisions_by_point[point].values()) for point in sorted(checkpoints)},
        },
        "limitations": [
            "Approval is a recorded human decision; this utility does not independently assess spatial geometry or coverage.",
            "The utility enforces accepted image-observation decisions for every selected control and checkpoint.",
            "The utility does not prove reviewer independence, survey accuracy or suitability of the source ground coordinates.",
            "Checkpoint image coordinates must still be independently remeasured from original unannotated images.",
            "This approval does not authorize controlled-GCP processing until the coordinate-reference and implementation gates are satisfied.",
        ],
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate human sign-off and lock the HEIG-VD point partition.")
    parser.add_argument("proposed_split_json", type=Path)
    parser.add_argument("review_decisions_csv", type=Path)
    parser.add_argument("locked_review_json", type=Path)
    parser.add_argument("human_approval_json", type=Path)
    parser.add_argument("output_json", type=Path)
    args = parser.parse_args(argv)
    try:
        report = approve_split(
            args.proposed_split_json, args.review_decisions_csv,
            args.locked_review_json, args.human_approval_json, args.output_json,
        )
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        parser.error(str(exc))
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
