# Environmental observation records and validation

A standard-library Python reference implementation of the common observation
record envelope used by [SM-REC-014](../../../recipes/environmental-monitoring/README.md).

## Scope

This package provides:
- an immutable `ObservationRecord` data model;
- explicit observed and received timestamps, each requiring a UTC offset;
- finite numeric values and optional non-negative standard uncertainty;
- a support descriptor that can reference a station/sample or carry GeoJSON
  geometry with an explicit CRS label;
- controlled QC lifecycle states;
- source/method/instrument/calibration provenance as caller-supplied metadata;
- row-level batch validation, duplicate-ID detection and JSON loading.

It intentionally does **not** convert units, infer coordinate reference systems,
calibrate instruments, decide whether a measurement is physically plausible,
or apply measurand-specific QC. A valid record is structurally well-formed; it
is not evidence that the measurement is scientifically correct or accepted.

## Record contract

Required fields: `observation_id`, `measurand_id`, `observed_at`,
`received_at`, `value`, `unit`, `method_id`, `support`, `qc_status`
and `provenance`.

Support has a `support_type` (`point`, `line`, `area`, `volume`,
`profile`, `pixel` or `unknown`) and either a stable `support_id` or
a GeoJSON geometry plus explicit `crs`. The schema does not assume that every
measurement is a point sample. Geometry coordinates are checked for finite
numeric ordinates, but axis order, CRS validity, topology and physical support
semantics remain the responsibility of the project.

QC states are `raw`, `accepted`, `flagged`, `rejected` and `superseded`.
The validator does not promote records between states. Standard uncertainty,
when supplied, must be non-negative and carry a unit; the unit is not converted
or assumed to equal the measurement unit automatically.

## Run

Python 3.10+; no runtime dependencies.

```bash
cd implementations/python/environmental-observations
python -m pytest -q
```

Validate a JSON array or an object containing a `records` array:

```python
from environmental_observations import load_json_records

result = load_json_records("observations.json")
for error in result.errors:
    print(error)
for record in result.records:
    print(record.observation_id, record.qc_status)
```

A batch result retains valid records and reports invalid rows with their array
index. Duplicate identifiers are rejected rather than silently overwritten.
The source file is read only; this module never edits or normalises the raw
archive in place.

## Example record

```json
{
  "observation_id": "obs-001",
  "measurand_id": "water-temperature",
  "observed_at": "2026-11-22T08:30:00Z",
  "received_at": "2026-11-22T08:31:00+00:00",
  "value": 18.25,
  "unit": "Cel",
  "method_id": "field-probe-v1",
  "support": {
    "support_type": "point",
    "support_id": "station-7"
  },
  "qc_status": "raw",
  "provenance": {
    "source_id": "campaign-4",
    "instrument_id": "probe-2",
    "calibration_ref": "cal-2026-11"
  },
  "standard_uncertainty": 0.15,
  "uncertainty_unit": "Cel"
}
```

## Design cautions

- Preserve the original payload and source files outside this parser. This
  model is a validated working representation, not an immutable archive.
- Keep units explicit and perform conversions only through a declared,
  tested unit registry or measurand-specific rule.
- A timestamp with a timezone is syntactically valid; clock synchronisation,
  latency and event-time ordering require separate project checks.
- GeoJSON coordinates alone do not establish a CRS. The required `crs` label
  is explicit metadata, not a CRS parser or validator.
- Do not treat `accepted` as a universal regulatory status. Its meaning must
  be defined by the monitoring programme and method.
- Detection limits, censored values, categorical results, laboratory batches,
  calibration uncertainty and sensor drift need richer method-specific
  extensions; they must not be forced into an invented generic numeric rule.

## Tests

Tests cover round-trip preservation, timezone-aware timestamps, finite numeric
values, uncertainty constraints, QC vocabulary, support geometry/CRS,
unknown support, duplicate IDs, batch error reporting and JSON loading.
