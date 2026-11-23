#!/usr/bin/env python3
"""Reproduce Exercise B; standard-library only, synthetic data only."""
import csv
import math
from pathlib import Path

DATA = Path(__file__).resolve().parents[2] / "data" / "measurement" / "exercise-b-synthetic-levelling.csv"
START_ELEVATION_M = 100.0
SIGMA_FACTOR_MM_PER_SQRT_KM = 2.0  # illustrative assumption, not a standard


def read_runs():
    runs = {"FORWARD": [], "REVERSE": []}
    with DATA.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            row["distance_km"] = float(row["distance_km"])
            row["sum_bs_m"] = float(row["sum_bs_m"])
            row["sum_fs_m"] = float(row["sum_fs_m"])
            row["observed_delta_h_m"] = float(row["observed_delta_h_m"])
            runs[row["run_id"]].append(row)
    return runs


def adjust_forward(rows):
    lengths = [r["distance_km"] for r in rows]
    dh = [r["observed_delta_h_m"] for r in rows]
    variances_mm2 = [(SIGMA_FACTOR_MM_PER_SQRT_KM ** 2) * length for length in lengths]
    misclosure_m = sum(dh)
    total_variance = sum(variances_mm2)
    corrections_m = [-misclosure_m * q / total_variance for q in variances_mm2]
    adjusted = [value + correction for value, correction in zip(dh, corrections_m)]

    # Covariance of increments conditioned on the exact closure constraint:
    # Q_adj[i,j] = q_i*delta_ij - q_i*q_j/sum(q), in mm^2.
    q = variances_mm2
    q_adj = [[(q[i] if i == j else 0.0) - q[i] * q[j] / total_variance
              for j in range(len(q))] for i in range(len(q))]

    # First three cumulative heights are linear combinations of adjusted increments.
    point_count = len(rows) - 1
    height_cov = []
    for i in range(point_count):
        cov_row = []
        for j in range(point_count):
            cov_row.append(sum(q_adj[a][b]
                               for a in range(i + 1)
                               for b in range(j + 1)))
        height_cov.append(cov_row)

    elevations = [START_ELEVATION_M]
    for value in adjusted[:-1]:
        elevations.append(elevations[-1] + value)
    return misclosure_m, corrections_m, adjusted, elevations, height_cov


def main():
    runs = read_runs()
    forward = runs["FORWARD"]
    reverse = runs["REVERSE"]

    # Confirm that recorded aggregate BS-FS reductions match supplied dH values.
    for run_name, rows in runs.items():
        for row in rows:
            reduced = row["sum_bs_m"] - row["sum_fs_m"]
            if abs(reduced - row["observed_delta_h_m"]) > 1e-9:
                raise ValueError(f"BS-FS mismatch in {run_name}, section {row['section_id']}")

    fwd_misclosure = sum(r["observed_delta_h_m"] for r in forward)
    rev_misclosure = sum(r["observed_delta_h_m"] for r in reverse)
    directional_sum = fwd_misclosure + rev_misclosure

    misclosure, corrections, adjusted, elevations, height_cov = adjust_forward(forward)
    if abs(sum(adjusted)) > 1e-12:
        raise ArithmeticError("Adjusted loop does not close numerically")

    print("SYNTHETIC DATA ONLY — NOT FIELD EVIDENCE")
    print(f"Forward misclosure: {fwd_misclosure*1000:.3f} mm")
    print(f"Reverse misclosure: {rev_misclosure*1000:.3f} mm")
    print(f"Combined directional discrepancy: {directional_sum*1000:.3f} mm")
    print("\nForward weighted adjustment:")
    print("section,length_km,correction_mm,adjusted_dh_m")
    for i, row in enumerate(forward):
        print(f"{row['section_id']},{row['distance_km']:.3f},"
              f"{corrections[i]*1000:.3f},{adjusted[i]:.6f}")

    print("\nAdjusted elevations:")
    point_names = ["BM-A", "TP1", "TP2", "TP3"]
    for i, (name, elevation) in enumerate(zip(point_names, elevations)):
        if i == 0:
            print(f"{name}: {elevation:.6f} m; fixed constraint in this example")
        else:
            standard_uncertainty_mm = math.sqrt(height_cov[i-1][i-1])
            print(f"{name}: {elevation:.6f} m; u={standard_uncertainty_mm:.3f} mm")

    print("\nAdjusted height covariance matrix (mm^2):")
    for row in height_cov:
        print("  " + ", ".join(f"{value:.3f}" for value in row))
    print("\nAssumed section standard uncertainty: "
          f"{SIGMA_FACTOR_MM_PER_SQRT_KM} * sqrt(distance_km) mm")
    print("No survey-class tolerance or standards-compliance claim is made.")


if __name__ == "__main__":
    main()
