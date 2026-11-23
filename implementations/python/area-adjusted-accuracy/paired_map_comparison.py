"""Design-based paired comparison of two maps on the same stratified sample.

The baseline map is represented by the original sampling-stratum label in the
Fiji sample. The evaluated map is the sampled WorldCover class. The estimator
uses within-stratum paired correctness differences, preserving covariance
between the two map assessments.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
from collections import defaultdict
from pathlib import Path


def compare_maps(
    rows: list[dict[str, str]],
    stratum_area_weights: dict[str, float],
    *,
    baseline_column: str = "sampling_stratum",
    stratum_population_sizes: dict[str, int] | None = None,
) -> dict:
    if not rows:
        raise ValueError("At least one paired sample record is required.")
    weights = {str(k): float(v) for k, v in stratum_area_weights.items()}
    if not weights or any(not math.isfinite(v) or v <= 0 for v in weights.values()):
        raise ValueError("Stratum area weights must be finite and positive.")
    if not math.isclose(sum(weights.values()), 1.0, rel_tol=0.0, abs_tol=1e-9):
        raise ValueError("Stratum area weights must sum to one.")
    populations = None
    if stratum_population_sizes is not None:
        populations = {str(k): int(v) for k, v in stratum_population_sizes.items()}
        if set(populations) != set(weights):
            raise ValueError("Population-size keys must exactly match area-weight keys.")
        if any(v <= 0 for v in populations.values()):
            raise ValueError("Stratum population sizes must be positive.")

    grouped = defaultdict(list)
    for index, row in enumerate(rows, start=1):
        required = ("sampling_stratum", "map_class", "reference_class", baseline_column)
        if any(not str(row.get(key, "")).strip() for key in required):
            raise ValueError(f"Record {index} has a missing required class label.")
        stratum = str(row["sampling_stratum"]).strip()
        if stratum not in weights:
            raise ValueError(f"Record {index} has unknown sampling stratum {stratum!r}.")
        evaluated_correct = int(str(row["map_class"]).strip() == str(row["reference_class"]).strip())
        baseline_correct = int(str(row[baseline_column]).strip() == str(row["reference_class"]).strip())
        grouped[stratum].append((evaluated_correct, baseline_correct))

    if set(grouped) != set(weights):
        missing = sorted(set(weights) - set(grouped))
        raise ValueError(f"No sample records for weighted strata: {missing}.")
    if any(len(values) < 2 for values in grouped.values()):
        raise ValueError("At least two sampled units are required in every stratum.")

    evaluated_oa = 0.0
    baseline_oa = 0.0
    difference = 0.0
    variance_difference = 0.0
    stratum_results = {}
    for stratum in sorted(weights):
        values = grouped[stratum]
        n = len(values)
        evaluated_values = [pair[0] for pair in values]
        baseline_values = [pair[1] for pair in values]
        differences = [a - b for a, b in values]
        mean_evaluated = sum(evaluated_values) / n
        mean_baseline = sum(baseline_values) / n
        mean_difference = sum(differences) / n
        sample_variance = sum((x - mean_difference) ** 2 for x in differences) / (n - 1)
        fpc = 1.0
        if populations is not None:
            if populations[stratum] < n:
                raise ValueError(
                    f"Population size for {stratum!r} is smaller than its sample size."
                )
            fpc = 1.0 - n / populations[stratum]
        contribution = weights[stratum] ** 2 * fpc * sample_variance / n
        evaluated_oa += weights[stratum] * mean_evaluated
        baseline_oa += weights[stratum] * mean_baseline
        difference += weights[stratum] * mean_difference
        variance_difference += contribution
        stratum_results[stratum] = {
            "sample_size": n,
            "evaluated_map_accuracy": mean_evaluated,
            "baseline_map_accuracy": mean_baseline,
            "paired_accuracy_difference": mean_difference,
            "sample_variance_of_paired_difference": sample_variance,
            "finite_population_correction": fpc,
            "variance_contribution": contribution,
        }

    standard_error = math.sqrt(max(0.0, variance_difference))
    return {
        "design": "paired comparison under stratified simple random sampling without replacement",
        "evaluated_map_column": "map_class",
        "baseline_map_column": baseline_column,
        "sampling_stratum_column": "sampling_stratum",
        "reference_column": "reference_class",
        "sampling_stratum_area_proportions": weights,
        "stratum_population_sizes": populations,
        "sample_size": len(rows),
        "evaluated_map_overall_accuracy": evaluated_oa,
        "baseline_map_overall_accuracy": baseline_oa,
        "evaluated_minus_baseline_accuracy_difference": {
            "estimate": difference,
            "standard_error": standard_error,
            "ci95_wald": [difference - 1.96 * standard_error, difference + 1.96 * standard_error],
        },
        "stratum_diagnostics": stratum_results,
        "limitations": [
            "Both maps must be evaluated on the same sampled units, reference labels, target domain and response protocol.",
            "The baseline map column must contain its mapped class at each sampled location; using the sampling stratum as the baseline is valid only when the original map class defined that stratum.",
            "Assumes independent simple random sampling without replacement within each supplied sampling stratum.",
            "The Wald interval is an approximation; small strata or degenerate within-stratum paired differences can make variance estimates unstable.",
            "This paired difference does not resolve uncertainty in reference labels, class harmonisation, positional support or temporal alignment.",
        ],
    }


def read_rows(path: str | Path) -> list[dict[str, str]]:
    with Path(path).open("r", newline="", encoding="utf-8-sig") as stream:
        reader = csv.DictReader(stream)
        required = {"sampling_stratum", "map_class", "reference_class"}
        if not reader.fieldnames or not required.issubset(reader.fieldnames):
            raise ValueError("CSV must contain sampling_stratum,map_class,reference_class.")
        return list(reader)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("observations_csv")
    parser.add_argument("--stratum-area-weights", required=True)
    parser.add_argument("--stratum-population-sizes", default=None)
    parser.add_argument("--baseline-map-column", default="sampling_stratum")
    parser.add_argument("--json-out", default=None)
    args = parser.parse_args()
    try:
        weights = json.loads(args.stratum_area_weights)
        if not isinstance(weights, dict):
            raise ValueError("--stratum-area-weights must be a JSON object.")
        populations = (
            json.loads(args.stratum_population_sizes)
            if args.stratum_population_sizes else None
        )
        if populations is not None and not isinstance(populations, dict):
            raise ValueError("--stratum-population-sizes must be a JSON object.")
        report = compare_maps(
            read_rows(args.observations_csv),
            weights,
            baseline_column=args.baseline_map_column,
            stratum_population_sizes=populations,
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
