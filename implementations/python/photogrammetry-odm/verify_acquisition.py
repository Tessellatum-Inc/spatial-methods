#!/usr/bin/env python3
"""Verify an acquired HEIG-VD snapshot against its SHA-256 provenance manifest.

This is a local integrity check. It does not establish publisher authenticity,
licence compliance, semantic correctness or fitness for photogrammetric use.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def verify_manifest(manifest_path: str | Path) -> dict:
    manifest_file = Path(manifest_path).expanduser().resolve()
    if not manifest_file.is_file():
        raise ValueError(f"Acquisition manifest does not exist: {manifest_file}")
    try:
        manifest = json.loads(manifest_file.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"Acquisition manifest is not valid JSON: {exc}") from exc

    revision = manifest.get("resolved_revision")
    if not isinstance(revision, str) or len(revision) != 40 or any(
        char not in "0123456789abcdefABCDEF" for char in revision
    ):
        raise ValueError("Manifest resolved_revision must be a 40-character hexadecimal commit SHA.")

    snapshot_root = manifest_file.parent.resolve()
    selected_path = manifest.get("selected_path")
    if selected_path != "datasets/drone_heig_2019":
        raise ValueError("Manifest selected_path does not match the expected rehearsal dataset.")

    entries = manifest.get("files")
    if not isinstance(entries, list) or not entries:
        raise ValueError("Manifest files must be a non-empty list.")
    if manifest.get("file_count") != len(entries):
        raise ValueError("Manifest file_count does not match the files list.")

    seen = set()
    checks = []
    for entry in entries:
        if not isinstance(entry, dict):
            raise ValueError("Every manifest file entry must be an object.")
        relative_text = entry.get("path")
        if not isinstance(relative_text, str):
            raise ValueError("Every manifest file entry requires a relative path.")
        relative = PurePosixPath(relative_text)
        if relative.is_absolute() or ".." in relative.parts or not relative.parts:
            raise ValueError(f"Unsafe manifest path: {relative_text}")
        if not relative_text.startswith(selected_path + "/"):
            raise ValueError(f"Manifest path is outside the selected dataset: {relative_text}")
        if relative_text in seen:
            raise ValueError(f"Duplicate manifest path: {relative_text}")
        seen.add(relative_text)
        candidate = snapshot_root.joinpath(*relative.parts)
        components = [snapshot_root.joinpath(*relative.parts[:index]) for index in range(1, len(relative.parts) + 1)]
        linked_components = [item.relative_to(snapshot_root).as_posix() for item in components if item.is_symlink()]
        if linked_components:
            checks.append({
                "path": relative_text, "status": "invalid",
                "reason": "symbolic link component: " + ", ".join(linked_components),
            })
            continue
        if snapshot_root not in candidate.resolve().parents:
            raise ValueError(f"Manifest path escapes snapshot directory: {relative_text}")
        if not candidate.is_file():
            checks.append({"path": relative_text, "status": "missing", "reason": "file not found"})
            continue
        actual_size = candidate.stat().st_size
        actual_hash = sha256_file(candidate)
        expected_size = entry.get("size_bytes")
        expected_hash = entry.get("sha256")
        matches = actual_size == expected_size and actual_hash == expected_hash
        checks.append({
            "path": relative_text,
            "status": "verified" if matches else "mismatch",
            "expected_size_bytes": expected_size,
            "actual_size_bytes": actual_size,
            "expected_sha256": expected_hash,
            "actual_sha256": actual_hash,
        })

    dataset_root = snapshot_root / selected_path
    dataset_entries = list(dataset_root.rglob("*")) if dataset_root.is_dir() else []
    unmanifested_symlinks = sorted(
        path.relative_to(snapshot_root).as_posix()
        for path in dataset_entries if path.is_symlink()
    )
    actual_files = {
        path.relative_to(snapshot_root).as_posix()
        for path in dataset_entries
        if path.is_file() and not path.is_symlink()
    }
    unmanifested = sorted(actual_files - seen)
    missing = sum(item["status"] == "missing" for item in checks)
    mismatched = sum(item["status"] in {"mismatch", "invalid"} for item in checks)
    verified = sum(item["status"] == "verified" for item in checks)
    status = "verified" if verified == len(checks) and not unmanifested and not unmanifested_symlinks else "integrity_error"
    return {
        "schema_version": "1.0",
        "status": status,
        "manifest_path": str(manifest_file),
        "manifest_sha256": sha256_file(manifest_file),
        "manifest_size_bytes": manifest_file.stat().st_size,
        "repository_id": manifest.get("repository_id"),
        "resolved_revision": revision.lower(),
        "selected_path": selected_path,
        "declared_file_count": len(entries),
        "verified_file_count": verified,
        "missing_file_count": missing,
        "mismatched_or_invalid_file_count": mismatched,
        "unmanifested_file_count": len(unmanifested),
        "unmanifested_files": unmanifested,
        "symbolic_link_paths": unmanifested_symlinks,
        "files": checks,
        "limitations": [
            "Hash agreement establishes local byte identity with this manifest, not publisher authenticity.",
            "This check does not validate licence obligations, file semantics, image decoding or photogrammetric suitability.",
            "A clean result does not replace the dataset audit or human review.",
        ],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Verify downloaded files against acquisition-provenance.json.")
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--json-out", type=Path)
    args = parser.parse_args(argv)
    try:
        report = verify_manifest(args.manifest)
    except (OSError, ValueError) as exc:
        parser.error(str(exc))
    rendered = json.dumps(report, indent=2, sort_keys=True)
    print(rendered)
    if args.json_out:
        args.json_out.write_text(rendered + "\n", encoding="utf-8")
    return 0 if report["status"] == "verified" else 2


if __name__ == "__main__":
    raise SystemExit(main())
