#!/usr/bin/env sh
set -eu

cd "$(dirname "$0")"

if ! command -v docker >/dev/null 2>&1; then
  echo "Docker is required to run the PostGIS integration and ingestion tests." >&2
  exit 2
fi

docker compose up -d --wait postgis

# Recreate the disposable schema and execute database constraints/integration tests.
docker compose exec -T postgis psql \
  --username spatial_methods \
  --dbname spatial_methods_test \
  --set ON_ERROR_STOP=1 \
  --file /tests/integration.sql

# Run pure input-package tests before attempting a database load.
docker compose run --rm --no-deps ingest python -m unittest -v test_ingest_pilot

# Load the explicitly synthetic fixture into the isolated EPSG:3857 test database.
docker compose run --rm ingest

# Generate a machine-readable QA report. A hard QA failure makes psql return nonzero.
mkdir -p output
docker compose exec -T postgis psql \
  --username spatial_methods \
  --dbname spatial_methods_test \
  --set ON_ERROR_STOP=1 \
  --tuples-only --no-align \
  --file /tests/spatial-qa.sql > output/spatial-qa-report.json

echo "Spatial QA report:"
cat output/spatial-qa-report.json
