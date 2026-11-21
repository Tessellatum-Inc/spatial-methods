"""Assemble a traceable photogrammetry delivery dossier.

The ZIP bundles evidence records, not raw imagery or processing products.
Assembly is not a release/acceptance decision.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import tempfile
import zipfile
from pathlib import Path
from typing import Any


ARTIFACTS = (
    ("project_manifest", "project-manifest.json"),
    ("preflight", "preflight-report.json"),
    ("processing_run", "processing-run.json"),
    ("output_inspection", "output-inspection.json"),
    ("validation_evidence", "validation-evidence.json"),
)


def _read_json(path: Path, label: str) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"{label} must be a readable JSON file: {exc}") from exc
    if not isinstance(value, dict):
        raise ValueError(f"{label} JSON root must be an object.")
    return value


def _hash(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def build_dossier(
    manifest_path: str | Path,
    preflight_path: str | Path,
    run_path: str | Path,
    output_inspection_path: str | Path,
    validation_path: str | Path,
) -> tuple[dict, dict[str, Path]]:
    supplied = {
        "project_manifest": Path(manifest_path).expanduser().resolve(),
        "preflight": Path(preflight_path).expanduser().resolve(),
        "processing_run": Path(run_path).expanduser().resolve(),
        "output_inspection": Path(output_inspection_path).expanduser().resolve(),
        "validation_evidence": Path(validation_path).expanduser().resolve(),
    }
    records: dict[str, dict] = {}
    for key, path in supplied.items():
        if not path.is_file():
            raise ValueError(f"Required evidence file is missing: {key} ({path})")
        records[key] = _read_json(path, key)

    manifest = records["project_manifest"]
    preflight = records["preflight"]
    run = records["processing_run"]
    outputs = records["output_inspection"]
    validation = records["validation_evidence"]

    project_id = manifest.get("project_id")
    if not isinstance(project_id, str) or not project_id.strip():
        raise ValueError("Project manifest must declare a non-empty project_id.")

    mismatches = []
    for label, value in (
        ("preflight", preflight.get("project_id")),
        ("validation evidence", validation.get("project_id")),
    ):
        if value and value != project_id:
            mismatches.append(f"{label} project_id {value!r} does not match manifest {project_id!r}.")

    run_id = run.get("run_id") or run.get("processing_run_id")
    validation_run_id = validation.get("processing_run_id")
    if validation_run_id and run_id and validation_run_id != run_id:
        mismatches.append(
            f"Validation processing_run_id {validation_run_id!r} does not match run record {run_id!r}."
        )

    warnings = []
    if preflight.get("status") not in {"ready_for_operator_review"}:
        warnings.append(f"Preflight status is {preflight.get('status', 'unspecified')}.")
    if run.get("status") != "succeeded":
        warnings.append(f"Processing-run status is {run.get('status', 'unspecified')}; execution success is not established.")
    if outputs.get("status") != "inspected":
        warnings.append(f"Output-inspection status is {outputs.get('status', 'unspecified')}.")
    if validation.get("evidence_status") != "assessable":
        warnings.append(f"Checkpoint evidence status is {validation.get('evidence_status', 'unspecified')}.")
    acceptance = validation.get("acceptance") or {}
    if acceptance.get("decision") != "accepted":
        warnings.append(f"Human validation acceptance decision is {acceptance.get('decision', 'unspecified')}.")

    if mismatches:
        status = "inconsistent"
    elif warnings:
        status = "review_required"
    else:
        status = "assembled"

    artifacts = {}
    for key, path in supplied.items():
        artifacts[key] = {
            "archive_path": f"evidence/{ARTIFACTS[[item[0] for item in ARTIFACTS].index(key)][1]}",
            "sha256": _hash(path),
            "size_bytes": path.stat().st_size,
            "source_filename": path.name,
        }

    dossier = {
        "schema_version": "1.0",
        "dossier_type": "photogrammetry_project_delivery_evidence",
        "project_id": project_id,
        "processing_run_id": run_id,
        "status": status,
        "release_authorized": False,
        "release_authorization_note": "Dossier assembly never authorizes delivery; use the project-specific release process.",
        "artifacts": artifacts,
        "observed_statuses": {
            "preflight": preflight.get("status"),
            "processing_run": run.get("status"),
            "output_inspection": outputs.get("status"),
            "checkpoint_evidence": validation.get("evidence_status"),
            "human_acceptance": acceptance.get("decision"),
        },
        "warnings": warnings,
        "consistency_errors": mismatches,
        "scope": {
            "included": "The five named JSON evidence records and this dossier index.",
            "not_included": "Raw imagery, full processing outputs, Docker images, logs not embedded in the run record, and external reference datasets.",
            "verification": "SHA-256 hashes identify the exact evidence files copied into the archive.",
        },
        "limitations": [
            "A checksum proves byte identity, not source authenticity or scientific correctness.",
            "A structurally readable output is not necessarily spatially accurate.",
            "An assessable checkpoint report is not necessarily accepted.",
            "A human acceptance record is not independent multi-reviewer validation unless the review design establishes that.",
            "This dossier does not replace project-specific contractual, legal, safety or professional release checks.",
        ],
    }
    return dossier, supplied


def create_delivery_bundle(
    manifest_path: str | Path,
    preflight_path: str | Path,
    run_path: str | Path,
    output_inspection_path: str | Path,
    validation_path: str | Path,
    destination: str | Path,
) -> dict:
    dossier, supplied = build_dossier(
        manifest_path, preflight_path, run_path, output_inspection_path, validation_path
    )
    destination = Path(destination).expanduser().resolve()
    destination.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="spatial-delivery-") as temporary:
        staging = Path(temporary)
        evidence_dir = staging / "evidence"
        evidence_dir.mkdir()
        for key, archive_name in ARTIFACTS:
            source = supplied[key]
            (evidence_dir / archive_name).write_bytes(source.read_bytes())
        (staging / "delivery-dossier.json").write_text(
            json.dumps(dossier, indent=2, sort_keys=True) + chr(10), encoding="utf-8"
        )
        with zipfile.ZipFile(destination, "w", compression=zipfile.ZIP_DEFLATED) as archive:
            for path in sorted(staging.rglob("*")):
                if path.is_file():
                    archive.write(path, path.relative_to(staging).as_posix())
    return {"archive": str(destination), "sha256": _hash(destination), "size_bytes": destination.stat().st_size, "dossier": dossier}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Bundle photogrammetry project evidence into a reviewable ZIP dossier.")
    parser.add_argument("--manifest", required=True, type=Path)
    parser.add_argument("--preflight", required=True, type=Path)
    parser.add_argument("--run-record", required=True, type=Path)
    parser.add_argument("--output-inspection", required=True, type=Path)
    parser.add_argument("--validation-evidence", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path, help="Destination ZIP archive")
    args = parser.parse_args(argv)
    try:
        result = create_delivery_bundle(
            args.manifest, args.preflight, args.run_record, args.output_inspection,
            args.validation_evidence, args.output,
        )
    except (OSError, ValueError) as exc:
        parser.error(str(exc))
    print(json.dumps(result, indent=2, sort_keys=True))
    return 2 if result["dossier"]["status"] == "inconsistent" else 0


if __name__ == "__main__":
    raise SystemExit(main())
