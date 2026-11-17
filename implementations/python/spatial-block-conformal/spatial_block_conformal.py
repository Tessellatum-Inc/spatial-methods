"""Block-level split conformal prediction intervals.

The calibration unit is a caller-defined spatial block. Each block contributes
its maximum absolute (optionally scale-normalised) calibration residual.
"""
from __future__ import annotations

from dataclasses import dataclass
from math import ceil
from typing import Hashable

import numpy as np


@dataclass(frozen=True)
class BlockConformalCalibration:
    """Finite-sample calibration summary for exchangeable spatial blocks."""

    alpha: float
    quantile: float
    rank: int
    n_observations: int
    n_blocks: int
    block_scores: tuple[float, ...]


def _vector(values: object, name: str, *, dtype: object = float) -> np.ndarray:
    array = np.asarray(values, dtype=dtype)
    if array.ndim != 1 or array.size == 0:
        raise ValueError(f"{name} must be a non-empty one-dimensional array")
    return array


def _positive_scale(scale: object | None, n: int, name: str) -> np.ndarray:
    if scale is None:
        return np.ones(n, dtype=float)
    result = _vector(scale, name)
    if result.size != n:
        raise ValueError(f"{name} must have the same length as predictions")
    if not np.all(np.isfinite(result)) or np.any(result <= 0):
        raise ValueError(f"{name} must contain finite, strictly positive values")
    return result


def calibrate_spatial_blocks(
    y_true: object,
    y_pred: object,
    block_ids: object,
    *,
    alpha: float = 0.1,
    scale: object | None = None,
) -> BlockConformalCalibration:
    """Calibrate a two-sided interval using one maximum score per spatial block.

    Scores are |y - prediction| / scale. The scale is optional and must be
    supplied for both calibration and prediction when using locally adaptive
    (normalised) intervals. The finite-sample order statistic uses
    ceil((B + 1) * (1 - alpha)); if that rank exceeds B, the quantile is +inf.
    """
    truth = _vector(y_true, "y_true")
    prediction = _vector(y_pred, "y_pred")
    labels = _vector(block_ids, "block_ids", dtype=object)
    if truth.size != prediction.size or truth.size != labels.size:
        raise ValueError("y_true, y_pred and block_ids must have equal lengths")
    if not np.all(np.isfinite(truth)) or not np.all(np.isfinite(prediction)):
        raise ValueError("y_true and y_pred must contain only finite values")
    if not np.isfinite(alpha) or not 0 < alpha < 1:
        raise ValueError("alpha must be strictly between zero and one")

    normalizer = _positive_scale(scale, truth.size, "scale")
    scores = np.abs(truth - prediction) / normalizer

    # Dict insertion order makes the returned block-score order deterministic.
    grouped: dict[Hashable, list[float]] = {}
    for label, score in zip(labels.tolist(), scores.tolist()):
        try:
            hash(label)
        except TypeError as exc:
            raise ValueError("block_ids must contain hashable scalar labels") from exc
        if label is None:
            raise ValueError("block_ids must not contain missing labels")
        grouped.setdefault(label, []).append(float(score))

    block_scores = tuple(max(values) for values in grouped.values())
    n_blocks = len(block_scores)
    rank = ceil((n_blocks + 1) * (1.0 - alpha))
    ordered = sorted(block_scores)
    quantile = float(ordered[rank - 1]) if rank <= n_blocks else float("inf")
    return BlockConformalCalibration(
        alpha=float(alpha),
        quantile=quantile,
        rank=rank,
        n_observations=int(truth.size),
        n_blocks=n_blocks,
        block_scores=block_scores,
    )


def spatial_block_interval(
    y_pred: object,
    calibration: BlockConformalCalibration,
    *,
    scale: object | None = None,
) -> tuple[np.ndarray, np.ndarray]:
    """Return lower and upper prediction bounds for new observations."""
    if not isinstance(calibration, BlockConformalCalibration):
        raise TypeError("calibration must be a BlockConformalCalibration")
    prediction = _vector(y_pred, "y_pred")
    if not np.all(np.isfinite(prediction)):
        raise ValueError("y_pred must contain only finite values")
    normalizer = _positive_scale(scale, prediction.size, "scale")
    half_width = calibration.quantile * normalizer
    return prediction - half_width, prediction + half_width
