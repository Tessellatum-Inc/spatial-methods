# Environmental observation records: implementation walkthrough

This walkthrough explains the common record envelope implemented in the Python module. It is a structural ingestion boundary, not a universal environmental measurement model.

## 1. Why a common envelope?

A water sample, a fixed air-quality station, a satellite pixel and a river transect do not share one observation operator or spatial support. They do, however, need traceable identifiers, event and receipt times, a measured value with an explicit unit, a method reference, a support description, a QC state and provenance.

The record separates the measurand; value and unit; observed and received time; support; method and provenance; and QC lifecycle state. This keeps common data-management requirements distinct from the measurement model.

## 2. Validation boundary

`ObservationRecord.from_dict` checks required and unexpected fields, non-empty identifiers, timezone-aware ISO-8601 timestamps, finite numeric values, non-negative optional standard uncertainty with an explicit unit, support metadata, finite geometry ordinates, provenance structure and the QC vocabulary.

A timezone offset makes a timestamp unambiguous syntactically. It does not prove clock synchronisation. A CRS label is required when geometry is supplied, but the label is not parsed or verified.

The validator does not convert units, infer axis order, transform coordinates, verify topology, apply detection limits, calibrate instruments, promote raw observations to accepted, or decide physical plausibility. Those decisions belong to the declared method and quality plan.

## 3. Preserve the input boundary

The dataclass is frozen and nested support/provenance structures are recursively copied into immutable mappings and tuples. Mutating the caller input cannot alter the validated record. `to_dict()` returns fresh JSON-compatible containers.

The original files still need to be retained in an immutable or versioned raw archive. This object is a validated working representation, not a replacement for source-file preservation, checksums or an append-only audit log.

## 4. Batch validation

`validate_batch` processes each array row independently. Valid rows are retained, invalid rows are reported with their array index, and duplicate `observation_id` values are rejected. `load_json_records` accepts a top-level JSON array or an object containing a `records` array. Neither function rewrites source files.

## 5. Method-specific rule layer

`MethodRule` provides an opt-in contract keyed by `method_id`. A project can declare required provenance keys, allowed support types, allowed unit identifiers and finite minimum/maximum value bounds. `validate_method_rules` reports violations without modifying observations. Rules are caller-supplied from the applicable method specification or quality plan; the package supplies no default environmental ranges and performs no unit conversion. Methods without a configured rule remain unconstrained by this layer.

The structural validator answers “is this record shaped and typed correctly?” The method rule answers “does this record meet the explicitly configured contract for this acquisition method?” Neither alone proves calibration validity, scientific correctness or regulatory acceptance.

## 6. Run and extend

From this directory run `python -m pytest -q`. Tests cover round trips, timezone requirements, finite values, uncertainty units, QC vocabulary, support/CRS requirements, duplicate IDs, batch errors, JSON loading and deep immutability.

Add method-specific validators separately, keyed by measurand and method. Do not turn the common envelope into an overconfident universal schema. A future database layer should use an authoritative spatial library for CRS and topology checks.