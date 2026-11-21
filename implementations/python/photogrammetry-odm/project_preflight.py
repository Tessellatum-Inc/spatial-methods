"""Integrated, read-only photogrammetry project preflight.

Connects the project manifest, generic image audit and ODM command builder.
It never invokes Docker or modifies source imagery.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from dataset_audit import inspect_images
from odm_runner import build_command
from project_manifest import validate_manifest


def build_preflight(manifest: dict, manifest_path: str | Path) -> dict:
    """Run configured structural checks and return one reviewable report."""
    base_report = validate_manifest(manifest, manifest_path)
    project_dir = Path(base_report["project_directory"])
    expected_count = manifest["dataset"].get("expected_image_count")
    blockers = list(base_report["blockers"])
    warnings = list(base_report["warnings"])

    try:
        image_report = inspect_images(project_dir / "images", expected_count)
    except (OSError, ValueError) as exc:
        image_report = {"status": "not_run", "error": str(exc)}
        blockers.append(f"Image audit could not run: {exc}")

    if image_report.get("invalid_images"):
        blockers.append(
            f"{image_report['invalid_images']} image file(s) failed image decoding."
        )
    if image_report.get("image_count_matches_expectation") is False:
        warnings.append(
            f"Expected {expected_count} images but audited {image_report['image_count']}."
        )
    if image_report.get("pillow_available") is False:
        warnings.append(
            "Pillow is unavailable; image inventory and hashes were produced, "
            "but image decoding and dimensions were not checked."
        )

    processing = manifest["processing"]
    arguments = processing.get("arguments", [])
    if not isinstance(arguments, list) or not all(
        isinstance(value, str) and value.strip() for value in arguments
    ):
        raise ValueError("processing.arguments must contain non-empty strings.")
    try:
        command = build_command(
            project_dir,
            processing["container_image"],
            arguments,
        )
    except ValueError as exc:
        command = None
        blockers.append(f"Processing handoff could not be constructed: {exc}")

    status = "blocked" if blockers else (
        "review_required" if warnings else "ready_for_operator_review"
    )
    return {
        "schema_version": "1.0",
        "project_id": base_report["project_id"],
        "status": status,
        "project": {
            "directory": str(project_dir),
            "image_count": image_report.get("image_count", 0),
            "expected_image_count": expected_count,
        },
        "checks": {
            "manifest": base_report,
            "images": image_report,
        },
        "processing_handoff": {
            "engine": processing.get("engine", "OpenDroneMap"),
            "container_image": processing["container_image"],
            "command": command,
            "executed": False,
            "note": "Review-only command construction; Docker was not invoked.",
        },
        "blockers": blockers,
        "warnings": warnings,
        "limitations": [
            "This preflight checks project structure, image readability when Pillow is available, and command construction only.",
            "It does not establish image coverage, sharpness, overlap, camera calibration, CRS correctness, control quality or product accuracy.",
            "The dataset-specific metadata auditor remains a separate check for the documented HEIG-VD export structure.",
            "A ready status is not authorisation to fly, survey, process or deliver.",
        ],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Build an integrated, read-only photogrammetry preflight report."
    )
    parser.add_argument("manifest", type=Path, help="Project manifest JSON")
    parser.add_argument("--json-out", type=Path, help="Optional report destination")
    args = parser.parse_args(argv)
    try:
        manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
        report = build_preflight(manifest, args.manifest)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        parser.error(str(exc))
    rendered = json.dumps(report, indent=2, sort_keys=True)
    print(rendered)
    if args.json_out:
        args.json_out.write_text(rendered + "\n", encoding="utf-8")
    return 2 if report["status"] == "blocked" else 0


if __name__ == "__main__":
    raise SystemExit(main())
