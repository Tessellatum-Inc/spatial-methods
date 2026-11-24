#!/usr/bin/env python3
"""Cross-processor OPERA RTC-S1 vs Sentinel Hub gamma0 comparison for Surat R009."""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import numpy as np
import rasterio
from rasterio.enums import Resampling
from rasterio.warp import reproject, transform as transform_coords

TARGETS = [
    ("Surat Basin 26", 150.485114, -27.258849),
    ("Surat Basin 31", 150.331548, -27.207314),
    ("Surat Basin 35", 150.259625, -27.085649),
]
BURST_RE = re.compile(r"(T\d{3}-\d{6}-IW\d)", re.IGNORECASE)
DATE_RE = re.compile(r"(20\d{6})T\d{6}Z")
POLARIZATIONS = ("VV", "VH")
DB_FLOOR = 1e-12
REFLECTOR_EXCLUSION_M = 450.0  # 15 OPERA 30 m pixels; metric, circular buffer.


def db(values: np.ndarray) -> np.ndarray:
    return 10.0 * np.log10(np.maximum(values, DB_FLOOR))


def residual_metrics(values: np.ndarray) -> dict:
    v = np.asarray(values, dtype=np.float64)
    v = v[np.isfinite(v)]
    if not v.size:
        raise ValueError("No finite residual samples")
    return {
        "count": int(v.size),
        "bias_mean_db": float(np.mean(v)),
        "bias_median_db": float(np.median(v)),
        "mae_db": float(np.mean(np.abs(v))),
        "rmse_db": float(np.sqrt(np.mean(v * v))),
        "std_db": float(np.std(v)),
        "p05_db": float(np.percentile(v, 5)),
        "p95_db": float(np.percentile(v, 95)),
        "p95_absolute_db": float(np.percentile(np.abs(v), 95)),
        "max_absolute_db": float(np.max(np.abs(v))),
    }


def regression_summary(observed: np.ndarray, predicted: np.ndarray) -> dict:
    x = np.asarray(predicted, dtype=np.float64)
    y = np.asarray(observed, dtype=np.float64)
    ok = np.isfinite(x) & np.isfinite(y)
    x, y = x[ok], y[ok]
    if x.size < 10 or np.std(x) == 0:
        raise ValueError("Insufficient or invariant samples for regression")
    slope, intercept = np.polyfit(x, y, 1)
    fitted = intercept + slope * x
    ss_res = float(np.sum((y - fitted) ** 2))
    ss_tot = float(np.sum((y - np.mean(y)) ** 2))
    return {
        "sample_count": int(x.size),
        "slope": float(slope),
        "intercept_db": float(intercept),
        "r_squared": float(1.0 - ss_res / ss_tot) if ss_tot > 0 else None,
    }


def find_unique(folder: Path, predicate, description: str) -> Path:
    matches = sorted(p for p in folder.rglob("*.tif") if predicate(p))
    if len(matches) != 1:
        raise ValueError(f"Expected exactly one {description}; found {len(matches)}: {[p.name for p in matches]}")
    return matches[0]


def same_grid(reference, candidate, label: str) -> None:
    if (reference.crs != candidate.crs or reference.transform != candidate.transform
            or reference.width != candidate.width or reference.height != candidate.height):
        raise ValueError(f"Grid mismatch for {label}")


def reproject_average(source: np.ndarray, src, dst) -> np.ndarray:
    result = np.full((dst.height, dst.width), np.nan, dtype=np.float32)
    reproject(
        source=source.astype(np.float32, copy=False),
        destination=result,
        src_transform=src.transform,
        src_crs=src.crs,
        src_nodata=np.nan,
        dst_transform=dst.transform,
        dst_crs=dst.crs,
        dst_nodata=np.nan,
        resampling=Resampling.average,
        init_dest_nodata=True,
    )
    return result


def reflector_exclusion(ds) -> np.ndarray:
    excluded = np.zeros((ds.height, ds.width), dtype=bool)
    for _, lon, lat in TARGETS:
        xs, ys = transform_coords("EPSG:4326", ds.crs, [lon], [lat])
        x, y = xs[0], ys[0]
        row, col = ds.index(x, y)
        # A circular buffer in map units; works for the projected OPERA UTM grid.
        rows, cols = np.ogrid[:ds.height, :ds.width]
        xx, yy = rasterio.transform.xy(ds.transform, rows, cols, offset="center")
        excluded |= (np.asarray(xx) - x) ** 2 + (np.asarray(yy) - y) ** 2 <= REFLECTOR_EXCLUSION_M ** 2
    return excluded


