# PostGIS schema — survey-to-spatial-dataset capstone

**Status:** authored schema and integration harness; execution against a live PostGIS service is pending.  
**Purpose:** move the capstone from CSV-only record validation toward a spatially enabled, traceable relational model.

## Files

- [`postgis-schema.sql`](postgis-schema.sql) — schema, constraints, triggers and indexes.
- [`compose.yaml`](compose.yaml) — disposable local PostGIS service.
- [`integration.sql`](integration.sql) — database-level positive and negative tests.
- [`run-integration.sh`](run-integration.sh) — starts the service and executes the tests.

## Run the integration test

Requires Docker Engine with the Docker Compose plugin.

```bash
cd recipes/survey-to-spatial-dataset/postgis
sh run-integration.sh
```

The service listens on localhost port 55432. It uses a local-only test password and a disposable test database. Do not reuse these credentials or expose the service publicly. Stop the service with:

```bash
docker compose down
```

The test script drops and recreates the `pilot` schema each time it runs. Do not point this compose file at a production database or modify it to use production credentials.

## Test CRS boundary

The integration test uses EPSG:3857 solely as a known PostGIS SRID for software-level enforcement tests, with synthetic coordinates at (0, 0). This does **not** select a CRS for the Nairobi pilot, does not represent a Nairobi location and does not validate a real-world coordinate transformation.

The existing CSV rehearsal contains arbitrary local Cartesian X/Y values with no CRS. **Do not load those values into this schema, assign them an EPSG code, or export them as mapped locations.**

Before loading actual project geometry, select the CRS from the intended use, authoritative source and applicable jurisdictional requirements. Confirm the SRID in the target PostGIS installation and record the authority, code, official name, units, coordinate epoch where relevant, axis convention and evidence reference.

## What the integration test checks

1. Geometry insertion is rejected before project CRS configuration.
2. A configured test CRS allows a matching geometry.
3. The stored geometry retains its SRID.
4. A mismatched SRID is rejected.
5. A stop subtype must reference a base feature typed as a stop.
6. A stop feature cannot be inserted as an asset subtype.
7. An asset cannot reference a nonexistent stop.
8. An invalid asset type is rejected.

A passing run establishes only that these database behaviours work in the tested container/image version. It does not establish positional accuracy, independent quality evidence, topology, completeness, CRS suitability or fitness for operational use.

## Architecture

The schema separates:

- `project_config`: approved horizontal CRS and coordinate convention;
- `inventory_feature`: shared point geometry and stable feature identity;
- `stop` and `asset`: typed feature attributes;
- `raw_record`: immutable-source references and SHA-256 provenance;
- `survey_observation`: how each feature was observed or derived;
- `equipment_register` and `control_reference`: instrument and reference provenance;
- `quality_check`: checks, evidence, acceptance rules and decisions;
- `processing_run`: reproducible processing metadata;
- `data_dictionary`: versioned field definitions.

## Remaining limitations

- The schema models point features only. Lines/polygons, 3D geometry, vertical CRS, multiple project CRSs and full event/version history require explicit requirements.
- `is_independent` records a documented assertion; the database cannot prove that a check is genuinely independent.
- Geometry validity and SRID checks do not establish positional accuracy or fitness for use.
- Raw bytes should be held in controlled object/file storage; `storage_uri` is a reference, not a storage implementation.
- GeoPackage export and real-data ingestion are not implemented.
- The integration harness must actually be run in a Docker-capable environment before the SQL can be described as tested.
