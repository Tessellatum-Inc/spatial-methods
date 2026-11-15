"""Fail CI when implementation packages or learning notebooks are omitted."""
from collections import Counter
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
workflow_path = ROOT / ".github" / "workflows" / "python-tests.yml"
workflow = workflow_path.read_text(encoding="utf-8")

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

notebook_files = {
    path.relative_to(ROOT).as_posix()
    for path in (ROOT / "notebooks").glob("*.ipynb")
}
notebook_refs = [
    "notebooks/" + name
    for name in re.findall(r"notebooks/([A-Za-z0-9._-]+\.ipynb)", workflow)
]

errors = []
for label, expected, actual in (
    ("Python implementation directories", python_dirs, set(matrix_dirs)),
    ("Learning notebooks", notebook_files, set(notebook_refs)),
):
    missing = sorted(expected - actual)
    stale = sorted(actual - expected)
    if missing:
        errors.append(f"{label} missing from CI: " + ", ".join(missing))
    if stale:
        errors.append(f"{label} referenced but not present: " + ", ".join(stale))

for label, values in (
    ("Python matrix directories", matrix_dirs),
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
