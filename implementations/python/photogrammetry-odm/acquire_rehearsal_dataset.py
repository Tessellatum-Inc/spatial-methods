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


def build_manifest(destination: Path, dataset_dir: Path, revision: str) -> dict:
    """Build a deterministic file inventory plus acquisition environment metadata."""
    manifest = build_manifest(destination, dataset_dir, revision)

    manifest_path = destination / "acquisition-provenance.json"
    manifest_path.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    print(f"Repository: {manifest['repository']}")
    print(f"Resolved revision: {revision}")
    print(f"Dataset directory: {dataset_dir}")
    print(f"Files fingerprinted: {len(files)}")
    print(f"Provenance manifest: {manifest_path}")
    print("Next: run dataset_audit.py against the dataset directory.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
