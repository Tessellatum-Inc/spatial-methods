#!/usr/bin/env python3
"""Reproduce synthetic Exercise E with the reusable exact-constraint GLS solver."""
import csv
import math
from pathlib import Path

from constrained_gls import constrained_gls

ROOT = Path(__file__).resolve().parents[3]
DATA = ROOT / "data" / "measurement" / "exercise-c-synthetic-control-network.csv"
POINTS = ("A", "B", "C", "D", "E")


def load_network():
    design, observed, sigmas = [], [], []
    with DATA.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            coefficients = [0.0] * len(POINTS)
            coefficients[POINTS.index(row["from_point"])] -= 1.0
            coefficients[POINTS.index(row["to_point"])] += 1.0
            design.append(coefficients)
            observed.append(float(row["observed_delta_h_m"]))
            sigma = float(row["assumed_sigma_mm"]) / 1000.0
            if sigma <= 0:
                raise ValueError("Observation standard uncertainties must be positive")
            sigmas.append(sigma)
    covariance = [[sigmas[i] ** 2 if i == j else 0.0
                   for j in range(len(sigmas))]
                  for i in range(len(sigmas))]
    return design, observed, covariance


def main():
    design, observed, covariance = load_network()
    # The height-difference design has one common-translation datum defect.
    # The sum-to-zero constraint selects an arbitrary mathematical origin.
    constraint = [[1.0] * len(POINTS)]
    estimate, parameter_covariance, residuals, multipliers = constrained_gls(
        design, observed, covariance, constraint, [0.0]
    )
    print("SYNTHETIC DATA ONLY — NOT FIELD OBSERVATIONS")
    print("Exercise E: minimally constrained vertical network")
    print(f"Design rank: 4 of {len(POINTS)}; datum defect: 1")
    print("Exact inner constraint: sum(H_i) = 0")
    print("\nFree-network heights (m):")
    for point, height in zip(POINTS, estimate):
        print(f"  {point}: {height:+.6f}")
    print("\nFormal constrained covariance (mm^2; gauge-dependent):")
    for row in parameter_covariance:
        print("  " + ", ".join(f"{value * 1e6:.4f}" for value in row))
    print("\nRelative-height standard uncertainties (mm):")
    for p, q in (("B", "C"), ("B", "D"), ("C", "E")):
        i, j = POINTS.index(p), POINTS.index(q)
        variance = (parameter_covariance[i][i] + parameter_covariance[j][j]
                    - 2.0 * parameter_covariance[i][j])
        print(f"  {p} to {q}: {math.sqrt(max(0.0, variance)) * 1000:.3f}")
    print(f"\nResidual count: {len(residuals)}; constraint multiplier: {multipliers[0]:.6g}")
    print("\nThis reproduces the free-network solution only. The separate external")
    print("control translation in the Exercise E analysis remains a distinct step.")


if __name__ == "__main__":
    main()
