"""End-to-end example: trace environmental observations into an IDW surface.

Run from any working directory:
    python observation_to_idw.py [source.jsonl] [predictions.json]

The geostatistics implementation is imported from this repository; no copy of
the interpolation algorithm is maintained in this example.
"""
from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
from collections.abc import Mapping
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
REPOSITORY_ROOT = HERE.parents[3]
OBSERVATION_PACKAGE = HERE.parent
GEOSTATISTICS_PACKAGE = REPOSITORY_ROOT / "implementations" / "python" / "geostatistics"
for directory in (OBSERVATION_PACKAGE, GEOSTATISTICS_PACKAGE):
    if str(directory) not in sys.path:
        sys.path.insert(0, str(directory))

from environmental_observations import (  # noqa: E402
    MethodRule,
    ProcessingActivity,
    canonical_parameters_sha256,
    load_jsonl_records,
    validate_lineage,
    validate_method_rules,
)
from interpolation import idw_predict  # noqa: E402


METHOD_ID = "field-probe-v1"
CRS = "EPSG:32637"
PARAMETERS = {"power": 2.0, "radius": 2000.0, "max_neighbors": 4}
TARGETS = [(500.0, 500.0), (0.0, 0.0), (1500.0, 500.0)]


def _now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _activity(
    activity_id: str,
    activity_type: str,
    method_id: str,
    method_version: str,
    input_refs: tuple[str, ...],
    output_refs: tuple[str, ...],
    parameters: dict,
    started_at: str,
) -> ProcessingActivity:
    return ProcessingActivity(
        activity_id=activity_id,
        activity_type=activity_type,
        method_id=method_id,
        method_version=method_version,
        software_name="spatial-methods-reference-example",
        software_version="1.0.0",
        started_at=started_at,
        ended_at=_now(),
        input_refs=input_refs,
        output_refs=output_refs,
        parameters_sha256=canonical_parameters_sha256(parameters),
    )


def run_pipeline(source_path: str | Path, output_path: str | Path) -> dict:
    """Validate a JSONL source, interpolate accepted points, and record lineage."""
    source_path = Path(source_path)
    output_path = Path(output_path)
    ingest_started = _now()
    ingestion = load_jsonl_records(source_path)
    if not ingestion.is_valid:
        raise ValueError("source ingestion failed: " + "; ".join(ingestion.errors))
    if not ingestion.records:
        raise ValueError("source contains no valid observations")

    rule = MethodRule(
        method_id=METHOD_ID,
        required_provenance=("instrument_id",),
        allowed_support_types=frozenset({"point"}),
        allowed_units=frozenset({"degC"}),
    )
    method_validation = validate_method_rules(ingestion.records, {METHOD_ID: rule})
    if not method_validation.is_valid:
        raise ValueError("method validation failed: " + "; ".join(method_validation.violations))

    records = tuple(record for record in ingestion.records if record.qc_status == "accepted")
    if len(records) != len(ingestion.records):
        raise ValueError("this demonstration requires every input record to have QC status 'accepted'")

    samples = []
    for record in records:
        if record.method_id != METHOD_ID:
            raise ValueError(f"{record.observation_id}: unexpected method_id {record.method_id!r}")
        support = record.support
        geometry = support.get("geometry")
        if support.get("crs") != CRS or not isinstance(geometry, Mapping) or geometry.get("type") != "Point":
            raise ValueError(f"{record.observation_id}: expected a Point geometry in {CRS}")
        coordinates = geometry["coordinates"]
        if len(coordinates) < 2:
            raise ValueError(f"{record.observation_id}: point needs x and y coordinates")
        samples.append((float(coordinates[0]), float(coordinates[1]), record.value))

    source_ref = f"sha256:{ingestion.source_sha256}"
    ingest_activity = _activity(
        "ingest-observations", "observation-ingestion", "jsonl-observation-ingestion",
        "1.0.0", (source_ref,), tuple(record.observation_id for record in records),
        {"encoding": "UTF-8", "format": "JSON Lines"}, ingest_started,
    )
    estimate_started = _now()
    predictions = idw_predict(samples, TARGETS, **PARAMETERS)
    product = {
        "measurand_id": records[0].measurand_id,
        "unit": records[0].unit,
        "crs": CRS,
        "method": "inverse-distance-weighting",
        "parameters": PARAMETERS,
        "predictions": [
            {"x": target[0], "y": target[1], "value": value}
            for target, value in zip(TARGETS, predictions)
        ],
    }
    output_bytes = (
        json.dumps(product, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)
        + "\n"
    ).encode("utf-8")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(output_bytes)
    output_digest = hashlib.sha256(output_bytes).hexdigest()

    output_ref = f"sha256:{output_digest}"
    estimate_activity = _activity(
        "estimate-surface", "spatial-estimation", "inverse-distance-weighting",
        "1.0.0", tuple(record.observation_id for record in records), (output_ref,),
        PARAMETERS, estimate_started,
    )
    lineage = validate_lineage(
        (ingest_activity, estimate_activity), source_refs=(source_ref,)
    )
    if not lineage.is_valid:
        raise RuntimeError("generated lineage is invalid: " + "; ".join(lineage.violations))

    manifest = {
        "source_sha256": ingestion.source_sha256,
        "source_line_numbers": list(ingestion.record_line_numbers),
        "output_path": str(output_path),
        "output_sha256": output_digest,
        "activities": [
            {
                "activity_id": item.activity_id,
                "activity_type": item.activity_type,
                "method_id": item.method_id,
                "method_version": item.method_version,
                "software_name": item.software_name,
                "software_version": item.software_version,
                "started_at": item.started_at,
                "ended_at": item.ended_at,
                "input_refs": list(item.input_refs),
                "output_refs": list(item.output_refs),
                "parameters_sha256": item.parameters_sha256,
            }
            for item in (ingest_activity, estimate_activity)
        ],
        "lineage_valid": lineage.is_valid,
    }
    manifest_path = output_path.with_suffix(output_path.suffix + ".lineage.json")
    manifest_path.write_text(
        json.dumps(manifest, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return manifest


if __name__ == "__main__":
    default_source = HERE / "observations.jsonl"
    default_output = HERE / "predictions.json"
    source = Path(sys.argv[1]) if len(sys.argv) > 1 else default_source
    output = Path(sys.argv[2]) if len(sys.argv) > 2 else default_output
    result = run_pipeline(source, output)
    print(json.dumps(result, indent=2, sort_keys=True))
