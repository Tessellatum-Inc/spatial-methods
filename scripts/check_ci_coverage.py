"""Fail CI when implementation packages or learning notebooks are omitted."""
from collections import Counter
import ast
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
workflow_path = ROOT / ".github" / "workflows" / "python-tests.yml"
workflow = workflow_path.read_text(encoding="utf-8")
executor_path = ROOT / "scripts" / "execute_learning_notebooks.py"
executor = ast.parse(executor_path.read_text(encoding="utf-8"))
notebook_assignment = next(node for node in executor.body if isinstance(node, ast.Assign) and any(isinstance(target, ast.Name) and target.id == "NOTEBOOKS" for target in node.targets))
notebook_manifest = ast.literal_eval(notebook_assignment.value)

python_dirs = {
    path.relative_to(ROOT).as_posix()
    for path in (ROOT / "implementations" / "python").iterdir()
    if path.is_dir()
}
manifest_path = ROOT / "scripts" / "python-ci-packages.json"
package_manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
if not isinstance(package_manifest, list) or any(
    not isinstance(entry, dict)
    or set(entry) != {"directory", "pythonpath"}
    or not isinstance(entry["directory"], str)
    or not isinstance(entry["pythonpath"], str)
    for entry in package_manifest
):
    raise SystemExit("Python CI package manifest has an invalid entry schema")
manifest_dirs = [entry["directory"] for entry in package_manifest]
if "scripts/run_python_package_tests.py" not in workflow:
    raise SystemExit("Workflow does not invoke the sharded Python package runner")

notebook_files = {
    path.relative_to(ROOT).as_posix()
    for path in (ROOT / "notebooks").glob("*.ipynb")
}
notebook_refs = ["notebooks/" + name for name, _timeout in notebook_manifest]

errors = []
for label, expected, actual in (
    ("Python implementation directories", python_dirs, set(manifest_dirs)),
    ("Learning notebooks", notebook_files, set(notebook_refs)),
):
    missing = sorted(expected - actual)
    stale = sorted(actual - expected)
    if missing:
        errors.append(f"{label} missing from CI: " + ", ".join(missing))
    if stale:
        errors.append(f"{label} referenced but not present: " + ", ".join(stale))

for label, values in (
    ("Python CI package manifest entries", manifest_dirs),
    ("Notebook references", notebook_refs),
):
    duplicates = sorted(value for value, count in Counter(values).items() if count > 1)
    if duplicates:
        errors.append(f"{label} occur more than once: " + ", ".join(duplicates))

if errors:
    print("\n".join(errors), file=sys.stderr)
    raise SystemExit(1)

print(
    f"CI coverage verified: {len(python_dirs)} Python implementation directories "
    f"and {len(notebook_files)} notebooks, each referenced exactly once."
)
