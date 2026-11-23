#!/usr/bin/env python3
"""Process a fixed-grid multi-date Sentinel-1 Nairobi candidate stack via Sentinel Hub.

Uses OAuth client_credentials and the Process API. Catalogue candidates come
from the repository inventory; each date is independently re-resolved against
the live Sentinel Hub catalogue.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timedelta, timezone
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
RADAR = Path(__file__).resolve().parent
_BUILDER_SPEC = importlib.util.spec_from_file_location(
    "build_sentinel1_stack_manifest", RADAR / "build_sentinel1_stack_manifest.py"
)
_BUILDER = importlib.util.module_from_spec(_BUILDER_SPEC)
_BUILDER_SPEC.loader.exec_module(_BUILDER)
_PROCESS_SPEC = importlib.util.spec_from_file_location(
    "process_sentinelhub_sentinel1", RADAR / "process_sentinelhub_sentinel1.py"
)
_PROCESS = importlib.util.module_from_spec(_PROCESS_SPEC)
_PROCESS_SPEC.loader.exec_module(_PROCESS)

CATALOGUE_METADATA_FIELDS = (
    "platform",
    "constellation",
    "instruments",
    "datetime",
    "start_datetime",
    "end_datetime",
    "sat:orbit_state",
    "sat:relative_orbit",
    "sat:absolute_orbit",
    "sar:instrument_mode",
    "sar:product_type",
    "sar:polarizations",
    "sar:observation_direction",
    "sar:frequency_band",
    "sar:center_frequency",
    "sar:resolution_range",
    "sar:resolution_azimuth",
    "sar:pixel_spacing_range",
    "sar:pixel_spacing_azimuth",
    "s1:polarization",
    "s1:resolution",
    "s1:timeliness",
    "view:incidence_angle",
    "processing:datetime",
    "processing:facility",
    "processing:software",
    "processing:version",
)


def catalogue_acquisition_metadata(feature: dict) -> dict:
    """Retain relevant STAC/Sentinel-1 acquisition properties without inference."""
    properties = feature.get("properties", {})
    if not isinstance(properties, dict):
        return {}
    return {
        key: properties[key]
        for key in CATALOGUE_METADATA_FIELDS
        if key in properties and properties[key] is not None
    }


def resolve_feature(token: str, target: datetime, timeout: int) -> dict:
    start = (target - timedelta(minutes=2)).isoformat(timespec="seconds").replace("+00:00", "Z")
    end = (target + timedelta(minutes=2)).isoformat(timespec="seconds").replace("+00:00", "Z")
    query = _PROCESS._CATALOG.build_search_payload(start, end, 100)
    result = _PROCESS._CATALOG.search_catalog(token, query, timeout=min(timeout, 60))
    matches = []
    for feature in result["features"]:
        stamp = feature.get("properties", {}).get("datetime")
        if not isinstance(stamp, str):
            continue
        try:
            acquired = datetime.fromisoformat(stamp.replace("Z", "+00:00"))
        except ValueError:
            continue
        if acquired.tzinfo is None:
            continue
        if abs((acquired.astimezone(timezone.utc) - target).total_seconds()) > 120:
            continue
        covers, fraction = _PROCESS.feature_coverage(feature)
        if covers:
            matches.append((abs((acquired.astimezone(timezone.utc) - target).total_seconds()), feature))
    if not matches:
        raise ValueError(
            f"No live Sentinel Hub catalogue item within 120 seconds of {target.isoformat()} "
            "fully covers the Nairobi discovery rectangle."
        )
    matches.sort(key=lambda pair: pair[0])
    return matches[0][1]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--inventory", type=Path, default=ROOT / "explorations/radar/nairobi-sentinel-1-catalogue-inventory.csv")
    parser.add_argument("--output-dir", type=Path, default=Path("data/sentinelhub/nairobi/stack"))
    parser.add_argument("--timeout", type=int, default=240)
    parser.add_argument("--max-scenes", type=int, default=4)
    args = parser.parse_args(argv)
    if args.timeout < 30 or not 2 <= args.max_scenes <= 12:
        parser.error("--timeout must be >=30 and --max-scenes between 2 and 12")

    try:
        rows, inventory_digest = _BUILDER.load_inventory(args.inventory)
        manifest = _BUILDER.build_manifest(rows, inventory_digest, args.inventory.as_posix())
        candidates = manifest["candidates"][:args.max_scenes]
        if len(candidates) < 2:
            raise ValueError("At least two catalogue candidates are required for a temporal stack.")
        if manifest["temporal_sampling"]["status"] != "regular_12_day_candidate_cadence":
            raise ValueError("Candidate cadence is not a regular 12-day sequence; refusing stack processing.")
        client_id = os.environ.get("SENTINEL_HUB_CLIENT_ID", "")
        client_secret = os.environ.get("SENTINEL_HUB_CLIENT_SECRET", "")
        token = _PROCESS._CATALOG.request_access_token(client_id, client_secret, timeout=30)
    except (OSError, ValueError, RuntimeError) as exc:
        print(f"Cannot prepare Sentinel-1 stack: {exc}", file=sys.stderr)
        return 2

    args.output_dir.mkdir(parents=True, exist_ok=True)
    outputs = []
    failures = []
    processing_config = {
        "bbox_crs84": _PROCESS.NAIROBI_BBOX,
        "width": _PROCESS.WIDTH,
        "height": _PROCESS.HEIGHT,
        "bands": ["VV", "VH", "dataMask"],
        "polarization_units": "LINEAR_POWER",
        "backscatter_coefficient": "GAMMA0_ELLIPSOID",
        "orthorectify": True,
        "temporal_match_tolerance_seconds": 120,
    }
    config_sha = hashlib.sha256(
        json.dumps(processing_config, sort_keys=True).encode("utf-8")
    ).hexdigest()

    for candidate in candidates:
        target = datetime.fromisoformat(
            candidate["sensing_start_utc"].replace("Z", "+00:00")
        ).astimezone(timezone.utc)
        try:
            feature = resolve_feature(token, target, args.timeout)
            payload = _PROCESS.build_process_payload(feature)
            raster = _PROCESS.request_geotiff(token, payload, timeout=args.timeout)
            acquired = datetime.fromisoformat(
                feature["properties"]["datetime"].replace("Z", "+00:00")
            ).astimezone(timezone.utc)
            stamp = acquired.strftime("%Y%m%dT%H%M%SZ")
            raster_name = f"sentinel1_nairobi_stack_{stamp}_vv-vh.tif"
            metadata_name = f"sentinel1_nairobi_stack_{stamp}_vv-vh.metadata.json"
            raster_path = args.output_dir / raster_name
            raster_path.write_bytes(raster)
            metadata = {
                "catalog_item_id": feature.get("id"),
                "catalog_item_datetime_utc": acquired.isoformat().replace("+00:00", "Z"),
                "catalogue_acquisition_metadata": catalogue_acquisition_metadata(feature),
                "inventory_product_id": candidate["product_id"],
                "inventory_product_name": candidate["product_name"],
                "inventory_sensing_start_utc": candidate["sensing_start_utc"],
                "catalogue_footprint_covers_search_rectangle": True,
                "processing_config": processing_config,
                "processing_config_sha256": config_sha,
                "output": {
                    "file": raster_name,
                    "width": _PROCESS.WIDTH,
                    "height": _PROCESS.HEIGHT,
                    "bytes": len(raster),
                    "sha256": hashlib.sha256(raster).hexdigest(),
                },
                "analysis_ready": False,
                "limitations": [
                    "Same bbox and pixel dimensions establish a common requested grid, not verified sub-pixel co-registration.",
                    "Catalogue slice selection may not represent a complete datatake; inspect seams and edge coverage.",
                    "Radiometric comparability and geometric registration remain unvalidated.",
                    "This is a processed subset, not an original SAFE archive.",
                    "Catalogue metadata availability varies; missing orbit or viewing fields are not inferred.",
                ],
            }
            (args.output_dir / metadata_name).write_text(
                json.dumps(metadata, indent=2) + "\n", encoding="utf-8"
            )
            outputs.append(metadata)
            print(f"Processed {acquired.isoformat()} -> {raster_path}")
        except (ValueError, RuntimeError, OSError) as exc:
            failures.append({"inventory_product_id": candidate["product_id"], "error": str(exc)})
            print(f"Scene failed ({candidate['sensing_start_utc']}): {exc}", file=sys.stderr)

    stack = {
        "schema": "tessellatum.sentinel1.processed-stack.v1",
        "inventory_sha256": inventory_digest,
        "processing_config_sha256": config_sha,
        "processing_config": processing_config,
        "candidate_count": len(candidates),
        "processed_count": len(outputs),
        "failed_count": len(failures),
        "scenes": outputs,
        "failures": failures,
        "stack_status": "processed_candidates_pending_geometric_and_radiometric_qa"
        if len(outputs) >= 2 else "insufficient_processed_scenes",
        "analysis_ready": False,
    }
    stack_path = args.output_dir / "sentinel1_nairobi_temporal_stack.metadata.json"
    stack_path.write_text(json.dumps(stack, indent=2) + "\n", encoding="utf-8")
    print(f"Stack manifest: {stack_path}")
    print(f"Processed scenes: {len(outputs)}; failures: {len(failures)}")
    return 0 if len(outputs) >= 2 and not failures else 2


if __name__ == "__main__":
    raise SystemExit(main())
