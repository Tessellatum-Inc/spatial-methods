#!/usr/bin/env sh
set -eu

cd "$(dirname "$0")"

if ! command -v docker >/dev/null 2>&1; then
  echo "Docker is required to run the PostGIS integration test." >&2
  exit 2
fi

docker compose up -d --wait postgis
docker compose exec -T postgis psql \
  --username spatial_methods \
  --dbname spatial_methods_test \
  --set ON_ERROR_STOP=1 \
  --file /tests/integration.sql
