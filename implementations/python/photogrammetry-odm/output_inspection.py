"""Read-only inspection of generated photogrammetry products.

Inventories project outputs, checks declared paths and inspects GeoTIFF
structure when Rasterio is installed. It does not assess positional accuracy.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

RASTER_SUFFIXES = {".tif", ".tiff"}
POINT_CLOUD_SUFFIXES = {".las", ".laz"}


def inspect_raster(path: Path) -> dict:
    try:
        import rasterio
    except ImportError:
        return {
            "path": str(path),
            "status": "not_inspected",
            "reason": "Rasterio is not installed; only file inventory is available.",
        }
    try:
        with rasterio.open(path) as dataset:
            bounds = list(dataset.bounds)
            transform = list(dataset.transform)[:6]
            sample_read = dataset.read(1, window=((0, 1), (0, 1))).tolist()
            finite_bounds = all(math.isfinite(float(value)) for value in bounds)
            return {
                "path": str(path),
                "status": "readable" if dataset.width > 0 and dataset.height > 0 and finite_bounds else "invalid",
                "driver": dataset.driver,
                "width": dataset.width,
                "height": dataset.height,
                "band_count": dataset.count,
                "dtypes": list(dataset.dtypes),
                "crs": str(dataset.crs) if dataset.crs else None,
                "transform": transform,
                "bounds": bounds,
                "pixel_size": [dataset.transform.a, dataset.transform.e],
                "nodata": dataset.nodata,
                "sample_read_succeeded": bool(sample_read),
            }
    except Exception as exc:
        return {"path": str(path), "status": "invalid", "error": str(exc)}



def inspect_point_cloud(path: Path) -> dict:
    """Stream LAS/LAZ point records and summarize structural content, not accuracy."""
    try:
        import laspy
    except ImportError:
        return {
            "path": str(path),
            "status": "not_inspected",
            "reason": "laspy is not installed; only file inventory is available.",
        }
    try:
        with laspy.open(path) as reader:
            header = reader.header
            mins = [float(value) for value in header.mins]
            maxs = [float(value) for value in header.maxs]
            finite_extent = all(math.isfinite(value) for value in mins + maxs)
            ordered_extent = all(low <= high for low, high in zip(mins, maxs))
            declared_count = int(header.point_count)
            class_counts: dict[str, int] = {}
            intensity_min = None
            intensity_max = None
            observed_count = 0
            non_finite_coordinates = 0
            sample = []
            for points in reader.chunk_iterator(100_000):
                xs, ys, zs = points.x, points.y, points.z
                classes = points.classification
                intensities = points.intensity
                for index, (x, y, z) in enumerate(zip(xs, ys, zs)):
                    observed_count += 1
                    xyz = [float(x), float(y), float(z)]
                    if not all(math.isfinite(value) for value in xyz):
                        non_finite_coordinates += 1
                    elif len(sample) < 5:
                        sample.append({"x": xyz[0], "y": xyz[1], "z": xyz[2]})
                    class_key = str(int(classes[index]))
                    class_counts[class_key] = class_counts.get(class_key, 0) + 1
                    intensity = int(intensities[index])
                    intensity_min = intensity if intensity_min is None else min(intensity_min, intensity)
                    intensity_max = intensity if intensity_max is None else max(intensity_max, intensity)
            count_matches = observed_count == declared_count
            valid = (
                declared_count > 0 and count_matches and finite_extent
                and ordered_extent and non_finite_coordinates == 0
            )
            return {
                "path": str(path),
                "status": "readable" if valid else "invalid",
                "declared_point_count": declared_count,
                "observed_point_count": observed_count,
                "point_count_matches_header": count_matches,
                "point_format_id": int(header.point_format.id),
                "version": str(header.version),
                "scales": [float(value) for value in header.scales],
                "offsets": [float(value) for value in header.offsets],
                "header_mins": mins,
                "header_maxs": maxs,
                "crs": str(header.parse_crs()) if header.parse_crs() else None,
                "classification_counts": class_counts,
                "intensity_range": [intensity_min, intensity_max],
                "non_finite_coordinate_count": non_finite_coordinates,
                "first_five_finite_points": sample,
                "inspection_method": "streamed point-record scan in chunks of 100000",
            }
    except Exception as exc:
        message = str(exc)
        backend_unavailable = path.suffix.lower() == ".laz" and any(
            token in message.lower() for token in ("laz backend", "lazrs", "backend is not available")
        )
        if backend_unavailable:
            return {
                "path": str(path),
                "status": "not_inspected",
                "reason": f"LAZ decompression backend unavailable: {message}",
            }
        return {"path": str(path), "status": "invalid", "error": message}


def inspect_outputs(project: Path, expected: list[str] | None = None) -> dict:
    project = project.expanduser().resolve()
    if not project.is_dir():
        raise ValueError(f"Project directory does not exist: {project}")
    expected = expected or []
    expected_results = []
    for relative in expected:
        candidate = (project / relative).resolve()
        if project not in candidate.parents and candidate != project:
            raise ValueError(f"Expected output path escapes project directory: {relative}")
        expected_results.append({
            "path": relative,
            "exists": candidate.is_file(),
            "size_bytes": candidate.stat().st_size if candidate.is_file() else None,
        })
    files = sorted(path for path in project.rglob("*") if path.is_file())
    inventory = [
        {
            "path": path.relative_to(project).as_posix(),
            "size_bytes": path.stat().st_size,
        }
        for path in files
    ]
    rasters = [
        inspect_raster(path) for path in files
        if path.suffix.lower() in RASTER_SUFFIXES
    ]
    point_clouds = [
        inspect_point_cloud(path) for path in files
        if path.suffix.lower() in POINT_CLOUD_SUFFIXES
    ]
    blockers = [
        f"Declared output is missing: {item['path']}"
        for item in expected_results if not item["exists"]
    ]
    blockers.extend(
        f"Raster could not be read: {item['path']}"
        for item in rasters if item["status"] == "invalid"
    )
    blockers.extend(
        f"Point cloud could not be read: {item['path']}"
        for item in point_clouds if item["status"] == "invalid"
    )
    warnings = [
        f"Raster structure not inspected: {item['path']} ({item['reason']})"
        for item in rasters if item["status"] == "not_inspected"
    ]
    warnings.extend(
        f"Point-cloud records not inspected: {item['path']} ({item['reason']})"
        for item in point_clouds if item["status"] == "not_inspected"
    )
    if not rasters:
        warnings.append("No GeoTIFF outputs were found for raster inspection.")
    status = "blocked" if blockers else ("review_required" if warnings else "inspected")
    return {
        "schema_version": "1.0",
        "project_directory": str(project),
        "status": status,
        "expected_outputs": expected_results,
        "file_inventory": inventory,
        "rasters": rasters,
        "point_clouds": point_clouds,
        "blockers": blockers,
        "warnings": warnings,
        "limitations": [
            "Structural readability is not thematic or positional accuracy.",
            "CRS presence does not establish that the CRS is correct for the project.",
            "Pixel size and bounds are descriptive; no independent reference comparison is performed.",
            "Point-cloud inspection is limited to LAS/LAZ header metadata; point content, classification quality and positional accuracy are not assessed.",
            "Mesh semantic and topology inspection is not implemented in this adapter.",
        ],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Inspect ODM outputs without modifying them.")
    parser.add_argument("project", type=Path, help="ODM project directory")
    parser.add_argument("--expect", action="append", default=[], help="Expected project-relative output path; repeat as needed")
    parser.add_argument("--json-out", type=Path, help="Optional JSON report destination")
    args = parser.parse_args(argv)
    try:
        report = inspect_outputs(args.project, args.expect)
    except (OSError, ValueError) as exc:
        parser.error(str(exc))
    rendered = json.dumps(report, indent=2, sort_keys=True)
    print(rendered)
    if args.json_out:
        args.json_out.write_text(rendered + "\n", encoding="utf-8")
    return 2 if report["status"] == "blocked" else 0


if __name__ == "__main__":
    raise SystemExit(main())
