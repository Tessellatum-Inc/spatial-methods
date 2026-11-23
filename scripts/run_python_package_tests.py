"""Run a deterministic shard of isolated Python implementation-package tests."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import venv

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "scripts" / "python-ci-packages.json"


def packages_for_shard(packages, shard_index, shard_count):
    if shard_count < 1 or shard_index < 0 or shard_index >= shard_count:
        raise ValueError("shard index must be within a positive shard count")
    return packages[shard_index::shard_count]


def run(command, *, cwd, env):
    print("+", " ".join(str(part) for part in command), flush=True)
    subprocess.run(command, cwd=cwd, env=env, check=True)


def test_package(entry):
    relative = entry["directory"]
    package_dir = ROOT / relative
    if not package_dir.is_dir():
        raise FileNotFoundError(f"package directory does not exist: {relative}")

    with tempfile.TemporaryDirectory(prefix="spatial-package-venv-") as temp_dir:
        venv_dir = Path(temp_dir) / "venv"
        venv.EnvBuilder(with_pip=True).create(venv_dir)
        python = venv_dir / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
        env = os.environ.copy()
        pythonpath = entry.get("pythonpath", "").strip()
        if pythonpath:
            env["PYTHONPATH"] = str((package_dir / pythonpath).resolve())
        else:
            env.pop("PYTHONPATH", None)

        run([str(python), "-m", "pip", "install", "pytest"], cwd=package_dir, env=env)
        requirements = package_dir / "requirements.txt"
        if requirements.exists():
            run([str(python), "-m", "pip", "install", "-r", str(requirements)], cwd=package_dir, env=env)
        run([str(python), "-m", "pytest", "-q"], cwd=package_dir, env=env)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--shard-count", type=int, required=True)
    parser.add_argument("--shard-index", type=int, required=True)
    args = parser.parse_args()

    packages = json.loads(MANIFEST.read_text(encoding="utf-8"))
    selected = packages_for_shard(packages, args.shard_index, args.shard_count)
    if not selected:
        raise SystemExit(f"empty package shard {args.shard_index}/{args.shard_count}")
    print(
        f"Testing {len(selected)} package(s) in shard "
        f"{args.shard_index + 1}/{args.shard_count}",
        flush=True,
    )
    for entry in selected:
        print(f"\n=== {entry['directory']} ===", flush=True)
        test_package(entry)


if __name__ == "__main__":
    main()
