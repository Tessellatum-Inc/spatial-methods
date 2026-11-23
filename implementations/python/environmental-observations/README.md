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
- row-level batch validation, duplicate-ID detection, JSON-array loading and traceable JSON Lines ingestion.

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
The structural validator does not promote records between states. Standard uncertainty,
when supplied, must be non-negative and carry a unit; the unit is not converted
or assumed to equal the measurement unit automatically.

## Method-specific rules

The common record contract does not define universal environmental thresholds. A project may opt into explicit rules from its approved method specification or quality plan:

```python
from environmental_observations import MethodRule, validate_method_rules

rule = MethodRule(
    method_id="field-probe-v1",
    required_provenance=("instrument_id", "calibration_ref"),
    allowed_support_types=frozenset({"point"}),
    allowed_units=frozenset({"Cel"}),
    minimum_value=-5.0,
    maximum_value=50.0,
)
findings = validate_method_rules(records, {rule.method_id: rule})
for finding in findings.violations:
    print(finding)
```

Only records whose `method_id` has a configured rule are checked. The caller supplies every constraint; no default physical range or unit conversion is inferred. Structural validation and method-rule validation are separate gates.

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


Load newline-delimited observations with a source digest and physical-line diagnostics:

```python
from environmental_observations import load_jsonl_records

ingestion = load_jsonl_records("observations.jsonl")
print(ingestion.source_sha256, ingestion.total_lines)
for error in ingestion.errors:
    print(error)
for record in ingestion.records:
    print(record.observation_id)
```

`load_jsonl_records` ignores blank lines while retaining physical line
numbers, keeps valid records when another line is malformed, rejects duplicate
observation IDs, and computes SHA-256 over the exact source bytes. A digest
identifies the bytes presented to the loader; it does not prove who supplied
them or that an external archive is immutable. Retain the original file and
record its digest in the project's controlled archive or ingestion log.


## Processing lineage

The ProcessingActivity record captures an activity ID/type, method ID and
version, software name and version, timezone-aware start/end times, input/output
entity references and a SHA-256 digest of canonicalised parameters. Use a
source digest as an input reference (for example,
sha256:<64-hex-digest>), then link observation IDs and derived product IDs
through subsequent activities.

```python
from environmental_observations import (
    ProcessingActivity, canonical_parameters_sha256, validate_lineage,
)

activity = ProcessingActivity(
    activity_id="estimate-001",
    activity_type="spatial-estimation",
    method_id="ordinary-kriging",
    method_version="2.1",
    software_name="spatial-engine",
    software_version="1.0.0",
    started_at="2026-11-22T08:02:00Z",
    ended_at="2026-11-22T08:03:00Z",
    input_refs=("obs-001", "obs-002"),
    output_refs=("surface-v1",),
    parameters_sha256=canonical_parameters_sha256({"resolution": 10}),
)
result = validate_lineage([activity], source_refs=("obs-001", "obs-002"))
assert result.is_valid
```

The validator checks that inputs exist before each activity in the supplied
execution order and that outputs are not silently redefined. It does not prove
that software ran, verify output bytes, establish operator identity, or provide
a tamper-evident audit log. Persist the manifest alongside the immutable raw
archive and actual output artifacts; add output content digests and signatures
in a controlled deployment when those guarantees are required.

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
unknown support, duplicate IDs, batch error reporting, JSON loading, deep
immutability and caller-defined method rules.


## End-to-end example: observations to an interpolated product

The [observation-to-IDW example](examples/observation_to_idw.py) connects the
JSON Lines ingestion and method-rule boundary above to the repository's
existing geostatistics implementation. It reads point-supported water
temperature records, requires an explicitly configured field-probe method
contract, uses only records already marked `accepted`, runs the shared
`idw_predict` implementation, and writes a deterministic JSON prediction
artifact plus a processing-lineage manifest.

The core observation-record module uses only the Python standard library.
The end-to-end example additionally imports the repository's NumPy-based
geostatistics implementation. Install the example's optional dependencies
from this directory before running it:

```bash
python -m pip install -r requirements.txt
python examples/observation_to_idw.py
```

The example data are synthetic and use a declared projected CRS label
(`EPSG:32637`) with coordinates in metres. The example does not transform
coordinates or establish that this CRS is suitable for a real project.
Its IDW parameters and target points are illustrative, not recommended
environmental defaults. The output file's SHA-256 digest is linked as the
estimation activity output; the manifest also links the exact source-file
digest to the ingested observation identifiers. The lineage validator checks
the declared dependency order, not the scientific validity of the model or
proof that a computation occurred.
