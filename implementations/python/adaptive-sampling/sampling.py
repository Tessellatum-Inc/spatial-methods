"""Greedy spatial active-learning and multi-armed bandit teaching baselines."""
from __future__ import annotations
from math import isfinite, log, sqrt
from typing import Sequence


def select_spatial_batch(points: Sequence[Sequence[float]],
                         uncertainty: Sequence[float], batch_size: int, *,
                         selected: Sequence[int] = (), diversity_weight: float = 1.0,
                         min_distance: float = 0.0) -> list[int]:
    """Greedily select uncertain, spatially diverse candidate indices.

    Score = normalized uncertainty + diversity_weight * normalized distance
    to the nearest already-selected point. If no point is selected initially,
    the first choice is the highest-uncertainty candidate. Ties use input order.
    """
    coords = [tuple(float(v) for v in p) for p in points]
    if not coords or any(not p or any(not isfinite(v) for v in p) for p in coords):
        raise ValueError("points must be non-empty finite coordinate vectors")
    dim = len(coords[0])
    if any(len(p) != dim for p in coords):
        raise ValueError("all points must have the same dimension")
    u = [float(v) for v in uncertainty]
    if len(u) != len(coords) or any(not isfinite(v) or v < 0 for v in u):
        raise ValueError("uncertainty must be finite, non-negative and match points")
    if not isinstance(batch_size, int) or isinstance(batch_size, bool) or not 0 <= batch_size <= len(coords):
        raise ValueError("batch_size must be an integer between zero and candidate count")
    if not isfinite(diversity_weight) or diversity_weight < 0:
        raise ValueError("diversity_weight must be finite and non-negative")
    if not isfinite(min_distance) or min_distance < 0:
        raise ValueError("min_distance must be finite and non-negative")
    chosen = list(selected)
    if len(set(chosen)) != len(chosen) or any(not isinstance(i, int) or isinstance(i, bool) or not 0 <= i < len(coords) for i in chosen):
        raise ValueError("selected indices must be unique valid integers")
    if len(chosen) + batch_size > len(coords):
        raise ValueError("selected plus batch_size exceeds candidate count")
    remaining = set(range(len(coords))) - set(chosen)
    max_u = max(u) or 1.0
    def distance(i, j):
        return sqrt(sum((a-b)**2 for a,b in zip(coords[i], coords[j])))
    output = []
    while len(output) < batch_size:
        if chosen:
            distances = {i: min(distance(i, j) for j in chosen) for i in remaining}
            scale = max(distances.values()) or 1.0
        else:
            distances, scale = {}, 1.0
        scored = []
        for i in remaining:
            dscore = distances[i] / scale if chosen else 0.0
            score = u[i] / max_u + diversity_weight * dscore
            if chosen and distances[i] < min_distance:
                continue
            scored.append((score, -i, i))
        if not scored:
            break
        pick = max(scored)[2]
        output.append(pick)
        chosen.append(pick)
        remaining.remove(pick)
    return output


def ucb1_arm(counts: Sequence[int], rewards: Sequence[float]) -> int:
    """Return the next arm under UCB1; rewards are cumulative observed rewards.

    Untried arms are selected first in ascending index order. Once every arm
    has been tried, maximize mean_reward + sqrt(2 ln(total_pulls)/arm_pulls).
    """
    if not counts or len(counts) != len(rewards):
        raise ValueError("counts and rewards must have equal non-zero length")
    if any(not isinstance(n, int) or isinstance(n, bool) or n < 0 for n in counts):
        raise ValueError("counts must be non-negative integers")
    if any(not isfinite(float(r)) for r in rewards):
        raise ValueError("rewards must be finite")
    for i, n in enumerate(counts):
        if n == 0:
            return i
    total = sum(counts)
    scores = [float(rewards[i]) / counts[i] + sqrt(2.0 * log(total) / counts[i])
              for i in range(len(counts))]
    return max(range(len(scores)), key=lambda i: (scores[i], -i))
