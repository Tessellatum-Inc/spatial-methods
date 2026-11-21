"""Create a provenance record for an explicitly requested ODM run.

Dry-run is the default. Processing occurs only with --execute.
Source imagery is hashed before execution; logs and a JSON run record are
written to a separate run directory.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import platform
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

from odm_runner import IMAGE_SUFFIXES, build_command, validate_project


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def inventory_files(root: Path, suffixes: set[str] | None = None) -> list[dict]:
    allowed = {item.lower() for item in suffixes} if suffixes else None
    records = []
    for path in sorted(p for p in root.rglob("*") if p.is_file()):
        if allowed is not None and path.suffix.lower() not in allowed:
            continue
        records.append({
            "path": path.relative_to(root).as_posix(),
            "size_bytes": path.stat().st_size,
            "sha256": sha256_file(path),
        })
    return records


def docker_image_metadata(image: str) -> dict:
    if shutil.which("docker") is None:
        return {"available": False, "reason": "Docker executable not found"}
    result = subprocess.run(
        ["docker", "image", "inspect", image],
        capture_output=True, text=True, check=False,
    )
    if result.returncode != 0:
        return {"available": False, "reason": result.stderr.strip() or "Image inspect failed"}
    try:
        item = json.loads(result.stdout)[0]
    except (json.JSONDecodeError, IndexError, TypeError):
        return {"available": False, "reason": "Unrecognised Docker inspect response"}
    return {
        "available": True,
        "image_id": item.get("Id"),
        "repo_digests": item.get("RepoDigests") or [],
        "os": item.get("Os"),
        "architecture": item.get("Architecture"),
    }


def create_run_record(
    project: Path,
    image: str,
    arguments: list[str],
    run_directory: Path,
    execute: bool = False,
) -> dict:
    project = project.expanduser().resolve()
    run_directory = run_directory.expanduser().resolve()
    validate_project(project)
    if run_directory == project or project in run_directory.parents:
        raise ValueError("Run directory must be outside the project directory.")
    run_directory.mkdir(parents=True, exist_ok=True)
    command = build_command(project, image, arguments)
    inputs = inventory_files(project / "images", IMAGE_SUFFIXES)
    started = datetime.now(timezone.utc)
    metadata = (\n        docker_image_metadata(image) if execute\n        else {"available": False, "reason": "Not inspected during dry-run"}\n    )
    record = {
        "schema_version": "1.0",
        "run_id": started.strftime("%Y%m%dT%H%M%S%fZ"),
        "status": "prepared" if not execute else "running",
        "project_directory": str(project),
        "input_inventory": inputs,
        "input_count": len(inputs),
        "container": {"requested_reference": image, **metadata},
        "processing": {
            "engine": "OpenDroneMap",
            "command": command,
            "arguments": arguments,
            "executed": False,
        },
        "environment": {
            "python": sys.version,
            "platform": platform.platform(),
        },
        "started_at": started.isoformat(),
        "finished_at": None,
        "exit_code": None,
        "logs": {},
        "outputs": [],
        "limitations": [
            "Input hashes identify the files present at preflight; they do not prove acquisition authenticity or survey correctness.",
            "Docker image metadata is recorded only when inspect succeeds; requested tags may be mutable.",
            "Output inventory covers files present under the project directory after execution.",
            "A successful process exit is not evidence of photogrammetric accuracy or acceptance.",
        ],
    }
    if execute:
        if shutil.which("docker") is None:
            raise RuntimeError("Docker executable not found; processing was not started.")
        completed = subprocess.run(command, capture_output=True, text=True, check=False)
        (run_directory / "stdout.log").write_text(completed.stdout, encoding="utf-8")
        (run_directory / "stderr.log").write_text(completed.stderr, encoding="utf-8")
        record["processing"]["executed"] = True
        record["status"] = "succeeded" if completed.returncode == 0 else "failed"
        record["exit_code"] = completed.returncode
        record["logs"] = {"stdout": "stdout.log", "stderr": "stderr.log"}
        record["outputs"] = inventory_files(project)
        record["finished_at"] = datetime.now(timezone.utc).isoformat()
    record_path = run_directory / "processing-run.json"
    record_path.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return record


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Record an ODM processing run; dry-run unless --execute is supplied.")
    parser.add_argument("project", type=Path, help="ODM project directory containing images/")
    parser.add_argument("--image", required=True, help="Pinned ODM container reference")
    parser.add_argument("--run-directory", required=True, type=Path, help="Separate directory for logs and run record")
    parser.add_argument("--odm-arg", action="append", default=[], help="Additional ODM argument; repeat per token")
    parser.add_argument("--execute", action="store_true", help="Actually invoke Docker; otherwise only prepare provenance")
    args = parser.parse_args(argv)
    try:
        record = create_run_record(args.project, args.image, args.odm_arg, args.run_directory, args.execute)
    except (OSError, ValueError, RuntimeError) as exc:
        parser.error(str(exc))
    print(json.dumps(record, indent=2, sort_keys=True))
    return 0 if record["status"] in {"prepared", "succeeded"} else 2


if __name__ == "__main__":
    raise SystemExit(main())
