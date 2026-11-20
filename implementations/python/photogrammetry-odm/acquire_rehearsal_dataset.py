#!/usr/bin/env python3
"""Download and fingerprint the HEIG-VD photogrammetry rehearsal subset.

The Hub repository's moving default branch is resolved once; the selected
subset is downloaded at that immutable commit. A local provenance JSON records
the revision and SHA-256/size of every downloaded file.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import re
from datetime import datetime, timezone
from importlib.metadata import version
from pathlib import Path

REPO_ID = "heig-vd-geo/scop-datasets"
REPO_TYPE = "dataset"
DATASET_PATH = "datasets/drone_heig_2019"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def revision_snapshot_dir(destination: Path, revision: str) -> Path:
    """Return an isolated local directory for one immutable Hub revision."""
    if not re.fullmatch(r"[0-9a-fA-F]{40}", revision):
        raise ValueError("Expected a 40-character hexadecimal repository commit SHA.")
    return destination / "snapshots" / revision.lower()


def build_manifest(destination: Path, dataset_dir: Path, revision: str) -> dict:
    """Build a file inventory plus acquisition environment metadata."""
    files = sorted(path for path in dataset_dir.rglob("*") if path.is_file())
    if not files:
        raise RuntimeError(f"No files were downloaded under {dataset_dir}.")

    return {
        "repository": f"https://huggingface.co/datasets/{REPO_ID}",
        "repository_id": REPO_ID,
        "repository_type": REPO_TYPE,
        "resolved_revision": revision,
        "selected_path": DATASET_PATH,
        "retrieved_at_utc": datetime.now(timezone.utc).isoformat(),
        "python_version": platform.python_version(),
        "huggingface_hub_version": version("huggingface_hub"),
        "file_count": len(files),
        "files": [
            {
                "path": path.relative_to(destination).as_posix(),
                "size_bytes": path.stat().st_size,
                "sha256": sha256_file(path),
            }
            for path in files
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Download and fingerprint the HEIG-VD drone 2019 subset."
    )
    parser.add_argument(
        "destination",
        nargs="?",
        default="./data/heig-vd-scop",
        help="Local download directory (default: ./data/heig-vd-scop)",
    )
    args = parser.parse_args()

    try:
        from huggingface_hub import HfApi, snapshot_download
    except ImportError:
        parser.error(
            "Missing optional dependency. Install it with: "
            "python -m pip install huggingface_hub"
        )

    destination = Path(args.destination).expanduser().resolve()
    destination.mkdir(parents=True, exist_ok=True)

    # Resolve the moving default branch once, then download that exact commit.
    revision = HfApi().repo_info(repo_id=REPO_ID, repo_type=REPO_TYPE).sha
    if not revision:
        raise RuntimeError("The Hub did not return a repository commit SHA.")
    snapshot_dir = revision_snapshot_dir(destination, revision)
    snapshot_dir.mkdir(parents=True, exist_ok=True)

    snapshot_download(
        repo_id=REPO_ID,
        repo_type=REPO_TYPE,
        revision=revision,
        allow_patterns=[f"{DATASET_PATH}/**"],
        local_dir=str(snapshot_dir),
        max_workers=4,
    )

    dataset_dir = snapshot_dir / DATASET_PATH
    if not dataset_dir.is_dir():
        raise RuntimeError(
            f"Download completed without the expected directory: {dataset_dir}. "
            "Check the repository tree and selected revision."
        )

    manifest = build_manifest(destination, dataset_dir, revision)
    manifest_path = snapshot_dir / "acquisition-provenance.json"
    manifest_path.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    print(f"Repository: {manifest['repository']}")
    print(f"Resolved revision: {revision}")
    print(f"Revision snapshot: {snapshot_dir}")
    print(f"Dataset directory: {dataset_dir}")
    print(f"Files fingerprinted: {manifest['file_count']}")
    print(f"Provenance manifest: {manifest_path}")
    print("Next: run dataset_audit.py against the dataset directory.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
