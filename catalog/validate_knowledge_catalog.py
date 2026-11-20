#!/usr/bin/env python3
"""Validate Spatial Methods' machine-readable knowledge catalogue using stdlib only."""
from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path

RELATIONSHIPS = {
    "explains", "depends_on", "implements", "uses", "collects_with",
    "applies_to", "alternative_to", "validates", "benchmarked_by",
    "derived_from", "cites", "part_of", "supersedes",
}
KINDS = {
    "foundation", "algorithm", "operation", "data_structure", "model",
    "statistic", "metric", "method", "workflow", "system", "standard",
    "implementation", "dataset", "application", "review",
}
STATUSES = {
    "captured", "mapped", "sourced", "curated", "researched",
    "implemented", "tested", "validated", "maintained",
}
SUBJECT_PATTERN = re.compile(r"SM-(?:FND|ALG|COL|REC|INF|APP)-\d{3}")
RECORD_PATTERN = re.compile(r"SM-KB-\d{6}")


def validate_catalog(root: Path) -> list[str]:
    catalog = root / "catalog"
    errors: list[str] = []
    subject_file = catalog / "master-subject-index.md"
    records_file = catalog / "knowledge-records.jsonl"
    schema_file = catalog / "schemas" / "knowledge-record.schema.json"
    graph_file = catalog / "knowledge-graph-reference-positioning-measurement.csv"

    for path in (subject_file, records_file, schema_file, graph_file):
        if not path.is_file():
            errors.append(f"Required catalogue file missing: {path.relative_to(root)}")
    if errors:
        return errors

    subject_ids = set(SUBJECT_PATTERN.findall(subject_file.read_text(encoding="utf-8")))
    try:
        schema = json.loads(schema_file.read_text(encoding="utf-8"))
        if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
            errors.append("Knowledge-record schema does not declare JSON Schema 2020-12.")
        if schema.get("type") != "object":
            errors.append("Knowledge-record schema root must be an object.")
    except (json.JSONDecodeError, OSError) as exc:
        errors.append(f"Invalid knowledge-record schema JSON: {exc}")
        return errors

    records: list[dict] = []
    seen_ids: set[str] = set()
    for line_number, line in enumerate(records_file.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            errors.append(f"Blank JSONL line at {line_number}.")
            continue
        try:
            item = json.loads(line)
        except json.JSONDecodeError as exc:
            errors.append(f"Invalid JSONL at line {line_number}: {exc}")
            continue
        if not isinstance(item, dict):
            errors.append(f"Record at line {line_number} must be a JSON object.")
            continue
        required = {"record_id", "title", "kind", "canonical_path", "subject_ids", "summary", "status", "relationships"}
        missing = required - item.keys()
        if missing:
            errors.append(f"Record at line {line_number} missing fields: {sorted(missing)}")
            continue
        rid = item["record_id"]
        if not isinstance(rid, str) or not RECORD_PATTERN.fullmatch(rid):
            errors.append(f"Invalid record_id at line {line_number}: {rid!r}")
        elif rid in seen_ids:
            errors.append(f"Duplicate record_id: {rid}")
        else:
            seen_ids.add(rid)
        if item["kind"] not in KINDS:
            errors.append(f"{rid}: unsupported kind {item['kind']!r}")
        if item["status"] not in STATUSES:
            errors.append(f"{rid}: unsupported status {item['status']!r}")
        if not isinstance(item["summary"], str) or len(item["summary"].strip()) < 20:
            errors.append(f"{rid}: summary must contain at least 20 characters.")
        path_value = item["canonical_path"]
        if not isinstance(path_value, str) or path_value.startswith("/") or ".." in Path(path_value).parts:
            errors.append(f"{rid}: unsafe canonical_path {path_value!r}")
        elif not (root / path_value).is_file():
            errors.append(f"{rid}: canonical file does not exist: {path_value}")
        for sid in item["subject_ids"] if isinstance(item["subject_ids"], list) else []:
            if sid not in subject_ids:
                errors.append(f"{rid}: unknown subject_id {sid!r}")
        for edge in item["relationships"] if isinstance(item["relationships"], list) else []:
            if not isinstance(edge, dict) or edge.get("relationship") not in RELATIONSHIPS:
                errors.append(f"{rid}: malformed or unsupported relationship {edge!r}")
                continue
            target = edge.get("target_id")
            if target not in subject_ids and target not in seen_ids and not RECORD_PATTERN.fullmatch(str(target)):
                errors.append(f"{rid}: unresolved relationship target {target!r}")
        for ref in item.get("evidence_refs", []):
            if not isinstance(ref, str) or ref.startswith("/") or ".." in Path(ref).parts or not (root / ref).is_file():
                errors.append(f"{rid}: unresolved or unsafe evidence_ref {ref!r}")
        records.append(item)

    all_record_ids = {r.get("record_id") for r in records}
    for item in records:
        for edge in item.get("relationships", []):
            target = edge.get("target_id") if isinstance(edge, dict) else None
            if isinstance(target, str) and target.startswith("SM-KB-") and target not in all_record_ids:
                errors.append(f"{item.get('record_id')}: relationship points to missing record {target}")

    try:
        with graph_file.open(newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            expected = {"source_id", "relationship", "target_id", "evidence_path", "relationship_basis", "qualification"}
            if set(reader.fieldnames or []) != expected:
                errors.append("Knowledge graph CSV header does not match the required six columns.")
            for line_number, edge in enumerate(reader, 2):
                if edge["source_id"] not in subject_ids and edge["source_id"] not in all_record_ids:
                    errors.append(f"Graph row {line_number}: unknown source {edge['source_id']!r}")
                if edge["target_id"] not in subject_ids and edge["target_id"] not in all_record_ids:
                    errors.append(f"Graph row {line_number}: unknown target {edge['target_id']!r}")
                if edge["relationship"] not in RELATIONSHIPS:
                    errors.append(f"Graph row {line_number}: unsupported relationship {edge['relationship']!r}")
                ref = edge["evidence_path"]
                if ref.startswith("/") or ".." in Path(ref).parts or not (root / ref).is_file():
                    errors.append(f"Graph row {line_number}: missing evidence path {ref!r}")
    except (OSError, csv.Error) as exc:
        errors.append(f"Unable to read knowledge graph CSV: {exc}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1],
                        help="Repository root (defaults to parent of catalog/).")
    args = parser.parse_args()
    errors = validate_catalog(args.root.resolve())
    if errors:
        print(f"FAIL: {len(errors)} catalogue validation error(s)")
        for error in errors:
            print(f"- {error}")
        return 1
    print("PASS: knowledge-record metadata and graph references are internally consistent.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
