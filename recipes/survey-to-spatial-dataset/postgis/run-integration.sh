#!/usr/bin/env sh
set -eu
cd "$(dirname "$0")"
if ! command -v docker >/dev/null 2>&1; then
  echo "Docker is required to run the PostGIS integration and ingestion tests." >&2
  exit 2
fi
docker compose up -d --wait postgis

# Wait for the PostGIS extension, not only the generic PostgreSQL health check.
attempt=0
until docker compose exec -T postgis psql --username spatial_methods --dbname spatial_methods_test --tuples-only --no-align --command "SELECT EXISTS (SELECT 1 FROM pg_extension WHERE extname = 'postgis')" | grep -q '^t'; do
  attempt=$((attempt + 1))
  if [ "$attempt" -ge 30 ]; then
    echo "PostGIS extension did not become available within 60 seconds." >&2
    exit 1
  fi
  sleep 2
done

docker compose exec -T postgis psql --username spatial_methods --dbname spatial_methods_test --set ON_ERROR_STOP=1 --file /tests/integration.sql
docker compose run --rm --no-deps ingest python -m unittest -v test_ingest_pilot
docker compose run --rm ingest
mkdir -p output
set +e
docker compose exec -T postgis psql --quiet --username spatial_methods --dbname spatial_methods_test --set ON_ERROR_STOP=1 --tuples-only --no-align --file /tests/spatial-qa.sql > output/spatial-qa-report.json
qa_exit=$?
set -e
echo "Spatial QA report:"
cat output/spatial-qa-report.json
if [ "$qa_exit" -ne 0 ]; then
  echo "Spatial QA reported hard failures (psql exit $qa_exit)." >&2
  exit "$qa_exit"
fi
docker compose run --rm --no-deps export
echo "Delivery artifacts:"
ls -lh output/spatial-methods-pilot.gpkg output/spatial-methods-pilot-delivery.zip
