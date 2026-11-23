#!/usr/bin/env python3
"""Compare ellipsoid and terrain-corrected Sentinel-1 backscatter on common valid pixels.

This is a paired processing-branch diagnostic, not a calibration or validation
of radiometric equivalence. Inputs must share an identical raster grid.
"""
from __future__ import annotations

import argparse
from datetime import datetime
import json
from pathlib import Path

import numpy as np
import rasterio


def _quantiles(values: np.ndarray) -> dict:
    q = np.percentile(values, [1, 5, 25, 50, 75, 95, 99])
    return {
        "min": float(np.min(values)), "p01": float(q[0]), "p05": float(q[1]),
        "p25": float(q[2]), "median": float(q[3]), "p75": float(q[4]),
        "p95": float(q[5]), "p99": float(q[6]), "max": float(np.max(values)),
    }



def _stratified_summary(delta: np.ndarray, strata: np.ndarray,
                        edges: list[float], labels: list[str]) -> list[dict]:
    """Summarize paired dB differences within fixed, interpretable strata."""
    if strata.shape != delta.shape or len(edges) != len(labels) + 1:
        raise ValueError("Stratification values, edges, and labels are inconsistent.")
    records = []
    for index, label in enumerate(labels):
        selected = np.isfinite(strata) & (strata >= edges[index])
        if index == len(labels) - 1:
            selected &= strata <= edges[index + 1]
        else:
            selected &= strata < edges[index + 1]
        values = delta[selected]
        records.append({
            "stratum": label,
            "pixels": int(values.size),
            "median_delta_db": float(np.median(values)) if values.size else None,
            "mean_absolute_delta_db": float(np.mean(np.abs(values))) if values.size else None,
            "p95_absolute_delta_db": float(np.percentile(np.abs(values), 95)) if values.size else None,
        })
    return records



def _stratified_residual_summary(
    residual: np.ndarray, strata: np.ndarray, edges: list[float], labels: list[str]
) -> list[dict]:
    """Summarize centered factor residuals within geometry strata."""
    if residual.shape != strata.shape or len(edges) != len(labels) + 1:
        raise ValueError("Residuals, strata, edges, and labels are inconsistent.")
    records = []
    for index, label in enumerate(labels):
        selected = np.isfinite(residual) & np.isfinite(strata) & (strata >= edges[index])
        if index == len(labels) - 1:
            selected &= strata <= edges[index + 1]
        else:
            selected &= strata < edges[index + 1]
        values = residual[selected]
        records.append({
            "stratum": label,
            "pixels": int(values.size),
            "median_centered_residual_db": float(np.median(values)) if values.size else None,
            "mean_absolute_centered_residual_db": float(np.mean(np.abs(values))) if values.size else None,
            "p95_absolute_centered_residual_db": float(np.percentile(np.abs(values), 95)) if values.size else None,
        })
    return records

