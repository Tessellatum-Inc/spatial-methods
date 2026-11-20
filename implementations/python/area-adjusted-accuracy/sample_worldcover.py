"""Sample ESA WorldCover classes at the pinned Fiji reference points.

Requires rasterio. The raster must be a local GeoTIFF/COG or VRT covering all
834 points. The output preserves the original Fiji sampling strata and
reference labels, while adding the evaluated map class.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path

FIJI_REVISION = "050021d57c99abaaa6f2c511e4f718a402c7ca2a"
EXPECTED_GIT_BLOB_SHA1 = "d07afda85d40b2eb6b13d2c17089e5b061a577c9"
EXPECTED_SAMPLE_COUNT = 834
STRATUM_NAMES = {
    1: "water",
    2: "mangrove",
    3: "bare_soil_rock",
    4: "urban",
    5: "agriculture",
    6: "grassland",
    7: "shrubland",
    8: "tree",
}
REFERENCE_NAMES = {
    1: "water",
    2: "mangrove",
    3: "bare_soil_rock",
    4: "urban",
    5: "agriculture",
    6: "grassland",
    7: "shrubland",
    8: "tree",
}
WORLDCOVER_NAMES = {
    10: "tree",
    20: "shrubland",
    30: "grassland",
    40: "agriculture",
    50: "urban",
    60: "bare_soil_rock",
    70: "snow_ice",
    80: "water",
    90: "herbaceous_wetland",
    95: "mangrove",
    100: "moss_lichen",
}


def git_blob_sha1(data: bytes) -> str:
    header = b"blob " + str(len(data)).encode("ascii") + b"\0"
    return hashlib.sha1(header + data).hexdigest()


def read_pinned_points(path: str) -> tuple[list[dict], str]:
    data = Path(path).read_bytes()
    actual = git_blob_sha1(data)
    if actual != EXPECTED_GIT_BLOB_SHA1:
        raise ValueError(
            "Fiji sample GeoJSON Git blob SHA-1 mismatch: "
            f"expected {EXPECTED_GIT_BLOB_SHA1}, received {actual}"
        )
    collection = json.loads(data.decode("utf-8"))
    if collection.get("type") != "FeatureCollection":
        raise ValueError("Expected a GeoJSON FeatureCollection.")
    features = collection.get("features", [])
    if len(features) != EXPECTED_SAMPLE_COUNT:
        raise ValueError(f"Expected {EXPECTED_SAMPLE_COUNT} points; found {len(features)}.")

    points = []
    for index, feature in enumerate(features, start=1):
        props = feature.get("properties") or {}
        geometry = feature.get("geometry") or {}
        if geometry.get("type") != "Point":
            raise ValueError(f"Feature {index} is not a Point.")
        coords = geometry.get("coordinates")
        if not isinstance(coords, list) or len(coords) < 2:
            raise ValueError(f"Feature {index} has invalid coordinates.")
        try:
            longitude, latitude = float(coords[0]), float(coords[1])
            stratum = STRATUM_NAMES[int(props["strata"])]
            reference = REFERENCE_NAMES[int(props["ref_class"])]
        except (KeyError, TypeError, ValueError) as exc:
            raise ValueError(f"Feature {index} has an unknown stratum/reference code.") from exc
        points.append({
            "sample_id": f"FJI2021-{index:06d}",
            "sampling_stratum": stratum,
            "reference_class": reference,
            "longitude": longitude,
            "latitude": latitude,
        })
    return points, actual


def sample_worldcover(
    points: list[dict],
    raster_path: str,
    class_names: dict[int, str],
) -> tuple[list[dict], dict]:
    try:
        import rasterio
        from rasterio.warp import transform
    except ImportError as exc:
        raise RuntimeError(
            "rasterio is required. Install with: pip install -r requirements-worldcover.txt"
        ) from exc

    if not class_names or any(not str(label).strip() for label in class_names.values()):
        raise ValueError("WorldCover class mapping must contain non-empty labels.")

    output = []
    with rasterio.open(raster_path) as src:
        if src.crs is None:
            raise ValueError("WorldCover raster has no CRS.")
        xs, ys = transform(
            "EPSG:4326",
            src.crs,
            [point["longitude"] for point in points],
            [point["latitude"] for point in points],
        )
        coordinates = list(zip(xs, ys))
        sampled = src.sample(coordinates, indexes=1, masked=True)

        for point, value in zip(points, sampled):
            cell = value[0]
            mask = getattr(value, "mask", False)
            is_masked = bool(mask[0]) if hasattr(mask, "__getitem__") else bool(mask)
            if is_masked or str(cell) == "--":
                raise ValueError(
                    f"WorldCover raster has nodata/out-of-coverage at {point['sample_id']}."
                )
            numeric = float(cell)
            if not numeric.is_integer():
                raise ValueError(
                    f"Non-integer WorldCover class {numeric} at {point['sample_id']}."
                )
            code = int(numeric)
            if code not in class_names:
                raise ValueError(
                    f"Unknown WorldCover code {code} at {point['sample_id']}; "
                    "supply a complete --class-names JSON mapping."
                )
            output.append({
                "sample_id": point["sample_id"],
                "sampling_stratum": point["sampling_stratum"],
                "map_class": class_names[code],
                "reference_class": point["reference_class"],
                "worldcover_code": code,
                "longitude": point["longitude"],
                "latitude": point["latitude"],
            })

        metadata = {
            "product": "ESA WorldCover 2021 v200",
            "raster_path_as_supplied": str(Path(raster_path)),
            "raster_driver": src.driver,
            "raster_crs": str(src.crs),
            "raster_width": src.width,
            "raster_height": src.height,
            "raster_band": 1,
            "raster_nodata": src.nodata,
            "raster_bounds": list(src.bounds),
            "raster_resolution": list(src.res),
            "raster_dtype": src.dtypes[0],
            "sampling_method": "single-pixel containing each point using rasterio.sample",
            "point_coordinate_crs": "EPSG:4326",
            "point_count": len(output),
            "fiji_source_revision": FIJI_REVISION,
            "fiji_geojson_git_blob_sha1": EXPECTED_GIT_BLOB_SHA1,
            "worldcover_class_name_mapping": {
                str(code): label for code, label in sorted(class_names.items())
            },
        }
    return output, metadata


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--geojson", required=True, help="Pinned Fiji reference-sample GeoJSON")
    parser.add_argument("--raster", required=True, help="Local WorldCover COG, GeoTIFF or covering VRT")
    parser.add_argument("--output", required=True, help="Output CSV path")
    parser.add_argument("--class-names", default=None,
                        help="Optional JSON object mapping WorldCover integer codes to harmonised labels")
    args = parser.parse_args()

    try:
        class_names = dict(WORLDCOVER_NAMES)
        if args.class_names:
            supplied = json.loads(args.class_names)
            if not isinstance(supplied, dict):
                raise ValueError("--class-names must decode to a JSON object.")
            class_names = {int(code): str(label).strip() for code, label in supplied.items()}
        points, geojson_sha = read_pinned_points(args.geojson)
        rows, metadata = sample_worldcover(points, args.raster, class_names)
        metadata["fiji_geojson_sha256"] = hashlib.sha256(
            Path(args.geojson).read_bytes()
        ).hexdigest()
        metadata["fiji_geojson_path_as_supplied"] = str(Path(args.geojson))
        metadata["worldcover_raster_sha256"] = hashlib.sha256(
            Path(args.raster).read_bytes()
        ).hexdigest()
        metadata["worldcover_raster_size_bytes"] = Path(args.raster).stat().st_size
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with output_path.open("w", newline="", encoding="utf-8") as stream:
            writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)
        metadata_path = output_path.with_suffix(output_path.suffix + ".metadata.json")
        metadata_path.write_text(json.dumps(metadata, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    except (OSError, ValueError, RuntimeError, json.JSONDecodeError) as exc:
        parser.error(str(exc))

    print(f"Wrote {len(rows)} sample records to {output_path}")
    print(f"Wrote raster and provenance metadata to {metadata_path}")
    print("All points were sampled; nodata and out-of-coverage points cause an error, not silent omission.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
