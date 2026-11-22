"""Integration tests for the observation-to-IDW reference workflow."""
import hashlib
import importlib.util
import json
from pathlib import Path

import pytest


MODULE_PATH = Path(__file__).parent / "examples" / "observation_to_idw.py"
SPEC = importlib.util.spec_from_file_location("observation_to_idw", MODULE_PATH)
PIPELINE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(PIPELINE)


def _source(path: Path) -> None:
    rows = [
        ("water-temp-001", 0, 0, 10),
        ("water-temp-002", 1000, 0, 20),
        ("water-temp-003", 0, 1000, 30),
        ("water-temp-004", 1000, 1000, 40),
    ]
    with path.open("w", encoding="utf-8", newline="\n") as stream:
        for observation_id, x, y, value in rows:
            record = {
                "observation_id": observation_id,
                "measurand_id": "water-temperature",
                "observed_at": "2026-11-22T08:00:00Z",
                "received_at": "2026-11-22T08:01:00Z",
                "value": value,
                "unit": "degC",
                "method_id": "field-probe-v1",
                "support": {
                    "support_type": "point",
                    "geometry": {"type": "Point", "coordinates": [x, y]},
                    "crs": "EPSG:32637",
                },
                "qc_status": "accepted",
                "provenance": {"campaign_id": "test", "instrument_id": observation_id},
            }
            stream.write(json.dumps(record, separators=(",", ":")) + "\n")


def test_end_to_end_pipeline_writes_spatial_product_and_valid_lineage(tmp_path):
    source = tmp_path / "observations.jsonl"
    output = tmp_path / "predictions.json"
    _source(source)

    manifest = PIPELINE.run_pipeline(source, output)
    product_bytes = output.read_bytes()
    product = json.loads(product_bytes)

    assert [item["value"] for item in product["predictions"]] == pytest.approx([25, 10, 25])
    assert manifest["lineage_valid"] is True
    assert manifest["source_sha256"] == hashlib.sha256(source.read_bytes()).hexdigest()
    output_digest = hashlib.sha256(product_bytes).hexdigest()
    assert manifest["output_sha256"] == output_digest
    assert manifest["activities"][0]["input_refs"] == [
        "sha256:" + manifest["source_sha256"]
    ]
    assert manifest["activities"][1]["input_refs"] == [
        "water-temp-001", "water-temp-002", "water-temp-003", "water-temp-004"
    ]
    assert manifest["activities"][1]["output_refs"] == ["sha256:" + output_digest]
    assert (tmp_path / "predictions.json.lineage.json").exists()


def test_pipeline_refuses_structurally_invalid_source(tmp_path):
    source = tmp_path / "bad.jsonl"
    output = tmp_path / "predictions.json"
    source.write_text('{"not":"an observation"}\n', encoding="utf-8")
    with pytest.raises(ValueError, match="source ingestion failed"):
        PIPELINE.run_pipeline(source, output)
    assert not output.exists()


def test_pipeline_refuses_unaccepted_or_wrong_method_observations(tmp_path):
    source = tmp_path / "observations.jsonl"
    output = tmp_path / "predictions.json"
    _source(source)
    rows = source.read_text(encoding="utf-8").splitlines()
    changed = json.loads(rows[0])
    changed["qc_status"] = "raw"
    rows[0] = json.dumps(changed)
    source.write_text("\n".join(rows) + "\n", encoding="utf-8")
    with pytest.raises(ValueError, match="requires every input record"):
        PIPELINE.run_pipeline(source, output)
    assert not output.exists()


def test_pipeline_never_overwrites_the_raw_source(tmp_path):
    source = tmp_path / "observations.jsonl"
    _source(source)
    original = source.read_bytes()
    with pytest.raises(ValueError, match="source and output paths must be different"):
        PIPELINE.run_pipeline(source, source)
    assert source.read_bytes() == original


def test_pipeline_rejects_mixed_observation_times(tmp_path):
    source = tmp_path / "observations.jsonl"
    output = tmp_path / "predictions.json"
    _source(source)
    rows = source.read_text(encoding="utf-8").splitlines()
    changed = json.loads(rows[-1])
    changed["observed_at"] = "2026-11-22T09:00:00Z"
    rows[-1] = json.dumps(changed)
    source.write_text("\n".join(rows) + "\n", encoding="utf-8")
    with pytest.raises(ValueError, match="one measurand, unit and observation timestamp"):
        PIPELINE.run_pipeline(source, output)
    assert not output.exists()



def test_pipeline_rejects_non_numeric_point_coordinates(tmp_path):
    source = tmp_path / "observations.jsonl"
    output = tmp_path / "predictions.json"
    _source(source)
    rows = source.read_text(encoding="utf-8").splitlines()
    changed = json.loads(rows[0])
    changed["support"]["geometry"]["coordinates"] = [[0, 1], 2]
    rows[0] = json.dumps(changed)
    source.write_text("\n".join(rows) + "\n", encoding="utf-8")
    with pytest.raises(ValueError, match="finite numeric coordinate ordinates"):
        PIPELINE.run_pipeline(source, output)
    assert not output.exists()



def test_spatial_product_bytes_are_reproducible_for_identical_inputs(tmp_path):
    source = tmp_path / "observations.jsonl"
    first_output = tmp_path / "first.json"
    second_output = tmp_path / "second.json"
    _source(source)

    first_manifest = PIPELINE.run_pipeline(source, first_output)
    second_manifest = PIPELINE.run_pipeline(source, second_output)

    assert first_output.read_bytes() == second_output.read_bytes()
    assert first_manifest["output_sha256"] == second_manifest["output_sha256"]
    assert first_manifest["activities"][1]["parameters_sha256"] == (
        second_manifest["activities"][1]["parameters_sha256"]
    )
