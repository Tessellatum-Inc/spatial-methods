"""Tukey median polish for robust two-way additive decomposition."""
from __future__ import annotations
from math import fsum, isfinite
from numbers import Integral
from statistics import median


def _as_table(values, na_rm):
    try:
        rows = [list(row) for row in values]
    except TypeError as exc:
        raise ValueError("values must be a non-empty rectangular table") from exc
    if not rows or not rows[0]:
        raise ValueError("values must be a non-empty rectangular table")
    ncols = len(rows[0])
    if any(len(row) != ncols for row in rows):
        raise ValueError("all rows must have equal length")
    table, missing = [], False
    for row in rows:
        converted = []
        for value in row:
            if value is None:
                converted.append(None)
                missing = True
                continue
            try:
                number = float(value)
            except (TypeError, ValueError) as exc:
                raise ValueError("table values must be numeric or missing") from exc
            if number != number:
                converted.append(None)
                missing = True
            elif not isfinite(number):
                raise ValueError("infinite table values are not supported")
            else:
                converted.append(number)
        table.append(converted)
    if missing and not na_rm:
        raise ValueError("missing values require na_rm=True")
    observed = [value for row in table for value in row if value is not None]
    if not observed:
        raise ValueError("at least one observed table value is required")
    return table, observed


def _median(values):
    return median(values) if values else 0.0


def median_polish(values, *, eps=0.01, max_iterations=10, na_rm=False):
    """Fit overall + row effects + column effects using Tukey median polish.

    Missing cells may be ignored with na_rm=True. Effects for all-missing rows
    or columns are zero. Convergence follows the proportional reduction in
    the sum of absolute residuals used by R stats::medpolish.
    """
    if isinstance(eps, bool):
        raise ValueError("eps must be finite and positive")
    try:
        eps = float(eps)
    except (TypeError, ValueError) as exc:
        raise ValueError("eps must be finite and positive") from exc
    if not isfinite(eps) or eps <= 0:
        raise ValueError("eps must be finite and positive")
    if isinstance(max_iterations, bool) or not isinstance(max_iterations, Integral) or max_iterations < 1:
        raise ValueError("max_iterations must be a positive integer")
    if not isinstance(na_rm, bool):
        raise ValueError("na_rm must be boolean")

    table, observed = _as_table(values, na_rm)
    nrows, ncols = len(table), len(table[0])
    row_active = [any(value is not None for value in row) for row in table]
    col_active = [any(table[i][j] is not None for i in range(nrows)) for j in range(ncols)]
    overall = median(observed)
    residuals = [
        [None if value is None else value - overall for value in row]
        for row in table
    ]
    row_effects = [0.0] * nrows
    col_effects = [0.0] * ncols
    history = [fsum(abs(value) for row in residuals for value in row if value is not None)]
    converged = history[-1] == 0.0
    iterations = 0

    for iteration in range(1, int(max_iterations) + 1):
        for i, row in enumerate(residuals):
            if not row_active[i]:
                continue
            shift = _median([value for value in row if value is not None])
            row_effects[i] += shift
            residuals[i] = [None if value is None else value - shift for value in row]

        for j in range(ncols):
            if not col_active[j]:
                continue
            shift = _median([
                residuals[i][j] for i in range(nrows)
                if residuals[i][j] is not None
            ])
            col_effects[j] += shift
            for i in range(nrows):
                if residuals[i][j] is not None:
                    residuals[i][j] -= shift

        row_shift = _median([row_effects[i] for i in range(nrows) if row_active[i]])
        row_effects = [
            value - row_shift if row_active[i] else 0.0
            for i, value in enumerate(row_effects)
        ]
        overall += row_shift

        col_shift = _median([col_effects[j] for j in range(ncols) if col_active[j]])
        col_effects = [
            value - col_shift if col_active[j] else 0.0
            for j, value in enumerate(col_effects)
        ]
        overall += col_shift

        residual_sum = fsum(abs(value) for row in residuals for value in row if value is not None)
        history.append(residual_sum)
        iterations = iteration
        previous = history[-2]
        if previous == 0.0 or (previous - residual_sum) / previous < eps:
            converged = True
            break

    fitted = [
        [overall + row_effects[i] + col_effects[j] for j in range(ncols)]
        for i in range(nrows)
    ]
    return {
        "overall": overall,
        "row_effects": row_effects,
        "column_effects": col_effects,
        "fitted": fitted,
        "residuals": residuals,
        "iterations": iterations,
        "converged": converged,
        "residual_sum_history": history,
    }
