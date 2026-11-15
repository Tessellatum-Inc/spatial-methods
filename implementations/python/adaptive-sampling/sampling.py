"""Greedy spatial active-learning and multi-armed bandit teaching baselines."""
from __future__ import annotations
from math import exp, isfinite, log, sqrt
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


def gp_select_next(observed_x: Sequence[Sequence[float]], observed_y: Sequence[float],
                   candidates: Sequence[Sequence[float]], *,
                   length_scale: float = 1.0, signal_variance: float = 1.0,
                   noise: float = 1e-6, beta: float = 2.0,
                   acquisition: str = "ucb") -> tuple[int, list[float], list[float]]:
    """Select a finite candidate using an RBF Gaussian-process posterior.

    Returns (candidate_index, posterior_means, posterior_standard_deviations).
    Maximizes the latent function. Acquisition is 'ucb' or 'ei'. This is a
    small dense exact-GP baseline: O(n^3 + m*n^2), not a scalable GP system.
    """
    from math import erf, pi
    X = [tuple(float(v) for v in row) for row in observed_x]
    C = [tuple(float(v) for v in row) for row in candidates]
    y = [float(v) for v in observed_y]
    if not X or len(X) != len(y) or not C:
        raise ValueError("observations and candidates must be non-empty and aligned")
    dim = len(X[0])
    if dim == 0 or any(len(row) != dim for row in X + C):
        raise ValueError("all coordinate vectors must have the same non-zero dimension")
    if any(not isfinite(v) for row in X + C for v in row) or any(not isfinite(v) for v in y):
        raise ValueError("coordinates and observations must be finite")
    if not isfinite(length_scale) or length_scale <= 0 or not isfinite(signal_variance) or signal_variance <= 0:
        raise ValueError("length_scale and signal_variance must be positive and finite")
    if not isfinite(noise) or noise < 0 or not isfinite(beta) or beta < 0:
        raise ValueError("noise and beta must be finite and non-negative")
    if acquisition not in ("ucb", "ei"):
        raise ValueError("acquisition must be 'ucb' or 'ei'")

    def kernel(a, b):
        squared = sum((u-v)**2 for u, v in zip(a, b))
        return signal_variance * exp(-0.5 * squared / (length_scale**2))

    # Cholesky factorization of K(X,X) + noise*I with adaptive numerical jitter.
    n = len(X)
    K = [[kernel(X[i], X[j]) + (noise if i == j else 0.0)
          for j in range(n)] for i in range(n)]
    L = [[0.0] * n for _ in range(n)]
    jitter = 1e-12
    for attempt in range(8):
        try:
            for i in range(n):
                for j in range(i + 1):
                    value = K[i][j] + (jitter if i == j else 0.0)
                    value -= sum(L[i][k] * L[j][k] for k in range(j))
                    if i == j:
                        if value <= 0:
                            raise ArithmeticError("kernel matrix is not positive definite")
                        L[i][j] = sqrt(value)
                    else:
                        L[i][j] = value / L[j][j]
            break
        except ArithmeticError:
            jitter *= 10.0
            L = [[0.0] * n for _ in range(n)]
    else:
        raise ValueError("could not stabilize Gaussian-process covariance matrix")

    # Solve K^-1 y via forward/back substitution.
    z = [0.0] * n
    for i in range(n):
        z[i] = (y[i] - sum(L[i][j] * z[j] for j in range(i))) / L[i][i]
    alpha = [0.0] * n
    for i in range(n - 1, -1, -1):
        alpha[i] = (z[i] - sum(L[j][i] * alpha[j] for j in range(i + 1, n))) / L[i][i]

    means, stds, acquisitions = [], [], []
    best_observed = max(y)
    normal_cdf = lambda value: 0.5 * (1.0 + erf(value / sqrt(2.0)))
    normal_pdf = lambda value: exp(-0.5 * value * value) / sqrt(2.0 * pi)
    for point in C:
        k = [kernel(row, point) for row in X]
        mean = sum(k[i] * alpha[i] for i in range(n))
        v = [0.0] * n
        for i in range(n):
            v[i] = (k[i] - sum(L[i][j] * v[j] for j in range(i))) / L[i][i]
        variance = max(0.0, signal_variance - sum(value * value for value in v))
        std = sqrt(variance)
        if acquisition == "ucb":
            score = mean + beta * std
        elif std <= 1e-12:
            score = max(0.0, mean - best_observed)
        else:
            improvement = mean - best_observed
            zscore = improvement / std
            score = improvement * normal_cdf(zscore) + std * normal_pdf(zscore)
        means.append(mean)
        stds.append(std)
        acquisitions.append(score)
    return max(range(len(C)), key=lambda i: (acquisitions[i], -i)), means, stds
