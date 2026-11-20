#!/usr/bin/env python3
"""Download only the selected HEIG-VD photogrammetry rehearsal dataset.

The script resolves the dataset repository's current commit first, then downloads
the selected directory at that immutable revision and prints the revision used.
It does not modify the source repository or process the imagery.
"""

from __future__ import annotations

import argparse
from pathlib import Path


REPO_ID = "heig-vd-geo/scop-datasets"
REPO_TYPE = "dataset"
DATASET_PATH = "datasets/drone_heig_2019"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Download the HEIG-VD drone 2019 subset at a recorded Hub revision."
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

    snapshot_download(
        repo_id=REPO_ID,
        repo_type=REPO_TYPE,
        revision=revision,
        allow_patterns=[f"{DATASET_PATH}/**"],
        local_dir=str(destination),
        max_workers=4,
    )

    dataset_dir = destination / DATASET_PATH
    if not dataset_dir.is_dir():
        raise RuntimeError(
            f"Download completed without the expected directory: {dataset_dir}. "
            "Check the repository tree and selected revision."
        )

    print(f"Repository: https://huggingface.co/datasets/{REPO_ID}")
    print(f"Resolved revision: {revision}")
    print(f"Dataset directory: {dataset_dir}")
    print("Next: run dataset_audit.py against this directory and inspect source metadata.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
