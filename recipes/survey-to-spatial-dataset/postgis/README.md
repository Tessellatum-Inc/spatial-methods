# PostGIS schema — survey-to-spatial-dataset capstone

**Status:** authored SQL design; not yet executed against a live PostgreSQL/PostGIS database.  
**Purpose:** move the capstone from CSV-only record validation toward a spatially enabled, traceable relational model.

## Files

- [`postgis-schema.sql`](postgis-schema.sql) — schema, constraints, triggers and indexes.

## Architecture

The schema separates:

- `project_config`: the approved horizontal CRS and coordinate convention for this project;
- `inventory_feature`: shared point geometry and stable feature identity;
- `stop` and `asset`: typed feature attributes;
- `raw_record`: immutable-source references and SHA-256 provenance;
- `survey_observation`: how each feature was observed or derived;
- `equipment_register` and `control_reference`: instrument and reference provenance;
- `quality_check`: checks, evidence, acceptance rules and decisions;
- `processing_run`: reproducible processing metadata;
- `data_dictionary`: versioned field definitions.

The feature geometry uses a PostGIS `geometry(Point)` column and a trigger that requires its SRID to match the single configured project SRID. This avoids embedding an invented CRS in the schema. The configuration row must be populated only after the reference decision is made.

## Important CRS and fixture boundary

The existing CSV rehearsal contains arbitrary local Cartesian X/Y values with no CRS. **Do not load those values into this schema, assign them an EPSG code, or export them as mapped locations.** They remain useful for record-validation tests only.

Before loading any geometry:

1. Select the coordinate reference system from the intended use, authoritative source and applicable jurisdictional requirements.
2. Confirm the SRID is present and correctly defined in the target PostGIS installation.
3. Record authority, code, official CRS name, units, coordinate epoch where relevant, axis convention and the decision's evidence reference.
4. Populate `pilot.project_config`.
5. Transform source coordinates only through a documented, suitable coordinate operation. Preserve original coordinates and transformation provenance.

A CRS label alone is not proof that a coordinate transformation is correct.

## Deployment assumptions and caveats

- PostgreSQL with a compatible PostGIS extension is required.
- The script creates a dedicated `pilot` schema and enables PostGIS at the database level.
- UUIDs are supplied by the ingestion process; no UUID-generation extension is assumed.
- The script is intended for a new/empty `pilot` schema. It is not an idempotent migration framework.
- The SQL has not yet been run against a live database. Syntax, trigger behaviour, constraints and indexes still require integration testing.
- The `is_independent` field records a documented assertion; the database cannot prove that a check is genuinely independent.
- Geometry checks here are limited to non-empty, valid point geometry and matching SRID. They do not establish positional accuracy, topology, completeness or fitness for use.
- The schema currently models point features. Lines/polygons, 3D geometry, vertical CRS, multiple project CRSs and full event/version history require explicit requirements before extension.
- Raw bytes should be held in controlled object/file storage; `storage_uri` is a reference, not a storage implementation.
- GeoPackage export is not implemented by this SQL file.

## Next implementation gate

Build a small integration test against a disposable PostGIS database, including:

- valid configured SRID and accepted point insertion;
- rejection when project CRS is not configured;
- rejection of a point with the wrong SRID;
- rejection of stop/asset subtype mismatch;
- foreign-key and controlled-value failures;
- retrieval of geometry with SRID preserved.

Only after those tests should we implement ingestion from a genuinely georeferenced, explicitly synthetic fixture. Keep that fixture separate from the current unreferenced local-plane CSV rehearsal.
