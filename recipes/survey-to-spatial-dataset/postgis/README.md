# PostGIS schema — survey-to-spatial-dataset capstone

**Status:** schema, integration tests and synthetic ingestion pipeline authored; live container execution remains pending.  
**Purpose:** test a traceable spatial data ingestion path without misrepresenting synthetic data as field evidence.

## Files

- [`postgis-schema.sql`](postgis-schema.sql) — schema, constraints, triggers and indexes.
- [`compose.yaml`](compose.yaml) — disposable local PostGIS service and ingestion container.
- [`integration.sql`](integration.sql) — database-level positive and negative tests.
- [`ingest_pilot.py`](ingest_pilot.py) — validates and loads the synthetic fixture.
- [`input/`](input/) — manifest and explicitly synthetic CSV point records.
- [`requirements.txt`](requirements.txt) and [`Dockerfile`](Dockerfile) — isolated Python ingestion environment.
- [`run-integration.sh`](run-integration.sh) — executes database tests and ingestion.

## Run the full rehearsal

Requires Docker Engine with the Docker Compose plugin.

```bash
cd recipes/survey-to-spatial-dataset/postgis
sh run-integration.sh
```

The script starts PostGIS, recreates the disposable `pilot` schema, runs the database integration tests, then runs the ingestion container. The service listens on localhost port 55432. It uses local-only test credentials; do not reuse them or expose the service publicly.

Stop the database with:

```bash
docker compose down
```

The integration SQL drops and recreates the `pilot` schema each time. Never point this compose project at production data or credentials.

## Fixture CRS boundary

The fixture manifest explicitly declares source EPSG:4326 (WGS 84), with coordinate order longitude, latitude. Coordinates are invented and clustered close to (0, 0) solely to make a small software test fixture. They do not represent Nairobi or any real transport stop.

The database integration script configures EPSG:3857 as a test target and PostGIS transforms the fixture coordinates into that target. This tests a coordinate-operation path; it does **not** select a CRS for the Nairobi pilot, validate a Kenya-specific transformation, or establish positional accuracy.

The original CSV rehearsal under the sibling `synthetic/` directory contains arbitrary local Cartesian values with no CRS. Do not load those records into this pipeline or assign them an EPSG code.

## What ingestion does

1. Requires a manifest explicitly marked `dataset_status: synthetic`.
2. Requires the fixture's declared EPSG:4326 source and longitude/latitude order.
3. Validates required columns, unique identifiers, coordinate ranges, timestamps and asset-to-stop references.
4. Computes SHA-256 hashes for the input CSV files.
5. Checks that the database has a configured target SRID present in PostGIS.
6. Uses PostGIS `ST_Transform` to transform source points into the configured target SRID.
7. Inserts feature geometry, stop/asset attributes, raw-file references and observation provenance in one database transaction.
8. Uses deterministic identifiers so rerunning the same fixture does not create duplicate feature/observation records.
9. Writes a processing-run record and prints a JSON ingestion summary.

The source file hashes and raw-record references preserve traceability. The fixture's `repo-fixture://` storage references are identifiers for this teaching package, not a production object-storage implementation.

## Integration tests

The database script tests CRS configuration, SRID enforcement, SRID retrieval, subtype integrity, foreign keys and controlled values. The ingestion script adds input validation, hash capture, coordinate transformation and relational loading.

A successful run demonstrates software behaviour for this synthetic fixture only. It does not prove field acquisition quality, positional accuracy, independence of checks, completeness, topology or operational fitness.

## Architecture and limitations

The relational model separates project CRS configuration, shared feature geometry, stop/asset attributes, raw records, survey observations, equipment, control references, quality checks, processing runs and data dictionary entries.

- The schema models point features only; line/polygon layers, 3D geometry, vertical CRS and multi-CRS projects need separate design.
- `is_independent` is a recorded assertion, not proof of independence.
- The loader currently accepts only the declared EPSG:4326 synthetic fixture format; it is not yet a general ingestion framework.
- It does not load actual GNSS/instrument-native data or implement a field data capture form.
- GeoPackage export, spatial topology rules and independent positional QA are not yet implemented.
- Live Docker/PostGIS execution is still required before describing this rehearsal as passed.
