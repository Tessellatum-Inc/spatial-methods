"""Validate a photogrammetry project manifest and produce a safe preflight report.

This utility does not download data, invoke Docker, modify source files, or
approve a survey design. It checks explicit project configuration and local
input readiness before processing is considered.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def _nonblank(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def validate_manifest(manifest: dict, manifest_path: str | Path) -> dict:
    """Return a structured preflight report; malformed manifests raise ValueError."""
    if not isinstance(manifest, dict):
        raise ValueError("Manifest root must be a JSON object.")
    if manifest.get("schema_version") != "1.0":
        raise ValueError("schema_version must be '1.0'.")
    required = ("project_id", "title", "intended_use", "dataset", "processing", "validation", "deliverables")
    missing = [key for key in required if key not in manifest]
    if missing:
        raise ValueError("Missing required top-level fields: " + ", ".join(missing))

    for key in ("project_id", "title", "intended_use"):
        if not _nonblank(manifest[key]):
            raise ValueError(f"{key} must be a non-empty string.")

    base = Path(manifest_path).expanduser().resolve().parent
    dataset = manifest["dataset"]
    processing = manifest["processing"]
    validation = manifest["validation"]
    if not isinstance(dataset, dict) or not _nonblank(dataset.get("project_directory")):
        raise ValueError("dataset.project_directory must be a non-empty path.")
    if not isinstance(processing, dict) or not _nonblank(processing.get("container_image")):
        raise ValueError("processing.container_image must be a non-empty pinned image reference.")
    if not isinstance(validation, dict):
        raise ValueError("validation must be an object.")
    if not isinstance(manifest["deliverables"], list) or not manifest["deliverables"]:
        raise ValueError("deliverables must be a non-empty list.")

    project_dir = Path(dataset["project_directory"]).expanduser()
    if not project_dir.is_absolute():
        project_dir = (base / project_dir).resolve()
    image_dir = project_dir / "images"
    blockers: list[str] = []
    warnings: list[str] = []
    info: list[str] = []

    if not project_dir.is_dir():
        blockers.append(f"Project directory does not exist: {project_dir}")
        image_count = 0
    elif not image_dir.is_dir():
        blockers.append(f"Expected images/ directory: {image_dir}")
        image_count = 0
    else:
        suffixes = {".jpg", ".jpeg", ".tif", ".tiff", ".dng"}
        image_count = sum(
            1 for path in image_dir.rglob("*")
            if path.is_file() and path.suffix.lower() in suffixes
        )
        if image_count == 0:
            blockers.append("No supported image files found under images/.")
    expected = dataset.get("expected_image_count")
    if expected is not None:
        if isinstance(expected, bool) or not isinstance(expected, int) or expected < 1:
            raise ValueError("dataset.expected_image_count must be a positive integer.")
        if image_count and image_count != expected:
            warnings.append(f"Expected {expected} images but found {image_count}.")

    image_ref = processing["container_image"]
    if image_ref.endswith(":latest") or (":" not in image_ref.rsplit("/", 1)[-1] and "@sha256:" not in image_ref):
        warnings.append("Processing image does not appear explicitly pinned; record a version tag or digest.")
    if "@sha256:" not in image_ref:
        warnings.append("Container image digest is not recorded; a version tag alone may be mutable.")

    for field in ("horizontal_crs", "vertical_reference", "coordinate_units"):
        if not _nonblank(validation.get(field)):
            warnings.append(f"validation.{field} is not specified.")
    if validation.get("independent_checkpoints") is not True:
        warnings.append("Independent checkpoints are not explicitly confirmed; external accuracy assessment may be unavailable.")
    if not _nonblank(validation.get("acceptance_criteria")):
        warnings.append("Project-specific acceptance criteria are not documented.")
    if not _nonblank(validation.get("reference_uncertainty")):
        warnings.append("Reference measurement uncertainty is not documented.")

    if not isinstance(manifest.get("data_sources", []), list):
        raise ValueError("data_sources must be a list when supplied.")
    if not isinstance(manifest.get("processing", {}).get("arguments", []), list):
        raise ValueError("processing.arguments must be a list.")
    if not all(_nonblank(item) for item in manifest["deliverables"]):
        raise ValueError("Each deliverable must be a non-empty string.")

    info.append("Read-only preflight; no source files were modified and no processing engine was invoked.")
    info.append("Image count and path checks do not establish image quality, coverage, georeferencing or survey accuracy.")
    return {
        "schema_version": "1.0",
        "project_id": manifest["project_id"],
        "project_directory": str(project_dir),
        "image_count": image_count,
        "container_image": image_ref,
        "status": "blocked" if blockers else ("review_required" if warnings else "ready_for_operator_review"),
        "blockers": blockers,
        "warnings": warnings,
        "information": info,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run a read-only photogrammetry project-manifest preflight.")
    parser.add_argument("manifest", type=Path, help="Project manifest JSON")
    parser.add_argument("--json-out", type=Path, help="Optional JSON report destination")
    args = parser.parse_args(argv)
    try:
        manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
        report = validate_manifest(manifest, args.manifest)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        parser.error(str(exc))
    rendered = json.dumps(report, indent=2, sort_keys=True)
    print(rendered)
    if args.json_out:
        args.json_out.write_text(rendered + "\n", encoding="utf-8")
    return 0 if report["status"] != "blocked" else 2


if __name__ == "__main__":
    raise SystemExit(main())
