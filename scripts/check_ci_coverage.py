"""Fail CI when implementation packages or learning notebooks are omitted.

The audit checks more than manifest membership: every package must have a
reader-facing README, an independently discoverable top-level test module,
and a valid optional import path. This keeps newly added directories from
silently escaping the isolated-package test matrix.
"""
from __future__ import annotations

import ast
from collections import Counter
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]


def _notebook_manifest(executor_path: Path) -> list[tuple[str, int]]:
    tree = ast.parse(executor_path.read_text(encoding="utf-8"))
    assignments = [
        node for node in tree.body
        if isinstance(node, ast.Assign)
        and any(
            isinstance(target, ast.Name) and target.id == "NOTEBOOKS"
            for target in node.targets
        )
    ]
    if len(assignments) != 1:
        raise ValueError("Notebook executor must define NOTEBOOKS exactly once")
    value = ast.literal_eval(assignments[0].value)
    if not isinstance(value, list):
        raise ValueError("NOTEBOOKS must be a list")
    result = []
    for item in value:
        if (
            not isinstance(item, (tuple, list))
            or len(item) != 2
            or not isinstance(item[0], str)
            or not item[0]
            or not isinstance(item[1], int)
            or isinstance(item[1], bool)
            or item[1] < 1
        ):
            raise ValueError(f"Invalid notebook manifest entry: {item!r}")
        result.append((item[0], item[1]))
    return result


def audit_coverage(root: Path = ROOT) -> tuple[list[str], int, int]:
    """Return (errors, Python package count, notebook count)."""
    errors: list[str] = []
    python_root = root / "implementations" / "python"
    workflow_path = root / ".github" / "workflows" / "python-tests.yml"
    executor_path = root / "scripts" / "execute_learning_notebooks.py"
    manifest_path = root / "scripts" / "python-ci-packages.json"

    if not python_root.is_dir():
        return ([f"Python implementation root is missing: {python_root}"], 0, 0)
    if not workflow_path.is_file() or not executor_path.is_file() or not manifest_path.is_file():
        missing = [str(path.relative_to(root)) for path in
                   (workflow_path, executor_path, manifest_path) if not path.is_file()]
        return ([f"Required CI coverage file is missing: {', '.join(missing)}"], 0, 0)

    workflow = workflow_path.read_text(encoding="utf-8")
    if "scripts/run_python_package_tests.py" not in workflow:
        errors.append("Workflow does not invoke the sharded Python package runner")

    python_dirs = {
        path.relative_to(root).as_posix()
        for path in python_root.iterdir()
        if path.is_dir()
    }
    try:
        package_manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return ([f"Cannot read Python CI package manifest: {exc}"], len(python_dirs), 0)

    if not isinstance(package_manifest, list):
        return (["Python CI package manifest must be a JSON list"], len(python_dirs), 0)

    manifest_dirs: list[str] = []
    for index, entry in enumerate(package_manifest):
        if (
            not isinstance(entry, dict)
            or set(entry) != {"directory", "pythonpath"}
            or not isinstance(entry.get("directory"), str)
            or not entry["directory"]
            or not isinstance(entry.get("pythonpath"), str)
        ):
            errors.append(f"Python CI package manifest entry {index} has an invalid schema")
            continue
        relative = Path(entry["directory"])
        if relative.is_absolute() or ".." in relative.parts:
            errors.append(f"Unsafe package directory in manifest: {entry['directory']}")
            continue
        manifest_dirs.append(relative.as_posix())
        package_dir = root / relative
        if not package_dir.is_dir():
            errors.append(f"Package directory referenced but not present: {relative.as_posix()}")
            continue
        if not (package_dir / "README.md").is_file():
            errors.append(f"Package README is missing: {relative.as_posix()}/README.md")
        tests = list(package_dir.glob("test_*.py")) + list(package_dir.glob("*_test.py"))
        if not tests:
            errors.append(f"Package has no top-level test module: {relative.as_posix()}")
        pythonpath = entry["pythonpath"].strip()
        if pythonpath:
            resolved = (package_dir / pythonpath).resolve()
            try:
                resolved.relative_to(root.resolve())
            except ValueError:
                errors.append(f"Package import path escapes repository: {relative.as_posix()} -> {pythonpath}")
            else:
                if not resolved.is_dir():
                    errors.append(f"Package import path does not exist: {relative.as_posix()} -> {pythonpath}")

    for label, values in (("Python CI package manifest entries", manifest_dirs),):
        duplicates = sorted(value for value, count in Counter(values).items() if count > 1)
        if duplicates:
            errors.append(f"{label} occur more than once: " + ", ".join(duplicates))

    missing = sorted(python_dirs - set(manifest_dirs))
    stale = sorted(set(manifest_dirs) - python_dirs)
    if missing:
        errors.append("Python implementation directories missing from CI: " + ", ".join(missing))
    if stale:
        errors.append("Python CI entries not present in repository: " + ", ".join(stale))

    try:
        notebook_manifest = _notebook_manifest(executor_path)
    except (OSError, SyntaxError, ValueError) as exc:
        return (errors + [f"Cannot read notebook execution manifest: {exc}"], len(python_dirs), 0)

    notebook_files = {
        path.relative_to(root).as_posix()
        for path in (root / "notebooks").glob("*.ipynb")
    }
    notebook_refs = ["notebooks/" + name for name, _timeout in notebook_manifest]
    duplicates = sorted(value for value, count in Counter(notebook_refs).items() if count > 1)
    if duplicates:
        errors.append("Notebook references occur more than once: " + ", ".join(duplicates))
    missing = sorted(notebook_files - set(notebook_refs))
    stale = sorted(set(notebook_refs) - notebook_files)
    if missing:
        errors.append("Learning notebooks missing from CI: " + ", ".join(missing))
    if stale:
        errors.append("Notebook references not present in repository: " + ", ".join(stale))

    return errors, len(python_dirs), len(notebook_files)


def main() -> int:
    errors, package_count, notebook_count = audit_coverage()
    if errors:
        print("\\n".join(errors), file=sys.stderr)
        return 1
    print(
        f"CI coverage verified: {package_count} Python implementation directories "
        f"and {notebook_count} notebooks, each referenced exactly once; "
        "package READMEs, tests and import paths are present."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
