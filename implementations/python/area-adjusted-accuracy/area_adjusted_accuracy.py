"""Design-based accuracy and reference-area estimates for map-stratified samples.

Input observations are sampled units with map_class and reference_class labels.
The estimator assumes independent simple random sampling within each mapped
class (map class = sampling stratum). It is not a generic estimator for
arbitrary unequal-probability, clustered, systematic, or spatially balanced
designs.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
from collections import Counter
from pathlib import Path
from typing import Iterable, Mapping

Z_975 = 1.959963984540054


def _validate_weights(weights: Mapping[str, float]) -> dict[str, float]:
    if not weights:
        raise ValueError("At least one mapped-class area weight is required.")
    clean = {}
    for key, value in weights.items():
        name = str(key).strip()
        if not name:
            raise ValueError("Mapped-class labels must be non-empty.")
        number = float(value)
        if not math.isfinite(number) or number <= 0:
            raise ValueError(f"Area weight for {name!r} must be finite and positive.")
        clean[name] = number
    total = sum(clean.values())
    if not math.isclose(total, 1.0, rel_tol=0.0, abs_tol=1e-8):
        raise ValueError(f"Mapped-class area weights must sum to 1 (got {total:.12g}).")
    return clean


def _interval(estimate: float, variance: float) -> dict[str, float]:
    se = math.sqrt(max(0.0, variance))
    lo = max(0.0, estimate - Z_975 * se)
    hi = min(1.0, estimate + Z_975 * se)
    return {"estimate": estimate, "standard_error": se,
            "ci95_wald": [lo, hi]}


def estimate_stratified_accuracy(
    observations: Iterable[Mapping[str, str]],
    mapped_class_area_proportions: Mapping[str, float],
    *,
    total_area: float | None = None,
) -> dict:
    """Estimate area-adjusted accuracy for SRS samples within mapped classes.

    Confusion-matrix orientation: rows = mapped classes (strata),
    columns = reference classes. Area weights are proportions of total map area.
    """
    weights = _validate_weights(mapped_class_area_proportions)
    rows = list(observations)
    if not rows:
        raise ValueError("At least one labelled sample observation is required.")
    if total_area is not None and (not math.isfinite(float(total_area)) or float(total_area) <= 0):
        raise ValueError("total_area must be finite and positive.")

    mapped = set(weights)
    reference_classes = set()
    counts: dict[str, Counter] = {k: Counter() for k in weights}
    for row_number, row in enumerate(rows, start=1):
        m = str(row.get("map_class", "")).strip()
        r = str(row.get("reference_class", "")).strip()
        if not m or not r:
            raise ValueError(f"Row {row_number}: map_class and reference_class are required.")
        if m not in mapped:
            raise ValueError(f"Row {row_number}: mapped class {m!r} has no area weight.")
        counts[m][r] += 1
        reference_classes.add(r)

    classes = sorted(mapped | reference_classes)
    n_by_stratum = {m: sum(counts[m].values()) for m in weights}
    missing = [m for m, n in n_by_stratum.items() if n < 2]
    if missing:
        raise ValueError("At least two observations are required in every mapped-class stratum: "
                         + ", ".join(missing))

    # Estimated area-proportion error matrix.
    matrix = {}
    row_proportions = {}
    for m, w in weights.items():
        n = n_by_stratum[m]
        row_proportions[m] = {r: counts[m][r] / n for r in classes}
        matrix[m] = {r: w * row_proportions[m][r] for r in classes}

    overall_accuracy = sum(matrix[c][c] for c in classes if c in matrix)
    var_oa = sum(
        weights[m] ** 2 * row_proportions[m][m] *
        (1.0 - row_proportions[m][m]) / (n_by_stratum[m] - 1)
        for m in weights
    )
    oa = _interval(overall_accuracy, var_oa)

    users = {}
    for m in weights:
        p = row_proportions[m][m] if m in classes else 0.0
        users[m] = _interval(p, p * (1.0 - p) / (n_by_stratum[m] - 1))

    reference_area = {}
    producers = {}
    for ref in classes:
        estimate = sum(matrix[m][ref] for m in weights)
        variance = sum(
            weights[m] ** 2 * row_proportions[m][ref] *
            (1.0 - row_proportions[m][ref]) / (n_by_stratum[m] - 1)
            for m in weights
        )
        area_result = _interval(estimate, variance)
        if total_area is not None:
            area_result["estimated_area"] = estimate * float(total_area)
            area_result["estimated_area_standard_error"] = math.sqrt(max(0.0, variance)) * float(total_area)
            area_result["estimated_area_ci95_wald"] = [
                area_result["ci95_wald"][0] * float(total_area),
                area_result["ci95_wald"][1] * float(total_area),
            ]
        reference_area[ref] = area_result

        if estimate <= 0:
            producers[ref] = None
            continue
        numerator = matrix.get(ref, {}).get(ref, 0.0)
        # Delta-method variance for the ratio of the diagonal cell to the
        # reference-class column total. Stratum samples are treated as
        # independent; the numerator is one component of the denominator.
        numerator_var = (
            weights[ref] ** 2 * row_proportions[ref][ref] *
            (1.0 - row_proportions[ref][ref]) / (n_by_stratum[ref] - 1)
            if ref in weights else 0.0
        )
        covariance = numerator_var
        ratio_var = (
            numerator_var / estimate**2
            + numerator**2 * variance / estimate**4
            - 2.0 * numerator * covariance / estimate**3
        )
        producers[ref] = _interval(numerator / estimate, max(0.0, ratio_var))

    return {
        "design": "stratified simple random sampling within mapped classes",
        "confusion_matrix_orientation": "rows=mapped classes; columns=reference classes",
        "mapped_class_area_proportions": weights,
        "sample_counts_by_mapped_class": n_by_stratum,
        "sample_size": len(rows),
        "estimated_area_proportion_error_matrix": matrix,
        "overall_accuracy": oa,
        "users_accuracy_by_mapped_class": users,
        "producers_accuracy_by_reference_class": producers,
        "reference_class_area_proportions": reference_area,
        "total_area": float(total_area) if total_area is not None else None,
        "interval_method": "normal-approximation Wald 95% intervals, clipped to [0, 1]",
        "limitations": [
            "Requires probability sampling with independent SRS within each mapped-class stratum.",
            "Does not support arbitrary unequal inclusion probabilities, cluster designs, or general systematic/spatially balanced designs.",
            "Reference labels are treated as error-free; reference uncertainty is not propagated.",
            "Wald intervals may perform poorly for small samples or estimates near 0 or 1.",
            "No finite-population correction is applied because stratum population sizes are not supplied.",
            "No nonresponse adjustment, variance from map-area weights, or spatial covariance is included.",
            "Area estimates are only as defensible as the sampling frame, response protocol, map-area proportions, and reference interpretation."
        ],
    }


def read_observations(path: str | Path) -> list[dict[str, str]]:
    with Path(path).open("r", newline="", encoding="utf-8-sig") as stream:
        reader = csv.DictReader(stream)
        required = {"map_class", "reference_class"}
        if not reader.fieldnames or not required.issubset(reader.fieldnames):
            raise ValueError("CSV must contain map_class and reference_class columns.")
        return list(reader)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("observations_csv", help="CSV with map_class,reference_class columns")
    parser.add_argument("--area-weights", required=True,
                        help='JSON object, e.g. \'{"forest":0.6,"other":0.4}\'')
    parser.add_argument("--total-area", type=float, default=None,
                        help="Optional total mapped area in stated area units")
    parser.add_argument("--json-out", default=None)
    args = parser.parse_args()
    try:
        weights = json.loads(args.area_weights)
        if not isinstance(weights, dict):
            raise ValueError("--area-weights must decode to a JSON object.")
        report = estimate_stratified_accuracy(
            read_observations(args.observations_csv), weights, total_area=args.total_area
        )
    except (OSError, ValueError, TypeError, json.JSONDecodeError) as exc:
        parser.error(str(exc))
    rendered = json.dumps(report, indent=2, sort_keys=True)
    if args.json_out:
        Path(args.json_out).write_text(rendered + "\n", encoding="utf-8")
    print(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
