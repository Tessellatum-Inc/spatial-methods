"""Transparent independent-checkpoint residual statistics; standard library only."""
from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path
from statistics import median
from typing import Iterable


REQUIRED = ("point_id", "ref_x", "ref_y", "ref_z", "model_x", "model_y", "model_z")


def _number(value: str, field: str, row_number: int) -> float:
    try:
        result = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"Row {row_number}: {field} must be numeric") from exc
    if not math.isfinite(result):
        raise ValueError(f"Row {row_number}: {field} must be finite")
    return result


def read_checkpoints(path: str | Path) -> list[dict[str, float | str]]:
    with open(path, newline="", encoding="utf-8-sig") as stream:
        reader = csv.DictReader(stream)
        if reader.fieldnames is None:
            raise ValueError("CSV must include a header row")
        missing = [field for field in REQUIRED if field not in reader.fieldnames]
        if missing:
            raise ValueError("Missing required columns: " + ", ".join(missing))
        records = []
        seen = set()
        for row_number, row in enumerate(reader, start=2):
            point_id = (row.get("point_id") or "").strip()
            if not point_id:
                raise ValueError(f"Row {row_number}: point_id cannot be blank")
            if point_id in seen:
                raise ValueError(f"Row {row_number}: duplicate point_id {point_id!r}")
            seen.add(point_id)
            record: dict[str, float | str] = {"point_id": point_id}
            for field in REQUIRED[1:]:
                record[field] = _number(row.get(field, ""), field, row_number)
            records.append(record)
    if not records:
        raise ValueError("CSV contains no checkpoint observations")
    return records


def _rmse(values: Iterable[float]) -> float:
    values = list(values)
    return math.sqrt(sum(value * value for value in values) / len(values))


def _bias(values: list[float]) -> float:
    return sum(values) / len(values)


def assess_checkpoints(records: list[dict[str, float | str]]) -> dict:
    if not records:
        raise ValueError("At least one checkpoint is required")
    residuals = []
    for record in records:
        dx = float(record["model_x"]) - float(record["ref_x"])
        dy = float(record["model_y"]) - float(record["ref_y"])
        dz = float(record["model_z"]) - float(record["ref_z"])
        residuals.append({"point_id": str(record["point_id"]), "dx": dx, "dy": dy, "dz": dz,
                          "horizontal_radial": math.hypot(dx, dy)})
    dxs = [r["dx"] for r in residuals]
    dys = [r["dy"] for r in residuals]
    dzs = [r["dz"] for r in residuals]
    radial = sorted(r["horizontal_radial"] for r in residuals)
    # Linear interpolation, equivalent to the common inclusive (n-1) quantile definition.
    def quantile(values: list[float], q: float) -> float:
        if len(values) == 1:
            return values[0]
        position = (len(values) - 1) * q
        lower = math.floor(position)
        upper = math.ceil(position)
        fraction = position - lower
        return values[lower] * (1 - fraction) + values[upper] * fraction

    return {
        "n": len(records),
        "residual_convention": "model minus reference",
        "coordinate_units": "same units as input CSV; not inferred",
        "component_bias": {"x": _bias(dxs), "y": _bias(dys), "z": _bias(dzs)},
        "component_rmse": {"x": _rmse(dxs), "y": _rmse(dys), "z": _rmse(dzs)},
        "horizontal_rmse_2d": math.sqrt((_rmse(dxs) ** 2 + _rmse(dys) ** 2)),
        "vertical_rmse_1d": _rmse(dzs),
        "horizontal_radial_error": {
            "median": median(radial),
            "p95_descriptive": quantile(radial, 0.95),
            "maximum": max(radial),
        },
        "point_residuals": residuals,
        "interpretation_note": (
            "Descriptive statistics for the supplied independent checkpoints only. "
            "The radial P95 is not automatically CE95 or a confidence bound. "
            "No CRS transformation, reference-uncertainty propagation, sampling-design "
            "assessment, outlier deletion or standards-compliance decision is performed."
        ),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Compute transparent residual statistics for independent 3D checkpoints."
    )
    parser.add_argument("csv_file", type=Path, help="CSV with ref_x/ref_y/ref_z and model_x/model_y/model_z")
    parser.add_argument("--json-out", type=Path, help="Optional path for a JSON report")
    args = parser.parse_args(argv)
    try:
        report = assess_checkpoints(read_checkpoints(args.csv_file))
    except (OSError, ValueError) as exc:
        parser.error(str(exc))
    rendered = json.dumps(report, indent=2, sort_keys=True)
    print(rendered)
    if args.json_out:
        args.json_out.write_text(rendered + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
