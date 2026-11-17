"""Fail CI when implementation packages or learning notebooks are omitted."""
from collections import Counter
import ast
from pathlib import Path
import re
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
matrix_dirs = re.findall(
    r"^\s*directory:\s*(implementations/python/[^\s#]+)",
    workflow,
    flags=re.MULTILINE,
)
standalone_dirs = sorted(set(re.findall(
    r"^\s*working-directory:\s*(implementations/python/[^\s#]+)",
    workflow,
    flags=re.MULTILINE,
)))
ci_package_dirs = matrix_dirs + standalone_dirs

notebook_files = {
    path.relative_to(ROOT).as_posix()
    for path in (ROOT / "notebooks").glob("*.ipynb")
}
notebook_refs = ["notebooks/" + name for name, _timeout in notebook_manifest]

errors = []
for label, expected, actual in (
    ("Python implementation directories", python_dirs, set(ci_package_dirs)),
    ("Learning notebooks", notebook_files, set(notebook_refs)),
):
    missing = sorted(expected - actual)
    stale = sorted(actual - expected)
    if missing:
        errors.append(f"{label} missing from CI: " + ", ".join(missing))
    if stale:
        errors.append(f"{label} referenced but not present: " + ", ".join(stale))

for label, values in (
    ("Python CI package references", ci_package_dirs),
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
