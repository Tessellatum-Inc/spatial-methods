"""Sensitivity analysis for alternative Fiji–WorldCover class harmonisations.

Reads the sampled point-level WorldCover classes and Fiji reference labels,
then recomputes area-adjusted overall accuracy and paired map differences
under three explicitly declared class legends. Assumes stratified SRSWOR
within the original Fiji sampling strata.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path

from paired_map_comparison import compare_maps
from stratified_accuracy import estimate_stratified_accuracy


def strict_crosswalk(label: str) -> str:
    return label


def wetland_to_grassland(label: str) -> str:
    return "grassland" if label == "herbaceous_wetland" else label


def broad_vegetation_groups(label: str) -> str:
    if label in {"tree", "mangrove"}:
        return "woody_cover"
    if label in {"grassland", "shrubland", "herbaceous_wetland"}:
        return "open_vegetation"
    return label


SCENARIOS = (
    {
        "scenario_id": "strict_8_class",
        "title": "Strict eight-class comparison",
        "description": (
            "Retain the supplied working labels. WorldCover herbaceous wetland "
            "has no matching Fiji reference class and is counted as disagreement."
        ),
        "map_transform": strict_crosswalk,
        "reference_transform": strict_crosswalk,
        "baseline_transform": strict_crosswalk,
        "crosswalk": {
            "WorldCover herbaceous_wetland": "kept distinct; no Fiji reference counterpart"
        },
    },
    {
        "scenario_id": "wetland_as_grassland",
        "title": "Herbaceous wetland grouped with grassland",
        "description": (
            "Recode WorldCover herbaceous wetland as grassland before comparison. "
            "This is a sensitivity assumption, not an authoritative equivalence."
        ),
        "map_transform": wetland_to_grassland,
        "reference_transform": strict_crosswalk,
        "baseline_transform": strict_crosswalk,
        "crosswalk": {"WorldCover herbaceous_wetland": "grassland"},
    },
    {
        "scenario_id": "broad_vegetation_groups",
        "title": "Broad six-class vegetation grouping",
        "description": (
            "Merge tree and mangrove into woody_cover; merge grassland, shrubland "
            "and herbaceous wetland into open_vegetation in both maps and reference. "
            "This evaluates broader thematic agreement, not the original detailed legend."
        ),
        "map_transform": broad_vegetation_groups,
        "reference_transform": broad_vegetation_groups,
        "baseline_transform": broad_vegetation_groups,
        "crosswalk": {
            "tree, mangrove": "woody_cover",
            "grassland, shrubland, herbaceous_wetland": "open_vegetation",
        },
    },
)


def load_observations(path: str | Path) -> list[dict[str, str]]:
    source = Path(path)
    with source.open("r", newline="", encoding="utf-8-sig") as stream:
        reader = csv.DictReader(stream)
        required = {"sampling_stratum", "map_class", "reference_class"}
        if not reader.fieldnames or not required.issubset(reader.fieldnames):
            raise ValueError(
                "CSV must contain sampling_stratum,map_class,reference_class."
            )
        rows = list(reader)
    if not rows:
        raise ValueError("Input CSV contains no observations.")
    for i, row in enumerate(rows, start=1):
        if any(not str(row.get(k, "")).strip() for k in required):
            raise ValueError(f"CSV row {i} has a blank required class label.")
    return rows


def run_sensitivity(
    observations: list[dict[str, str]],
    area_weights: dict[str, float],
    population_sizes: dict[str, int] | None = None,
) -> dict:
    results = []
    for scenario in SCENARIOS:
        transformed = []
        for row in observations:
            transformed.append({
                "sampling_stratum": row["sampling_stratum"].strip(),
                "map_class": scenario["map_transform"](row["map_class"].strip()),
                "reference_class": scenario["reference_transform"](row["reference_class"].strip()),
                "baseline_map_class": scenario["baseline_transform"](row["sampling_stratum"].strip()),
            })
        accuracy = estimate_stratified_accuracy(
            transformed, area_weights, stratum_population_sizes=population_sizes
        )
        paired = compare_maps(
            transformed,
            area_weights,
            baseline_column="baseline_map_class",
            stratum_population_sizes=population_sizes,
        )
        oa = accuracy["overall_accuracy"]
        diff = paired["evaluated_minus_baseline_accuracy_difference"]
        results.append({
            "scenario_id": scenario["scenario_id"],
            "title": scenario["title"],
            "description": scenario["description"],
            "crosswalk": scenario["crosswalk"],
            "sample_size": len(transformed),
            "worldcover_overall_accuracy": oa,
            "original_fiji_map_overall_accuracy": paired["baseline_map_overall_accuracy"],
            "worldcover_minus_original_accuracy_difference": diff,
            "paired_stratum_diagnostics": paired["stratum_diagnostics"],
        })

    return {
        "analysis": "Fiji–WorldCover class-crosswalk sensitivity analysis",
        "design": "stratified simple random sampling without replacement within original Fiji sampling strata",
        "sample_size": len(observations),
        "sampling_stratum_area_proportions": area_weights,
        "stratum_population_sizes": population_sizes,
        "scenarios": results,
        "interpretation_limits": [
            "Scenarios are analyst-defined harmonisation choices, not authoritative semantic equivalences.",
            "The broad six-class scenario changes the target legend and should not be compared as if it measured detailed eight-class accuracy.",
            "All estimates apply only to the eligible Fiji sampling frame represented by the supplied stratum weights, excluding training Tikinas.",
            "The reference labels are supplied visual interpretations, not independently field-verified labels.",
            "The analysis assumes independent simple random sampling without replacement within each original sampling stratum.",
            "Wald intervals are approximate; class-specific ratios and sparse classes may be unstable.",
            "No positional tolerance, mixed-pixel rule, reference-label uncertainty or uncertainty in supplied area weights is modelled.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("observations_csv")
    parser.add_argument("--stratum-area-weights", required=True)
    parser.add_argument("--stratum-population-sizes", default=None)
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
        input_path = Path(args.observations_csv)
        rows = load_observations(input_path)
        report = run_sensitivity(rows, weights, populations)
        report["input"] = {
            "file_name": input_path.name,
            "sha256": hashlib.sha256(input_path.read_bytes()).hexdigest(),
        }
        rendered = json.dumps(report, indent=2, sort_keys=True)
        if args.json_out:
            Path(args.json_out).write_text(rendered + "\n", encoding="utf-8")
        print(rendered)
        return 0
    except (OSError, ValueError, TypeError, json.JSONDecodeError) as exc:
        parser.error(str(exc))
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
