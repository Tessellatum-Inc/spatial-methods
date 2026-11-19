#!/usr/bin/env python3
"""Exercise E: free/minimally constrained adjustment of a synthetic height network.

Standard-library only. Reuses Exercise C's synthetic observations.
All values and uncertainty assumptions are educational, not field evidence.
"""
import csv
import math
from pathlib import Path

DATA = Path(__file__).resolve().parents[2] / "data" / "measurement" / "exercise-c-synthetic-control-network.csv"
POINTS = ("A", "B", "C", "D", "E")
CONTROL_A_M = 100.001
CONTROL_A_SIGMA_MM = 2.0


def solve(matrix, rhs, tolerance=1e-12):
    n = len(rhs)
    aug = [list(map(float, matrix[i])) + [float(rhs[i])] for i in range(n)]
    for col in range(n):
        pivot = max(range(col, n), key=lambda r: abs(aug[r][col]))
        if abs(aug[pivot][col]) <= tolerance:
            raise ValueError("Singular system: inspect network connectivity and constraints")
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


def transpose(a):
    return [list(col) for col in zip(*a)]


def multiply(a, b):
    bt = transpose(b)
    return [[sum(x * y for x, y in zip(row, col)) for col in bt] for row in a]


def matvec(a, x):
    return [sum(v * z for v, z in zip(row, x)) for row in a]


def read_observations():
    with DATA.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    for row in rows:
        row["observed_delta_h_m"] = float(row["observed_delta_h_m"])
        row["assumed_sigma_mm"] = float(row["assumed_sigma_mm"])
    return rows


def matrix_rank(matrix, tolerance=1e-10):
    a = [list(map(float, row)) for row in matrix]
    m, n = len(a), len(a[0])
    rank = 0
    for col in range(n):
        pivot = max(range(rank, m), key=lambda r: abs(a[r][col]), default=rank)
        if rank >= m or abs(a[pivot][col]) <= tolerance:
            continue
        a[rank], a[pivot] = a[pivot], a[rank]
        scale = a[rank][col]
        a[rank] = [v / scale for v in a[rank]]
        for r in range(m):
            if r != rank:
                factor = a[r][col]
                a[r] = [a[r][j] - factor * a[rank][j] for j in range(n)]
        rank += 1
        if rank == m:
            break
    return rank


def main():
    rows = read_observations()
    design, observed, variances = [], [], []
    for row in rows:
        coeff = [0.0] * len(POINTS)
        coeff[POINTS.index(row["from_point"])] -= 1.0
        coeff[POINTS.index(row["to_point"])] += 1.0
        design.append(coeff)
        observed.append(row["observed_delta_h_m"])
        sigma = row["assumed_sigma_mm"] / 1000.0
        if sigma <= 0:
            raise ValueError("Observation standard uncertainties must be positive")
        variances.append(sigma * sigma)

    n_obs, n_points = len(rows), len(POINTS)
    rank_a = matrix_rank(design)
    dof = n_obs - rank_a
    weights = [1.0 / v for v in variances]
    at = transpose(design)
    normal = multiply(multiply(at, [[weights[i] if i == j else 0.0
                                     for j in range(n_obs)] for i in range(n_obs)]), design)
    normal_rhs = matvec(multiply(at, [[weights[i] if i == j else 0.0
                                       for j in range(n_obs)] for i in range(n_obs)]), observed)

    # The unconstrained normal matrix is singular by one datum translation.
    try:
        solve(normal, normal_rhs)
        raise AssertionError("Expected one vertical datum defect, but normal matrix solved")
    except ValueError:
        pass

    # Inner constraint: arithmetic mean of all five heights equals zero.
    # This selects a coordinate origin; it is not an external height observation.
    constraint = [1.0] * n_points
    kkt = [normal[i] + [constraint[i]] for i in range(n_points)]
    kkt.append(constraint + [0.0])
    kkt_rhs = normal_rhs + [0.0]
    estimate = solve(kkt, kkt_rhs)[:n_points]
    kkt_inverse = inverse(kkt)
    covariance_inner = [row[:n_points] for row in kkt_inverse[:n_points]]

    residuals = [fit - obs for fit, obs in zip(matvec(design, estimate), observed)]
    weighted_sse = sum(w * v * v for w, v in zip(weights, residuals))
    variance_factor = weighted_sse / dof

    # A single external control transfers the free-network solution by a
    # common vertical translation. Its finite uncertainty affects absolute
    # heights, but cancels from all relative height differences.
    shift = CONTROL_A_M - estimate[POINTS.index("A")]
    transformed = [h + shift for h in estimate]
    control_var = (CONTROL_A_SIGMA_MM / 1000.0) ** 2
    covariance_external = [
        [covariance_inner[i][j] + control_var for j in range(n_points)]
        for i in range(n_points)
    ]

    print("SYNTHETIC DATA ONLY — NOT FIELD OBSERVATIONS")
    print(f"Observations: {n_obs}; height unknowns: {n_points}")
    print(f"Design-matrix rank: {rank_a}; datum defect: {n_points-rank_a}")
    print(f"Redundancy / residual degrees of freedom: {dof}")
    print("Unconstrained normal matrix is singular, as expected for a free height network.")
    print("Inner constraint: sum(H_i) = 0 (arbitrary vertical origin, not external control).")
    print(f"Weighted residual sum: {weighted_sse:.6f}; variance factor: {variance_factor:.6f}")
    print("\nFree-network elevations (m; mean is zero by inner constraint):")
    for p, h in zip(POINTS, estimate):
        print(f"  {p}: {h:+.6f}")
    print("\nExternal datum transfer:")
    print(f"  Control A: {CONTROL_A_M:.6f} m; assumed sigma: {CONTROL_A_SIGMA_MM:.3f} mm")
    print(f"  Applied common shift: {shift:+.6f} m")
    for p, h in zip(POINTS, transformed):
        i = POINTS.index(p)
        u = math.sqrt(max(0.0, covariance_external[i][i])) * 1000.0
        print(f"  {p}: {h:.6f} m; absolute formal u (illustrative): {u:.3f} mm")

    print("\nInner-constrained covariance matrix (formal mm^2; gauge-dependent):")
    for row in covariance_inner:
        print("  " + ", ".join(f"{v*1e6:.4f}" for v in row))
    print("\nRelative-height standard uncertainties (formal; invariant to common shift):")
    for p, q in (("B", "C"), ("B", "D"), ("C", "E")):
        i, j = POINTS.index(p), POINTS.index(q)
        var = covariance_inner[i][i] + covariance_inner[j][j] - 2*covariance_inner[i][j]
        print(f"  {p} to {q}: {math.sqrt(max(0.0, var))*1000:.3f} mm")

    print("\nInterpretation:")
    print("- The free network determines relative heights, not an absolute vertical origin.")
    print("- The sum-to-zero inner constraint selects one representative from equivalent solutions.")
    print("- One external height control supplies a translation; it does not independently validate the network.")
    print("- The external control's uncertainty is common to all transformed absolute heights.")
    print("- Relative-height uncertainty is unchanged by that common translation.")
    print("- The covariance matrix under the inner constraint depends on the chosen gauge; use relative quantities for datum-invariant interpretation.")


if __name__ == "__main__":
    main()
