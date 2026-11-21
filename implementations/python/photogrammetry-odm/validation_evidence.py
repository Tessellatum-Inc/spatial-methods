"""Project-level independent checkpoint evidence and human acceptance record.

Statistics are descriptive. This adapter never infers acceptance from generic
thresholds and never treats GCPs or AI interpretations as independent checks.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

from checkpoint_qa import assess_checkpoints, read_checkpoints


REQUIRED_CONTEXT = (
    "project_id", "processing_run_id", "horizontal_crs",
    "vertical_reference", "coordinate_units", "reference_uncertainty",
    "sample_design", "checkpoint_independence",
)


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def build_validation_record(
    checkpoint_csv: str | Path,
    context: dict[str, Any],
    *,
    run_record: str | Path | None = None,
    output_inspection: str | Path | None = None,
) -> dict:
    """Build a traceable evidence record; acceptance remains an explicit human act."""
    if not isinstance(context, dict):
        raise ValueError("Validation context must be a JSON object.")
    csv_path = Path(checkpoint_csv).expanduser().resolve()
    records = read_checkpoints(csv_path)
    stats = assess_checkpoints(records)

    missing = [key for key in REQUIRED_CONTEXT if context.get(key) in (None, "", [])]
    if context.get("checkpoint_independence") not in (True, False):
        missing.append("checkpoint_independence (must be true or false)")
    if context.get("checkpoint_independence") is not True:
        missing.append("independent checkpoints not confirmed")

    links = {}
    for label, supplied in (("processing_run", run_record), ("output_inspection", output_inspection)):
        if supplied is None:
            continue
        path = Path(supplied).expanduser().resolve()
        if not path.is_file():
            raise ValueError(f"{label} record does not exist: {path}")
        links[label] = {"path": str(path), "sha256": _sha256(path)}
        try:
            parsed = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise ValueError(f"{label} record must be valid JSON: {exc}") from exc
        if label == "processing_run":
            recorded_id = parsed.get("run_id") or parsed.get("processing_run_id")
            if context.get("processing_run_id") and recorded_id and recorded_id != context["processing_run_id"]:
                raise ValueError("processing_run_id does not match the supplied processing-run record.")

    decision = context.get("acceptance_decision", "pending")
    allowed = {"pending", "accepted", "rejected", "not_assessable"}
    if decision not in allowed:
        raise ValueError("acceptance_decision must be pending, accepted, rejected or not_assessable.")
    rationale = context.get("acceptance_rationale")
    if decision == "accepted" and missing:\n        raise ValueError("Cannot record accepted while required evidence is missing or checkpoint independence is unconfirmed.")\n    if decision != "pending" and not (isinstance(rationale, str) and rationale.strip()):
        raise ValueError("A non-pending human acceptance decision requires acceptance_rationale.")
    reviewer = context.get("reviewer")
    if decision != "pending" and not (isinstance(reviewer, str) and reviewer.strip()):
        raise ValueError("A non-pending human acceptance decision requires reviewer.")

    evidence_status = "assessable" if not missing else "not_assessable"
    if decision == "not_assessable":
        evidence_status = "not_assessable"
    return {
        "schema_version": "1.0",
        "project_id": context.get("project_id"),
        "processing_run_id": context.get("processing_run_id"),
        "evidence_status": evidence_status,
        "checkpoint_source": {
            "path": str(csv_path),
            "sha256": _sha256(csv_path),
            "count": stats["n"],
            "independence_confirmed": context.get("checkpoint_independence") is True,
        },
        "reference_definition": {
            "horizontal_crs": context.get("horizontal_crs"),
            "vertical_reference": context.get("vertical_reference"),
            "coordinate_units": context.get("coordinate_units"),
            "reference_uncertainty": context.get("reference_uncertainty"),
        },
        "sample_design": context.get("sample_design"),
        "residual_statistics": stats,
        "linked_evidence": links,
        "acceptance": {
            "decision": decision,
            "reviewer": reviewer,
            "rationale": rationale,
            "decision_is_human_supplied": True,
            "automatic_threshold_decision": False,
        },
        "missing_evidence": missing,
        "limitations": [
            "Residuals use model minus reference and the coordinate units supplied by the operator.",
            "No CRS transformation or compatibility check is performed.",
            "Reference uncertainty is recorded, not propagated into residual statistics.",
            "Sample representativeness and independence are declared, not independently proven.",
            "The descriptive radial P95 is not CE95 or a confidence bound.",
            "GCPs, training points and AI-assisted interpretations are not independent checkpoints.",
            "A pending or accepted decision is not a substitute for a documented project-specific acceptance protocol.",
            "A single reviewer decision is not independent multi-reviewer validation.",
        ],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Create an independent-checkpoint validation evidence record.")
    parser.add_argument("checkpoint_csv", type=Path)
    parser.add_argument("context_json", type=Path, help="JSON metadata and explicit human acceptance decision")
    parser.add_argument("--run-record", type=Path)
    parser.add_argument("--output-inspection", type=Path)
    parser.add_argument("--json-out", type=Path)
    args = parser.parse_args(argv)
    try:
        context = json.loads(args.context_json.read_text(encoding="utf-8"))
        report = build_validation_record(
            args.checkpoint_csv, context,
            run_record=args.run_record, output_inspection=args.output_inspection,
        )
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        parser.error(str(exc))
    rendered = json.dumps(report, indent=2, sort_keys=True)
    print(rendered)
    if args.json_out:
        args.json_out.write_text(rendered + "\n", encoding="utf-8")
    return 0 if report["evidence_status"] == "assessable" else 2


if __name__ == "__main__":
    raise SystemExit(main())
