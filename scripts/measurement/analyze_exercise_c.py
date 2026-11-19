#!/usr/bin/env python3
"""Reproduce Exercise C: weighted adjustment of a synthetic height network."""
import csv, math
from pathlib import Path

DATA = Path(__file__).resolve().parents[2] / "data" / "measurement" / "exercise-c-synthetic-control-network.csv"
FIXED_POINT, FIXED_ELEVATION_M = "A", 100.0
UNKNOWN_POINTS = ("B", "C", "D", "E")

def solve(matrix, rhs):
    n = len(rhs)
    aug = [list(map(float, matrix[i])) + [float(rhs[i])] for i in range(n)]
    for col in range(n):
        pivot = max(range(col, n), key=lambda row: abs(aug[row][col]))
        if abs(aug[pivot][col]) < 1e-18:
            raise ValueError("Singular normal matrix: check datum and connectivity")
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
    cols = [solve(matrix, [1.0 if i == j else 0.0 for i in range(n)]) for j in range(n)]
    return [[cols[j][i] for j in range(n)] for i in range(n)]

def dot(a, b):
    return sum(x*y for x, y in zip(a, b))

def main():
    with DATA.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    for row in rows:
        for key in ("length_km", "observed_delta_h_m", "assumed_sigma_mm"):
            row[key] = float(row[key])
    n_obs, n_unknown = len(rows), len(UNKNOWN_POINTS)
    if n_obs <= n_unknown:
        raise ValueError("Network requires redundant observations")
    design, rhs, variances = [], [], []
    for row in rows:
        coeff, constant = [0.0]*n_unknown, 0.0
        for point, sign in ((row["from_point"], -1.0), (row["to_point"], 1.0)):
            if point == FIXED_POINT:
                constant += sign * FIXED_ELEVATION_M
            elif point in UNKNOWN_POINTS:
                coeff[UNKNOWN_POINTS.index(point)] += sign
            else:
                raise ValueError("Unknown point ID: " + point)
        design.append(coeff)
        rhs.append(row["observed_delta_h_m"] - constant)
        sigma = row["assumed_sigma_mm"] / 1000.0
        if sigma <= 0:
            raise ValueError("A-priori standard uncertainties must be positive")
        variances.append(sigma*sigma)
    weights = [1.0/q for q in variances]
    normal = [[sum(design[k][i]*weights[k]*design[k][j] for k in range(n_obs))
               for j in range(n_unknown)] for i in range(n_unknown)]
    normal_rhs = [sum(design[k][i]*weights[k]*rhs[k] for k in range(n_obs))
                  for i in range(n_unknown)]
    q_x = inverse(normal)
    estimates = solve(normal, normal_rhs)
    residuals = [dot(row, estimates)-rhs[k] for k, row in enumerate(design)]
    weighted_sse = sum(weights[k]*residuals[k]**2 for k in range(n_obs))
    dof = n_obs-n_unknown
    variance_factor = weighted_sse/dof
    sigma0 = math.sqrt(variance_factor)
    qvv_diag = []
    for k in range(n_obs):
        propagated = sum(design[k][i]*q_x[i][j]*design[k][j]
                         for i in range(n_unknown) for j in range(n_unknown))
        qvv_diag.append(variances[k]-propagated)

    print("SYNTHETIC DATA ONLY — NOT FIELD OBSERVATIONS")
    print(f"Observations: {n_obs}; unknowns: {n_unknown}; redundancy/DOF: {dof}")
    print(f"Fixed datum: A = {FIXED_ELEVATION_M:.3f} m (treated as exact)")
    print(f"Weighted sum of squared residuals: {weighted_sse:.6f}")
    print(f"Posterior variance factor: {variance_factor:.6f}; sqrt: {sigma0:.6f}")
    print("\nAdjusted elevations and formal standard uncertainties:")
    for i, point in enumerate(UNKNOWN_POINTS):
        u = math.sqrt(q_x[i][i])
        print(f"{point}: {estimates[i]:.6f} m; "
              f"formal u={u*1000:.3f} mm; posterior-scaled u={u*sigma0*1000:.3f} mm")
    print("\nResiduals (adjusted minus observed):")
    print("id,from,to,residual_mm,normalized_residual")
    for k, row in enumerate(rows):
        nr = residuals[k]/math.sqrt(qvv_diag[k]) if qvv_diag[k] > 1e-18 else float("nan")
        print(f"{row['observation_id']},{row['from_point']},{row['to_point']},"
              f"{residuals[k]*1000:.3f},{nr:.3f}")
    print("\nParameter covariance matrix (formal, mm^2):")
    for row in q_x:
        print("  "+", ".join(f"{v*1e6:.4f}" for v in row))
    print("\nRelative-height uncertainty examples (formal):")
    for p, q in (("B","C"),("B","D"),("C","E")):
        i, j = UNKNOWN_POINTS.index(p), UNKNOWN_POINTS.index(q)
        var = q_x[i][i]+q_x[j][j]-2*q_x[i][j]
        print(f"{p} to {q}: u(ΔH)={math.sqrt(max(0.0,var))*1000:.3f} mm")
    print("\nResiduals are internal diagnostics, not automatic blunder verdicts.")
    print("Independent checks and field evidence remain necessary.")

if __name__ == "__main__":
    main()
