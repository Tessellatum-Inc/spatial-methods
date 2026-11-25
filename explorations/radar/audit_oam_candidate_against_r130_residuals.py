#!/usr/bin/env python3
"""Intersect OAM STAC candidate footprints with georeferenced R130 residual support.

This is a raster-grid overlap audit, not a source-image registration or
positional-accuracy assessment. Residual nodata is treated as unavailable
common support for the corresponding date/burst/polarization map.
"""
from __future__ import annotations
import argparse, json, re
from pathlib import Path
from datetime import datetime, timezone
import numpy as np
import rasterio
from rasterio.features import geometry_mask
from rasterio.warp import transform_geom

DATE_RE = re.compile(r"(20\d{2})-(\d{2})-(\d{2})")
BURST_RE = re.compile(r"(T130-\d{6}-IW3)")
POL_RE = re.compile(r"_(VV|VH)_")


def inspect_raster(path: Path, geometry_wgs84: dict) -> dict:
    with rasterio.open(path) as ds:
        if ds.crs is None:
            raise ValueError(f"Residual raster has no CRS: {path}")
        geom = transform_geom("EPSG:4326", ds.crs, geometry_wgs84, precision=3)
        footprint = geometry_mask([geom], out_shape=(ds.height, ds.width),
                                  transform=ds.transform, invert=True,
                                  all_touched=False)
        values = ds.read(1)
        valid = np.isfinite(values)
        if ds.nodata is not None:
            if np.isnan(ds.nodata):
                valid &= ~np.isnan(values)
            else:
                valid &= values != ds.nodata
        footprint_count = int(footprint.sum())
        valid_count = int((footprint & valid).sum())
        date_match = DATE_RE.search(path.name)
        burst_match = BURST_RE.search(path.name)
        pol_match = POL_RE.search(path.name)
        if not (date_match and burst_match and pol_match):
            raise ValueError(f"Cannot parse date/burst/polarization from {path.name}")
        pixel_area = abs(ds.res[0] * ds.res[1])
        return {
            "file": path.name,
            "date": "-".join(date_match.groups()),
            "burst": burst_match.group(1),
            "polarization": pol_match.group(1),
            "crs": ds.crs.to_string(),
            "pixel_size": list(ds.res),
            "candidate_footprint_pixel_centres": footprint_count,
            "candidate_footprint_valid_residual_pixels": valid_count,
            "valid_fraction_within_candidate": (valid_count / footprint_count if footprint_count else None),
            "candidate_supported_area_km2": valid_count * pixel_area / 1_000_000,
        }


def audit(audit_json: Path, residual_dir: Path) -> dict:
    source = json.loads(audit_json.read_text(encoding="utf-8"))
    candidates = source.get("items", [])
    if not candidates:
        raise ValueError("OAM audit contains no candidate items")
    rows = []
    for item in candidates:
        geometry = item.get("geometry")
        if not geometry:
            continue
        item_rows = [inspect_raster(p, geometry) for p in sorted(residual_dir.glob("*_delta-residual-db.tif"))]
        if len(item_rows) != 30:
            raise ValueError(f"Expected 30 R130 residual maps; found {len(item_rows)}")
        grouped = {}
        for row in item_rows:
            key = (row["date"], row["burst"])
            grouped.setdefault(key, {})[row["polarization"]] = row
        date_burst = []
        for (day, burst), pols in sorted(grouped.items()):
            vv, vh = pols.get("VV"), pols.get("VH")
            date_burst.append({
                "date": day, "burst": burst,
                "VV_candidate_pixels": vv["candidate_footprint_valid_residual_pixels"] if vv else 0,
                "VH_candidate_pixels": vh["candidate_footprint_valid_residual_pixels"] if vh else 0,
                "both_polarizations_supported": bool(vv and vh and vv["candidate_footprint_valid_residual_pixels"] > 0 and vh["candidate_footprint_valid_residual_pixels"] > 0),
            })
        rows.append({"item_id": item.get("id"), "producer": item.get("producer_name"),
                     "acquisition_start": item.get("start_datetime"), "acquisition_end": item.get("end_datetime"),
                     "gsd_m": item.get("gsd"), "license": item.get("license"),
                     "catalogue_source_metadata_status": (item.get("source_metadata") or {}).get("status"),
                     "maps": item_rows, "date_burst_support": date_burst})
    if not rows:
        raise ValueError("No candidate item had a usable catalogue geometry")
    return {
        "schema": "tessellatum.nairobi-r130-oam-residual-support-audit.v1",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "method": "Transform each STAC footprint from CRS84 to each residual raster CRS, then count pixel centres inside the footprint and inside valid residual support. Valid residual support is used as the available common-support proxy.",
        "candidate_audits": rows,
        "limitations": [
            "This intersects catalogue footprint geometry with residual-grid support; it does not verify source COG georeferencing or sub-pixel registration.",
            "Residual valid pixels represent common OPERA/Sentinel Hub support for the residual product, not independently verified source-image validity.",
            "Pixel-centre inclusion is used; boundary cells are not counted unless their centres fall inside the footprint.",
            "The candidate source metadata JSON returned HTTP 404 in the live catalogue audit; acquisition, GSD and licence remain catalogue assertions pending provider confirmation.",
            "No imagery was visually interpreted and no reference labels or accuracy estimates were produced."
        ]
    }


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--audit-json", type=Path, required=True)
    p.add_argument("--residual-dir", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    a = p.parse_args()
    report = audit(a.audit_json, a.residual_dir)
    a.output.parent.mkdir(parents=True, exist_ok=True)
    a.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    for item in report["candidate_audits"]:
        supported = sum(x["VV_candidate_pixels"] for x in item["date_burst_support"])
        both = sum(x["both_polarizations_supported"] for x in item["date_burst_support"])
        print(f"{item['item_id']}: VV supported pixel-date-burst count={supported}; date/burst pairs with both pols={both}/15")
    print(f"Wrote {a.output}")

if __name__ == "__main__":
    main()
