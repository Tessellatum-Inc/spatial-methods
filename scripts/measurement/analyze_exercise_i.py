#!/usr/bin/env python3
"""Exercise I: compare least squares, iterative data snooping and Huber IRLS.

Standard-library only. All scenarios are synthetic. The Huber estimator uses
fixed a-priori observation standard uncertainties as its scale reference.
Sequential data snooping is a diagnostic heuristic, not an exact family-wise
procedure across repeated rounds of testing.
"""
import csv
import math
from pathlib import Path

DATA = (Path(__file__).resolve().parents[2] / "data" / "measurement"
        / "exercise-c-synthetic-control-network.csv")
POINTS = ("B", "C", "D", "E")
FIXED_POINT = "A"
FIXED_HEIGHT_M = 100.0
TRUE_HEIGHTS_M = (101.2, 102.0, 101.7, 102.4)
FAMILY_ALPHA = 0.01
HUBER_C = 1.345
MAX_ITERATIONS = 100
CONVERGENCE_TOLERANCE = 1e-10


def solve(matrix, rhs):
    n = len(rhs)
    augmented = [list(map(float, matrix[i])) + [float(rhs[i])]
                 for i in range(n)]
    for col in range(n):
        pivot = max(range(col, n), key=lambda row: abs(augmented[row][col]))
        if abs(augmented[pivot][col]) < 1e-18:
            raise ValueError("Singular or underconstrained adjustment")
        augmented[col], augmented[pivot] = augmented[pivot], augmented[col]
        scale = augmented[col][col]
        augmented[col] = [value / scale for value in augmented[col]]
        for row in range(n):
            if row != col:
                factor = augmented[row][col]
                augmented[row] = [
                    augmented[row][j] - factor * augmented[col][j]
                    for j in range(n + 1)
                ]
    return [augmented[i][-1] for i in range(n)]


def inverse(matrix):
    n = len(matrix)
    columns = [
        solve(matrix, [float(i == j) for i in range(n)])
        for j in range(n)
    ]
    return [[columns[j][i] for j in range(n)] for i in range(n)]


def normal_cdf(value):
    return 0.5 * (1.0 + math.erf(value / math.sqrt(2.0)))


def normal_quantile(probability):
    lower, upper = -9.0, 9.0
    for _ in range(100):
        middle = (lower + upper) / 2.0
        if normal_cdf(middle) < probability:
            lower = middle
        else:
            upper = middle
    return (lower + upper) / 2.0


def load_rows():
    with DATA.open(newline="", encoding="utf-8") as source:
        rows = list(csv.DictReader(source))
    for row in rows:
        for field in ("observed_delta_h_m", "assumed_sigma_mm"):
            row[field] = float(row[field])
    return rows


def build_observation_model(rows):
    design, reduced_observations, sigmas = [], [], []
    for row in rows:
        coefficients = [0.0] * len(POINTS)
        fixed_contribution = 0.0
        for point, sign in (
            (row["from_point"], -1.0),
            (row["to_point"], 1.0),
        ):
            if point == FIXED_POINT:
                fixed_contribution += sign * FIXED_HEIGHT_M
            elif point in POINTS:
                coefficients[POINTS.index(point)] += sign
            else:
                raise ValueError("Unknown point identifier: " + point)
        design.append(coefficients)
        reduced_observations.append(
            row["observed_delta_h_m"] - fixed_contribution
        )
        sigma = row["assumed_sigma_mm"] / 1000.0
        if sigma <= 0:
            raise ValueError("Observation standard uncertainties must be positive")
        sigmas.append(sigma)
    return design, reduced_observations, sigmas


def fit(rows, equivalent_weights=None):
    design, observations, sigmas = build_observation_model(rows)
    n, u = len(rows), len(POINTS)
    if n <= u:
        raise ValueError("No residual redundancy remains")
    multipliers = equivalent_weights or [1.0] * n
    weights = [
        multipliers[i] / (sigmas[i] ** 2) for i in range(n)
    ]
    normal = [
        [
            sum(design[k][i] * weights[k] * design[k][j]
                for k in range(n))
            for j in range(u)
        ]
        for i in range(u)
    ]
    qx = inverse(normal)
    normal_rhs = [
        sum(design[k][i] * weights[k] * observations[k]
            for k in range(n))
        for i in range(u)
    ]
    estimates = solve(normal, normal_rhs)
    residuals = [
        sum(design[k][j] * estimates[j] for j in range(u)) - observations[k]
        for k in range(n)
    ]

    # Formal standardised residuals for the unmodified LS stochastic model.
    # They are used by data snooping, where equivalent_weights are all unity.
    residual_variances = []
    for k in range(n):
        propagated = sum(
            design[k][i] * qx[i][j] * design[k][j]
            for i in range(u) for j in range(u)
        )
        residual_variances.append(max(1e-24, sigmas[k] ** 2 - propagated))
    standardised = [
        residuals[i] / math.sqrt(residual_variances[i]) for i in range(n)
    ]
    return estimates, residuals, standardised


def least_squares(rows):
    return fit(rows)


