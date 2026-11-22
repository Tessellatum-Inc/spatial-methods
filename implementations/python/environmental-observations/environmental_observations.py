"""Validated, provenance-aware records for heterogeneous environmental observations.

This module validates a common record envelope. It deliberately does not infer
measurement units, calibrate instruments, or apply measurand-specific QC rules.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from math import isfinite
from numbers import Real
from pathlib import Path
from typing import Any, Mapping
from types import MappingProxyType
import json
import hashlib


QC_STATUSES = frozenset({"raw", "accepted", "flagged", "rejected", "superseded"})
SUPPORT_TYPES = frozenset({"point", "line", "area", "volume", "profile", "pixel", "unknown"})
GEOMETRY_TYPES = frozenset({
    "Point", "MultiPoint", "LineString", "MultiLineString",
    "Polygon", "MultiPolygon", "GeometryCollection",
})
_REQUIRED = {
    "observation_id", "measurand_id", "observed_at", "received_at",
    "value", "unit", "method_id", "support", "qc_status", "provenance",
}
_OPTIONAL = {"standard_uncertainty", "uncertainty_unit", "notes"}
_SUPPORT_KEYS = {"support_type", "geometry", "crs", "support_id"}


class ObservationValidationError(ValueError):
    """Raised when one observation or a batch violates the record contract."""


def _nonempty_string(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ObservationValidationError(f"{field} must be a non-empty string")
    return value.strip()


def _timestamp(value: Any, field: str) -> str:
    if not isinstance(value, str):
        raise ObservationValidationError(f"{field} must be an ISO-8601 string")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ObservationValidationError(f"{field} must be a valid ISO-8601 timestamp") from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ObservationValidationError(f"{field} must include a UTC offset or Z")
    return value


def _finite_number(value: Any, field: str, *, nonnegative: bool = False) -> float:
    if isinstance(value, bool) or not isinstance(value, Real):
        raise ObservationValidationError(f"{field} must be a finite number")
    number = float(value)
    if not isfinite(number):
        raise ObservationValidationError(f"{field} must be a finite number")
    if nonnegative and number < 0:
        raise ObservationValidationError(f"{field} must be non-negative")
    return number


def _freeze_json(value: Any, field: str) -> Any:
    """Copy JSON-compatible data into recursively immutable containers."""
    if isinstance(value, Mapping):
        frozen = {}
        for key, item in value.items():
            if not isinstance(key, str):
                raise ObservationValidationError(f"{field} object keys must be strings")
            frozen[key] = _freeze_json(item, f"{field}.{key}")
        return MappingProxyType(frozen)
    if isinstance(value, (list, tuple)):
        return tuple(_freeze_json(item, field) for item in value)
    if value is None or isinstance(value, (str, bool, int)):
        return value
    if isinstance(value, float) and isfinite(value):
        return value
    raise ObservationValidationError(f"{field} must contain only finite JSON-compatible values")


def _thaw_json(value: Any) -> Any:
    """Return fresh mutable JSON containers for serialization."""
    if isinstance(value, Mapping):
        return {key: _thaw_json(item) for key, item in value.items()}
    if isinstance(value, tuple):
        return [_thaw_json(item) for item in value]
    return value


def _validate_coordinates(value: Any, field: str) -> None:
    """Validate finite numeric coordinate leaves without assuming a CRS or axis order."""
    if isinstance(value, (list, tuple)):
        if not value:
            raise ObservationValidationError(f"{field} coordinate arrays must not be empty")
        if all(isinstance(v, Real) and not isinstance(v, bool) for v in value):
            if len(value) < 2 or any(not isfinite(float(v)) for v in value):
                raise ObservationValidationError(f"{field} positions need at least two finite ordinates")
            return
        for item in value:
            _validate_coordinates(item, field)
        return
    raise ObservationValidationError(f"{field} must contain numeric coordinate arrays")


@dataclass(frozen=True)
class ObservationRecord:
    observation_id: str
    measurand_id: str
    observed_at: str
    received_at: str
    value: float
    unit: str
    method_id: str
    support: Mapping[str, Any]
    qc_status: str
    provenance: Mapping[str, Any]
    standard_uncertainty: float | None = None
    uncertainty_unit: str | None = None
    notes: str | None = None

    @classmethod
    def from_dict(cls, raw: Mapping[str, Any]) -> "ObservationRecord":
        if not isinstance(raw, Mapping):
            raise ObservationValidationError("observation must be an object")
        missing = _REQUIRED - set(raw)
        unknown = set(raw) - _REQUIRED - _OPTIONAL
        if missing:
            raise ObservationValidationError(f"missing required fields: {', '.join(sorted(missing))}")
        if unknown:
            raise ObservationValidationError(f"unknown fields: {', '.join(sorted(unknown))}")

        support = raw["support"]
        if not isinstance(support, Mapping):
            raise ObservationValidationError("support must be an object")
        support_unknown = set(support) - _SUPPORT_KEYS
        if support_unknown:
            raise ObservationValidationError(f"unknown support fields: {', '.join(sorted(support_unknown))}")
        support_type = _nonempty_string(support.get("support_type"), "support.support_type")
        if support_type not in SUPPORT_TYPES:
            raise ObservationValidationError(f"support.support_type must be one of {sorted(SUPPORT_TYPES)}")
        geometry = support.get("geometry")
        crs = support.get("crs")
        if geometry is not None:
            if not isinstance(geometry, Mapping) or geometry.get("type") not in GEOMETRY_TYPES:
                raise ObservationValidationError("support.geometry must be a GeoJSON geometry object")
            if geometry["type"] == "GeometryCollection":
                geometries = geometry.get("geometries")
                if not isinstance(geometries, list) or not geometries:
                    raise ObservationValidationError("GeometryCollection must contain geometries")
                for item in geometries:
                    if not isinstance(item, Mapping) or item.get("type") not in GEOMETRY_TYPES - {"GeometryCollection"}:
                        raise ObservationValidationError("GeometryCollection contains an invalid geometry")
                    _validate_coordinates(item.get("coordinates"), "support.geometry")
            else:
                _validate_coordinates(geometry.get("coordinates"), "support.geometry")
            _nonempty_string(crs, "support.crs")
        if support_type == "unknown" and geometry is not None:
            raise ObservationValidationError("unknown support must not claim a geometry")
        if support_type != "unknown" and geometry is None:
            # Station identifiers and non-geometric support descriptions remain valid.
            if not support.get("support_id"):
                raise ObservationValidationError("support needs geometry or a support_id")
        if support.get("support_id") is not None:
            _nonempty_string(support["support_id"], "support.support_id")

        provenance = raw["provenance"]
        if not isinstance(provenance, Mapping):
            raise ObservationValidationError("provenance must be an object")
        if not provenance:
            raise ObservationValidationError("provenance must contain at least one source/provenance attribute")
        for key, value in provenance.items():
            _nonempty_string(key, "provenance key")
            if value is None:
                raise ObservationValidationError(f"provenance.{key} must not be null")
        frozen_support = _freeze_json(support, "support")
        frozen_provenance = _freeze_json(provenance, "provenance")

        status = _nonempty_string(raw["qc_status"], "qc_status")
        if status not in QC_STATUSES:
            raise ObservationValidationError(f"qc_status must be one of {sorted(QC_STATUSES)}")
        uncertainty = raw.get("standard_uncertainty")
        if uncertainty is not None:
            uncertainty = _finite_number(uncertainty, "standard_uncertainty", nonnegative=True)
        uncertainty_unit = raw.get("uncertainty_unit")
        if uncertainty_unit is not None:
            uncertainty_unit = _nonempty_string(uncertainty_unit, "uncertainty_unit")
        if uncertainty is not None and uncertainty_unit is None:
            raise ObservationValidationError("uncertainty_unit is required when standard_uncertainty is supplied")
        if uncertainty is None and uncertainty_unit is not None:
            raise ObservationValidationError("uncertainty_unit requires standard_uncertainty")
        notes = raw.get("notes")
        if notes is not None and not isinstance(notes, str):
            raise ObservationValidationError("notes must be a string")

        return cls(
            observation_id=_nonempty_string(raw["observation_id"], "observation_id"),
            measurand_id=_nonempty_string(raw["measurand_id"], "measurand_id"),
            observed_at=_timestamp(raw["observed_at"], "observed_at"),
            received_at=_timestamp(raw["received_at"], "received_at"),
            value=_finite_number(raw["value"], "value"),
            unit=_nonempty_string(raw["unit"], "unit"),
            method_id=_nonempty_string(raw["method_id"], "method_id"),
            support=frozen_support,
            qc_status=status,
            provenance=frozen_provenance,
            standard_uncertainty=uncertainty,
            uncertainty_unit=uncertainty_unit,
            notes=notes,
        )

    def to_dict(self) -> dict[str, Any]:
        result = {
            "observation_id": self.observation_id,
            "measurand_id": self.measurand_id,
            "observed_at": self.observed_at,
            "received_at": self.received_at,
            "value": self.value,
            "unit": self.unit,
            "method_id": self.method_id,
            "support": _thaw_json(self.support),
            "qc_status": self.qc_status,
            "provenance": _thaw_json(self.provenance),
        }
        if self.standard_uncertainty is not None:
            result["standard_uncertainty"] = self.standard_uncertainty
            result["uncertainty_unit"] = self.uncertainty_unit
        if self.notes is not None:
            result["notes"] = self.notes
        return result


@dataclass(frozen=True)
class BatchValidation:
    records: tuple[ObservationRecord, ...]
    errors: tuple[str, ...]

    @property
    def is_valid(self) -> bool:
        return not self.errors


def validate_batch(rows: Any) -> BatchValidation:
    """Validate records independently and report duplicate IDs and row errors."""
    if not isinstance(rows, list):
        raise ObservationValidationError("batch must be a JSON array of observation objects")
    records: list[ObservationRecord] = []
    errors: list[str] = []
    seen: set[str] = set()
    for index, row in enumerate(rows):
        try:
            record = ObservationRecord.from_dict(row)
            if record.observation_id in seen:
                raise ObservationValidationError(
                    f"duplicate observation_id {record.observation_id!r} in batch"
                )
            seen.add(record.observation_id)
            records.append(record)
        except ObservationValidationError as exc:
            errors.append(f"records[{index}]: {exc}")
    return BatchValidation(tuple(records), tuple(errors))



@dataclass(frozen=True)
class MethodRule:
    """Project-defined constraints for one acquisition/measurement method.

    No environmental thresholds are built in: callers supply allowed units,
    supports, provenance requirements and optional value bounds from the
    method specification or monitoring quality plan.
    """
    method_id: str
    required_provenance: tuple[str, ...] = ()
    allowed_support_types: frozenset[str] | None = None
    allowed_units: frozenset[str] | None = None
    minimum_value: float | None = None
    maximum_value: float | None = None

    def __post_init__(self) -> None:
        _nonempty_string(self.method_id, "method_id")
        if isinstance(self.required_provenance, str):
            raise ObservationValidationError("required_provenance must be a sequence of field names")
        required = tuple(_nonempty_string(key, "required_provenance item")
                         for key in self.required_provenance)
        if len(required) != len(set(required)):
            raise ObservationValidationError("required_provenance must not contain duplicates")
        object.__setattr__(self, "required_provenance", required)
        if self.allowed_support_types is not None:
            allowed_support = frozenset(self.allowed_support_types)
            invalid = allowed_support - SUPPORT_TYPES
            if invalid:
                raise ObservationValidationError(f"unknown support types in method rule: {sorted(invalid)}")
            object.__setattr__(self, "allowed_support_types", allowed_support)
        if self.allowed_units is not None:
            if isinstance(self.allowed_units, str):
                raise ObservationValidationError("allowed_units must be a collection of unit identifiers")
            allowed_units = frozenset(_nonempty_string(unit, "allowed_units item")
                                      for unit in self.allowed_units)
            if not allowed_units:
                raise ObservationValidationError("allowed_units must not be empty")
            object.__setattr__(self, "allowed_units", allowed_units)
        if self.minimum_value is not None:
            object.__setattr__(self, "minimum_value", _finite_number(self.minimum_value, "minimum_value"))
        if self.maximum_value is not None:
            object.__setattr__(self, "maximum_value", _finite_number(self.maximum_value, "maximum_value"))
        if (self.minimum_value is not None and self.maximum_value is not None
                and self.minimum_value > self.maximum_value):
            raise ObservationValidationError("minimum_value must not exceed maximum_value")


@dataclass(frozen=True)
class MethodRuleValidation:
    """Method-rule findings; structural validity is checked separately."""
    violations: tuple[str, ...]

    @property
    def is_valid(self) -> bool:
        return not self.violations


def validate_method_rules(
    records: Any, rules: Mapping[str, MethodRule]
) -> MethodRuleValidation:
    """Apply only explicitly supplied method rules to structurally valid records.

    Records whose method_id has no configured rule are left untouched. This
    prevents the library from inventing universal environmental constraints.
    """
    if not isinstance(records, (list, tuple)) or not all(
        isinstance(record, ObservationRecord) for record in records
    ):
        raise ObservationValidationError("records must be a list or tuple of ObservationRecord objects")
    if not isinstance(rules, Mapping):
        raise ObservationValidationError("rules must map method_id strings to MethodRule objects")
    for method_id, rule in rules.items():
        _nonempty_string(method_id, "rule key")
        if not isinstance(rule, MethodRule) or method_id != rule.method_id:
            raise ObservationValidationError("each rule key must match its MethodRule.method_id")

    violations: list[str] = []
    for record in records:
        rule = rules.get(record.method_id)
        if rule is None:
            continue
        prefix = f"{record.observation_id} ({record.method_id})"
        missing = sorted(set(rule.required_provenance) - set(record.provenance))
        if missing:
            violations.append(f"{prefix}: missing required provenance: {', '.join(missing)}")
        support_type = record.support["support_type"]
        if rule.allowed_support_types is not None and support_type not in rule.allowed_support_types:
            violations.append(f"{prefix}: support type {support_type!r} is not allowed")
        if rule.allowed_units is not None and record.unit not in rule.allowed_units:
            violations.append(f"{prefix}: unit {record.unit!r} is not allowed")
        if rule.minimum_value is not None and record.value < rule.minimum_value:
            violations.append(f"{prefix}: value is below configured minimum {rule.minimum_value}")
        if rule.maximum_value is not None and record.value > rule.maximum_value:
            violations.append(f"{prefix}: value is above configured maximum {rule.maximum_value}")
    return MethodRuleValidation(tuple(violations))

def load_json_records(path: str | Path) -> BatchValidation:
    """Load a JSON array or an object with a 'records' array; never rewrite raw input."""
    with Path(path).open("r", encoding="utf-8") as stream:
        payload = json.load(stream)
    rows = payload.get("records") if isinstance(payload, dict) else payload
    return validate_batch(rows)


@dataclass(frozen=True)
class JSONLinesIngestion:
    """Traceable result from parsing a newline-delimited JSON source file."""
    source_sha256: str
    total_lines: int
    records: tuple[ObservationRecord, ...]
    errors: tuple[str, ...]

    @property
    def is_valid(self) -> bool:
        return not self.errors


def load_jsonl_records(path: str | Path) -> JSONLinesIngestion:
    """Parse JSON Lines while retaining source digest and physical line diagnostics.

    Blank lines are ignored but still count toward physical line numbers. Each
    non-blank line must contain one observation object. The source is read as
    bytes so the digest identifies the exact archived input, including line
    endings and any byte-order mark. No source file is modified.
    """
    source = Path(path).read_bytes()
    digest = hashlib.sha256(source).hexdigest()
    try:
        content = source.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ObservationValidationError("JSON Lines source must be UTF-8") from exc

    records: list[ObservationRecord] = []
    errors: list[str] = []
    seen: set[str] = set()
    lines = content.splitlines()
    for line_number, line in enumerate(lines, start=1):
        if not line.strip():
            continue
        try:
            raw = json.loads(line)
            record = ObservationRecord.from_dict(raw)
            if record.observation_id in seen:
                raise ObservationValidationError(
                    f"duplicate observation_id {record.observation_id!r} in source"
                )
            seen.add(record.observation_id)
            records.append(record)
        except (json.JSONDecodeError, ObservationValidationError) as exc:
            errors.append(f"line {line_number}: {exc}")
    return JSONLinesIngestion(digest, len(lines), tuple(records), tuple(errors))