def locate_scene_files(opera_dir: Path, vv_path: Path) -> dict:
    burst_match = BURST_RE.search(vv_path.name)
    date_match = DATE_RE.search(vv_path.name)
    if not burst_match or not date_match:
        raise ValueError(f"Cannot parse burst/date from OPERA filename: {vv_path.name}")
    burst, date = burst_match.group(1), date_match.group(1)
    stem = vv_path.name[:-len("_VV.tif")]
    rtc_dir = opera_dir / "rtc"
    static_dir = opera_dir / "static"

    def exact_rtc(suffix):
        return find_unique(rtc_dir, lambda p: p.name == stem + suffix, f"{burst} {date} {suffix}")

    def static_layer(suffix):
        return find_unique(static_dir, lambda p: burst in p.name and p.name.endswith(suffix),
                           f"{burst} static {suffix}")

    return {
        "burst": burst, "date": date,
        "vv": vv_path, "vh": exact_rtc("_VH.tif"), "rtc_mask": exact_rtc("_mask.tif"),
        "anf": static_layer("_rtc_anf_gamma0_to_beta0.tif"),
        "incidence": static_layer("_incidence_angle.tif"),
        "static_mask": static_layer("_mask.tif"),
    }


def load_sentinelhub(scene_dir: Path, date: str):
    iso = f"{date[:4]}-{date[4:6]}-{date[6:8]}"
    ell_path = scene_dir / f"surat_r009_{iso}_gamma0-ellipsoid.tif"
    rtc_path = scene_dir / f"surat_r009_{iso}_gamma0-terrain-rtc.tif"
    if not ell_path.is_file() or not rtc_path.is_file():
        raise FileNotFoundError(f"Missing Sentinel Hub pair for {iso}")
    return rasterio.open(ell_path), rasterio.open(rtc_path)


