#!/usr/bin/env python3
"""Validate the synthetic stop/asset inventory using only the Python standard library."""
from __future__ import annotations
import argparse, csv, hashlib, json, math
from collections import Counter
from datetime import datetime
from pathlib import Path

REQUIRED = {
    "stops.csv": ["stop_id", "x_local_m", "y_local_m", "stop_status", "evidence_basis", "observed_at", "position_method", "position_quality_class", "observer_id"],
    "assets.csv": ["asset_id", "stop_id", "x_local_m", "y_local_m", "asset_type", "presence", "condition", "observed_at", "observer_id"],
    "observations.csv": ["observation_id", "feature_type", "feature_id", "raw_record_ref", "method", "observed_at", "operator_id", "processing_status"],
    "quality_checks.csv": ["check_id", "feature_type", "feature_id", "check_type", "result_value", "result_unit", "acceptance_rule", "decision", "independent", "reviewer_id"],
}
STOP_STATUS = {"observed_stop", "signed_stop", "designated_verified", "uncertain"}
ASSET_TYPES = {"shelter", "seat", "sign", "light", "kerb_ramp", "crossing", "footway_link", "obstruction", "other"}
PRESENCE = {"present", "absent_after_inspection", "not_assessed", "obscured"}
CONDITION = {"good", "fair", "poor", "damaged", "unknown", "not_assessed"}
DECISIONS = {"pass", "fail", "conditional", "not_assessed"}
FEATURE_TYPES = {"stop", "asset"}

def read_csv(path: Path, errors: list[str]) -> list[dict[str, str]]:
    if not path.exists():
        errors.append(f"Missing input file: {path.name}")
        return []
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        missing = [x for x in REQUIRED[path.name] if x not in (reader.fieldnames or [])]
        if missing:
            errors.append(f"{path.name}: missing columns: {', '.join(missing)}")
            return []
        return list(reader)

def unique_ids(rows: list[dict[str, str]], key: str, label: str, errors: list[str]) -> set[str]:
    vals = [r.get(key, "").strip() for r in rows]
    duplicates = sorted(v for v, n in Counter(vals).items() if n > 1 or not v)
    for value in duplicates:
        errors.append(f"{label}: duplicate or blank {key}: {value!r}")
    return {v for v in vals if v}

def valid_timestamp(value: str) -> bool:
    try:
        datetime.fromisoformat(value.replace("Z", "+00:00"))
        return True
    except ValueError:
        return False

