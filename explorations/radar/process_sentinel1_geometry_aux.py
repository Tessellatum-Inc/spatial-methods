#!/usr/bin/env python3
"""Retrieve per-pixel Sentinel-1 local incidence angle for each temporal scene.

This is a geometry diagnostic. It does not perform terrain correction, remove
layover/shadow, validate geolocation, or establish radiometric comparability.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timedelta, timezone
import importlib.util
import json
import os
from pathlib import Path
import sys

import numpy as np
import rasterio

ROOT = Path(__file__).resolve().parents[2]
RADAR = Path(__file__).resolve().parent
_PROCESS_SPEC = importlib.util.spec_from_file_location(
    "process_sentinelhub_sentinel1", RADAR / "process_sentinelhub_sentinel1.py"
)
_PROCESS = importlib.util.module_from_spec(_PROCESS_SPEC)
_PROCESS_SPEC.loader.exec_module(_PROCESS)

EVALSCRIPT = """//VERSION=3
function setup() {
  return {
    input: [{
      bands: ["localIncidenceAngle", "dataMask"],
      units: ["DN", "DN"]
    }],
    output: { bands: 2, sampleType: "FLOAT32" }
  };
}
function evaluatePixel(sample) {
  return [sample.localIncidenceAngle, sample.dataMask];
}
"""


def build_angle_payload(feature: dict, width: int = _PROCESS.WIDTH,
                        height: int = _PROCESS.HEIGHT) -> dict:
    if not 1 <= width <= 2500 or not 1 <= height <= 2500:
        raise ValueError("Output width and height must each be between 1 and 2500.")
    stamp = feature.get("properties", {}).get("datetime")
    if not isinstance(stamp, str):
        raise ValueError("Catalogue feature has no acquisition datetime.")
    acquired = datetime.fromisoformat(stamp.replace("Z", "+00:00"))
    if acquired.tzinfo is None:
        raise ValueError("Acquisition datetime must include a timezone.")
    acquired = acquired.astimezone(timezone.utc)
    start = (acquired - timedelta(seconds=1)).isoformat(timespec="milliseconds").replace("+00:00", "Z")
    end = (acquired + timedelta(seconds=1)).isoformat(timespec="milliseconds").replace("+00:00", "Z")
    return {
        "input": {
            "bounds": {
                "bbox": _PROCESS.NAIROBI_BBOX,
                "properties": {"crs": "http://www.opengis.net/def/crs/OGC/1.3/CRS84"},
            },
            "data": [{
                "type": "sentinel-1-grd",
                "dataFilter": {"timeRange": {"from": start, "to": end},
                               "mosaickingOrder": "mostRecent"},
                "processing": {"orthorectify": True, "backCoeff": "GAMMA0_ELLIPSOID"},
            }],
        },
        "output": {
            "width": width, "height": height,
            "responses": [{"identifier": "default", "format": {"type": "image/tiff"}}],
        },
        "evalscript": EVALSCRIPT,
    }


def summarize_angle(values: np.ndarray, valid: np.ndarray) -> dict:
    values = np.asarray(values, dtype=np.float32)
    valid = np.asarray(valid, dtype=bool)
    if values.shape != valid.shape or values.ndim != 2:
        raise ValueError("Angle and validity arrays must be matching 2D arrays.")
    selected = values[valid]
    if selected.size == 0:
        raise ValueError("No valid local-incidence-angle pixels.")
    if not np.isfinite(selected).all():
        raise ValueError("Non-finite local incidence angle in valid pixels.")
    if np.any((selected < 0) | (selected > 180)):
        raise ValueError("Local incidence angle outside documented 0–180 degree range.")
    q = np.percentile(selected, [1, 5, 25, 50, 75, 95, 99])
    return {
        "valid_pixels": int(selected.size),
        "valid_fraction": float(valid.mean()),
        "min_degrees": float(selected.min()),
        "p01_degrees": float(q[0]),
        "p05_degrees": float(q[1]),
        "p25_degrees": float(q[2]),
        "median_degrees": float(q[3]),
        "p75_degrees": float(q[4]),
        "p95_degrees": float(q[5]),
        "p99_degrees": float(q[6]),
        "max_degrees": float(selected.max()),
    }


def process_stack(stack_metadata: Path, output_dir: Path, timeout: int = 240) -> dict:
    stack = json.loads(stack_metadata.read_text(encoding="utf-8"))
    scenes = stack.get("scenes")
    if not isinstance(scenes, list) or len(scenes) < 2:
        raise ValueError("Stack metadata must contain at least two processed scenes.")
    client_id = os.environ.get("SENTINEL_HUB_CLIENT_ID", "")
    client_secret = os.environ.get("SENTINEL_HUB_CLIENT_SECRET", "")
    token = _PROCESS._CATALOG.request_access_token(client_id, client_secret, timeout=30)
    output_dir.mkdir(parents=True, exist_ok=True)
    records = []
    failures = []
    for scene in scenes:
        try:
            target = datetime.fromisoformat(
                scene["catalog_item_datetime_utc"].replace("Z", "+00:00")
            ).astimezone(timezone.utc)
            feature = _PROCESS._CATALOG.search_catalog(
                token,
                _PROCESS._CATALOG.build_search_payload(
                    (target - timedelta(minutes=2)).isoformat(timespec="seconds").replace("+00:00", "Z"),
                    (target + timedelta(minutes=2)).isoformat(timespec="seconds").replace("+00:00", "Z"),
                    100,
                ),
                timeout=min(timeout, 60),
            )
            matches = []
            for item in feature.get("features", []):
                stamp = item.get("properties", {}).get("datetime")
                if not isinstance(stamp, str):
                    continue
                try:
                    acquired = datetime.fromisoformat(stamp.replace("Z", "+00:00"))
                except ValueError:
                    continue
                if acquired.tzinfo is None:
                    continue
                delta = abs((acquired.astimezone(timezone.utc) - target).total_seconds())
                covers, _ = _PROCESS.feature_coverage(item)
                if delta <= 120 and covers:
                    matches.append((delta, item))
            if not matches:
                raise ValueError(f"No full-coverage catalogue item matches {target.isoformat()} within 120 seconds.")
            matches.sort(key=lambda item: item[0])
            feature_item = matches[0][1]
            payload = build_angle_payload(feature_item)
            body = _PROCESS.request_geotiff(token, payload, timeout=timeout)
            stamp = target.strftime("%Y%m%dT%H%M%SZ")
            path = output_dir / f"sentinel1_nairobi_{stamp}_local-incidence-angle.tif"
            path.write_bytes(body)
            source_raster = Path("data/sentinelhub/nairobi/stack") / scene["output"]["file"]
            with rasterio.open(source_raster) as reference, rasterio.open(path) as ds:
                if ds.count != 2 or ds.crs != reference.crs or ds.transform != reference.transform or (ds.width, ds.height) != (reference.width, reference.height):
                    raise ValueError("Angle raster grid/bands do not match its corresponding VV/VH scene.")
                angle = ds.read(1)
                mask = ds.read(2) > 0.5
                stats = summarize_angle(angle, mask)
            records.append({
                "acquisition_datetime_utc": target.isoformat().replace("+00:00", "Z"),
                "catalog_item_id": feature_item.get("id"),
                "file": path.name,
                "reference_vv_vh_file": scene["output"]["file"],
                "grid_matches_reference": True,
                "local_incidence_angle": stats,
            })
            print(f"Local incidence angle processed: {path}; median={stats['median_degrees']:.3f} degrees")
        except (KeyError, OSError, ValueError, RuntimeError) as exc:
            failures.append({"scene": scene.get("catalog_item_datetime_utc"), "error": str(exc)})
            print(f"Geometry auxiliary failed: {exc}", file=sys.stderr)

    report = {
        "schema": "tessellatum.sentinel1.local-incidence-angle-screen.v1",
        "created_at_utc": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "source": "Copernicus Data Space Sentinel Hub Sentinel-1 GRD Process API",
        "processing": {
            "band": "localIncidenceAngle",
            "units": "degrees",
            "orthorectify": True,
            "backscatter_coefficient_context": "GAMMA0_ELLIPSOID (angle itself is geometry, not backscatter)",
            "bbox_crs84": _PROCESS.NAIROBI_BBOX,
            "width": _PROCESS.WIDTH,
            "height": _PROCESS.HEIGHT,
        },
        "scene_count": len(scenes),
        "processed_count": len(records),
        "failed_count": len(failures),
        "scenes": records,
        "failures": failures,
        "status": "geometry_angle_screen_only" if not failures and len(records) == len(scenes) else "incomplete_geometry_angle_screen",
        "analysis_ready": False,
        "limitations": [
            "Local incidence angle is an auxiliary geometry layer, not a geolocation accuracy or co-registration measurement.",
            "This request does not enable radiometric terrain correction, scatteringArea, or shadowMask.",
            "No DEM-derived slope/aspect, layover/shadow exclusion, precise-orbit comparison, or stable tie-point validation is performed.",
            "Angle distributions are summarized over the rectangular request grid; they are not a county-only summary.",
            "Do not use these outputs to normalize backscatter automatically.",
        ],
    }
    report_path = output_dir / "sentinel1_nairobi_local_incidence_angle_screen.json"
    report_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    if failures or len(records) != len(scenes):
        raise RuntimeError(f"Local incidence angle processing incomplete: {len(records)}/{len(scenes)} scenes.")
    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--stack-metadata", type=Path, default=Path("data/sentinelhub/nairobi/stack/sentinel1_nairobi_temporal_stack.metadata.json"))
    parser.add_argument("--output-dir", type=Path, default=Path("data/sentinelhub/nairobi/stack/geometry_aux"))
    parser.add_argument("--timeout", type=int, default=240)
    args = parser.parse_args(argv)
    try:
        report = process_stack(args.stack_metadata, args.output_dir, args.timeout)
    except (OSError, ValueError, RuntimeError) as exc:
        parser.exit(2, f"Local incidence angle screen failed: {exc}\n")
    print(f"Processed local incidence angle for {report['processed_count']} scenes; analysis_ready=false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