def compare_burst(files: dict, scene_dir: Path) -> dict:
    ell = rtc = None
    with rasterio.open(files["vv"]) as vv, rasterio.open(files["vh"]) as vh, \
         rasterio.open(files["rtc_mask"]) as rm, rasterio.open(files["anf"]) as anf, \
         rasterio.open(files["incidence"]) as angle, rasterio.open(files["static_mask"]) as sm:
        for label, ds in (("VH", vh), ("RTC mask", rm), ("ANF", anf),
                          ("ellipsoid incidence", angle), ("static mask", sm)):
            same_grid(vv, ds, label)
        if vv.count != 1 or vh.count != 1 or rm.count != 1 or anf.count != 1 or angle.count != 1 or sm.count != 1:
            raise ValueError("Expected single-band OPERA COG layers")
        if vv.crs is None or vv.crs.to_epsg() != 32755:
            raise ValueError(f"Unexpected OPERA CRS: {vv.crs}")
        if not (abs(vv.transform.a - 30) < 1e-6 and abs(vv.transform.e + 30) < 1e-6):
            raise ValueError(f"Expected 30 m OPERA grid, got {vv.transform}")

        opera_mask = (rm.read(1) == 0) & (sm.read(1) == 0)
        anf_values = anf.read(1).astype(np.float32)
        theta = angle.read(1).astype(np.float32)
        valid_static = np.isfinite(anf_values) & (anf_values > 0) & np.isfinite(theta) & (theta > 0) & (theta < 90)
        excluded = reflector_exclusion(vv)
        valid_opera = opera_mask & valid_static & ~excluded
        if int(valid_opera.sum()) < 100:
            raise ValueError(f"Too few valid OPERA pixels for {files['burst']} {files['date']}")

        sh_ell, sh_rtc = load_sentinelhub(scene_dir, files["date"])
        try:
            same_grid(sh_ell, sh_rtc, "Sentinel Hub ellipsoid/RTC")
            if sh_ell.count != 3 or sh_rtc.count != 6:
                raise ValueError("Unexpected Sentinel Hub band schema (expected 3 ellipsoid and 6 RTC bands)")
            if sh_ell.crs is None:
                raise ValueError("Sentinel Hub raster has no CRS")
            ell_mask = sh_ell.read(3) > 0.5
            rtc_mask = (sh_rtc.read(6) > 0.5) & (sh_rtc.read(5) < 0.5)
            source_common = ell_mask & rtc_mask
            source_common &= np.isfinite(sh_ell.read(1)) & np.isfinite(sh_ell.read(2))
            source_common &= np.isfinite(sh_rtc.read(1)) & np.isfinite(sh_rtc.read(2))
            if not source_common.any():
                raise ValueError(f"No common valid Sentinel Hub pixels for {files['date']}")
            sh_support = reproject_average(source_common.astype(np.float32), sh_ell, vv)
            sh_valid = np.isfinite(sh_support) & (sh_support >= 0.95)

            outputs = {}
            for index, pol in enumerate(POLARIZATIONS, start=1):
                sh_ell_src = np.where(source_common, sh_ell.read(index), np.nan).astype(np.float32)
                sh_rtc_src = np.where(source_common, sh_rtc.read(index), np.nan).astype(np.float32)
                sh_ell_on_opera = reproject_average(sh_ell_src, sh_ell, vv)
                sh_rtc_on_opera = reproject_average(sh_rtc_src, sh_rtc, vv)
                opera_rtc = vv.read(1).astype(np.float32) if pol == "VV" else vh.read(1).astype(np.float32)
                valid = valid_opera & sh_valid
                valid &= np.isfinite(opera_rtc) & (opera_rtc > 0)
                valid &= np.isfinite(sh_ell_on_opera) & (sh_ell_on_opera > 0)
                valid &= np.isfinite(sh_rtc_on_opera) & (sh_rtc_on_opera > 0)
                if int(valid.sum()) < 100:
                    raise ValueError(f"Too few common pixels for {files['burst']} {files['date']} {pol}")

                # OPERA RTC gamma0 -> beta0 -> ellipsoid gamma0.
                opera_ell = opera_rtc * anf_values * np.tan(np.deg2rad(theta))
                valid &= np.isfinite(opera_ell) & (opera_ell > 0)
                if int(valid.sum()) < 100:
                    raise ValueError("Too few valid pixels after OPERA radiometric reconstruction")

                opera_delta = db(opera_rtc[valid]) - db(opera_ell[valid])
                sh_delta = db(sh_rtc_on_opera[valid]) - db(sh_ell_on_opera[valid])
                outputs[pol] = {
                    "common_valid_pixels": int(valid.sum()),
                    "valid_fraction_of_burst_grid": float(valid.mean()),
                    "opera_terrain_vs_sentinelhub_terrain_db": residual_metrics(db(opera_rtc[valid]) - db(sh_rtc_on_opera[valid])),
                    "opera_reconstructed_ellipsoid_vs_sentinelhub_ellipsoid_db": residual_metrics(db(opera_ell[valid]) - db(sh_ell_on_opera[valid])),
                    "cross_processor_terrain_minus_ellipsoid_difference_db": residual_metrics(sh_delta - opera_delta),
                    "cross_processor_difference_regression": regression_summary(sh_delta, opera_delta),
                    "mean_ellipsoid_incidence_angle_deg": float(np.mean(theta[valid])),
                    "mean_anf_gamma0_to_beta0": float(np.mean(anf_values[valid])),
                }
            return {
                "date": files["date"], "burst": files["burst"],
                "grid": {"crs": str(vv.crs), "width": vv.width, "height": vv.height,
                         "pixel_size_m": [float(vv.transform.a), float(abs(vv.transform.e))]},
                "opera_valid_mask_pixels_before_sentinelhub_intersection": int(valid_opera.sum()),
                "sentinelhub_support_fraction": float(sh_valid.mean()),
                "polarizations": outputs,
            }
        finally:
            sh_ell.close()
            sh_rtc.close()