def validate(input_dir: Path) -> tuple[dict, list[str]]:
    errors: list[str] = []
    tables = {name: read_csv(input_dir / name, errors) for name in REQUIRED}
    stops, assets = tables["stops.csv"], tables["assets.csv"]
    observations, checks = tables["observations.csv"], tables["quality_checks.csv"]
    stop_ids = unique_ids(stops, "stop_id", "stops", errors)
    asset_ids = unique_ids(assets, "asset_id", "assets", errors)
    unique_ids(observations, "observation_id", "observations", errors)
    unique_ids(checks, "check_id", "quality checks", errors)
    feature_ids = {"stop": stop_ids, "asset": asset_ids}

    def coordinates(row: dict[str, str], label: str) -> None:
        for field in ("x_local_m", "y_local_m"):
            try:
                value = float(row[field])
                if not math.isfinite(value): raise ValueError()
            except (ValueError, TypeError, KeyError):
                errors.append(f"{label} {row.get('stop_id') or row.get('asset_id')}: invalid {field}")

    for r in stops:
        coordinates(r, "stop")
        if r["stop_status"] not in STOP_STATUS: errors.append(f"stop {r['stop_id']}: invalid stop_status")
        if not r["evidence_basis"].strip(): errors.append(f"stop {r['stop_id']}: evidence_basis is blank")
        if not valid_timestamp(r["observed_at"]): errors.append(f"stop {r['stop_id']}: invalid observed_at")
    for r in assets:
        coordinates(r, "asset")
        if r["stop_id"] and r["stop_id"] not in stop_ids: errors.append(f"asset {r['asset_id']}: unknown stop_id {r['stop_id']}")
        if r["asset_type"] not in ASSET_TYPES: errors.append(f"asset {r['asset_id']}: invalid asset_type")
        if r["presence"] not in PRESENCE: errors.append(f"asset {r['asset_id']}: invalid presence")
        if r["condition"] not in CONDITION: errors.append(f"asset {r['asset_id']}: invalid condition")
        if not valid_timestamp(r["observed_at"]): errors.append(f"asset {r['asset_id']}: invalid observed_at")
    for r in observations:
        if r["feature_type"] not in FEATURE_TYPES: errors.append(f"observation {r['observation_id']}: invalid feature_type")
        elif r["feature_id"] not in feature_ids[r["feature_type"]]: errors.append(f"observation {r['observation_id']}: unknown feature_id")
        if not r["raw_record_ref"].strip(): errors.append(f"observation {r['observation_id']}: raw_record_ref is blank")
        if r["processing_status"] not in {"raw", "processed", "checked", "rejected"}: errors.append(f"observation {r['observation_id']}: invalid processing_status")
        if not valid_timestamp(r["observed_at"]): errors.append(f"observation {r['observation_id']}: invalid observed_at")
    for r in checks:
        if r["feature_type"] not in FEATURE_TYPES: errors.append(f"quality check {r['check_id']}: invalid feature_type")
        elif r["feature_id"] not in feature_ids[r["feature_type"]]: errors.append(f"quality check {r['check_id']}: unknown feature_id")
        if r["decision"] not in DECISIONS: errors.append(f"quality check {r['check_id']}: invalid decision")
        if r["independent"].lower() not in {"true", "false"}: errors.append(f"quality check {r['check_id']}: independent must be true/false")
        if r["decision"] in {"pass", "fail", "conditional"} and not r["acceptance_rule"].strip(): errors.append(f"quality check {r['check_id']}: acceptance_rule required")

    summary = {
        "dataset_name": "synthetic_nairobi_stop_asset_inventory",
        "dataset_status": "SYNTHETIC — NOT FIELD OBSERVATIONS",
        "coordinate_model": "local_cartesian_xy_metres",
        "crs": None,
        "crs_note": "No geographic CRS is assigned. Coordinates are invented local-plane values and must not be mapped as Nairobi positions.",
        "input_sha256": {name: hashlib.sha256((input_dir / name).read_bytes()).hexdigest() for name in REQUIRED if (input_dir / name).exists()},
        "record_counts": {"stops": len(stops), "assets": len(assets), "observations": len(observations), "quality_checks": len(checks)},
        "quality_decisions": dict(Counter(r["decision"] for r in checks)),
        "independent_checks": sum(r["independent"].lower() == "true" for r in checks),
        "errors": errors,
        "validation_status": "PASS" if not errors else "FAIL",
        "limitations": [
            "Synthetic records test schema and validation logic only.",
            "No real corridor, instrument, control, field access or permissions are represented.",
            "A passing schema check is not evidence of positional accuracy or fitness for operational use.",
            "Independent-check flags are declarations in the fixture, not independently audited evidence."
        ]
    }
    return summary, errors

def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--input", type=Path, default=Path(__file__).parent / "input")
    p.add_argument("--output", type=Path, default=Path(__file__).parent / "output")
    args = p.parse_args()
    report, errors = validate(args.input)
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output / "qa_report.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    (args.output / "validation_errors.csv").write_text("error\n" + "".join('"' + e.replace('"', '""') + '"\n' for e in errors), encoding="utf-8")
    print(json.dumps({"status": report["validation_status"], "counts": report["record_counts"], "errors": len(errors), "report": str(args.output / "qa_report.json")}, indent=2))
    return 0 if not errors else 1

if __name__ == "__main__":
    raise SystemExit(main())
