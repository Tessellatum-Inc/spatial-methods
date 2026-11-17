#!/usr/bin/env python3
"""Reconcile source-entry status counts with the published 22-section dashboard.

Only tables with both "Source entry" and "Verification status" columns are
counted. Implementation inventories and explanatory tables are intentionally
excluded.
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


def is_separator(line: str) -> bool:
    return bool(re.fullmatch(r"\s*\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)*\|?\s*", line))


def source_rows(markdown: str) -> list[str]:
    """Return data rows from source-entry tables, not other Markdown tables."""
    lines = markdown.splitlines()
    found: list[str] = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if not line.lstrip().startswith("|"):
            i += 1
            continue
        header = [c.casefold() for c in cells(line)]
        if "source entry" not in header or "verification status" not in header:
            i += 1
            continue
        i += 1
        if i < len(lines) and is_separator(lines[i]):
            i += 1
        while i < len(lines) and lines[i].lstrip().startswith("|"):
            row = lines[i]
            if not is_separator(row):
                found.append(row)
            i += 1
    return found


def classify_status(row: str, path: Path) -> str:
    values = cells(row)
    if len(values) < 4:
        raise ValueError(f"{path}: malformed source-entry row: {row}")
    status = values[-1].casefold()
    if status.startswith("not checked") and "intake only" in status:
        return "intake"
    if status.startswith("partial") or status.startswith("partially implemented"):
        return "partial"
    raise ValueError(f"{path}: unrecognised source-entry status {values[-1]!r}")


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
        result[number] = tuple(int(v.replace(",", "")) for v in values[1:4])
    return result


def main() -> int:
    errors: list[str] = []
    totals = {"entries": 0, "partial": 0, "intake": 0}
    observed: dict[int, tuple[int, int, int]] = {}
    for number, path in enumerate(discover_indexes(), start=1):
        rows = source_rows(path.read_text(encoding="utf-8"))
        counts = {"partial": 0, "intake": 0}
        for row in rows:
            try:
                counts[classify_status(row, path)] += 1
            except ValueError as exc:
                errors.append(str(exc))
        observed[number] = (len(rows), counts["partial"], counts["intake"])
        totals["entries"] += len(rows)
        totals["partial"] += counts["partial"]
        totals["intake"] += counts["intake"]

    expected = dashboard_rows(DASHBOARD.read_text(encoding="utf-8"))
    if set(expected) != set(range(1, 23)):
        errors.append(f"Dashboard must contain sections 1–22; found {sorted(expected)}")
    for number, actual in observed.items():
        if expected.get(number) != actual:
            errors.append(
                f"Section {number}: dashboard {expected.get(number)} != source indexes {actual}"
            )

    headline = DASHBOARD.read_text(encoding="utf-8")
    expected_headline = (
        f"| Source-entry rows counted | {totals['entries']} |",
        f"| Partial | {totals['partial']} |",
        f"| Not checked — intake only | {totals['intake']} |",
    )
    for row in expected_headline:
        if row not in headline:
            errors.append(f"Dashboard headline does not contain: {row}")

    if totals["entries"] != totals["partial"] + totals["intake"]:
        errors.append("Source-entry status totals do not reconcile")
    if errors:
        print("\n".join(f"ERROR: {error}" for error in errors), file=sys.stderr)
        return 1
    print(
        f"Catalogue dashboard reconciled: {totals['entries']} source entries; "
        f"{totals['partial']} partial; {totals['intake']} intake-only; "
        "22 section indexes."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
