"""Univariate mean-shift detectors; dependency-free Python teaching baselines."""
from __future__ import annotations

from math import isfinite
from typing import Iterable


def _series(values: Iterable[float]) -> list[float]:
    x = [float(v) for v in values]
    if len(x) < 2 or any(not isfinite(v) for v in x):
        raise ValueError("values must contain at least two finite numbers")
    return x


def _prefix(x: list[float]) -> tuple[list[float], list[float]]:
    s, q = [0.0], [0.0]
    for v in x:
        s.append(s[-1] + v)
        q.append(q[-1] + v * v)
    return s, q


def _sse(s: list[float], q: list[float], a: int, b: int) -> float:
    n = b - a
    total = s[b] - s[a]
    return max(0.0, q[b] - q[a] - total * total / n)


def cusum(values: Iterable[float], *, target: float | None = None,
          threshold: float, drift: float = 0.0) -> list[int]:
    """Return 0-based indices flagged by a two-sided tabular CUSUM.

    The reference target defaults to the sample mean. Threshold and drift are
    expressed in the original data units; this is a detector, not a calibrated
    false-alarm guarantee. The returned index is the first observation in the
    run that crossed the threshold.
    """
    x = _series(values)
    if not isfinite(threshold) or threshold <= 0 or not isfinite(drift) or drift < 0:
        raise ValueError("threshold must be positive and drift non-negative")
    mu = sum(x) / len(x) if target is None else float(target)
    if not isfinite(mu):
        raise ValueError("target must be finite")
    pos = neg = 0.0
    out: list[int] = []
    for i, v in enumerate(x):
        pos = max(0.0, pos + v - mu - drift)
        neg = max(0.0, neg + mu - v - drift)
        if pos >= threshold or neg >= threshold:
            out.append(i)
            pos = neg = 0.0
    return out


def binary_segmentation(values: Iterable[float], *, max_changes: int,
                        min_size: int = 2, penalty: float = 0.0) -> list[int]:
    """Greedy binary segmentation for piecewise-constant means under SSE loss.

    Returns sorted 0-based split positions (the first sample of each new
    segment). This is a greedy approximation to the global penalized optimum.
    """
    x = _series(values)
    n = len(x)
    if not isinstance(max_changes, int) or isinstance(max_changes, bool) or max_changes < 0:
        raise ValueError("max_changes must be a non-negative integer")
    if not isinstance(min_size, int) or isinstance(min_size, bool) or min_size < 1:
        raise ValueError("min_size must be a positive integer")
    if not isfinite(penalty) or penalty < 0:
        raise ValueError("penalty must be finite and non-negative")
    s, q = _prefix(x)
    segments = [(0, n)]
    cuts: list[int] = []
    while len(cuts) < max_changes:
        best_gain, best_split, best_segment = penalty, None, None
        for a, b in segments:
            if b - a < 2 * min_size:
                continue
            parent = _sse(s, q, a, b)
            for t in range(a + min_size, b - min_size + 1):
                gain = parent - _sse(s, q, a, t) - _sse(s, q, t, b)
                if gain > best_gain:
                    best_gain, best_split, best_segment = gain, t, (a, b)
        if best_split is None or best_segment is None:
            break
        segments.remove(best_segment)
        segments.extend([(best_segment[0], best_split), (best_split, best_segment[1])])
        cuts.append(best_split)
    return sorted(cuts)


def pelt(values: Iterable[float], *, penalty: float, min_size: int = 2) -> list[int]:
    """PELT for piecewise-constant means with squared-error segment cost.

    Uses K=0 pruning for min_size=1. For min_size>1, uses exact unpruned
    dynamic programming because naive pruning can violate the minimum-length
    constraint. No automatic penalty calibration or false-alarm guarantee is implied.
    """
    x = _series(values)
    n = len(x)
    if not isfinite(penalty) or penalty < 0:
        raise ValueError("penalty must be finite and non-negative")
    if not isinstance(min_size, int) or isinstance(min_size, bool) or min_size < 1:
        raise ValueError("min_size must be a positive integer")
    s, q = _prefix(x)
    inf = float("inf")
    best = [inf] * (n + 1)
    previous = [-1] * (n + 1)
    best[0] = -penalty
    candidates = [0]
    for end in range(min_size, n + 1):
        eligible = [start for start in candidates if end - start >= min_size and best[start] < inf]
        if not eligible:
            continue
        costs = [(best[start] + _sse(s, q, start, end) + penalty, start)
                 for start in eligible]
        best[end], previous[end] = min(costs)
        # K=0 pruning: a start that cannot beat the current optimum is removed.
        if min_size == 1:
            candidates = [start for start in eligible
                          if best[start] + _sse(s, q, start, end) < best[end]]
        # With min_size > 1, retain all starts: pruning can discard a candidate
        # that is temporarily too close to the current end to form a legal
        # future segment. The constrained case therefore uses exact unpruned DP.
        if best[end] < inf:
            candidates.append(end)
    if previous[n] < 0:
        raise ValueError("series cannot be segmented with the requested min_size")
    cuts: list[int] = []
    end = n
    while end > 0:
        start = previous[end]
        if start < 0:
            raise RuntimeError("broken backpointer in optimal partition")
        if start:
            cuts.append(start)
        end = start
    return sorted(cuts)
