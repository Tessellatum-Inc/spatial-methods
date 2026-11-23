#!/usr/bin/env python3
"""Apply reusable covariance-aware GLS to the repository's synthetic Exercise D data."""
import csv
import math
from pathlib import Path

from covariance_gls import (
    diagonal_covariance, generalized_least_squares,
    session_common_covariance,
)

ROOT = Path(__file__).resolve().parents[3]
DATA = ROOT / "data" / "measurement" / "exercise-d-stochastic-control-network.csv"
POINTS = ("A", "B", "C", "D", "E")
CONTROL_VALUE_M = 100.001
CONTROL_SIGMA_MM = 2.0
SESSION_COMMON_SIGMA_MM = 0.35


def main():
    with DATA.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    design, observed, sigmas, sessions = [], [], [], []
    for row in rows:
        coeff = [0.0] * len(POINTS)
        coeff[POINTS.index(row["from_point"])] -= 1.0
        coeff[POINTS.index(row["to_point"])] += 1.0
        design.append(coeff)
        observed.append(float(row["observed_delta_h_m"]))
        sigmas.append(float(row["assumed_sigma_mm"]) / 1000.0)
        sessions.append(row["session_id"])
    control = [0.0] * len(POINTS)
    control[0] = 1.0
    design.append(control)
    observed.append(CONTROL_VALUE_M)
    sigmas.append(CONTROL_SIGMA_MM / 1000.0)
    sessions.append("CONTROL-INDEPENDENT")
    # The control observation has no shared session effect with the levelling
    # observations. Construct its independent variance separately.
    q_obs = session_common_covariance(
        sigmas[:-1], sessions[:-1], SESSION_COMMON_SIGMA_MM / 1000.0
    )
    n = len(q_obs)
    q = [[0.0] * (n + 1) for _ in range(n + 1)]
    for i in range(n):
        for j in range(n):
            q[i][j] = q_obs[i][j]
    q[-1][-1] = sigmas[-1] ** 2

    for label, covariance in (
        ("Full session covariance GLS", q),
        ("Diagonal WLS comparison", diagonal_covariance(q)),
    ):
        estimate, formal_cov, residuals = generalized_least_squares(
            design, observed, covariance
        )
        print(label)
        print("point,elevation_m,formal_u_mm")
        for i, point in enumerate(POINTS):
            print(f"{point},{estimate[i]:.6f},{math.sqrt(formal_cov[i][i])*1000:.3f}")
        print(f"weighted residual count: {len(residuals)}")
        print()


if __name__ == "__main__":
    main()
