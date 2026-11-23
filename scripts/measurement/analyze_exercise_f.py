#!/usr/bin/env python3
"""Exercise F: global and local quality tests on a synthetic vertical network.

Standard-library only. All observations are synthetic. The script compares the
original network, a deliberately contaminated copy, and a diagnostic refit
with the contaminated observation withheld. Withholding is not an automatic
field decision.
"""
import csv
import math
from pathlib import Path

DATA = Path(__file__).resolve().parents[2] / "data" / "measurement" / "exercise-c-synthetic-control-network.csv"
POINTS = ("B", "C", "D", "E")
FIXED_POINT, FIXED_HEIGHT_M = "A", 100.0
ALPHA = 0.05
# Two-sided 95% chi-square limits for 5 degrees of freedom.
CHI2_LOWER_DF5, CHI2_UPPER_DF5 = 0.831, 12.833
# Bonferroni two-sided family-wise alpha=.05 over 9 simultaneous residual tests.
BONFERRONI_Z_9 = 2.772921


def solve(matrix, rhs):
    n = len(rhs)
    aug = [list(map(float, matrix[i])) + [float(rhs[i])] for i in range(n)]
    for col in range(n):
        pivot = max(range(col, n), key=lambda r: abs(aug[r][col]))
        if abs(aug[pivot][col]) < 1e-18:
            raise ValueError("Singular normal matrix")
        aug[col], aug[pivot] = aug[pivot], aug[col]
        scale = aug[col][col]
        aug[col] = [v / scale for v in aug[col]]
        for r in range(n):
            if r != col:
                f = aug[r][col]
                aug[r] = [aug[r][j] - f * aug[col][j] for j in range(n + 1)]
    return [aug[i][-1] for i in range(n)]


def inverse(matrix):
    n = len(matrix)
    cols = [solve(matrix, [1.0 if i == j else 0.0 for i in range(n)]) for j in range(n)]
    return [[cols[j][i] for j in range(n)] for i in range(n)]


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def load_rows():
    with DATA.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    for row in rows:
        for key in ("length_km", "observed_delta_h_m", "assumed_sigma_mm"):
            row[key] = float(row[key])
    return rows


def adjust(rows):
    n, u = len(rows), len(POINTS)
    design, rhs, variances = [], [], []
    for row in rows:
        coeff, constant = [0.0] * u, 0.0
        for point, sign in ((row["from_point"], -1.0), (row["to_point"], 1.0)):
            if point == FIXED_POINT:
                constant += sign * FIXED_HEIGHT_M
            elif point in POINTS:
                coeff[POINTS.index(point)] += sign
            else:
                raise ValueError("Unknown point: " + point)
        design.append(coeff)
        rhs.append(row["observed_delta_h_m"] - constant)
        sigma = row["assumed_sigma_mm"] / 1000.0
        if sigma <= 0:
            raise ValueError("A-priori uncertainties must be positive")
        variances.append(sigma * sigma)

    weights = [1.0 / q for q in variances]
    normal = [[sum(design[k][i] * weights[k] * design[k][j]
                   for k in range(n)) for j in range(u)] for i in range(u)]
    normal_rhs = [sum(design[k][i] * weights[k] * rhs[k]
                      for k in range(n)) for i in range(u)]
    qx = inverse(normal)
    x = solve(normal, normal_rhs)
    residuals = [dot(row, x) - rhs[k] for k, row in enumerate(design)]
    qvv_diag = []
    for k in range(n):
        propagated = sum(design[k][i] * qx[i][j] * design[k][j]
                         for i in range(u) for j in range(u))
        qvv_diag.append(variances[k] - propagated)
    weighted_sse = sum(weights[k] * residuals[k] ** 2 for k in range(n))
    dof = n - u
    if dof <= 0:
        raise ValueError("No redundancy: global test is unavailable")
    standardized = [residuals[k] / math.sqrt(qvv_diag[k])
                    for k in range(n)]
    return x, residuals, standardized, weighted_sse, dof


def report(label, rows):
    x, residuals, z, q, dof = adjust(rows)
    print("\n" + label)
    print(f"observations={len(rows)} unknowns=4 dof={dof}")
    print(f"weighted residual sum Q={q:.6f}; variance factor Q/dof={q/dof:.6f}")
    if dof == 5:
        print("two-sided 95% chi-square interval for df=5: "
              f"[{CHI2_LOWER_DF5:.3f}, {CHI2_UPPER_DF5:.3f}]")
        if q < CHI2_LOWER_DF5:
            verdict = "LOWER-TAIL: residuals unusually small relative to assumed uncertainties"
        elif q > CHI2_UPPER_DF5:
            verdict = "UPPER-TAIL: global model/weighting inconsistency"
        else:
            verdict = "inside two-sided 95% interval"
        print("global result: " + verdict)
    print("point,elevation_m")
    for p, h in zip(POINTS, x):
        print(f"{p},{h + FIXED_HEIGHT_M:.6f}")
    print("observation,residual_mm,standardized_residual")
    for row, v, w in zip(rows, residuals, z):
        print(f"{row['observation_id']},{v*1000:.3f},{w:.3f}")
    print(f"largest absolute standardized residual={max(map(abs,z)):.3f}")
    if len(rows) == 9:
        print(f"Bonferroni two-sided family-wise 5% threshold (9 tests): "
              f"|w|>{BONFERRONI_Z_9:.3f}")
    return x, q, z


def main():
    original = load_rows()
    contaminated = [dict(r) for r in original]
    # Deliberate +20 mm gross error in CE; not a real observation.
    contaminated[-1]["observed_delta_h_m"] += 0.020

    print("SYNTHETIC EXPERIMENT ONLY — NOT FIELD OBSERVATIONS")
    print("A=100.000 m is treated as exact; diagonal a-priori covariance is assumed.")
    print("Tests use the stated a-priori covariance (sigma0=1), not an estimated")
    print("posterior scale factor. Residuals are correlated through the adjustment.")
    report("A. Original synthetic network", original)
    report("B. Same network with +20 mm injected into CE", contaminated)

    # Diagnostic sensitivity analysis only: compare the contaminated fit with
    # CE withheld. This does not prove CE is wrong and does not authorise deletion.
    withheld = contaminated[:-1]
    x, q, z = report("C. Diagnostic refit with CE withheld (not an automatic remedy)", withheld)
    predicted_ea = x[3] - FIXED_HEIGHT_M
    independent_check = 2.4010  # synthetic independent A-to-E check, excluded from fit
    print("\nD. Independent synthetic A-to-E check (excluded from all adjustments)")
    print(f"check_delta_h={independent_check:.4f} m")
    print(f"withheld-model prediction={predicted_ea:.6f} m")
    print(f"prediction minus check={(predicted_ea-independent_check)*1000:.3f} mm")
    print("The check is independent evidence in this constructed example; a real")
    print("check must come from a separately planned and measured observation.")

    # Illustrative multiple-test warning: raw per-test 1.96 is not a family-wise
    # 5% threshold across nine correlated tests.
    print("\nInterpretation: a large residual identifies incompatibility, not cause.")
    print("Investigate field notes, instrument/setup, units, point identity, timing,")
    print("correlated sessions and independent checks before correcting or excluding data.")


if __name__ == "__main__":
    main()
