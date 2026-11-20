"""Design-based accuracy estimation for samples stratified independently of the evaluated map.

Each observation has three distinct labels:
- sampling_stratum: the stratum used to select the sample;
- map_class: the evaluated map's class at the sampled location;
- reference_class: the interpreted reference class.

Assumes independent simple random sampling without replacement within each
sampling stratum and known stratum area proportions. It does not support
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

from area_adjusted_accuracy import (
    _interval,
    _validate_population_sizes,
    _validate_weights,
)


def _indicator_variance(
    predicate,
    counts: Mapping[str, Counter],
    sample_sizes: Mapping[str, int],
    weights: Mapping[str, float],
    fpc: Mapping[str, float],
) -> float:
    result = 0.0
    for stratum, weight in weights.items():
        n = sample_sizes[stratum]
        successes = sum(count for pair, count in counts[stratum].items() if predicate(*pair))
        p = successes / n
        result += weight**2 * p * (1.0 - p) / (n - 1) * fpc[stratum]
    return result


def _indicator_covariance(
    predicate_a,
    predicate_b,
    counts: Mapping[str, Counter],
    sample_sizes: Mapping[str, int],
    weights: Mapping[str, float],
    fpc: Mapping[str, float],
) -> float:
    result = 0.0
    for stratum, weight in weights.items():
        n = sample_sizes[stratum]
        p_a = sum(count for pair, count in counts[stratum].items() if predicate_a(*pair)) / n
        p_b = sum(count for pair, count in counts[stratum].items() if predicate_b(*pair)) / n
        # A is a subset of B for the UA and PA ratios below.
        covariance = p_a - p_a * p_b
        result += weight**2 * covariance / (n - 1) * fpc[stratum]
    return result


def _ratio_interval(
    numerator: float,
    denominator: float,
    variance_numerator: float,
    variance_denominator: float,
    covariance: float,
) -> dict | None:
    if denominator <= 0:
        return None
    estimate = numerator / denominator
    variance = (
        variance_numerator / denominator**2
        + numerator**2 * variance_denominator / denominator**4
        - 2.0 * numerator * covariance / denominator**3
    )
    return _interval(estimate, max(0.0, variance))


def estimate_stratified_accuracy(
    observations: Iterable[Mapping[str, str]],
    sampling_stratum_area_proportions: Mapping[str, float],
    *,
    total_area: float | None = None,
    stratum_population_sizes: Mapping[str, int] | None = None,
) -> dict:
    """Estimate accuracy when sample strata need not equal evaluated map classes.

    Matrix rows are evaluated-map classes; columns are reference classes.
    Every matrix cell is estimated as the sum, over sampling strata, of the
    stratum area weight multiplied by its observed joint class proportion.
    """
    weights = _validate_weights(sampling_stratum_area_proportions)
    population_sizes = _validate_population_sizes(stratum_population_sizes, weights)
    if total_area is not None and (
        not math.isfinite(float(total_area)) or float(total_area) <= 0
    ):
        raise ValueError("total_area must be finite and positive.")

    rows = list(observations)
    if not rows:
        raise ValueError("At least one labelled observation is required.")

    counts: dict[str, Counter] = {stratum: Counter() for stratum in weights}
    map_classes: set[str] = set()
    reference_classes: set[str] = set()

    for row_number, row in enumerate(rows, start=1):
        stratum = str(row.get("sampling_stratum", "")).strip()
        map_class = str(row.get("map_class", "")).strip()
        reference_class = str(row.get("reference_class", "")).strip()
        if not stratum or not map_class or not reference_class:
            raise ValueError(
                f"Row {row_number}: sampling_stratum, map_class and reference_class are required."
            )
        if stratum not in weights:
            raise ValueError(
                f"Row {row_number}: sampling stratum {stratum!r} has no area weight."
            )
        counts[stratum][(map_class, reference_class)] += 1
        map_classes.add(map_class)
        reference_classes.add(reference_class)

    sample_sizes = {
        stratum: sum(counts[stratum].values()) for stratum in weights
    }
    missing = [stratum for stratum, n in sample_sizes.items() if n < 2]
    if missing:
        raise ValueError(
            "At least two observations are required in every sampling stratum: "
            + ", ".join(missing)
        )
    if population_sizes is not None:
        undersized = [
            stratum for stratum, n in sample_sizes.items()
            if population_sizes[stratum] < n
        ]
        if undersized:
            raise ValueError(
                "Stratum population size cannot be smaller than its sample size: "
                + ", ".join(undersized)
            )

    fpc = {
        stratum: (
            1.0 - sample_sizes[stratum] / population_sizes[stratum]
            if population_sizes is not None else 1.0
        )
        for stratum in weights
    }

    maps = sorted(map_classes)
    refs = sorted(reference_classes)
    matrix: dict[str, dict[str, float]] = {}
    cell_variances: dict[str, dict[str, float]] = {}

    for map_class in maps:
        matrix[map_class] = {}
        cell_variances[map_class] = {}
        for reference_class in refs:
            predicate = lambda m, r, mc=map_class, rc=reference_class: (
                m == mc and r == rc
            )
            estimate = sum(
                weights[stratum]
                * sum(
                    count for (m, r), count in counts[stratum].items()
                    if predicate(m, r)
                ) / sample_sizes[stratum]
                for stratum in weights
            )
            variance = _indicator_variance(
                predicate, counts, sample_sizes, weights, fpc
            )
            matrix[map_class][reference_class] = estimate
            cell_variances[map_class][reference_class] = variance

    map_area = {}
    reference_area = {}
    for map_class in maps:
        predicate = lambda m, r, mc=map_class: m == mc
        estimate = sum(matrix[map_class].values())
        variance = _indicator_variance(
            predicate, counts, sample_sizes, weights, fpc
        )
        result = _interval(estimate, variance)
        if total_area is not None:
            result["estimated_area"] = estimate * float(total_area)
            result["estimated_area_standard_error"] = math.sqrt(max(0.0, variance)) * float(total_area)
            result["estimated_area_ci95_wald"] = [
                result["ci95_wald"][0] * float(total_area),
                result["ci95_wald"][1] * float(total_area),
            ]
        map_area[map_class] = result

    for reference_class in refs:
        predicate = lambda m, r, rc=reference_class: r == rc
        estimate = sum(matrix[map_class][reference_class] for map_class in maps)
        variance = _indicator_variance(
            predicate, counts, sample_sizes, weights, fpc
        )
        result = _interval(estimate, variance)
        if total_area is not None:
            result["estimated_area"] = estimate * float(total_area)
            result["estimated_area_standard_error"] = math.sqrt(max(0.0, variance)) * float(total_area)
            result["estimated_area_ci95_wald"] = [
                result["ci95_wald"][0] * float(total_area),
                result["ci95_wald"][1] * float(total_area),
            ]
        reference_area[reference_class] = result

    overall_accuracy = sum(
        matrix[map_class].get(map_class, 0.0)
        for map_class in maps if map_class in refs
    )
    correct = lambda m, r: m == r
    var_oa = _indicator_variance(
        correct, counts, sample_sizes, weights, fpc
    )
    oa = _interval(overall_accuracy, var_oa)

    users = {}
    for map_class in maps:
        numerator = matrix[map_class].get(map_class, 0.0)
        denominator = map_area[map_class]["estimate"]
        diag_predicate = lambda m, r, c=map_class: m == c and r == c
        map_predicate = lambda m, r, c=map_class: m == c
        var_num = _indicator_variance(
            diag_predicate, counts, sample_sizes, weights, fpc
        )
        var_den = _indicator_variance(
            map_predicate, counts, sample_sizes, weights, fpc
        )
        cov = _indicator_covariance(
            diag_predicate, map_predicate, counts, sample_sizes, weights, fpc
        )
        users[map_class] = _ratio_interval(
            numerator, denominator, var_num, var_den, cov
        )

    producers = {}
    for reference_class in refs:
        numerator = matrix.get(reference_class, {}).get(reference_class, 0.0)
        denominator = reference_area[reference_class]["estimate"]
        diag_predicate = lambda m, r, c=reference_class: m == c and r == c
        ref_predicate = lambda m, r, c=reference_class: r == c
        var_num = _indicator_variance(
            diag_predicate, counts, sample_sizes, weights, fpc
        )
        var_den = _indicator_variance(
            ref_predicate, counts, sample_sizes, weights, fpc
        )
        cov = _indicator_covariance(
            diag_predicate, ref_predicate, counts, sample_sizes, weights, fpc
        )
        producers[reference_class] = _ratio_interval(
            numerator, denominator, var_num, var_den, cov
        )

    return {
        "design": "stratified simple random sampling within supplied sampling strata",
        "confusion_matrix_orientation": "rows=evaluated map classes; columns=reference classes",
        "sampling_stratum_area_proportions": weights,
        "stratum_population_sizes": population_sizes,
        "finite_population_correction_by_sampling_stratum": (
            fpc if population_sizes is not None else None
        ),
        "sample_counts_by_sampling_stratum": sample_sizes,
        "sample_size": len(rows),
        "estimated_area_proportion_error_matrix": matrix,
        "estimated_cell_variances": cell_variances,
        "overall_accuracy": oa,
        "users_accuracy_by_map_class": users,
        "producers_accuracy_by_reference_class": producers,
        "mapped_class_area_proportions": map_area,
        "reference_class_area_proportions": reference_area,
        "total_area": float(total_area) if total_area is not None else None,
        "interval_method": "normal-approximation Wald 95% intervals, clipped to [0, 1]",
        "limitations": [
            "Requires probability sampling with independent simple random sampling within each supplied sampling stratum.",
            "Sampling strata may differ from evaluated map classes; stratum area proportions must describe the same target population as the reference sample.",
            "Does not support arbitrary unequal inclusion probabilities, cluster designs, or general systematic/spatially balanced designs.",
            "Map and reference class labels must be harmonised to a defensible common legend before accuracy metrics are interpreted.",
            "Reference labels are treated as error-free; reference uncertainty is not propagated.",
            "Wald intervals and delta-method ratio intervals are approximations and may perform poorly for small samples or estimates near 0 or 1.",
            "Finite-population correction is applied only when valid population sizes are supplied for every sampling stratum.",
            "No nonresponse adjustment, variance from stratum area weights, or spatial covariance is included."
        ],
    }


def read_observations(path: str | Path) -> list[dict[str, str]]:
    with Path(path).open("r", newline="", encoding="utf-8-sig") as stream:
        reader = csv.DictReader(stream)
        required = {"sampling_stratum", "map_class", "reference_class"}
        if not reader.fieldnames or not required.issubset(reader.fieldnames):
            raise ValueError(
                "CSV must contain sampling_stratum,map_class,reference_class columns."
            )
        return list(reader)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("observations_csv")
    parser.add_argument("--stratum-area-weights", required=True,
                        help='JSON object, e.g. \'{"stratum_a":0.5,"stratum_b":0.5}\'')
    parser.add_argument("--stratum-population-sizes", default=None,
                        help='Optional JSON object keyed by sampling stratum')
    parser.add_argument("--total-area", type=float, default=None)
    parser.add_argument("--json-out", default=None)
    args = parser.parse_args()
    try:
        weights = json.loads(args.stratum_area_weights)
        if not isinstance(weights, dict):
            raise ValueError("--stratum-area-weights must decode to a JSON object.")
        population_sizes = (
            json.loads(args.stratum_population_sizes)
            if args.stratum_population_sizes else None
        )
        if population_sizes is not None and not isinstance(population_sizes, dict):
            raise ValueError("--stratum-population-sizes must decode to a JSON object.")
        report = estimate_stratified_accuracy(
            read_observations(args.observations_csv),
            weights,
            total_area=args.total_area,
            stratum_population_sizes=population_sizes,
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
