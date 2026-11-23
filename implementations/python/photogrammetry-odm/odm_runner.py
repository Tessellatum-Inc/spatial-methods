"""Validate an ODM project directory and run a pinned Docker image."""
from __future__ import annotations

import argparse
from pathlib import Path
import shutil
import subprocess
import sys


IMAGE_SUFFIXES = {".jpg", ".jpeg", ".tif", ".tiff", ".dng"}


def validate_project(project: Path) -> tuple[Path, str, int]:
    project = project.expanduser().resolve()
    if not project.exists() or not project.is_dir():
        raise ValueError(f"Project directory does not exist: {project}")
    images = project / "images"
    if not images.is_dir():
        raise ValueError(f"Expected an images/ directory inside: {project}")
    image_files = [
        path for path in images.rglob("*")
        if path.is_file() and path.suffix.lower() in IMAGE_SUFFIXES
    ]
    if not image_files:
        raise ValueError(f"No supported image files found under: {images}")
    return project.parent, project.name, len(image_files)


def build_command(project: Path, image: str, odm_args: list[str] | None = None) -> list[str]:
    if not image or any(char.isspace() for char in image):
        raise ValueError("Provide one Docker image reference without whitespace")
    parent, name, _ = validate_project(project)
    command = [
        "docker", "run", "--rm",
        "-v", f"{parent}:/datasets",
        image,
        "--project-path", "/datasets", name,
        "--dsm",
    ]
    command.extend(odm_args or [])
    return command


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Run OpenDroneMap in Docker for an existing project/images directory."
    )
    parser.add_argument("project", type=Path, help="Project directory containing images/")
    parser.add_argument("--image", required=True, help="Pinned ODM Docker image tag or digest")
    parser.add_argument("--dry-run", action="store_true", help="Print command without executing")
    parser.add_argument(
        "--odm-arg", action="append", default=[],
        help="Additional ODM argument; repeat for each token, e.g. --odm-arg=--orthophoto-resolution --odm-arg=5",
    )
    args = parser.parse_args(argv)

    try:
        parent, name, count = validate_project(args.project)
        command = build_command(args.project, args.image, args.odm_arg)
    except ValueError as exc:
        parser.error(str(exc))

    print(f"Project: {parent / name}")
    print(f"Supported images found: {count}")
    print(f"Container image: {args.image}")
    print("Command: " + " ".join(command))
    if args.dry_run:
        print("Dry run only; Docker was not invoked.")
        return 0

    if shutil.which("docker") is None:
        print("Docker executable not found. Install Docker and ensure it is on PATH.", file=sys.stderr)
        return 2
    completed = subprocess.run(command, check=False)
    return completed.returncode


if __name__ == "__main__":
    raise SystemExit(main())
