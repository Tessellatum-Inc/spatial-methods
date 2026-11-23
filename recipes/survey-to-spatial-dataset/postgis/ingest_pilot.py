#!/usr/bin/env python3
"""Load the explicitly synthetic geospatial fixture into a configured PostGIS pilot schema."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import os
import sys
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any

NAMESPACE = uuid.UUID("f42a8c9e-3b8d-4c7f-8d61-1f0eac2d8a11")
REQUIRED_STOP = {
    "stop_id", "longitude", "latitude", "observed_name", "stop_status",
    "evidence_basis", "route_reference", "side_of_road",
    "observation_datetime", "positional_method", "position_quality_class",
    "source_observer",
}
REQUIRED_ASSET = {
    "asset_id", "stop_id", "longitude", "latitude", "asset_type", "presence",
    "condition", "observation_datetime",
}


class IngestionError(ValueError):
    """Raised when the input package is incomplete or inconsistent."""


def stable_uuid(value: str) -> str:
    return str(uuid.uuid5(NAMESPACE, value))


def parse_coordinate(value: str, field: str, minimum: float, maximum: float) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError) as exc:
        raise IngestionError(f"{field} must be numeric") from exc
    if not math.isfinite(number) or not minimum <= number <= maximum:
        raise IngestionError(f"{field} must be finite and within [{minimum}, {maximum}]")
    return number


def read_csv(path: Path, required: set[str]) -> list[dict[str, str]]:
    if not path.is_file():
        raise IngestionError(f"Missing input file: {path}")
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise IngestionError(f"{path.name} has no header")
        missing = required - set(reader.fieldnames)
        if missing:
            raise IngestionError(f"{path.name} missing columns: {', '.join(sorted(missing))}")
        rows = list(reader)
    if not rows:
        raise IngestionError(f"{path.name} contains no records")
    return rows


def load_package(input_dir: Path) -> tuple[dict[str, Any], list[dict[str, str]], list[dict[str, str]]]:
    manifest_path = input_dir / "manifest.json"
    if not manifest_path.is_file():
        raise IngestionError("Missing manifest.json")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest.get("dataset_status") != "synthetic":
        raise IngestionError("This loader accepts only fixtures explicitly marked dataset_status=synthetic")
    source_crs = manifest.get("source_crs", {})
    if source_crs.get("authority") != "EPSG" or str(source_crs.get("code")) != "4326":
        raise IngestionError("This fixture loader requires the declared test source CRS EPSG:4326")
    if manifest.get("coordinate_order") != "longitude_latitude":
        raise IngestionError("Expected coordinate_order=longitude_latitude")

    stops = read_csv(input_dir / "stops.csv", REQUIRED_STOP)
    assets = read_csv(input_dir / "assets.csv", REQUIRED_ASSET)

    stop_ids: set[str] = set()
    for row in stops:
        identifier = row["stop_id"].strip()
        if not identifier or identifier in stop_ids:
            raise IngestionError(f"Blank or duplicate stop_id: {identifier!r}")
        stop_ids.add(identifier)
        parse_coordinate(row["longitude"], "longitude", -180, 180)
        parse_coordinate(row["latitude"], "latitude", -90, 90)
        if not row["evidence_basis"].strip() or not row["source_observer"].strip():
            raise IngestionError(f"{identifier}: evidence_basis and source_observer are required")
        try:
            datetime.fromisoformat(row["observation_datetime"].replace("Z", "+00:00"))
        except ValueError as exc:
            raise IngestionError(f"{identifier}: invalid observation_datetime") from exc

    asset_ids: set[str] = set()
    for row in assets:
        identifier = row["asset_id"].strip()
        if not identifier or identifier in asset_ids:
            raise IngestionError(f"Blank or duplicate asset_id: {identifier!r}")
        asset_ids.add(identifier)
        if row["stop_id"].strip() not in stop_ids:
            raise IngestionError(f"{identifier}: unknown stop_id {row['stop_id']!r}")
        parse_coordinate(row["longitude"], "longitude", -180, 180)
        parse_coordinate(row["latitude"], "latitude", -90, 90)
        try:
            datetime.fromisoformat(row["observation_datetime"].replace("Z", "+00:00"))
        except ValueError as exc:
            raise IngestionError(f"{identifier}: invalid observation_datetime") from exc
    return manifest, stops, assets


def file_digest(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def ingest(input_dir: Path, dsn: str) -> dict[str, Any]:
    manifest, stops, assets = load_package(input_dir)
    try:
        import psycopg
        from psycopg.types.json import Jsonb
    except ImportError as exc:
        raise RuntimeError("Install requirements.txt (psycopg[binary]) to connect to PostGIS") from exc

    source_srid = int(manifest["source_crs"]["code"])
    stop_path, asset_path = input_dir / "stops.csv", input_dir / "assets.csv"
    stop_hash, asset_hash = file_digest(stop_path), file_digest(asset_path)
    run_id = stable_uuid(f"run:{stop_hash}:{asset_hash}")
    counts = {"stops": 0, "assets": 0, "observations": 0}

    with psycopg.connect(dsn) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT horizontal_srid FROM pilot.project_config WHERE project_config_id = 1")
            config = cur.fetchone()
            if config is None:
                raise IngestionError("pilot.project_config is not configured")
            target_srid = int(config[0])
            cur.execute("SELECT EXISTS (SELECT 1 FROM spatial_ref_sys WHERE srid = %s)", (target_srid,))
            if not cur.fetchone()[0]:
                raise IngestionError(f"Configured target SRID {target_srid} is absent from spatial_ref_sys")

            cur.execute(
                """INSERT INTO pilot.processing_run
                   (processing_run_id, run_name, software_name, software_version,
                    parameters, input_manifest, output_manifest, operator_id,
                    started_at, run_status, notes)
                   VALUES (%s, %s, 'Spatial Methods synthetic loader', '0.1.0',
                    %s, %s, '{}'::jsonb, 'synthetic_fixture_runner',
                    now(), 'running', 'Synthetic fixture only; not field data')
                   ON CONFLICT (processing_run_id) DO NOTHING""",
                (run_id, "synthetic-stop-asset-ingestion",
                 Jsonb({"source_srid": source_srid, "target_srid": target_srid}),
                 Jsonb({"manifest": manifest, "sha256": {"stops.csv": stop_hash, "assets.csv": asset_hash}})),
            )

            raw_ids: dict[str, str] = {}
            for filename, digest in (("stops.csv", stop_hash), ("assets.csv", asset_hash)):
                raw_id = stable_uuid(f"raw:{filename}:{digest}")
                raw_ids[filename] = raw_id
                cur.execute(
                    """INSERT INTO pilot.raw_record
                       (raw_record_id, source_filename, source_sha256, record_locator,
                        storage_uri, media_type, immutable, notes)
                       VALUES (%s, %s, %s, 'whole-file', %s, 'text/csv', true,
                               'Synthetic fixture input; original file retained in repository')
                       ON CONFLICT (raw_record_id) DO NOTHING""",
                    (raw_id, filename, digest, f"repo-fixture://{filename}"),
                )

            def add_geometry(feature_id: str, feature_type: str, row: dict[str, str]) -> None:
                lon = parse_coordinate(row["longitude"], "longitude", -180, 180)
                lat = parse_coordinate(row["latitude"], "latitude", -90, 90)
                cur.execute(
                    """INSERT INTO pilot.inventory_feature(feature_id, feature_type, geom)
                       VALUES (%s, %s,
                         ST_Transform(ST_SetSRID(ST_MakePoint(%s, %s), %s),
                                      (SELECT horizontal_srid FROM pilot.project_config WHERE project_config_id=1)))
                       ON CONFLICT (feature_id) DO NOTHING""",
                    (feature_id, feature_type, lon, lat, source_srid),
                )

            for row in stops:
                feature_id = stable_uuid(f"stop:{row['stop_id'].strip()}")
                add_geometry(feature_id, "stop", row)
                cur.execute(
                    """INSERT INTO pilot.stop
                       (feature_id, observed_name, stop_status, evidence_basis,
                        route_reference, side_of_road, observation_datetime,
                        positional_method, position_quality_class, source_observer)
                       VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                       ON CONFLICT (feature_id) DO NOTHING""",
                    (feature_id, row["observed_name"] or None, row["stop_status"],
                     row["evidence_basis"], row["route_reference"] or None,
                     row["side_of_road"] or None, row["observation_datetime"],
                     row["positional_method"], row["position_quality_class"],
                     row["source_observer"]),
                )
                observation_id = stable_uuid(f"observation:stop:{row['stop_id']}:{stop_hash}")
                cur.execute(
                    """INSERT INTO pilot.survey_observation
                       (observation_id, feature_id, raw_record_id, method,
                        observed_at, operator_id, processing_status, metadata)
                       VALUES (%s, %s, %s, 'other', %s, %s, 'raw', %s)
                       ON CONFLICT (observation_id) DO NOTHING""",
                    (observation_id, feature_id, raw_ids["stops.csv"],
                     row["observation_datetime"], row["source_observer"],
                     Jsonb({"source_crs": f"EPSG:{source_srid}", "source_record": row["stop_id"],
                            "synthetic": True, "coordinate_order": "longitude_latitude"})),
                )
                counts["stops"] += 1
                counts["observations"] += 1

            for row in assets:
                feature_id = stable_uuid(f"asset:{row['asset_id'].strip()}")
                stop_feature_id = stable_uuid(f"stop:{row['stop_id'].strip()}")
                add_geometry(feature_id, "asset", row)
                cur.execute(
                    """INSERT INTO pilot.asset
                       (feature_id, stop_id, asset_type, presence, condition,
                        observation_datetime, notes)
                       VALUES (%s, %s, %s, %s, %s, %s, %s)
                       ON CONFLICT (feature_id) DO NOTHING""",
                    (feature_id, stop_feature_id, row["asset_type"], row["presence"],
                     row["condition"] or None, row["observation_datetime"],
                     "Synthetic fixture record; not a field observation"),
                )
                observation_id = stable_uuid(f"observation:asset:{row['asset_id']}:{asset_hash}")
                cur.execute(
                    """INSERT INTO pilot.survey_observation
                       (observation_id, feature_id, raw_record_id, method,
                        observed_at, operator_id, processing_status, metadata)
                       VALUES (%s, %s, %s, 'other', %s, 'synthetic_fixture_runner',
                               'raw', %s)
                       ON CONFLICT (observation_id) DO NOTHING""",
                    (observation_id, feature_id, raw_ids["assets.csv"],
                     row["observation_datetime"],
                     Jsonb({"source_crs": f"EPSG:{source_srid}", "source_record": row["asset_id"],
                            "synthetic": True, "coordinate_order": "longitude_latitude"})),
                )
                counts["assets"] += 1
                counts["observations"] += 1

            cur.execute(
                """UPDATE pilot.processing_run
                   SET completed_at=now(), run_status='succeeded',
                       output_manifest=%s
                   WHERE processing_run_id=%s""",
                (Jsonb({"inserted_or_already_present": counts, "target_srid": target_srid}), run_id),
            )
            cur.execute(
                """SELECT count(*), count(*) FILTER (WHERE ST_SRID(geom) = %s)
                   FROM pilot.inventory_feature""",
                (target_srid,),
            )
            total_features, matching_srid = cur.fetchone()

    return {
        "status": "PASS",
        "dataset_status": "synthetic",
        "source_srid": source_srid,
        "target_srid": target_srid,
        "input_sha256": {"stops.csv": stop_hash, "assets.csv": asset_hash},
        "records_processed": counts,
        "database_features": total_features,
        "features_with_configured_srid": matching_srid,
        "processing_run_id": run_id,
        "limitations": [
            "All fixture coordinates and attributes are invented.",
            "The source coordinates use EPSG:4326 only for an isolated software test.",
            "The fixture does not represent Nairobi or any real transport stop.",
            "Successful ingestion does not establish positional accuracy or field fitness.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=Path(__file__).parent / "input")
    parser.add_argument("--dsn", default=os.environ.get("DATABASE_URL"))
    parser.add_argument("--report", type=Path, default=None)
    args = parser.parse_args()
    if not args.dsn:
        parser.error("Provide --dsn or DATABASE_URL")
    try:
        report = ingest(args.input, args.dsn)
    except (IngestionError, RuntimeError) as exc:
        print(f"INGESTION FAILED: {exc}", file=sys.stderr)
        return 1
    rendered = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.report:
        args.report.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