def iterative_data_snooping(rows):
    active = list(range(len(rows)))
    removed = []
    history = []
    while True:
        subset = [rows[index] for index in active]
        estimates, residuals, standardised = fit(subset)
        n = len(active)
        critical = normal_quantile(1.0 - FAMILY_ALPHA / (2.0 * n))
        worst = max(range(n), key=lambda index: abs(standardised[index]))
        history.append((n, critical, max(map(abs, standardised))))
        if abs(standardised[worst]) <= critical:
            break
        if n - 1 <= len(POINTS):
            break
        removed.append(active.pop(worst))
    return estimates, removed, history


def huber_irls(rows):
    n = len(rows)
    sigmas = [row["assumed_sigma_mm"] / 1000.0 for row in rows]
    equivalent_weights = [1.0] * n
    converged = False

    for iteration in range(1, MAX_ITERATIONS + 1):
        estimates, residuals, _ = fit(rows, equivalent_weights)
        # Huber IRLS uses residual / original a-priori sigma as its scale
        # reference. Do not use LS studentised residuals after reweighting.
        normalised = [
            residuals[i] / sigmas[i] for i in range(n)
        ]
        updated = [
            1.0 if abs(value) <= HUBER_C else HUBER_C / abs(value)
            for value in normalised
        ]
        change = max(
            abs(updated[i] - equivalent_weights[i]) for i in range(n)
        )
        equivalent_weights = updated
        if change < CONVERGENCE_TOLERANCE:
            converged = True
            break

    estimates, residuals, _ = fit(rows, equivalent_weights)
    normalised = [residuals[i] / sigmas[i] for i in range(n)]
    return estimates, equivalent_weights, iteration, converged, normalised


def coordinate_errors_mm(estimates):
    return [
        1000.0 * (estimates[i] - TRUE_HEIGHTS_M[i])
        for i in range(len(POINTS))
    ]


def rmse_mm(errors):
    return math.sqrt(sum(value * value for value in errors) / len(errors))


def report_scenario(rows, label):
    ls_estimates, _, _ = least_squares(rows)
    snoop_estimates, removed, history = iterative_data_snooping(rows)
    huber_estimates, weights, iterations, converged, normalised = huber_irls(rows)

    print("\n" + label)
    print("method,estimated_B_m,estimated_C_m,estimated_D_m,estimated_E_m,"
          "error_B_mm,error_C_mm,error_D_mm,error_E_mm,coordinate_RMSE_mm")
    for name, estimates in (
        ("least_squares", ls_estimates),
        ("iterative_data_snooping", snoop_estimates),
        ("Huber_IRLS", huber_estimates),
    ):
        errors = coordinate_errors_mm(estimates)
        print(
            name + "," +
            ",".join(f"{value:.6f}" for value in estimates) + "," +
            ",".join(f"{value:+.2f}" for value in errors) + "," +
            f"{rmse_mm(errors):.2f}"
        )

    print("Data-snooping observations withheld diagnostically:",
          [rows[index]["observation_id"] for index in removed])
    print("Sequential test history (n, critical value, max |standardised residual|):",
          [(n, round(critical, 3), round(maximum, 3))
           for n, critical, maximum in history])
    print(f"Huber iterations={iterations}; converged={converged}")
    print("Huber equivalent weights:",
          ", ".join(
              f"{rows[i]['observation_id']}={weights[i]:.3f}"
              for i in range(len(rows))
          ))
    print("Huber residuals / original a-priori sigma:",
          ", ".join(
              f"{rows[i]['observation_id']}={normalised[i]:+.2f}"
              for i in range(len(rows))
          ))


def main():
    original = load_rows()
    single_error = [dict(row) for row in original]
    single_error[-1]["observed_delta_h_m"] += 0.020
    multiple_errors = [dict(row) for row in original]
    multiple_errors[3]["observed_delta_h_m"] += 0.015  # BD +15 mm
    multiple_errors[8]["observed_delta_h_m"] -= 0.015  # CE -15 mm

    print("EXERCISE I — SYNTHETIC ONLY; NOT FIELD OBSERVATIONS")
    print(f"Huber tuning constant c={HUBER_C} (conventional normal-theory choice)")
    print(f"Data-snooping per-round Bonferroni alpha={FAMILY_ALPHA}")
    print("Constructed reference elevations: B=101.200, C=102.000, "
          "D=101.700, E=102.400 m.")
    report_scenario(original, "A. Original synthetic dataset")
    report_scenario(single_error, "B. Single gross error: CE +20 mm")
    report_scenario(
        multiple_errors,
        "C. Two gross errors: BD +15 mm and CE -15 mm"
    )
    print("\nCautions:")
    print("- Sequential data snooping is a heuristic; repeating tests after")
    print("  deletion does not retain a simple one-shot family-wise guarantee.")
    print("- A withheld observation is not automatically wrong; investigate")
    print("  field records and independent checks before any exclusion.")
    print("- Huber downweights influence but does not prove the cause of a")
    print("  large residual or identify a physical blunder by itself.")
    print("- Huber weights use fixed a-priori sigmas; no posterior scale")
    print("  rescaling or uncertainty-coverage claim is made.")


if __name__ == "__main__":
    main()
