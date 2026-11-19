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

# integration.sql configures EPSG:3857 for the isolated database test.
# The fixture arrives in EPSG:4326 and is transformed inside PostGIS.
docker compose run --rm ingest
