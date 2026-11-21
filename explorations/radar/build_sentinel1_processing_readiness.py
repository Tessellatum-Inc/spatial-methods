#!/usr/bin/env python3
"""Reconcile catalogue, download and SAFE audit evidence into a readiness record.

A passed structural preflight is necessary but never sufficient to authorize
scientific processing. This tool deliberately leaves processing_authorized false.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import sys

SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
REMAINING_PROCESSING_GATES = [
    "complete_datatake_or_required_slice_coverage_verified",
    "processing_software_version_and_parameters_locked",
    "radiometric_and_geometric_quality_assessment_completed",
    "independent_review_of_processing_outputs_completed",
]


def read_json(path: Path) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError(f"Cannot read JSON input {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise ValueError(f"JSON input must contain an object: {path}")
    return value


def build_readiness_record(stack: dict, download: dict, audit: dict) -> dict:
    """Join evidence by immutable product ID and archive checksum."""
    candidates = stack.get("candidates")
    if not isinstance(candidates, list):
        raise ValueError("Stack manifest candidates must be a list.")
    product_id = download.get("product_id")
    if not isinstance(product_id, str) or not product_id.strip():
        raise ValueError("Download sidecar is missing product_id.")
    matches = [item for item in candidates if item.get("product_id") == product_id]
    if len(matches) != 1:
        raise ValueError(
            f"Expected exactly one catalogue candidate for download product_id {product_id}; found {len(matches)}."
        )
    candidate = matches[0]
    blockers = []

    if candidate.get("catalogue_selection_status") != "candidate":
        blockers.append("catalogue_record_is_not_a_candidate")
    if download.get("validation") != "passed":
        blockers.append("download_archive_validation_not_passed")

    download_sha = download.get("archive_sha256")
    audit_sha = audit.get("archive_sha256")
    if not isinstance(download_sha, str) or not SHA256_RE.fullmatch(download_sha):
        blockers.append("download_sidecar_sha256_missing_or_invalid")
    if not isinstance(audit_sha, str) or not SHA256_RE.fullmatch(audit_sha):
        blockers.append("safe_audit_sha256_missing_or_invalid")
    if isinstance(download_sha, str) and isinstance(audit_sha, str) and download_sha != audit_sha:
        blockers.append("download_and_audit_archive_checksums_do_not_match")

    archive_file = download.get("archive_file")
    audit_archive = audit.get("archive")
    if not isinstance(archive_file, str) or not archive_file:
        blockers.append("download_sidecar_archive_filename_missing")
    elif audit_archive != Path(archive_file).name:
        blockers.append("download_and_audit_archive_filenames_do_not_match")

    if audit.get("structural_dual_pol_gate") != "passed":
        blockers.append("safe_structural_dual_polarisation_gate_not_passed")
    checks = audit.get("checks")
    if not isinstance(checks, dict) or not checks or not all(value is True for value in checks.values()):
        blockers.append("safe_audit_contains_missing_or_failed_checks")

    expected_name = candidate.get("product_name")
    actual_name = audit.get("safe_root_name")
    if expected_name and actual_name != expected_name:
        blockers.append("safe_root_name_does_not_match_catalogue_product_name")

    structural_passed = not blockers
    return {
        "readiness_schema": "tessellatum.sentinel1.processing-readiness.v1",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z"),
        "product_id": product_id,
        "product_name": expected_name,
        "archive_file": archive_file,
        "archive_sha256": download_sha if isinstance(download_sha, str) else None,
        "evidence": {
            "stack_manifest_schema": stack.get("manifest_schema"),
            "source_inventory_sha256": stack.get("source_inventory_sha256"),
            "catalogue_selection_status": candidate.get("catalogue_selection_status"),
            "download_validation": download.get("validation"),
            "downloaded_at_utc": download.get("downloaded_at_utc"),
            "safe_structural_dual_pol_gate": audit.get("structural_dual_pol_gate"),
            "safe_audit_checks": checks if isinstance(checks, dict) else {},
            "safe_audit_archive_sha256": audit_sha,
        },
        "structural_preflight_status": "passed" if structural_passed else "blocked",
        "structural_preflight_blockers": blockers,
        "processing_authorized": False,
        "processing_status": "not_started",
        "processing_blockers": REMAINING_PROCESSING_GATES,
        "interpretation": (
            "Structural evidence is reconciled; this record does not authorize scientific processing."
            if structural_passed
            else "One or more catalogue, download, archive identity or SAFE structural gates failed."
        ),
        "limitations": [
            "A structural preflight does not validate raster pixel readability or values.",
            "Calibration LUT contents, geolocation accuracy and radiometric correctness remain unverified.",
            "Catalogue coverage refers to the defined study AOI; a slice is not necessarily a complete datatake.",
            "No SNAP processing, scientific QA or independent review is performed by this tool.",
        ],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--stack-manifest", type=Path, required=True)
    parser.add_argument("--download-sidecar", type=Path, required=True)
    parser.add_argument("--safe-audit", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        record = build_readiness_record(
            read_json(args.stack_manifest),
            read_json(args.download_sidecar),
            read_json(args.safe_audit),
        )
    except (OSError, ValueError) as exc:
        print(f"Cannot build processing-readiness record: {exc}", file=sys.stderr)
        return 2
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(record, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Product: {record['product_id']}")
    print(f"Structural preflight: {record['structural_preflight_status']}")
    print("Scientific processing authorized: no")
    print(f"Readiness record: {args.output}")
    return 0 if record["structural_preflight_status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