def pool_metrics(records: list[dict]) -> dict:
    pooled = {}
    for pol in POLARIZATIONS:
        # Burst-level summaries are retained individually; pooled aggregate metrics
        # are reconstructed from count-weighted summary moments only where possible.
        metrics = [r["polarizations"][pol] for r in records]
        total = sum(x["common_valid_pixels"] for x in metrics)
        pooled[pol] = {
            "total_burst_pixel_samples": int(total),
            "count_weighted_bias_terrain_minus_ellipsoid_db": float(sum(
                x["cross_processor_terrain_minus_ellipsoid_difference_db"]["bias_mean_db"] * x["common_valid_pixels"]
                for x in metrics) / total),
            "count_weighted_mae_terrain_minus_ellipsoid_db": float(sum(
                x["cross_processor_terrain_minus_ellipsoid_difference_db"]["mae_db"] * x["common_valid_pixels"]
                for x in metrics) / total),
            "count_weighted_rmse_terrain_minus_ellipsoid_db": float(np.sqrt(sum(
                (x["cross_processor_terrain_minus_ellipsoid_difference_db"]["rmse_db"] ** 2) * x["common_valid_pixels"]
                for x in metrics) / total)),
        }
    return pooled


def run(opera_dir: Path, sentinelhub_dir: Path, output: Path) -> dict:
    vv_files = sorted((opera_dir / "rtc").rglob("*_VV.tif"))
    if len(vv_files) != 8:
        raise ValueError(f"Expected eight OPERA VV burst rasters, found {len(vv_files)}")
    records = []
    for vv_path in vv_files:
        files = locate_scene_files(opera_dir, vv_path)
        print(f"Comparing {files['date']} {files['burst']}", flush=True)
        records.append(compare_burst(files, sentinelhub_dir))
    if len({r["date"] for r in records}) != 4 or len({r["burst"] for r in records}) != 2:
        raise ValueError("Expected four dates and two adjacent IW3 bursts")
    report = {
        "schema": "tessellatum.sentinel1.opera-surat-r009-cross-processor-comparison.v1",
        "site": "CEOS Surat Basin, Queensland, Australia",
        "source_processors": {
            "opera": "NASA/JPL OPERA RTC-S1, SLC-derived, ISCE3, 30 m gamma0",
            "sentinelhub": "Sentinel Hub Sentinel-1 GRD, ellipsoid gamma0 and terrain gamma0 branches",
        },
        "radiometric_reconstruction": {
            "beta0": "OPERA_gamma0_RTC * ANF_gamma0_to_beta0",
            "ellipsoid_gamma0": "beta0 * tan(ellipsoid_incidence_angle)",
            "delta_db": "OPERA_gamma0_RTC_dB - reconstructed_ellipsoid_gamma0_dB = -10log10(ANF) - 10log10(tan(theta_E))",
            "sentinelhub_delta_db": "SentinelHub_gamma0_terrain_dB - SentinelHub_gamma0_ellipsoid_dB",
        },
        "resampling": "Sentinel Hub backscatter was masked and area-averaged in linear power onto each native OPERA burst grid; dB values were calculated only after aggregation.",
        "masking": "OPERA dynamic RTC mask class 0 and static mask class 0; common Sentinel Hub ellipsoid/RTC data masks and RTC shadowMask < 0.5; 450 m circular exclusions around three surveyed reflectors.",
        "reflector_exclusion_radius_m": REFLECTOR_EXCLUSION_M,
        "scene_burst_count": len(records),
        "per_burst": records,
        "count_weighted_summary": pool_metrics(records),
        "comparison_complete": True,
        "interpretation_limits": [
            "This is a cross-processor comparison, not a native-pixel equality test: OPERA uses SLC/ISCE3 and 30 m burst grids; Sentinel Hub uses GRD and a different processor.",
            "Sentinel Hub data are area-averaged to OPERA grids in linear power. The source footprints and effective spatial resolutions are not identical.",
            "The OPERA reconstruction uses the documented gamma0-to-beta0 ANF and ellipsoid incidence angle; it does not imply the two providers use identical DEMs, noise handling, multilooking, or radiometric calibration.",
            "The three reflector neighborhoods are excluded from distributed-target statistics; this comparison does not validate absolute corner-reflector RCS.",
            "Per-burst summaries are the primary diagnostic. The count-weighted aggregate is a descriptive summary, not a substitute for pooled-pixel statistics.",
        ],
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report["count_weighted_summary"], indent=2))
    print(f"Report written: {output}")
    return report


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--opera-dir", type=Path, required=True)
    parser.add_argument("--sentinelhub-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        result = run(args.opera_dir, args.sentinelhub_dir, args.output)
    except Exception as exc:
        print(f"OPERA cross-processor comparison failed: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 2
    return 0 if result["comparison_complete"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
