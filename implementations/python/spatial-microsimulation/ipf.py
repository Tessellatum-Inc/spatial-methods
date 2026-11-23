"""Iterative proportional fitting for contingency tables."""
import numpy as np


def iterative_proportional_fit(seed, margins, *, tolerance=1e-9, max_iterations=10000):
    """Rake a nonnegative 2D seed table to row and column marginal totals.

    margins must contain axis 0 (row totals) and axis 1 (column totals).
    Structural zeros in the seed remain zero. Returns the fitted table and
    convergence diagnostics rather than silently claiming convergence.
    """
    table = np.asarray(seed, dtype=float)
    if table.ndim != 2 or min(table.shape) < 1 or not np.isfinite(table).all() or np.any(table < 0):
        raise ValueError("seed must be a finite nonnegative 2D array")
    if not isinstance(margins, dict) or set(margins) != {0, 1}:
        raise ValueError("margins must provide exactly axes 0 and 1")
    targets = []
    for axis, size in ((0, table.shape[0]), (1, table.shape[1])):
        target = np.asarray(margins[axis], dtype=float)
        if target.shape != (size,) or not np.isfinite(target).all() or np.any(target < 0):
            raise ValueError(f"axis {axis} margins must be finite nonnegative values of length {size}")
        targets.append(target)
    row_target, col_target = targets
    total = float(row_target.sum())
    if not np.isclose(total, float(col_target.sum()), rtol=1e-10, atol=1e-12):
        raise ValueError("row and column margins must have equal grand totals")
    if isinstance(tolerance, bool) or not isinstance(tolerance, (int, float)) or not np.isfinite(tolerance) or tolerance <= 0:
        raise ValueError("tolerance must be finite and positive")
    if isinstance(max_iterations, bool) or not isinstance(max_iterations, int) or max_iterations < 1:
        raise ValueError("max_iterations must be a positive integer")
    if total == 0:
        return {"fitted": np.zeros_like(table).tolist(), "row_totals": row_target.tolist(),
                "column_totals": col_target.tolist(), "iterations": 0,
                "converged": True, "max_abs_error": 0.0}

    fitted = table.copy()
    for axis, target in ((0, row_target), (1, col_target)):
        support = np.sum(fitted, axis=1-axis)
        if np.any((target > 0) & (support == 0)):
            raise ValueError(f"positive axis {axis} target has no positive seed support")

    converged = False
    error = float("inf")
    for iteration in range(1, max_iterations + 1):
        for axis, target in ((0, row_target), (1, col_target)):
            current = fitted.sum(axis=1-axis)
            factors = np.divide(target, current, out=np.zeros_like(target), where=current > 0)
            if np.any((target > 0) & (current == 0)):
                raise ValueError(f"positive axis {axis} margin became unsupported")
            fitted *= factors[:, None] if axis == 0 else factors[None, :]
        row_error = np.max(np.abs(fitted.sum(axis=1) - row_target))
        col_error = np.max(np.abs(fitted.sum(axis=0) - col_target))
        error = float(max(row_error, col_error))
        if error <= float(tolerance) * max(total, 1.0):
            converged = True
            break
    return {"fitted": fitted.tolist(), "row_totals": fitted.sum(axis=1).tolist(),
            "column_totals": fitted.sum(axis=0).tolist(), "iterations": iteration,
            "converged": converged, "max_abs_error": error}
