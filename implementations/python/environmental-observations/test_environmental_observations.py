import json
import math
import pytest

from environmental_observations import (
    ObservationRecord, ObservationValidationError, load_json_records, validate_batch,
)


def row(**overrides):
    value = {
        "observation_id": "obs-001",
        "measurand_id": "water-temperature",
        "observed_at": "2026-11-22T08:30:00Z",
        "received_at": "2026-11-22T08:31:00+00:00",
        "value": 18.25,
        "unit": "Cel",
        "method_id": "field-probe-v1",
        "support": {"support_type": "point", "support_id": "station-7"},
        "qc_status": "raw",
        "provenance": {"source_id": "campaign-4", "instrument_id": "probe-2"},
    }
    value.update(overrides)
    return value


def test_valid_record_round_trips_without_losing_optional_fields():
    value = row(standard_uncertainty=0.15, uncertainty_unit="Cel", notes="duplicate field check")
    record = ObservationRecord.from_dict(value)
    assert record.value == pytest.approx(18.25)
    assert record.to_dict() == value


@pytest.mark.parametrize("timestamp", ["2026-11-22T08:30:00", "not-a-date", None])
def test_timestamps_must_be_valid_and_timezone_aware(timestamp):
    with pytest.raises(ObservationValidationError):
        ObservationRecord.from_dict(row(observed_at=timestamp))


@pytest.mark.parametrize("value", [math.nan, math.inf, -math.inf, True, "18.2"])
def test_measurement_value_must_be_finite_numeric_not_boolean_or_string(value):
    with pytest.raises(ObservationValidationError):
        ObservationRecord.from_dict(row(value=value))


def test_negative_uncertainty_and_missing_uncertainty_unit_are_rejected():
    with pytest.raises(ObservationValidationError):
        ObservationRecord.from_dict(row(standard_uncertainty=-0.1, uncertainty_unit="Cel"))
    with pytest.raises(ObservationValidationError):
        ObservationRecord.from_dict(row(standard_uncertainty=0.1))


@pytest.mark.parametrize("status", ["pending", "pass", ""])
def test_qc_status_is_a_controlled_vocabulary(status):
    with pytest.raises(ObservationValidationError):
        ObservationRecord.from_dict(row(qc_status=status))


def test_geometry_requires_crs_and_finite_coordinates():
    geometry = {"type": "Point", "coordinates": [36.8, -1.3]}
    record = ObservationRecord.from_dict(row(
        support={"support_type": "point", "geometry": geometry, "crs": "OGC:CRS84"}
    ))
    assert record.to_dict()["support"]["geometry"] == geometry
    with pytest.raises(ObservationValidationError):
        ObservationRecord.from_dict(row(
            support={"support_type": "point", "geometry": {"type": "Point", "coordinates": [math.nan, 0]}, "crs": "OGC:CRS84"}
        ))
    with pytest.raises(ObservationValidationError):
        ObservationRecord.from_dict(row(
            support={"support_type": "point", "geometry": geometry}
        ))


def test_unknown_support_cannot_claim_geometry_and_known_support_needs_locator():
    with pytest.raises(ObservationValidationError):
        ObservationRecord.from_dict(row(support={"support_type": "unknown", "geometry": {"type": "Point", "coordinates": [0, 0]}, "crs": "OGC:CRS84"}))
    with pytest.raises(ObservationValidationError):
        ObservationRecord.from_dict(row(support={"support_type": "area"}))


def test_batch_collects_row_errors_and_duplicate_identifiers():
    result = validate_batch([row(), row(), {"observation_id": "broken"}])
    assert len(result.records) == 1
    assert len(result.errors) == 2
    assert "duplicate observation_id" in result.errors[0]
    assert "missing required fields" in result.errors[1]
    assert not result.is_valid


def test_json_loader_accepts_wrapped_records(tmp_path):
    path = tmp_path / "observations.json"
    path.write_text(json.dumps({"records": [row()]}), encoding="utf-8")
    result = load_json_records(path)
    assert result.is_valid
    assert result.records[0].observation_id == "obs-001"


def test_batch_requires_array():
    with pytest.raises(ObservationValidationError):
        validate_batch({"records": []})


def test_support_geometry_collection_is_checked():
    geometry = {"type": "GeometryCollection", "geometries": [
        {"type": "Point", "coordinates": [36.8, -1.3]}
    ]}
    record = ObservationRecord.from_dict(row(
        support={"support_type": "area", "geometry": geometry, "crs": "OGC:CRS84"}
    ))
    assert record.support["geometry"]["type"] == "GeometryCollection"


def test_nested_support_and_provenance_are_deeply_immutable():
    source = row(
        support={
            "support_type": "point",
            "geometry": {"type": "Point", "coordinates": [36.8, -1.3]},
            "crs": "OGC:CRS84",
        },
        provenance={"source": {"file": "raw.csv", "line": 4}},
    )
    record = ObservationRecord.from_dict(source)
    source["support"]["geometry"]["coordinates"][0] = 0
    source["provenance"]["source"]["line"] = 99
    assert record.to_dict()["support"]["geometry"]["coordinates"] == [36.8, -1.3]
    assert record.to_dict()["provenance"]["source"]["line"] == 4
    with pytest.raises(TypeError):
        record.support["geometry"]["type"] = "LineString"
    with pytest.raises(TypeError):
        record.provenance["source"]["file"] = "changed.csv"
    exported = record.to_dict()
    exported["support"]["geometry"]["coordinates"][0] = 0
    assert record.to_dict()["support"]["geometry"]["coordinates"] == [36.8, -1.3]


def test_provenance_rejects_non_json_and_non_finite_values():
    with pytest.raises(ObservationValidationError):
        ObservationRecord.from_dict(row(provenance={"source": object()}))
    with pytest.raises(ObservationValidationError):
        ObservationRecord.from_dict(row(provenance={"source": math.inf}))