"""Reproduce the Fiji 2021 LULC stratified-sample case study.

Downloads one pinned GeoJSON snapshot (or accepts a local copy), verifies the
Git blob identity, and applies the bounded mapped-class-stratified estimator.
Only Python's standard library and the sibling area_adjusted_accuracy module
are required.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import urllib.request
from collections import Counter
from pathlib import Path

from area_adjusted_accuracy import estimate_stratified_accuracy

REPOSITORY = "livelihoods-and-landscapes/ccai-data"
REVISION = "050021d57c99abaaa6f2c511e4f718a402c7ca2a"
RELATIVE_PATH = "fiji-lulc-test-data/fiji-lulc-2021-test-data.geojson"
RAW_URL = (
    "https://raw.githubusercontent.com/"
    f"{REPOSITORY}/{REVISION}/{RELATIVE_PATH}"
)
EXPECTED_GIT_BLOB_SHA1 = "d07afda85d40b2eb6b13d2c17089e5b061a577c9"
CLASS_NAMES = {
    1: "water",
    2: "mangrove",
    3: "bare_soil_rock",
    4: "urban",
    5: "agriculture",
    6: "grassland",
    7: "shrubland",
    8: "tree",
}
STRATUM_POPULATION_SIZES = {
    "water": 1_779_768,
    "mangrove": 3_549_325,
    "bare_soil_rock": 541_204,
    "urban": 687_659,
    "agriculture": 14_279_258,
    "grassland": 15_115_599,
    "shrubland": 4_972_515,
    "tree": 116_131_948,
}
DOCUMENTED_SAMPLE_ALLOCATION = {
    "water": 100,
    "mangrove": 100,
    "bare_soil_rock": 100,
    "urban": 100,
    "agriculture": 100,
    "grassland": 100,
    "shrubland": 100,
    "tree": 133,
}
OBSERVED_SAMPLE_ALLOCATION = {
    "water": 100,
    "mangrove": 100,
    "bare_soil_rock": 100,
    "urban": 100,
    "agriculture": 100,
    "grassland": 100,
    "shrubland": 100,
    "tree": 134,
}


def git_blob_sha1(data: bytes) -> str:
    header = b"blob " + str(len(data)).encode("ascii") + b"\0"
    return hashlib.sha1(header + data).hexdigest()


def load_dataset(path: str | None) -> tuple[bytes, str]:
    if path:
        return Path(path).read_bytes(), "local_file"
    request = urllib.request.Request(
        RAW_URL, headers={"User-Agent": "SpatialMethods-reproducible-case-study"}
    )
    with urllib.request.urlopen(request, timeout=60) as response:
        return response.read(), "pinned_GitHub_raw_download"


def analyse(data: bytes, acquisition: str) -> dict:
    blob_sha = git_blob_sha1(data)
    if blob_sha != EXPECTED_GIT_BLOB_SHA1:
        raise ValueError(
            "Dataset Git blob SHA-1 mismatch: "
            f"expected {EXPECTED_GIT_BLOB_SHA1}, received {blob_sha}"
        )
    collection = json.loads(data.decode("utf-8"))
    if collection.get("type") != "FeatureCollection":
        raise ValueError("Expected a GeoJSON FeatureCollection.")

    observations = []
    counts = {name: Counter() for name in CLASS_NAMES.values()}
    coordinates = set()
    invalid_geometry_count = 0

    for index, feature in enumerate(collection.get("features", []), start=1):
        properties = feature.get("properties") or {}
        try:
            stratum_code = int(properties["strata"])
            reference_code = int(properties["ref_class"])
            map_class = CLASS_NAMES[stratum_code]
            reference_class = CLASS_NAMES[reference_code]
        except (KeyError, TypeError, ValueError) as exc:
            raise ValueError(f"Feature {index}: invalid strata/ref_class code.") from exc

        geometry = feature.get("geometry") or {}
        coords = geometry.get("coordinates")
        if geometry.get("type") != "Point" or not isinstance(coords, list) or len(coords) < 2:
            invalid_geometry_count += 1
        else:
            coordinates.add((float(coords[0]), float(coords[1])))

        observations.append(
            {"map_class": map_class, "reference_class": reference_class}
        )
        counts[map_class][reference_class] += 1

    if invalid_geometry_count:
        raise ValueError(f"{invalid_geometry_count} features do not contain valid Point geometry.")

    observed_allocation = {
        name: sum(counts[name].values()) for name in CLASS_NAMES.values()
    }
    if len(observations) != 834 or observed_allocation != OBSERVED_SAMPLE_ALLOCATION:
        raise ValueError(
            "Pinned dataset structure differs from the audited snapshot: "
            f"n={len(observations)}, allocation={observed_allocation}"
        )

    weights_total = sum(STRATUM_POPULATION_SIZES.values())
    weights = {
        name: population / weights_total
        for name, population in STRATUM_POPULATION_SIZES.items()
    }
    estimate = estimate_stratified_accuracy(
        observations,
        weights,
        stratum_population_sizes=STRATUM_POPULATION_SIZES,
    )

    raw_matrix = {
        map_class: {
            ref_class: counts[map_class][ref_class]
            for ref_class in CLASS_NAMES.values()
        }
        for map_class in CLASS_NAMES.values()
    }
    total_correct = sum(
        counts[name][name] for name in CLASS_NAMES.values()
    )
    raw_column_totals = {
        ref: sum(counts[mapped][ref] for mapped in CLASS_NAMES.values())
        for ref in CLASS_NAMES.values()
    }
    raw_producers = {
        ref: (
            counts[ref][ref] / raw_column_totals[ref]
            if raw_column_totals[ref] else None
        )
        for ref in CLASS_NAMES.values()
    }

    return {
        "dataset": {
            "title": "Fiji Land Use Land Cover Test Dataset",
            "publisher": "Pacific Data Hub / Pacific Community",
            "author": "John Duncan",
            "license": "Open Data Commons Open Database License (ODbL)",
            "geography": "Fiji; eligible Tikinas excluding those used for training data",
            "reference_year": 2021,
            "sampling_design": "Stratified random sampling within eight 2021 mapped-class strata",
            "response_design": (
                "Manual interpretation using 2021 Sentinel-2 and Planet NICFI "
                "annual median RGB composites and high-resolution Google Satellite Basemaps"
            ),
            "source_repository": f"https://github.com/{REPOSITORY}",
            "source_revision": REVISION,
            "source_path": RELATIVE_PATH,
            "raw_url": RAW_URL,
            "git_blob_sha1": blob_sha,
            "sha256": hashlib.sha256(data).hexdigest(),
            "acquisition": acquisition,
            "feature_count": len(observations),
            "unique_point_coordinates": len(coordinates),
            "invalid_geometry_count": invalid_geometry_count,
            "sample_allocation_documented": DOCUMENTED_SAMPLE_ALLOCATION,
            "sample_allocation_observed": observed_allocation,
            "allocation_documentation_discrepancy": (
                "The dataset documentation states 834 total samples and 133 tree-stratum "
                "samples, but 100 samples in each of seven minority strata plus 133 tree "
                "samples totals 833. The pinned GeoJSON contains 834 features: 100 in each "
                "minority stratum and 134 in the tree stratum."
            ),
            "target_population_boundary": (
                "The published stratum pixel counts and sample frame exclude Tikinas "
                "used to generate training samples. Do not describe estimates as "
                "unqualified accuracy for every pixel in all of Fiji."
            ),
        },
        "raw_count_summary": {
            "correct_count": total_correct,
            "overall_accuracy": total_correct / len(observations),
            "confusion_matrix_rows_mapped_classes_columns_reference_classes": raw_matrix,
            "producer_accuracy_by_reference_class_unweighted_counts": raw_producers,
        },
        "design_adjusted_estimates": estimate,
        "interpretation_limits": [
            "The mapped class is taken from the sample's strata field; this assesses the 2021 map that defined those strata.",
            "The implementation does not support comparing a different map whose classes differ from the sample strata.",
            "The reference labels are supplied as quality-checked visual interpretations; this script does not independently verify them.",
            "The estimates apply to the documented eligible sampling domain, not automatically to excluded training Tikinas.",
            "The source documentation's 133-versus-134 tree sample allocation discrepancy is retained rather than silently corrected.",
            "The small finite-population corrections reflect the supplied stratum pixel counts and are negligible at this sample fraction.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--geojson", help="Optional local copy of the exact pinned GeoJSON")
    parser.add_argument("--json-out", help="Optional path for the full JSON report")
    args = parser.parse_args()
    try:
        data, acquisition = load_dataset(args.geojson)
        report = analyse(data, acquisition)
    except (OSError, ValueError, KeyError, urllib.error.URLError) as exc:
        parser.error(str(exc))
    rendered = json.dumps(report, indent=2, sort_keys=True)
    if args.json_out:
        Path(args.json_out).write_text(rendered + "\n", encoding="utf-8")
    print(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
