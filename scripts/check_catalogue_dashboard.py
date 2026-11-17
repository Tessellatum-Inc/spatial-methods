#!/usr/bin/env python3
"""Recount source-entry review states from all 22 section indexes.

Only tables whose first header is "Source entry" are counted. Intake-only
labels are classified as not checked; explicit fully-verified labels are
counted separately; every other non-empty status is partial. This deliberately
treats implementation-linked rows as partial even when their prose does not
literally contain the word "partial".
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
    """Split a Markdown table row, respecting escaped literal pipes."""
    value = line.strip()
    if value.startswith("|"):
        value = value[1:]
    if value.endswith("|"):
        value = value[:-1]
    return [part.replace(r"\|", "|").strip()
            for part in re.split(r"(?<!\\)\|", value)]


def discover_indexes() -> list[Path]:
    if not INDEX.is_file():
        raise FileNotFoundError(INDEX)
    names = re.findall(
        r"\]\((\d{2}-[^)]+\.md)\)",
        INDEX.read_text(encoding="utf-8"),
    )
    paths = [SECTIONS / name for name in names]
    if len(paths) != 22 or len(set(paths)) != 22:
        raise ValueError(f"Expected 22 unique section indexes; found {len(paths)}")
    missing = [str(path.relative_to(ROOT)) for path in paths if not path.is_file()]
    if missing:
        raise FileNotFoundError("Missing section indexes: " + ", ".join(missing))
    return paths


def source_entry_counts(markdown: str, source: str = "<memory>") -> tuple[int, int, int, int]:
    """Return (entries, partial, intake_only, fully_verified) for source tables."""
    active = False
    found_table = False
    entries = partial = intake = verified = 0

    for line_number, line in enumerate(markdown.splitlines(), start=1):
        if not line.lstrip().startswith("|"):
            active = False
            continue
        values = cells(line)
        if values and values[0].casefold() == "source entry":
            active = True
            found_table = True
            if len(values) < 4:
                raise ValueError(f"{source}:{line_number}: malformed source-entry header")
            continue
        if not active:
            continue
        if not values or all(re.fullmatch(r":?-{3,}:?", cell.replace(" ", "")) for cell in values):
            continue
        if len(values) < 4:
            raise ValueError(f"{source}:{line_number}: malformed source-entry row")
        status = values[-1].casefold()
        if not status:
            raise ValueError(f"{source}:{line_number}: source-entry status is empty")
        entries += 1
        if "fully verified" in status:
            verified += 1
        elif "not checked" in status or "intake only" in status:
            intake += 1
        else:
            partial += 1

    if not found_table:
        raise ValueError(f"{source}: source-entry/status table is missing")
    return entries, partial, intake, verified


def dashboard_rows(markdown: str) -> dict[int, tuple[int, int, int]]:
    lines = markdown.splitlines()
    try:
        start = next(
            i for i, line in enumerate(lines)
            if line.strip() == "| Section | Source entries | Partial | Intake only |"
        )
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
    actual: dict[int, tuple[int, int, int, int]] = {}
    for number, path in enumerate(indexes, start=1):
        try:
            actual[number] = source_entry_counts(
                path.read_text(encoding="utf-8"),
                str(path.relative_to(ROOT)),
            )
        except (OSError, ValueError) as exc:
            errors.append(str(exc))

    dashboard = DASHBOARD.read_text(encoding="utf-8")
    published = dashboard_rows(dashboard)
    if set(published) != set(range(1, 23)):
        errors.append(f"Dashboard must contain sections 1–22; found {sorted(published)}")

    for number, counts in actual.items():
        entries, partial, intake, _verified = counts
        expected = (entries, partial, intake)
        if published.get(number) != expected:
            errors.append(
                f"Section {number} dashboard row is {published.get(number)}, "
                f"but source index recount is {expected}"
            )

    totals = tuple(sum(row[i] for row in actual.values()) for i in range(4))
    entries, partial, intake, verified = totals
    if entries != partial + intake + verified:
        errors.append(
            f"Source-entry recount does not reconcile: {entries} != "
            f"{partial} partial + {intake} intake-only + {verified} fully verified"
        )
    expected_lines = (
        f"| Source-entry rows counted | {entries} |",
        f"| Partial | {partial} |",
        f"| Not checked — intake only | {intake} |",
        f"| Fully verified | {verified} |",
        f"| **Total** | **{entries}** | **{partial}** | **{intake}** |",
    )
    for line in expected_lines:
        if line not in dashboard:
            errors.append(f"Dashboard aggregate does not match source indexes: {line}")

    if errors:
        print("\n".join(f"ERROR: {error}" for error in errors), file=sys.stderr)
        return 1
    print(
        f"Source catalogue reconciled from {len(indexes)} indexes: "
        f"{entries} entries; {partial} partial; {intake} intake-only; "
        f"{verified} fully verified."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
