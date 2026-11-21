"""Audit image files in a photogrammetry dataset without modifying the source data."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

IMAGE_SUFFIXES = {".jpg", ".jpeg", ".tif", ".tiff", ".png", ".dng"}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def inspect_images(
    root: Path,
    expected_count: int | None = None,
    supported_suffixes: set[str] | None = None,
) -> dict:
    root = root.expanduser().resolve()
    if not root.is_dir():
        raise ValueError(f"Dataset directory does not exist: {root}")
    suffixes = IMAGE_SUFFIXES if supported_suffixes is None else {s.lower() for s in supported_suffixes}
    files = sorted(
        p for p in root.rglob("*")
        if p.is_file() and p.suffix.lower() in suffixes
    )
    if not files:
        raise ValueError(f"No supported image files found under: {root}")

    try:
        from PIL import Image, ExifTags
        pillow_available = True
        exif_names = {value: key for key, value in ExifTags.TAGS.items()}
        gps_name = exif_names.get("GPSInfo")
    except ImportError:
        Image = None
        pillow_available = False
        gps_name = None

    records = []
    for path in files:
        item = {
            "path": path.relative_to(root).as_posix(),
            "bytes": path.stat().st_size,
            "sha256": sha256_file(path),
        }
        if pillow_available:
            try:
                with Image.open(path) as image:
                    image.verify()
                with Image.open(path) as image:
                    exif = image.getexif()
                    item.update({
                        "image_valid": True,
                        "format": image.format,
                        "width_px": image.width,
                        "height_px": image.height,
                        "exif_present": bool(exif),
                        "gps_metadata_present": bool(gps_name is not None and gps_name in exif),
                        "camera_make": exif.get(exif_names.get("Make", -1)),
                        "camera_model": exif.get(exif_names.get("Model", -1)),
                    })
            except Exception as exc:
                item.update({"image_valid": False, "inspection_error": str(exc)})
        records.append(item)

    valid_count = sum(1 for item in records if item.get("image_valid") is True)
    invalid_count = sum(1 for item in records if item.get("image_valid") is False)
    report = {
        "dataset_root": str(root),
        "image_count": len(records),
        "expected_image_count": expected_count,
        "image_count_matches_expectation": (
            None if expected_count is None else len(records) == expected_count
        ),
        "pillow_available": pillow_available,
        "valid_images": valid_count if pillow_available else None,
        "invalid_images": invalid_count if pillow_available else None,
        "gps_metadata_images": (
            sum(1 for item in records if item.get("gps_metadata_present"))
            if pillow_available else None
        ),
        "images": records,
        "limitations": [
            "A readable image and present EXIF GPS tag do not establish positional accuracy.",
            "This audit does not interpret coordinate reference systems, camera calibration, ground-control observations or checkpoint independence.",
            "File hashes establish identity for this audit run, not authenticity of the source or correctness of its metadata.",
        ],
    }
    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Create a read-only inventory, SHA-256 manifest and optional image metadata audit."
    )
    parser.add_argument("dataset_root", type=Path)
    parser.add_argument("--expected-images", type=int)
    parser.add_argument("--json-out", type=Path)
    args = parser.parse_args(argv)
    try:
        report = inspect_images(args.dataset_root, args.expected_images)
    except (OSError, ValueError) as exc:
        parser.error(str(exc))
    rendered = json.dumps(report, indent=2, sort_keys=True)
    print(rendered)
    if args.json_out:
        args.json_out.write_text(rendered + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
