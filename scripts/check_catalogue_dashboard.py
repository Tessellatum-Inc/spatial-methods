#!/usr/bin/env python3
"""Validate the source catalogue's 22-index inventory and dashboard arithmetic.

The section indexes contain both original source-entry tables and later
supplementary/implementation tables. Their labels are not all expressed using
one controlled vocabulary, so this checker deliberately does not infer a new
source-entry total from every Markdown table. It verifies the published
section-level ledger is internally consistent and that all 22 indexed files
remain present and contain a source-entry/status table.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SECTIONS = ROOT / "catalog" / "sections"
INDEX = SECTIONS / "README.md"
DASHBOARD = ROOT / "catalog" / "review-dashboard.md"


def cells(line: str) -> list[str]:
    return [part.strip() for part in line.strip().strip("|").split("|")]


def discover_indexes() -> list[Path]:
    if not INDEX.is_file():
        raise FileNotFoundError(INDEX)
    names = re.findall(r"\]\((\d{2}-[^)]+\.md)\)", INDEX.read_text(encoding="utf-8"))
    paths = [SECTIONS / name for name in names]
    if len(paths) != 22 or len(set(paths)) != 22:
        raise ValueError(f"Expected 22 unique section indexes; found {len(paths)}")
    missing = [str(path.relative_to(ROOT)) for path in paths if not path.is_file()]
    if missing:
        raise FileNotFoundError("Missing section indexes: " + ", ".join(missing))
    for path in paths:
        content = path.read_text(encoding="utf-8").casefold()
        if "source entry" not in content or "status" not in content:
            raise ValueError(f"{path}: source-entry/status table is missing")
    return paths


def dashboard_rows(markdown: str) -> dict[int, tuple[int, int, int]]:
    lines = markdown.splitlines()
    try:
        start = next(i for i, line in enumerate(lines)
                     if line.strip() == "| Section | Source entries | Partial | Intake only |")
    except StopIteration as exc:
        raise ValueError("Dashboard is missing its by-section table header") from exc
    result: dict[int, tuple[int, int, int]] = {}
    for line in lines[start + 2:]:
        if not line.lstrip().startswith("|"):
            break
        values = cells(line)
        if values[0].casefold().startswith("**total"):
            break
        match = re.match(r"(\d+)\s*[—-]", values[0])
        if not match:
            continue
        number = int(match.group(1))
        if len(values) != 4:
            raise ValueError(f"Malformed dashboard row for section {number}: {line}")
        if number in result:
            raise ValueError(f"Duplicate dashboard row for section {number}")
        result[number] = tuple(int(v.replace(",", "")) for v in values[1:4])
    return result


def main() -> int:
    errors: list[str] = []
    indexes = discover_indexes()
    dashboard = DASHBOARD.read_text(encoding="utf-8")
    rows = dashboard_rows(dashboard)
    if set(rows) != set(range(1, 23)):
        errors.append(f"Dashboard must contain sections 1–22; found {sorted(rows)}")

    totals = tuple(sum(row[i] for row in rows.values()) for i in range(3))
    entries, partial, intake = totals
    if entries != partial + intake:
        errors.append(
            f"By-section ledger does not reconcile: {entries} entries != "
            f"{partial} partial + {intake} intake-only"
        )
    expected = (
        f"| Source-entry rows counted | {entries} |",
        f"| Partial | {partial} |",
        f"| Not checked — intake only | {intake} |",
        f"| **Total** | **{entries}** | **{partial}** | **{intake}** |",
    )
    for line in expected:
        if line not in dashboard:
            errors.append(f"Dashboard aggregate does not match by-section ledger: {line}")

    if errors:
        print("\n".join(f"ERROR: {error}" for error in errors), file=sys.stderr)
        return 1
    print(
        f"Catalogue dashboard arithmetic reconciled: {entries} entries; "
        f"{partial} partial; {intake} intake-only; {len(indexes)} section indexes."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