def _spatial_holdout_residual_model(
    delta: np.ndarray, scattering_area: np.ndarray, local_incidence_angle: np.ndarray,
    rows: np.ndarray, cols: np.ndarray, grid_height: int, grid_width: int,
    tile_size: int = 512, buffer_pixels: int = 32,
) -> dict:
    """Compare area-only and area-plus-angle OLS on spatially separated blocks.

    Checkerboard blocks are split into train/test sets. A buffer is excluded
    around block edges to reduce direct spatial leakage; this remains a
    diagnostic holdout, not a substitute for independent acquisitions/sites.
    """
    arrays = (scattering_area, local_incidence_angle, rows, cols)
    if any(values.shape != delta.shape for values in arrays):
        raise ValueError("Spatial model inputs must align with paired differences.")
    if tile_size <= 0 or buffer_pixels < 0 or 2 * buffer_pixels >= tile_size:
        raise ValueError("Spatial tile size and buffer are invalid.")
    valid = (np.isfinite(delta) & np.isfinite(scattering_area) & (scattering_area > 0)
             & np.isfinite(local_incidence_angle))
    valid &= (rows >= 0) & (rows < grid_height) & (cols >= 0) & (cols < grid_width)
    row_in_tile, col_in_tile = rows % tile_size, cols % tile_size
    interior = ((row_in_tile >= buffer_pixels) & (row_in_tile < tile_size - buffer_pixels)
                & (col_in_tile >= buffer_pixels) & (col_in_tile < tile_size - buffer_pixels))
    tile_parity = (rows // tile_size + cols // tile_size) % 2
    train = valid & interior & (tile_parity == 0)
    test = valid & interior & (tile_parity == 1)
    if train.sum() < 1000 or test.sum() < 1000:
        return {
            "status": "insufficient_spatial_holdout_pixels",
            "train_pixels": int(train.sum()), "test_pixels": int(test.sum()),
            "tile_size_pixels": tile_size, "buffer_pixels": buffer_pixels,
        }

    x = -10.0 * np.log10(scattering_area.astype(np.float64))
    angle_scaled = (local_incidence_angle.astype(np.float64) - 45.0) / 10.0
    y = delta.astype(np.float64)
    area_design = np.column_stack((np.ones(train.sum()), x[train]))
    joint_design = np.column_stack((np.ones(train.sum()), x[train], angle_scaled[train],
                                    x[train] * angle_scaled[train]))
    area_coefficients, *_ = np.linalg.lstsq(area_design, y[train], rcond=None)
    joint_coefficients, *_ = np.linalg.lstsq(joint_design, y[train], rcond=None)
    area_prediction = area_coefficients[0] + area_coefficients[1] * x[test]
    joint_prediction = (joint_coefficients[0] + joint_coefficients[1] * x[test]
                        + joint_coefficients[2] * angle_scaled[test]
                        + joint_coefficients[3] * x[test] * angle_scaled[test])

    def metrics(prediction: np.ndarray) -> dict:
        error = y[test] - prediction
        return {
            "rmse_db": float(np.sqrt(np.mean(error ** 2))),
            "mae_db": float(np.mean(np.abs(error))),
            "p95_absolute_error_db": float(np.percentile(np.abs(error), 95)),
        }

    area_metrics = metrics(area_prediction)
    joint_metrics = metrics(joint_prediction)
    return {
        "status": "screening_only",
        "split": "checkerboard spatial blocks with edge buffer",
        "tile_size_pixels": tile_size,
        "buffer_pixels": buffer_pixels,
        "train_pixels": int(train.sum()),
        "test_pixels": int(test.sum()),
        "area_only_coefficients_intercept_slope": [float(v) for v in area_coefficients],
        "area_plus_angle_coefficients_intercept_area_angle_interaction": [float(v) for v in joint_coefficients],
        "area_only_test_metrics": area_metrics,
        "area_plus_angle_test_metrics": joint_metrics,
        "test_rmse_reduction_fraction": float(
            (area_metrics["rmse_db"] - joint_metrics["rmse_db"]) / area_metrics["rmse_db"]
        ) if area_metrics["rmse_db"] > 0 else 0.0,
        "limitations": [
            "Spatial blocks come from one acquisition and are not independent validation sites or dates.",
            "A fixed checkerboard split can still be sensitive to spatial gradients and scene structure.",
            "The model is diagnostic only; no normalization or correction is applied.",
        ],
    }


def _area_factor_relation(
    delta: np.ndarray, scattering_area: np.ndarray, local_incidence_angle: np.ndarray
) -> dict:
    """Test whether RTC/ellipsoid dB differences follow inverse scattering area."""
    if scattering_area.shape != delta.shape or local_incidence_angle.shape != delta.shape:
        raise ValueError("Scattering-area and incidence-angle values must align with paired differences.")
    valid = np.isfinite(delta) & np.isfinite(scattering_area) & (scattering_area > 0)
    if not valid.any():
        raise ValueError("No finite positive scattering-area values for factor diagnostic.")
    observed = delta[valid].astype(np.float64)
    predicted = -10.0 * np.log10(scattering_area[valid].astype(np.float64))
    residual = observed - predicted
    residual_offset = float(np.median(residual))
    centered_residual = residual - residual_offset
    correlation = None
    slope = intercept = r_squared = None
    if observed.size > 1 and np.std(observed) > 0 and np.std(predicted) > 0:
        correlation = float(np.corrcoef(observed, predicted)[0, 1])
        slope, intercept = (float(value) for value in np.polyfit(predicted, observed, 1))
        fitted = slope * predicted + intercept
        total_sum_squares = float(np.sum((observed - np.mean(observed)) ** 2))
        if total_sum_squares > 0:
            r_squared = float(1.0 - np.sum((observed - fitted) ** 2) / total_sum_squares)
    return {
        "pixels": int(observed.size),
        "hypothesis": "RTC_minus_ellipsoid_dB = -10*log10(scatteringArea)",
        "predicted_delta_db_quantiles": _quantiles(predicted),
        "observed_minus_predicted_db_quantiles": _quantiles(residual),
        "median_observed_minus_predicted_db": residual_offset,
        "median_absolute_residual_db": float(np.median(np.abs(residual))),
        "p95_absolute_residual_db": float(np.percentile(np.abs(residual), 95)),
        "centered_observed_minus_predicted_db_quantiles": _quantiles(centered_residual),
        "median_absolute_centered_residual_db": float(np.median(np.abs(centered_residual))),
        "p95_absolute_centered_residual_db": float(np.percentile(np.abs(centered_residual), 95)),
        "centered_residual_by_scattering_area": _stratified_residual_summary(
            centered_residual, scattering_area[valid].astype(np.float64),
            [0.0, 0.9, 1.0, 1.1, 1.2, float("inf")],
            ["<0.9", "0.9–1.0", "1.0–1.1", "1.1–1.2", "≥1.2"],
        ),
        "centered_residual_by_local_incidence_angle_degrees": _stratified_residual_summary(
            centered_residual, local_incidence_angle[valid].astype(np.float64),
            [0.0, 35.0, 40.0, 45.0, 50.0, 90.0],
            ["<35°", "35–40°", "40–45°", "45–50°", "≥50°"],
        ),
        "observed_predicted_pearson_r": correlation,
        "observed_on_predicted_ols_slope": slope,
        "observed_on_predicted_ols_intercept_db": intercept,
        "observed_on_predicted_ols_r_squared": r_squared,
    }


def compare_pair(ellipsoid_path: Path, rtc_path: Path) -> dict:
    with rasterio.open(ellipsoid_path) as ell, rasterio.open(rtc_path) as rtc:
        if ell.count < 3 or rtc.count != 6:
            raise ValueError("Expected ellipsoid VV/VH/dataMask (3 bands) and RTC six-band raster.")
        if (ell.crs != rtc.crs or ell.transform != rtc.transform
                or (ell.width, ell.height) != (rtc.width, rtc.height)):
            raise ValueError("Ellipsoid and RTC rasters do not have identical grids.")
        base = ell.read([1, 2, 3]).astype(np.float32)
        terrain = rtc.read().astype(np.float32)

    common = ((base[2] > 0.5) & (terrain[5] > 0.5)
              & np.isfinite(base).all(axis=0) & np.isfinite(terrain).all(axis=0))
    if not common.any():
        raise ValueError("No common valid pixels between ellipsoid and RTC rasters.")
    result = {
        "ellipsoid_file": ellipsoid_path.name,
        "rtc_file": rtc_path.name,
        "grid": {"width": int(base.shape[2]), "height": int(base.shape[1])},
        "ellipsoid_valid_pixels": int(np.count_nonzero(base[2] > 0.5)),
        "rtc_valid_pixels": int(np.count_nonzero(terrain[5] > 0.5)),
        "common_valid_pixels": int(common.sum()),
        "common_valid_fraction_of_grid": float(common.mean()),
        "rtc_shadow_fraction_of_common_valid_pixels": float(np.mean(terrain[4][common] > 0.5)),
        "scattering_area_quantiles_on_common_valid": _quantiles(terrain[2][common]),
        "polarizations": {},
        "interpretation": (
            "Descriptive paired difference between two processing branches. "
            "Not evidence of radiometric equivalence, calibration accuracy, or suitability for change detection."
        ),
    }
    for index, name in ((0, "VV"), (1, "VH")):
        a, b = base[index][common], terrain[index][common]
        positive = (a > 0) & (b > 0)
        if not positive.any():
            raise ValueError(f"No common positive linear-power pixels for {name}.")
        ell_db = 10.0 * np.log10(a[positive].astype(np.float64))
        rtc_db = 10.0 * np.log10(b[positive].astype(np.float64))
        delta = rtc_db - ell_db
        area_values = terrain[2][common][positive].astype(np.float64)
        angle_values = terrain[3][common][positive].astype(np.float64)
        stratified = {
            "scattering_area": _stratified_summary(
                delta, area_values,
                [0.0, 0.9, 1.0, 1.1, 1.2, float("inf")],
                ["<0.9", "0.9–1.0", "1.0–1.1", "1.1–1.2", "≥1.2"],
            ),
            "local_incidence_angle_degrees": _stratified_summary(
                delta, angle_values,
                [0.0, 35.0, 40.0, 45.0, 50.0, 90.0],
                ["<35°", "35–40°", "40–45°", "45–50°", "≥50°"],
            ),
        }
        result["polarizations"][name] = {
            "stratified_differences": stratified,
            "scattering_area_factor_relation": {
                **_area_factor_relation(delta, area_values, angle_values),
                "spatial_holdout_residual_model": _spatial_holdout_residual_model(
                    delta, area_values, angle_values,
                    (np.flatnonzero(common)[positive] // base.shape[2]).astype(np.int32),
                    (np.flatnonzero(common)[positive] % base.shape[2]).astype(np.int32),
                    base.shape[1], base.shape[2],
                ),
            },
            "positive_common_pixels": int(positive.sum()),
            "ellipsoid_median_db": float(np.median(ell_db)),
            "rtc_median_db": float(np.median(rtc_db)),
            "rtc_minus_ellipsoid_db": {
                "mean": float(np.mean(delta)),
                "median": float(np.median(delta)),
                "mean_absolute": float(np.mean(np.abs(delta))),
                "quantiles": _quantiles(delta),
            },
        }
    return result


def run(stack_metadata: Path, ellipsoid_dir: Path, rtc_dir: Path, output: Path) -> dict:
    stack = json.loads(stack_metadata.read_text(encoding="utf-8"))
    scenes = stack.get("scenes")
    if not isinstance(scenes, list) or len(scenes) < 2:
        raise ValueError("Stack metadata must contain at least two scenes.")
    comparisons = []
    failures = []
    for scene in scenes:
        try:
            stamp = datetime.fromisoformat(
                scene["catalog_item_datetime_utc"].replace("Z", "+00:00")
            ).strftime("%Y%m%dT%H%M%SZ")
            ell_path = ellipsoid_dir / scene["output"]["file"]
            rtc_path = rtc_dir / f"sentinel1_nairobi_{stamp}_gamma0-terrain-rtc.tif"
            comparisons.append(compare_pair(ell_path, rtc_path))
        except (KeyError, OSError, ValueError) as exc:
            failures.append({"scene": scene.get("catalog_item_datetime_utc"), "error": str(exc)})
    report = {
        "schema": "tessellatum.sentinel1.ellipsoid-vs-terrain-paired-screen.v1",
        "scene_count": len(scenes),
        "compared_count": len(comparisons),
        "failed_count": len(failures),
        "comparisons": comparisons,
        "failures": failures,
        "status": "paired_diagnostic_only" if not failures and len(comparisons) == len(scenes) else "incomplete_paired_diagnostic",
        "analysis_ready": False,
        "limitations": [
            "Only pixels valid in both processing branches are compared; this can select a non-random subset.",
            "The same requested output grid does not establish pixel-level geometric correspondence.",
            "Terrain correction changes both geometric and radiometric processing; differences must not be interpreted as a simple terrain-only correction.",
            "No automatic normalization, resampling, masking beyond common data validity, or change detection is performed.",
        ],
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    if failures or len(comparisons) != len(scenes):
        raise RuntimeError(f"Paired comparison incomplete: {len(comparisons)}/{len(scenes)} scenes.")
    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--stack-metadata", type=Path, default=Path("data/sentinelhub/nairobi/stack/sentinel1_nairobi_temporal_stack.metadata.json"))
    parser.add_argument("--ellipsoid-dir", type=Path, default=Path("data/sentinelhub/nairobi/stack"))
    parser.add_argument("--rtc-dir", type=Path, default=Path("data/sentinelhub/nairobi/stack/terrain_aux"))
    parser.add_argument("--output", type=Path, default=Path("data/sentinelhub/nairobi/stack/terrain_aux/sentinel1_nairobi_ellipsoid_vs_terrain_paired_screen.json"))
    args = parser.parse_args(argv)
    try:
        report = run(args.stack_metadata, args.ellipsoid_dir, args.rtc_dir, args.output)
    except (OSError, ValueError, RuntimeError) as exc:
        parser.exit(2, f"Paired comparison failed: {exc}\n")
    print(f"Compared {report['compared_count']} scenes; analysis_ready=false")
    for comparison in report["comparisons"]:
        for polarization, diagnostic in comparison["polarizations"].items():
            factor = diagnostic["scattering_area_factor_relation"]
            print(
                "RTC_AREA_FACTOR "
                f"{comparison['ellipsoid_file']} {polarization} "
                f"pixels={factor['pixels']} "
                f"median_abs_residual_db={factor['median_absolute_residual_db']:.6f} "
                f"median_offset_db={factor['median_observed_minus_predicted_db']:.6f} "
                f"p95_abs_residual_db={factor['p95_absolute_residual_db']:.6f} "
                f"centered_p95_abs_residual_db={factor['p95_absolute_centered_residual_db']:.6f} "
                f"ols_slope={factor['observed_on_predicted_ols_slope']} "
                f"ols_intercept_db={factor['observed_on_predicted_ols_intercept_db']} "
                f"ols_r2={factor['observed_on_predicted_ols_r_squared']} "
                f"pearson_r={factor['observed_predicted_pearson_r']}"
            )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
