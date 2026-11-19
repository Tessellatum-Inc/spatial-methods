# PostGIS schema — survey-to-spatial-dataset capstone

**Status:** schema, synthetic ingestion, spatial QA and GeoPackage delivery implemented; live end-to-end verification pending.  
**Purpose:** test a traceable spatial data ingestion, quality-review and handover path without misrepresenting synthetic data as field evidence.

## Files

- [postgis-schema.sql](postgis-schema.sql) — schema, constraints, triggers and indexes.
- [compose.yaml](compose.yaml) — disposable local PostGIS service and processing containers.
- [integration.sql](integration.sql) — database-level positive and negative tests.
- [ingest_pilot.py](ingest_pilot.py) — validates and loads the synthetic fixture.
- [test_ingest_pilot.py](test_ingest_pilot.py) — five standard-library preflight tests.
- [spatial-qa.sql](spatial-qa.sql) — spatial consistency checks and JSON report.
- [build_delivery.py](build_delivery.py) — creates a GeoPackage and portable ZIP handover using GDAL/OGR.
- [input/](input/) — manifest and explicitly synthetic CSV point records.
- [requirements.txt](requirements.txt) and [Dockerfile](Dockerfile) — isolated Python/GDAL processing environment.
- [run-integration.sh](run-integration.sh) — executes database tests, ingestion, QA and export.

## Run the full rehearsal

Requires Docker Engine with the Docker Compose plugin.

```bash
cd recipes/survey-to-spatial-dataset/postgis
sh run-integration.sh
```

The runner starts PostGIS, recreates the disposable pilot schema, runs database integration tests and five Python preflight tests, loads the synthetic fixture, generates spatial QA, then exports a GeoPackage and ZIP handover under output/. The database listens on localhost port 55432 with local-only test credentials. Do not expose it publicly or reuse those credentials.

Stop the database with `docker compose down`.

## GeoPackage delivery

The exporter creates two point layers, stops and assets, retaining the database geometry SRID and selected observation attributes. The ZIP package includes the GeoPackage, spatial QA JSON, delivery manifest with SHA-256 hashes and a concise README. The GeoPackage can be opened in QGIS or another GeoPackage-compatible GIS.

The exporter refuses to package a failed QA report and accepts only a report explicitly marked synthetic. It verifies that both expected layers are present using ogrinfo. The output is a reproducible software handover, not a production data-release process.

## Fixture CRS boundary

The fixture manifest declares source EPSG:4326 (WGS 84), with coordinate order longitude, latitude. Coordinates are invented and clustered close to (0, 0) solely to make a small software test fixture. They do not represent Nairobi or any real transport stop.

The integration script configures EPSG:3857 as a known test target and PostGIS transforms the fixture coordinates into that target. This tests a coordinate-operation path; it does not select a CRS for the Nairobi pilot, validate a Kenya-specific transformation, or establish positional accuracy.

The sibling synthetic rehearsal contains arbitrary local Cartesian values with no CRS. Do not load those records into this pipeline or assign them an EPSG code.

## QA interpretation

The QA report separates hard errors from review flags. CRS mismatches, invalid geometries and missing feature subtypes are hard failures. Coincident points and assets more than 100 m from their linked stop are review flags, not automatic rejections. The 100 m value is an explicit software-review trigger for this fixture, not a universal specification or positional tolerance.

A successful QA run means only that these programmed checks found no hard failures in this synthetic database. It does not establish positional accuracy, field acquisition quality, completeness against reality, accessibility compliance, topology for lines/polygons or operational fitness. No independent positional reference observations are available.

## Architecture and limitations

- The schema models point features only; line/polygon layers, 3D geometry, vertical CRS and multi-CRS projects need separate design.
- The loader accepts only the declared EPSG:4326 synthetic fixture format; it is not yet a general ingestion framework.
- It does not load actual GNSS/instrument-native data or implement a field data capture form.
- The export is a selected-attribute handover; it does not yet include every relational register, raw source file, or a full metadata standard profile.
- Live Docker/PostGIS end-to-end execution is required before describing the complete pipeline as passed.
