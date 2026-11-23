#!/usr/bin/env python3
"""Exercise D: uncertain datum control and correlated height-difference errors.

All observations, control values, standard uncertainties and correlation
assumptions are synthetic. Standard-library only.
"""
import csv
import math
from pathlib import Path

DATA = Path(__file__).resolve().parents[2] / "data" / "measurement" / "exercise-d-stochastic-control-network.csv"
POINTS = ("A", "B", "C", "D", "E")
CONTROL_VALUE_M = 100.001
CONTROL_SIGMA_MM = 2.0
SESSION_COMMON_SIGMA_MM = 0.35


def solve(matrix, rhs):
    n = len(rhs)
    aug = [list(map(float, matrix[i])) + [float(rhs[i])] for i in range(n)]
    for col in range(n):
        pivot = max(range(col, n), key=lambda row: abs(aug[row][col]))
        if abs(aug[pivot][col]) < 1e-20:
            raise ValueError("Singular system: inspect datum and network connectivity")
        aug[col], aug[pivot] = aug[pivot], aug[col]
        scale = aug[col][col]
        aug[col] = [v / scale for v in aug[col]]
        for row in range(n):
            if row != col:
                factor = aug[row][col]
                aug[row] = [aug[row][j] - factor * aug[col][j] for j in range(n + 1)]
    return [aug[i][-1] for i in range(n)]


def inverse(matrix):
    n = len(matrix)
    cols = [solve(matrix, [1.0 if i == j else 0.0 for i in range(n)])
            for j in range(n)]
    return [[cols[j][i] for j in range(n)] for i in range(n)]


def matvec(matrix, vector):
    return [sum(a * b for a, b in zip(row, vector)) for row in matrix]


def transpose(matrix):
    return [list(col) for col in zip(*matrix)]


def multiply(a, b):
    bt = transpose(b)
    return [[sum(x * y for x, y in zip(row, col)) for col in bt] for row in a]


def read_data():
    with DATA.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    for row in rows:
        for key in ("length_km", "observed_delta_h_m", "assumed_sigma_mm"):
            row[key] = float(row[key])
    return rows


def build_covariance(rows, correlated):
    n = len(rows)
    q = [[0.0] * n for _ in range(n)]
    tau = SESSION_COMMON_SIGMA_MM / 1000.0
    for i, left in enumerate(rows):
        for j, right in enumerate(rows):
            if i == j:
                q[i][j] += (left["assumed_sigma_mm"] / 1000.0) ** 2
            if correlated and left["session_id"] == right["session_id"]:
                # Illustrative common additive session effect, shared by rows
                # in a session. This is a synthetic covariance structure.
                q[i][j] += tau ** 2
    return q


def adjust(rows, fixed_control, correlated):
    n_obs = len(rows)
    q_obs = build_covariance(rows, correlated)
    if fixed_control:
        unknowns = POINTS[1:]
        design, observed = [], []
        for row in rows:
            coeff = [0.0] * len(unknowns)
            fixed_contribution = 0.0
            for point, sign in ((row["from_point"], -1.0),
                                (row["to_point"], 1.0)):
                if point == "A":
                    fixed_contribution += sign * 100.0
                else:
                    coeff[unknowns.index(point)] += sign
            design.append(coeff)
            observed.append(row["observed_delta_h_m"] - fixed_contribution)
        q = q_obs
    else:
        unknowns = POINTS
        design, observed = [], []
        for row in rows:
            coeff = [0.0] * len(unknowns)
            coeff[unknowns.index(row["from_point"])] -= 1.0
            coeff[unknowns.index(row["to_point"])] += 1.0
            design.append(coeff)
            observed.append(row["observed_delta_h_m"])
        # Add a stochastic observation of the datum point, not a hard fix.
        control_row = [1.0, 0.0, 0.0, 0.0, 0.0]
        design.append(control_row)
        observed.append(CONTROL_VALUE_M)
        q_full = [[0.0] * (n_obs + 1) for _ in range(n_obs + 1)]
        for i in range(n_obs):
            for j in range(n_obs):
                q_full[i][j] = q_obs[i][j]
        q_full[n_obs][n_obs] = (CONTROL_SIGMA_MM / 1000.0) ** 2
        q = q_full

    p = inverse(q)
    at = transpose(design)
    normal = multiply(multiply(at, p), design)
    rhs = matvec(multiply(at, p), observed)
    covariance = inverse(normal)
    estimate = solve(normal, rhs)
    fitted = matvec(design, estimate)
    residuals = [fitted[i] - observed[i] for i in range(len(observed))]
    weighted_sse = sum(residuals[i] * matvec(p, residuals)[i]
                       for i in range(len(residuals)))
    dof = len(observed) - len(unknowns)
    variance_factor = weighted_sse / dof if dof > 0 else float("nan")
    return unknowns, estimate, covariance, residuals, dof, variance_factor


def main():
    rows = read_data()
    cases = [
        ("A. Exact fixed datum; independent observations", True, False),
        ("B. Stochastic datum; independent observations", False, False),
        ("C. Stochastic datum; correlated observations", False, True),
    ]
    print("SYNTHETIC TEACHING DATA ONLY — NOT FIELD OBSERVATIONS")
    print(f"Control prior: A = {CONTROL_VALUE_M:.6f} m, sigma = {CONTROL_SIGMA_MM:.2f} mm")
    print(f"Session common-mode standard uncertainty: {SESSION_COMMON_SIGMA_MM:.2f} mm")
    results = {}
    for label, fixed, correlated in cases:
        names, x, cov, residuals, dof, vf = adjust(rows, fixed, correlated)
        values = dict(zip(names, x))
        results[label] = (names, x, cov, residuals, dof, vf)
        print("\n" + label)
        print(f"Unknowns: {len(names)}; observations including control: "
              f"{len(rows) + (0 if fixed else 1)}; redundancy: {dof}")
        print(f"Weighted residual sum: {vf*dof:.6f}; variance factor: {vf:.6f}")
        for i, name in enumerate(names):
            print(f"  {name}: {values[name]:.6f} m; formal u={math.sqrt(cov[i][i])*1000:.3f} mm")
        print("  Observation residuals (mm): " +
              ", ".join(f"{v*1000:+.3f}" for v in residuals[:len(rows)]))
        print("  Formal covariance matrix (mm^2):")
        for line in cov:
            print("    " + ", ".join(f"{v*1e6:.4f}" for v in line))

    print("\nInterpretation")
    print("- A fixed datum defines the datum as exact and suppresses its uncertainty.")
    print("- A stochastic control observation allows datum uncertainty to propagate.")
    print("- The correlated case uses Q = D + tau^2 Z Z^T, with one shared session effect per session.")
    print("- Correlation changes the information content and can change relative estimates and covariance.")
    print("- These outputs are conditional on the illustrative covariance model.")
    print("- Internal fit is not external validation; independent control/check observations remain necessary.")


if __name__ == "__main__":
    main()
