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
            observed_mins = [math.inf, math.inf, math.inf]
            observed_maxs = [-math.inf, -math.inf, -math.inf]
            points_outside_header_bounds = 0
            scales = [float(value) for value in header.scales]
            tolerances = [max(abs(value) * 1.5, 1e-9) for value in scales]
            for points in reader.chunk_iterator(100_000):
                xs, ys, zs = points.x, points.y, points.z
                classes = points.classification
                intensities = points.intensity
                for index, (x, y, z) in enumerate(zip(xs, ys, zs)):
                    observed_count += 1
                    xyz = [float(x), float(y), float(z)]
                    if not all(math.isfinite(value) for value in xyz):
                        non_finite_coordinates += 1
                    else:
                        if len(sample) < 5:
                            sample.append({"x": xyz[0], "y": xyz[1], "z": xyz[2]})
                        outside = False
                        for axis, value in enumerate(xyz):
                            observed_mins[axis] = min(observed_mins[axis], value)
                            observed_maxs[axis] = max(observed_maxs[axis], value)
                            if value < mins[axis] - tolerances[axis] or value > maxs[axis] + tolerances[axis]:
                                outside = True
                        if outside:
                            points_outside_header_bounds += 1
                    class_key = str(int(classes[index]))
                    class_counts[class_key] = class_counts.get(class_key, 0) + 1
                    intensity = int(intensities[index])
                    intensity_min = intensity if intensity_min is None else min(intensity_min, intensity)
                    intensity_max = intensity if intensity_max is None else max(intensity_max, intensity)
            count_matches = observed_count == declared_count
            valid = (
                declared_count > 0 and count_matches and finite_extent
                and ordered_extent and non_finite_coordinates == 0
                and points_outside_header_bounds == 0
            )
            return {
                "path": str(path),
                "status": "readable" if valid else "invalid",
                "declared_point_count": declared_count,
                "observed_point_count": observed_count,
                "point_count_matches_header": count_matches,
                "point_format_id": int(header.point_format.id),
                "version": str(header.version),
                "scales": scales,
                "offsets": [float(value) for value in header.offsets],
                "header_mins": mins,
                "header_maxs": maxs,
                "observed_mins": observed_mins if observed_count else None,
                "observed_maxs": observed_maxs if observed_count else None,
                "points_outside_header_bounds": points_outside_header_bounds,
                "header_bounds_tolerance": tolerances,
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


def inspect_obj_mesh(path: Path) -> dict:
    """Validate OBJ record syntax and references, not mesh topology or accuracy."""
    vertices: list[list[float]] = []
    texture_coordinates = 0
    normals = 0
    faces = 0
    invalid_lines: list[int] = []
    repeated_vertex_faces = 0
    zero_area_faces = 0
    referenced_vertices: set[int] = set()
    mins = [math.inf, math.inf, math.inf]
    maxs = [-math.inf, -math.inf, -math.inf]

    def resolve_index(token: str, count: int) -> int | None:
        try:
            value = int(token)
        except ValueError:
            return None
        if value == 0:
            return None
        resolved = value - 1 if value > 0 else count + value
        return resolved if 0 <= resolved < count else None

    def polygon_area_vector(points: list[list[float]]) -> list[float]:
        # Newell's method works for planar polygons with three or more vertices.
        normal = [0.0, 0.0, 0.0]
        for current, following in zip(points, points[1:] + points[:1]):
            normal[0] += (current[1] - following[1]) * (current[2] + following[2])
            normal[1] += (current[2] - following[2]) * (current[0] + following[0])
            normal[2] += (current[0] - following[0]) * (current[1] + following[1])
        return normal

    try:
        with path.open("r", encoding="utf-8", errors="strict") as stream:
            for line_no, raw in enumerate(stream, 1):
                fields = raw.partition("#")[0].split()
                if not fields:
                    continue
                kind, values = fields[0], fields[1:]
                if kind == "v":
                    if len(values) < 3:
                        invalid_lines.append(line_no)
                        continue
                    try:
                        xyz = [float(value) for value in values[:3]]
                    except ValueError:
                        invalid_lines.append(line_no)
                        continue
                    if not all(math.isfinite(value) for value in xyz):
                        invalid_lines.append(line_no)
                        continue
                    vertices.append(xyz)
                    for axis, value in enumerate(xyz):
                        mins[axis] = min(mins[axis], value)
                        maxs[axis] = max(maxs[axis], value)
                elif kind == "vt":
                    if not values:
                        invalid_lines.append(line_no)
                        continue
                    try:
                        coords = [float(value) for value in values]
                    except ValueError:
                        invalid_lines.append(line_no)
                        continue
                    if not all(math.isfinite(value) for value in coords):
                        invalid_lines.append(line_no)
                        continue
                    texture_coordinates += 1
                elif kind == "vn":
                    if len(values) < 3:
                        invalid_lines.append(line_no)
                        continue
                    try:
                        vector = [float(value) for value in values[:3]]
                    except ValueError:
                        invalid_lines.append(line_no)
                        continue
                    if not all(math.isfinite(value) for value in vector):
                        invalid_lines.append(line_no)
                        continue
                    normals += 1
                elif kind == "f":
                    faces += 1
                    if len(values) < 3:
                        invalid_lines.append(line_no)
                        continue
                    face_refs = []
                    face_valid = True
                    for token in values:
                        parts = token.split("/")
                        if len(parts) > 3 or not parts[0]:
                            face_valid = False
                            continue
                        vertex_index = resolve_index(parts[0], len(vertices))
                        if vertex_index is None:
                            face_valid = False
                        else:
                            face_refs.append(vertex_index)
                        if len(parts) >= 2 and parts[1]:
                            if resolve_index(parts[1], texture_coordinates) is None:
                                face_valid = False
                        if len(parts) == 3 and parts[2]:
                            if resolve_index(parts[2], normals) is None:
                                face_valid = False
                    if not face_valid or len(face_refs) != len(values):
                        invalid_lines.append(line_no)
                        continue
                    if len(set(face_refs)) < 3:
                        repeated_vertex_faces += 1
                    else:
                        referenced_vertices.update(face_refs)
                        face_points = [vertices[index] for index in face_refs]
                        area_vector = polygon_area_vector(face_points)
                        face_extent = max(
                            max(point[axis] for point in face_points)
                            - min(point[axis] for point in face_points)
                            for axis in range(3)
                        )
                        tolerance = face_extent * face_extent * 1e-12
                        if math.sqrt(sum(value * value for value in area_vector)) <= tolerance:
                            zero_area_faces += 1

        ok = (
            len(vertices) > 0 and faces > 0 and not invalid_lines
            and repeated_vertex_faces == 0 and zero_area_faces == 0
        )
        return {
            "path": str(path),
            "status": "readable" if ok else "invalid",
            "format": "Wavefront OBJ",
            "vertex_count": len(vertices),
            "texture_coordinate_count": texture_coordinates,
            "normal_count": normals,
            "face_count": faces,
            "referenced_vertex_count": len(referenced_vertices),
            "unreferenced_vertex_count": max(0, len(vertices) - len(referenced_vertices)),
            "repeated_vertex_face_count": repeated_vertex_faces,
            "zero_area_face_count": zero_area_faces,
            # Retain the earlier summary field for downstream consumers.
            "degenerate_face_count": repeated_vertex_faces + zero_area_faces,
            "invalid_line_numbers": invalid_lines[:100],
            "invalid_line_count": len(invalid_lines),
            "bounds": [mins, maxs] if vertices else None,
        }
    except Exception as exc:
        return {"path": str(path), "status": "invalid", "error": str(exc)}


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
    meshes = [inspect_obj_mesh(path) for path in files if path.suffix.lower() == ".obj"]
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
    blockers.extend(["OBJ mesh structure is invalid: " + item["path"] for item in meshes if item["status"] == "invalid"])
    expected_rasters = [
        value for value in expected
        if Path(value).suffix.lower() in RASTER_SUFFIXES
    ]
    if not rasters and (not expected or expected_rasters):
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
        "meshes": meshes,
        "blockers": blockers,
        "warnings": warnings,
        "limitations": [
            "Structural readability is not thematic or positional accuracy.",
            "CRS presence does not establish that the CRS is correct for the project.",
            "Pixel size and bounds are descriptive; no independent reference comparison is performed.",
            "Point-cloud records are scanned for structural summaries; classification correctness, density suitability and positional accuracy are not assessed.",
            "OBJ inspection checks finite vertex/texture/normal records, face index references and zero-area/repeated-index faces; manifoldness, self-intersections, texture-file availability, normal quality and geometric accuracy are not assessed.",
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
