# Synthetic rehearsal — stop and roadside-asset inventory

**Dataset status: synthetic only.** These records are invented to test the data structure and validation code. They are not observations from Nairobi or any other real place.

## Run

Requires Python 3.10+ and no third-party packages.

From this directory:

```bash
python validate_pilot.py
```

Or, from the repository root:

```bash
python recipes/survey-to-spatial-dataset/synthetic/validate_pilot.py
```

The command reads four CSV input tables and writes:

- `output/qa_report.json` — deterministic counts, input SHA-256 hashes, validation result and limitations.
- `output/validation_errors.csv` — validation messages; header-only when no errors are found.

A non-zero exit status indicates validation errors.

## Fixture contents

| Table | Records | Purpose |
|---|---:|---|
| stops.csv | 4 | Stop identity, local-plane coordinates and evidence status |
| assets.csv | 6 | Associated assets, including not-assessed and obscured examples |
| observations.csv | 4 | Raw-record provenance and processing state |
| quality_checks.csv | 4 | Example attribute, metadata and completeness checks |

## Coordinate warning

The fixture uses arbitrary local Cartesian X/Y values in metres. It deliberately has **no CRS**. These values are not Nairobi coordinates and must not be exported as GeoJSON, displayed on a basemap or interpreted as geographic positions. A real project must select and document its authoritative reference system and transformation before spatial delivery.

## What the validator checks

- Required input columns and file presence.
- Unique, nonblank primary identifiers.
- Finite numeric local coordinates.
- Controlled values for stop status, asset type, presence, condition and quality decision.
- Stop foreign keys for assets.
- Feature references from observation and quality-check records.
- Timestamp parseability.
- Raw-record provenance and acceptance-rule presence.
- Explicit true/false independent-check flags.

It does not calculate positional accuracy, certify independence, verify field evidence, test a real CRS transformation, assess accessibility compliance or establish fitness for operational use. The four declared independent checks are fixture attributes, not independently audited evidence.

## Negative test

A manual negative test was run by changing one asset's `stop_id` to a nonexistent identifier. The validator correctly returned FAIL and reported the unknown foreign key. The committed fixture remains clean so the standard run demonstrates a passing schema check.
