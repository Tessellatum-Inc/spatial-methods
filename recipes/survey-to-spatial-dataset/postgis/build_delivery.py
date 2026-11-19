#!/usr/bin/env python3
"""Build a GeoPackage and portable ZIP handover from the synthetic PostGIS rehearsal."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path

OUTPUT = Path(os.environ.get("DELIVERY_DIR", "/output"))
QA_REPORT = OUTPUT / "spatial-qa-report.json"
GPKG = OUTPUT / "spatial-methods-pilot.gpkg"
PACKAGE_DIR = OUTPUT / "spatial-methods-pilot-delivery"
ARCHIVE = OUTPUT / "spatial-methods-pilot-delivery.zip"
PG = os.environ.get(
    "OGR_PG_CONNECTION_STRING",
    "PG:host=postgis port=5432 dbname=spatial_methods_test "
    "user=spatial_methods password=spatial_methods_local_only",
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def run(command: list[str]) -> None:
    subprocess.run(command, check=True)


def main() -> int:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    if not QA_REPORT.is_file():
        raise SystemExit("Missing spatial-qa-report.json; run spatial QA successfully first.")
    qa = json.loads(QA_REPORT.read_text(encoding="utf-8"))
    if qa.get("status") not in {"PASS", "PASS_WITH_REVIEW_FLAGS"}:
        raise SystemExit("QA report is not in a deliverable state.")
    if qa.get("dataset_status") != "synthetic":
        raise SystemExit("This delivery builder accepts synthetic fixtures only.")

    GPKG.unlink(missing_ok=True)
    stop_sql = """
      SELECT f.feature_id::text AS feature_id, s.observed_name, s.stop_status,
             s.evidence_basis, s.route_reference, s.side_of_road,
             s.observation_datetime, s.positional_method,
             s.position_quality_class, s.source_observer, f.geom
      FROM pilot.inventory_feature AS f
      JOIN pilot.stop AS s ON s.feature_id = f.feature_id
      ORDER BY f.feature_id
    """
    asset_sql = """
      SELECT f.feature_id::text AS feature_id, a.stop_id::text AS parent_stop_id,
             a.asset_type, a.presence, a.condition, a.accessibility_observation,
             a.observation_datetime, a.evidence_ref, a.notes, f.geom
      FROM pilot.inventory_feature AS f
      JOIN pilot.asset AS a ON a.feature_id = f.feature_id
      ORDER BY f.feature_id
    """
    run(["ogr2ogr", "-f", "GPKG", str(GPKG), PG, "-sql", stop_sql,
         "-nln", "stops", "-nlt", "POINT", "-lco", "SPATIAL_INDEX=YES"])
    run(["ogr2ogr", "-f", "GPKG", "-update", str(GPKG), PG, "-sql", asset_sql,
         "-nln", "assets", "-nlt", "POINT", "-lco", "SPATIAL_INDEX=YES"])

    info = subprocess.run(
        ["ogrinfo", "-ro", "-so", str(GPKG)],
        check=True, capture_output=True, text=True
    ).stdout
    if "stops" not in info or "assets" not in info:
        raise SystemExit("GeoPackage validation did not find both expected layers.")

    PACKAGE_DIR.mkdir(parents=True, exist_ok=True)
    (PACKAGE_DIR / GPKG.name).write_bytes(GPKG.read_bytes())
    (PACKAGE_DIR / "spatial-qa-report.json").write_bytes(QA_REPORT.read_bytes())
    manifest = {
        "package_name": "Spatial Methods synthetic pilot delivery",
        "package_version": "0.1.0",
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "dataset_status": "synthetic",
        "project_srid": qa.get("project_srid"),
        "layers": [
            {"name": "stops", "geometry": "Point", "count": qa.get("stop_count", 0)},
            {"name": "assets", "geometry": "Point", "count": qa.get("asset_count", 0)},
        ],
        "qa_status": qa["status"],
        "qa_report": "spatial-qa-report.json",
        "limitations": [
            "All features and attributes are invented software fixtures.",
            "The EPSG:3857 CRS is used only for the isolated software integration test.",
            "The data do not represent Nairobi or real transport stops/assets.",
            "The package does not establish positional accuracy or operational fitness.",
            "No independent positional reference observations are available.",
        ],
        "files": {
            GPKG.name: {"sha256": sha256(GPKG), "bytes": GPKG.stat().st_size},
            "spatial-qa-report.json": {
                "sha256": sha256(PACKAGE_DIR / "spatial-qa-report.json"),
                "bytes": (PACKAGE_DIR / "spatial-qa-report.json").stat().st_size,
            },
        },
    }
    (PACKAGE_DIR / "delivery-manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    readme = """# Spatial Methods synthetic pilot delivery

This portable handover contains a GeoPackage with stops and assets point
layers, the machine-readable spatial QA report, and a delivery manifest with
file hashes and explicit limitations.

**Synthetic software fixture only.** The EPSG:3857 CRS is used solely by the
isolated integration test. These records do not represent Nairobi or real
transport infrastructure. This package is not positional-accuracy evidence,
a legal survey, an accessibility certification, or an operational inventory.

Open spatial-methods-pilot.gpkg in QGIS or another GeoPackage-compatible GIS.
Inspect spatial-qa-report.json and delivery-manifest.json before use.
"""
    (PACKAGE_DIR / "README.md").write_text(readme, encoding="utf-8")
    ARCHIVE.unlink(missing_ok=True)
    with zipfile.ZipFile(ARCHIVE, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for file in sorted(PACKAGE_DIR.iterdir()):
            archive.write(file, arcname=f"spatial-methods-pilot-delivery/{file.name}")

    print(json.dumps({
        "status": "PASS",
        "dataset_status": "synthetic",
        "geopackage": str(GPKG),
        "layers": ["stops", "assets"],
        "delivery_archive": str(ARCHIVE),
        "archive_sha256": sha256(ARCHIVE),
    }, indent=2))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except subprocess.CalledProcessError as exc:
        print(f"DELIVERY BUILD FAILED: {exc}", file=sys.stderr)
        raise SystemExit(exc.returncode or 1)
