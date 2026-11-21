#!/usr/bin/env python3
"""Prepare an ODM GCP list from the HEIG-VD drone 2019 source records.

Only the predeclared control points are exported. Checkpoint observations are
never written to the ODM GCP file.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
from pathlib import Path, PurePosixPath


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _read_gcp_coordinates(path: Path) -> dict[str, tuple[float, float, float]]:
    result = {}
    for line_no, line in enumerate(path.read_text(encoding="utf-8-sig").splitlines(), 1):
        values = line.split()
        if not values or values[0].startswith("#"):
            continue
        if len(values) != 4:
            raise ValueError(f"{path.name}:{line_no}: expected label E N H")
        label = values[0]
        if label in result:
            raise ValueError(f"Duplicate GCP label: {label}")
        try:
            coordinates = tuple(float(value) for value in values[1:])
        except ValueError as exc:
            raise ValueError(f"{path.name}:{line_no}: non-numeric coordinate") from exc
        if not all(math.isfinite(value) for value in coordinates):
            raise ValueError(f"{path.name}:{line_no}: non-finite coordinate")
        result[label] = coordinates
    if not result:
        raise ValueError("No GCP coordinates found")
    return result


def _read_observations(path: Path) -> dict[str, list[tuple[str, float, float]]]:
    result: dict[str, list[tuple[str, float, float]]] = {}
    seen = set()
    for line_no, line in enumerate(path.read_text(encoding="utf-8-sig").splitlines(), 1):
        values = line.split()
        if not values or values[0].startswith("#"):
            continue
        if len(values) != 4:
            raise ValueError(f"{path.name}:{line_no}: expected point image pixel_x pixel_y")
        label, image_label = values[:2]
        try:
            pixel_x, pixel_y = (float(value) for value in values[2:])
        except ValueError as exc:
            raise ValueError(f"{path.name}:{line_no}: non-numeric pixel coordinate") from exc
        if not all(math.isfinite(value) for value in (pixel_x, pixel_y)):
            raise ValueError(f"{path.name}:{line_no}: non-finite pixel coordinate")
        if pixel_x < 0 or pixel_y < 0:
            raise ValueError(f"{path.name}:{line_no}: negative pixel coordinate")
        key = (label, image_label)
        if key in seen:
            raise ValueError(f"Duplicate image observation for point {label} in {image_label}")
        seen.add(key)
        result.setdefault(label, []).append((image_label, pixel_x, pixel_y))
    return result


def _read_image_dimensions(readme: Path) -> tuple[int, int]:
    text = readme.read_text(encoding="utf-8")
    match = re.search(r"(\d+)\s*[×x]\s*(\d+)\s*px", text, flags=re.IGNORECASE)
    if not match:
        raise ValueError("Could not read image dimensions from the dataset README")
    return int(match.group(1)), int(match.group(2))


def prepare_gcp_list(
    dataset_root: str | Path,
    split_path: str | Path,
    acquisition_manifest_path: str | Path,
    output_path: str | Path,
    *,
    allow_proposed: bool = False,
    minimum_observations: int | None = None,
) -> dict:
    dataset_root = Path(dataset_root).expanduser().resolve()
    split_file = Path(split_path).expanduser().resolve()
    manifest_file = Path(acquisition_manifest_path).expanduser().resolve()
    output_file = Path(output_path).expanduser().resolve()

    if not dataset_root.is_dir():
        raise ValueError(f"Dataset directory does not exist: {dataset_root}")
    split = json.loads(split_file.read_text(encoding="utf-8"))
    manifest = json.loads(manifest_file.read_text(encoding="utf-8"))

    dataset = split.get("dataset", {})
    selection = split.get("selection", {})
    status = split.get("status")
    if status not in {"proposed_not_locked", "locked"}:
        raise ValueError(f"Unsupported split status: {status}")
    if status == "proposed_not_locked" and not allow_proposed:
        raise ValueError("Split is proposed_not_locked; pass --allow-proposed for a provisional GCP file.")
    if manifest.get("resolved_revision", "").lower() != dataset.get("resolved_revision", "").lower():
        raise ValueError("Acquisition manifest revision does not match the split")
    if manifest.get("selected_path") != "datasets/drone_heig_2019":
        raise ValueError("Acquisition manifest does not identify the expected dataset path")
    if dataset.get("selected_path") != manifest.get("selected_path"):
        raise ValueError("Split selected_path does not match acquisition manifest")

    for relative_text, expected_hash in dataset.get("source_files", {}).items():
        relative = PurePosixPath(relative_text)
        if relative.is_absolute() or ".." in relative.parts or not relative.parts:
            raise ValueError(f"Unsafe source-file path in split: {relative_text}")
        source_path = dataset_root.joinpath(*relative.parts)
        if not source_path.is_file() or source_path.is_symlink():
            raise ValueError(f"Required source file missing or linked: {relative_text}")
        if sha256_file(source_path) != expected_hash:
            raise ValueError(f"Source-file hash does not match split provenance: {relative_text}")

    gcp_path = dataset_root / "gcp" / "GCP_MN95.txt"
    observations_path = dataset_root / "gcp" / "gcp_obs.csv"
    readme_path = dataset_root / "README.md"
    coordinates = _read_gcp_coordinates(gcp_path)
    observations = _read_observations(observations_path)
    image_width, image_height = _read_image_dimensions(readme_path)

    if dataset_root == output_file or dataset_root in output_file.parents:
        raise ValueError("ODM GCP output must be outside the immutable source dataset directory")

    image_root = dataset_root / "images"
    image_files = [
        path for path in image_root.iterdir()
        if path.is_file() and path.suffix.lower() in {".jpg", ".jpeg", ".tif", ".tiff"}
    ]
    image_by_stem = {}
    for image in image_files:
        if image.stem in image_by_stem:
            raise ValueError(f"Ambiguous image filename stem: {image.stem}")
        image_by_stem[image.stem] = image.name

    control_ids = selection.get("control_points")
    if not isinstance(control_ids, list) or not control_ids or len(set(control_ids)) != len(control_ids):
        raise ValueError("Split must contain a non-empty unique control_points list")
    minimum = (
        selection.get("minimum_image_observations_per_point", 5)
        if minimum_observations is None else minimum_observations
    )
    if not isinstance(minimum, int) or minimum < 1:
        raise ValueError("minimum_observations must be a positive integer")

    selected_coordinates = []
    output_rows = []
    observation_counts = {}
    used_images = set()
    for label in control_ids:
        if label not in coordinates:
            raise ValueError(f"Control point {label} is missing from GCP coordinates")
        point_observations = observations.get(label, [])
        if len(point_observations) < minimum:
            raise ValueError(
                f"Control point {label} has {len(point_observations)} image observations; "
                f"minimum is {minimum}"
            )
        observation_counts[label] = len(point_observations)
        xyz = coordinates[label]
        for other_label, other_xyz in selected_coordinates:
            if all(abs(a - b) <= 1e-6 for a, b in zip(xyz, other_xyz)):
                raise ValueError(f"Control points {label} and {other_label} have duplicate coordinates")
        selected_coordinates.append((label, xyz))
        for image_label, pixel_x, pixel_y in point_observations:
            image_name = image_by_stem.get(Path(image_label).stem)
            if image_name is None:
                raise ValueError(f"Observation references missing image: {image_label}")
            if pixel_x >= image_width or pixel_y >= image_height:
                raise ValueError(
                    f"Pixel observation for {label} in {image_name} is outside "
                    f"{image_width}x{image_height}"
                )
            used_images.add(image_name)
            easting, northing, height = xyz
            output_rows.append(
                f"{easting:.3f} {northing:.3f} {height:.3f} "
                f"{pixel_x:.3f} {pixel_y:.3f} {image_name} {label}"
            )

    output_file.parent.mkdir(parents=True, exist_ok=True)
    rendered = "EPSG:2056\n" + "\n".join(output_rows) + "\n"
    output_file.write_text(rendered, encoding="utf-8")
    return {
        "schema_version": "1.0",
        "status": "prepared_provisional" if status == "proposed_not_locked" else "prepared",
        "split_status": status,
        "dataset_revision": manifest["resolved_revision"],
        "dataset_path": str(dataset_root),
        "horizontal_crs": "EPSG:2056",
        "vertical_reference": "LN02",
        "coordinate_units": "metres",
        "control_point_ids": control_ids,
        "control_point_count": len(control_ids),
        "control_observation_counts": observation_counts,
        "minimum_observations_per_control": minimum,
        "observation_record_count": len(output_rows),
        "image_count_with_control_observations": len(used_images),
        "image_dimensions_px": [image_width, image_height],
        "gcp_file": str(output_file),
        "gcp_file_size_bytes": output_file.stat().st_size,
        "gcp_file_sha256": sha256_file(output_file),
        "limitations": [
            "Only control-point observations are exported; checkpoint observations are excluded.",
            "The first-line EPSG:2056 declaration describes the horizontal CRS. Source heights are LN02 and must retain that separate vertical-reference metadata.",
            "A prepared GCP file does not establish that source image picks are correct or that the proposed split has been human-reviewed.",
            "The source OPK adjustment is not used by this converter.",
        ],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Prepare an ODM GCP list from a provenance-bound HEIG-VD control/checkpoint split."
    )
    parser.add_argument("dataset_root", type=Path)
    parser.add_argument("split", type=Path)
    parser.add_argument("acquisition_manifest", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--allow-proposed", action="store_true",
                        help="Allow preparation from a proposed, not yet human-locked split.")
    parser.add_argument("--minimum-observations", type=int)
    parser.add_argument("--json-out", type=Path)
    args = parser.parse_args(argv)
    try:
        report = prepare_gcp_list(
            args.dataset_root, args.split, args.acquisition_manifest, args.output,
            allow_proposed=args.allow_proposed,
            minimum_observations=args.minimum_observations,
        )
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        parser.error(str(exc))
    rendered = json.dumps(report, indent=2, sort_keys=True)
    print(rendered)
    if args.json_out:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(rendered + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
