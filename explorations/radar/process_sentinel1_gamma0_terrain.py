#!/usr/bin/env python3
"""Retrieve parallel Sentinel-1 terrain-corrected backscatter and geometry layers.

The ellipsoid-corrected temporal stack is not modified. This script requests
GAMMA0_TERRAIN on the same per-scene grid and retains RTC auxiliary bands.
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

BANDS = ["VV", "VH", "scatteringArea", "localIncidenceAngle", "shadowMask", "dataMask"]
EVALSCRIPT = """//VERSION=3
function setup() {
  return {
    input: [{
      bands: ["VV", "VH", "scatteringArea", "localIncidenceAngle", "shadowMask", "dataMask"],
      units: ["LINEAR_POWER", "LINEAR_POWER", "DN", "DN", "DN", "DN"]
    }],
    output: { bands: 6, sampleType: "FLOAT32" }
  };
}
function evaluatePixel(sample) {
  return [
    sample.VV,
    sample.VH,
    sample.scatteringArea,
    sample.localIncidenceAngle,
    sample.shadowMask,
    sample.dataMask
  ];
}
"""


def build_rtc_payload(feature: dict, width: int = _PROCESS.WIDTH,
                      height: int = _PROCESS.HEIGHT,
                      dem_instance: str = "COPERNICUS_30",
                      oversampling: int = 2) -> dict:
    if not 1 <= width <= 2500 or not 1 <= height <= 2500:
        raise ValueError("Output width and height must each be between 1 and 2500.")
    if dem_instance not in {"COPERNICUS_30", "COPERNICUS_90"}:
        raise ValueError("DEM must be COPERNICUS_30 or COPERNICUS_90.")
    if not 1 <= oversampling <= 4:
        raise ValueError("Radiometric terrain oversampling must be between 1 and 4.")
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
                "processing": {
                    "orthorectify": True,
                    "backCoeff": "GAMMA0_TERRAIN",
                    "demInstance": dem_instance,
                    "radiometricTerrainOversampling": oversampling,
                },
            }],
        },
        "output": {
            "width": width,
            "height": height,
            "responses": [{"identifier": "default", "format": {"type": "image/tiff"}}],
        },
        "evalscript": EVALSCRIPT,
    }


def summarize_rtc(array: np.ndarray) -> dict:
    data = np.asarray(array, dtype=np.float32)
    if data.ndim != 3 or data.shape[0] != 6:
        raise ValueError("RTC array must have six bands in the documented order.")
    valid = (data[5] > 0.5) & np.isfinite(data[:5]).all(axis=0)
    if not valid.any():
        raise ValueError("RTC raster contains no valid pixels.")
    vv, vh, area, angle, shadow = (data[i][valid] for i in range(5))
    if np.any((angle < 0) | (angle > 180)):
        raise ValueError("Local incidence angle outside 0–180 degrees.")
    if np.any((shadow < 0) | (shadow > 1)):
        raise ValueError("Shadow mask contains values outside 0–1.")
    if np.any(vv < 0) or np.any(vh < 0):
        raise ValueError("Linear-power RTC backscatter cannot be negative.")
    def quantiles(values):
        q = np.percentile(values, [1, 5, 25, 50, 75, 95, 99])
        return {
            "min": float(np.min(values)), "p01": float(q[0]), "p05": float(q[1]),
            "p25": float(q[2]), "median": float(q[3]), "p75": float(q[4]),
            "p95": float(q[5]), "p99": float(q[6]), "max": float(np.max(values)),
        }
    def db(value):
        return float(10.0 * np.log10(value)) if value > 0 else None
    return {
        "valid_pixels": int(valid.sum()),
        "valid_fraction": float(valid.mean()),
        "vv_linear_power": quantiles(vv),
        "vh_linear_power": quantiles(vh),
        "vv_median_db": db(float(np.median(vv))),
        "vh_median_db": db(float(np.median(vh))),
        "scattering_area": quantiles(area),
        "local_incidence_angle_degrees": quantiles(angle),
        "shadow_mask_fraction_of_valid_pixels": float(np.mean(shadow > 0.5)),
        "shadow_mask_flagged_pixels": int(np.count_nonzero(shadow > 0.5)),
    }


def process_stack(stack_metadata: Path, output_dir: Path, timeout: int = 300,
                  dem_instance: str = "COPERNICUS_30", oversampling: int = 2) -> dict:
    stack = json.loads(stack_metadata.read_text(encoding="utf-8"))
    scenes = stack.get("scenes")
    if not isinstance(scenes, list) or len(scenes) < 2:
        raise ValueError("Stack metadata must contain at least two processed scenes.")
    client_id = os.environ.get("SENTINEL_HUB_CLIENT_ID", "")
    client_secret = os.environ.get("SENTINEL_HUB_CLIENT_SECRET", "")
    token = _PROCESS._CATALOG.request_access_token(client_id, client_secret, timeout=30)
    output_dir.mkdir(parents=True, exist_ok=True)
    records, failures = [], []
    for scene in scenes:
        try:
            target = datetime.fromisoformat(
                scene["catalog_item_datetime_utc"].replace("Z", "+00:00")
            ).astimezone(timezone.utc)
            search = _PROCESS._CATALOG.build_search_payload(
                (target - timedelta(minutes=2)).isoformat(timespec="seconds").replace("+00:00", "Z"),
                (target + timedelta(minutes=2)).isoformat(timespec="seconds").replace("+00:00", "Z"),
                100,
            )
            result = _PROCESS._CATALOG.search_catalog(token, search, timeout=60)
            matches = []
            for item in result.get("features", []):
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
            matches.sort(key=lambda pair: pair[0])
            feature = matches[0][1]
            payload = build_rtc_payload(feature, dem_instance=dem_instance, oversampling=oversampling)
            body = _PROCESS.request_geotiff(token, payload, timeout=timeout)
            stamp = target.strftime("%Y%m%dT%H%M%SZ")
            path = output_dir / f"sentinel1_nairobi_{stamp}_gamma0-terrain-rtc.tif"
            path.write_bytes(body)
            reference_path = Path("data/sentinelhub/nairobi/stack") / scene["output"]["file"]
            with rasterio.open(reference_path) as reference, rasterio.open(path) as ds:
                if (ds.count != 6 or ds.crs != reference.crs or ds.transform != reference.transform
                        or (ds.width, ds.height) != (reference.width, reference.height)):
                    raise ValueError("RTC raster grid/bands do not match corresponding ellipsoid reference.")
                stats = summarize_rtc(ds.read())
            records.append({
                "acquisition_datetime_utc": target.isoformat().replace("+00:00", "Z"),
                "catalog_item_id": feature.get("id"),
                "file": path.name,
                "reference_ellipsoid_file": scene["output"]["file"],
                "grid_matches_ellipsoid_reference": True,
                "statistics": stats,
            })
            print(f"RTC processed: {path}; shadow fraction={stats['shadow_mask_fraction_of_valid_pixels']:.5f}")
        except (KeyError, OSError, ValueError, RuntimeError) as exc:
            failures.append({"scene": scene.get("catalog_item_datetime_utc"), "error": str(exc)})
            print(f"RTC scene failed: {exc}", file=sys.stderr)

    report = {
        "schema": "tessellatum.sentinel1.gamma0-terrain-rtc-screen.v1",
        "created_at_utc": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "source": "Copernicus Data Space Sentinel Hub Sentinel-1 GRD Process API",
        "processing": {
            "backscatter_coefficient": "GAMMA0_TERRAIN",
            "orthorectify": True,
            "dem_instance": dem_instance,
            "radiometric_terrain_oversampling": oversampling,
            "bands": BANDS,
            "polarization_units": "LINEAR_POWER",
            "bbox_crs84": _PROCESS.NAIROBI_BBOX,
            "width": _PROCESS.WIDTH,
            "height": _PROCESS.HEIGHT,
        },
        "scene_count": len(scenes),
        "processed_count": len(records),
        "failed_count": len(failures),
        "scenes": records,
        "failures": failures,
        "status": "rtc_parallel_diagnostic_only" if not failures and len(records) == len(scenes) else "incomplete_rtc_diagnostic",
        "analysis_ready": False,
        "limitations": [
            "Terrain-corrected outputs are a separate processing branch; ellipsoid-corrected source rasters remain unchanged.",
            "Copernicus DEM 30 m is used for radiometric terrain correction and orthorectification; terrain and DEM limitations remain.",
            "scatteringArea and shadowMask are processing diagnostics, not a substitute for independent terrain or geolocation validation.",
            "No automatic normalization, threshold-based deletion, or change detection is performed.",
            "Grid equality does not establish sub-pixel co-registration or radiometric equivalence between processing branches.",
        ],
    }
    (output_dir / "sentinel1_nairobi_gamma0_terrain_rtc_screen.json").write_text(
        json.dumps(report, indent=2) + "\n", encoding="utf-8"
    )
    if failures or len(records) != len(scenes):
        raise RuntimeError(f"RTC processing incomplete: {len(records)}/{len(scenes)} scenes.")
    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--stack-metadata", type=Path, default=Path("data/sentinelhub/nairobi/stack/sentinel1_nairobi_temporal_stack.metadata.json"))
    parser.add_argument("--output-dir", type=Path, default=Path("data/sentinelhub/nairobi/stack/terrain_aux"))
    parser.add_argument("--timeout", type=int, default=300)
    parser.add_argument("--dem-instance", choices=["COPERNICUS_30", "COPERNICUS_90"], default="COPERNICUS_30")
    parser.add_argument("--oversampling", type=int, choices=[1, 2, 3, 4], default=2)
    args = parser.parse_args(argv)
    try:
        report = process_stack(args.stack_metadata, args.output_dir, args.timeout,
                               args.dem_instance, args.oversampling)
    except (OSError, ValueError, RuntimeError) as exc:
        parser.exit(2, f"RTC processing failed: {exc}\n")
    print(f"Processed terrain-corrected backscatter for {report['processed_count']} scenes; analysis_ready=false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
