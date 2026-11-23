"""Structural audit for the HEIG-VD drone 2019 photogrammetry dataset.

Reads the publisher's GCP, image-observation and Metashape OPK text exports.
It does not alter source files, transform coordinates, or establish accuracy.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path

IMAGE_SUFFIXES = {".jpg", ".jpeg", ".tif", ".tiff"}
DEFAULTS = {
    "images": 32,
    "ground_points": 31,
    "observations": 206,
    "observed_points": 30,
    "orientations": 32,
}
IMAGE_WIDTH = 5472
IMAGE_HEIGHT = 3648


def _tokens(line: str) -> list[str]:
    line = line.strip()
    if not line or line.startswith("#"):
        return []
    if line.startswith("|"):
        line = line[1:].strip()
    if "," in line:
        return [part.strip() for part in next(csv.reader([line]))]
    return line.split()


def _read_rows(path: Path, field_count: int) -> list[list[str]]:
    if not path.is_file():
        raise ValueError(f"Required dataset file is missing: {path}")
    rows = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8-sig").splitlines(), 1):
        values = _tokens(line)
        if not values:
            continue
        if len(values) != field_count:
            raise ValueError(
                f"{path.name}:{line_number}: expected {field_count} fields, got {len(values)}"
            )
        rows.append(values)
    if not rows:
        raise ValueError(f"No data records found in {path}")
    return rows


def _finite_numbers(values: list[str], path: Path, row_number: int) -> list[float]:
    try:
        numbers = [float(value) for value in values]
    except ValueError as exc:
        raise ValueError(f"{path.name}: data row {row_number} contains a non-numeric field") from exc
    if not all(math.isfinite(value) for value in numbers):
        raise ValueError(f"{path.name}: data row {row_number} contains a non-finite value")
    return numbers


def _determinant3(m: list[list[float]]) -> float:
    return (
        m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1])
        - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0])
        + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0])
    )


def _rotation_diagnostics(values: list[float]) -> tuple[float, float]:
    matrix = [values[i:i + 3] for i in range(0, 9, 3)]
    max_orthogonality_error = 0.0
    for i in range(3):
        for j in range(3):
            dot = sum(matrix[k][i] * matrix[k][j] for k in range(3))
            target = 1.0 if i == j else 0.0
            max_orthogonality_error = max(max_orthogonality_error, abs(dot - target))
    return max_orthogonality_error, _determinant3(matrix)


def audit_dataset(
    root: str | Path,
    expected_images: int = DEFAULTS["images"],
    expected_ground_points: int = DEFAULTS["ground_points"],
    expected_observations: int = DEFAULTS["observations"],
    expected_observed_points: int = DEFAULTS["observed_points"],
    expected_orientations: int = DEFAULTS["orientations"],
) -> dict:
    root = Path(root).expanduser().resolve()
    if not root.is_dir():
        raise ValueError(f"Dataset directory does not exist: {root}")

    image_dir = root / "images"
    if not image_dir.is_dir():
        raise ValueError(f"Expected image directory: {image_dir}")
    image_files = sorted(
        path for path in image_dir.iterdir()
        if path.is_file() and path.suffix.lower() in IMAGE_SUFFIXES
    )
    image_stems = {path.stem for path in image_files}

    gcp_path = root / "gcp" / "GCP_MN95.txt"
    obs_path = root / "gcp" / "gcp_obs.csv"
    opk_path = root / "opk.txt"

    gcp_rows = _read_rows(gcp_path, 4)
    gcps = []
    for row_number, row in enumerate(gcp_rows, 1):
        values = _finite_numbers(row[1:], gcp_path, row_number)
        gcps.append({"label": row[0], "coordinates": values})
    gcp_labels = [item["label"] for item in gcps]
    if len(set(gcp_labels)) != len(gcp_labels):
        raise ValueError("GCP coordinate file contains duplicate point labels")

    duplicate_coordinate_groups = []
    unused = set(range(len(gcps)))
    while unused:
        first = min(unused)
        group = [
            index for index in sorted(unused)
            if all(abs(a - b) <= 1e-6 for a, b in zip(
                gcps[first]["coordinates"], gcps[index]["coordinates"]
            ))
        ]
        if len(group) > 1:
            duplicate_coordinate_groups.append([gcps[index]["label"] for index in group])
        unused.difference_update(group)

    obs_rows = _read_rows(obs_path, 4)
    observations = []
    for row_number, row in enumerate(obs_rows, 1):
        pixel = _finite_numbers(row[2:], obs_path, row_number)
        observations.append({
            "point_label": row[0],
            "image_label": row[1],
            "x": pixel[0],
            "y": pixel[1],
        })
    observed_labels = sorted({item["point_label"] for item in observations})
    observed_images = sorted({item["image_label"] for item in observations})
    unknown_gcp_labels = sorted(set(observed_labels) - set(gcp_labels))
    missing_image_labels = sorted(set(observed_images) - image_stems)
    images_without_ground_point_observations = sorted(image_stems - set(observed_images))
    out_of_bounds = [
        {"point_label": item["point_label"], "image_label": item["image_label"],
         "x": item["x"], "y": item["y"]}
        for item in observations
        if not (0 <= item["x"] < IMAGE_WIDTH and 0 <= item["y"] < IMAGE_HEIGHT)
    ]

    opk_rows = _read_rows(opk_path, 16)
    opk_ids = []
    rotation_errors = []
    rotation_determinants = []
    for row_number, row in enumerate(opk_rows, 1):
        numbers = _finite_numbers(row[1:], opk_path, row_number)
        opk_ids.append(Path(row[0]).stem)
        orth_error, determinant = _rotation_diagnostics(numbers[6:15])
        rotation_errors.append(orth_error)
        rotation_determinants.append(determinant)
    if len(set(opk_ids)) != len(opk_ids):
        raise ValueError("OPK file contains duplicate photo IDs")

    opk_unmatched_images = sorted(
        photo_id for photo_id in opk_ids
        if not any(stem.endswith(photo_id) for stem in image_stems)
    )
    observed_opk_unmatched = sorted(
        image_label for image_label in observed_images
        if not any(image_label.endswith(photo_id) for photo_id in opk_ids)
    )

    counts = {
        "images": len(image_files),
        "ground_points": len(gcps),
        "observations": len(observations),
        "observed_points": len(observed_labels),
        "orientations": len(opk_ids),
    }
    expected = {
        "images": expected_images,
        "ground_points": expected_ground_points,
        "observations": expected_observations,
        "observed_points": expected_observed_points,
        "orientations": expected_orientations,
    }
    count_matches = {key: counts[key] == expected[key] for key in counts}

    return {
        "dataset_root": str(root),
        "counts": counts,
        "expected_counts": expected,
        "count_matches": count_matches,
        "ground_points_without_image_observations": sorted(set(gcp_labels) - set(observed_labels)),
        "duplicate_coordinate_groups_within_1e-6_m": duplicate_coordinate_groups,
        "observation_labels_without_gcp": unknown_gcp_labels,
        "observation_images_missing_from_images_directory": missing_image_labels,
        "images_without_ground_point_observations": images_without_ground_point_observations,
        "observation_pixels_outside_readme_dimensions": out_of_bounds,
        "opk_photo_ids_without_matching_image": opk_unmatched_images,
        "observation_images_without_matching_opk": observed_opk_unmatched,
        "opk_rotation_max_orthogonality_error": max(rotation_errors),
        "opk_rotation_determinant_range": [min(rotation_determinants), max(rotation_determinants)],
        "interpretation_notes": [
            "Image dimensions 5472x3648 are taken from the dataset README; actual image bytes must be checked separately.",
            "Pixel bounds are checked against the README dimensions, not dimensions decoded from each image.",
            "The publisher README documents point 100 as having no image measurement and sharing coordinates with point 206; that duplicate/unobserved record is an expected source exception, not a second independent point.",
            "Images without ground-point observations are reported as coverage information; an image does not need to contain a surveyed target to contribute tie points to the reconstruction.",
            "The supplied OPK orientations came from a Metashape adjustment using the ground points as control; they are not independent validation.",
            "The audit checks structure and consistency only. It does not transform coordinates, validate survey accuracy, or determine a control/checkpoint split.",
        ],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Audit GCP, image-observation and Metashape OPK exports for the HEIG-VD dataset."
    )
    parser.add_argument("dataset_root", type=Path)
    parser.add_argument("--json-out", type=Path)
    args = parser.parse_args(argv)
    try:
        report = audit_dataset(args.dataset_root)
    except (OSError, ValueError) as exc:
        parser.error(str(exc))
    rendered = json.dumps(report, indent=2, sort_keys=True)
    print(rendered)
    if args.json_out:
        args.json_out.write_text(rendered + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
