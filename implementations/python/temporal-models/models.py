"""Small dependency-free temporal-analysis teaching implementations."""
from __future__ import annotations
from math import exp, isfinite, log
from statistics import median
from typing import Iterable, Sequence


def _finite(values: Iterable[float], minimum: int = 2) -> list[float]:
    x = [float(v) for v in values]
    if len(x) < minimum or any(not isfinite(v) for v in x):
        raise ValueError(f"values must contain at least {minimum} finite numbers")
    return x


def theil_sen(x: Iterable[float], y: Iterable[float]) -> tuple[float, float]:
    """Return median pairwise slope and median intercept for distinct x values."""
    xs, ys = _finite(x), _finite(y)
    if len(xs) != len(ys):
        raise ValueError("x and y must have equal length")
    slopes = [(ys[j] - ys[i]) / (xs[j] - xs[i])
              for i in range(len(xs)) for j in range(i + 1, len(xs))
              if xs[j] != xs[i]]
    if not slopes:
        raise ValueError("x must contain at least two distinct values")
    slope = median(slopes)
    intercept = median([yv - slope * xv for xv, yv in zip(xs, ys)])
    return slope, intercept


def pettitt(values: Iterable[float]) -> tuple[int, float, float]:
    """Return (split index, |U|max, approximate p-value) for one rank change.

    The split index is the first observation of the later segment. The
    exponential p-value is an approximation; ties use average ranks.
    """
    x = _finite(values)
    ordered = sorted((v, i) for i, v in enumerate(x))
    ranks = [0.0] * len(x)
    k = 0
    while k < len(ordered):
        j = k + 1
        while j < len(ordered) and ordered[j][0] == ordered[k][0]:
            j += 1
        rank = ((k + 1) + j) / 2.0
        for _, idx in ordered[k:j]:
            ranks[idx] = rank
        k = j
    running = 0.0
    best_abs, best_t = -1.0, 1
    n = len(x)
    for t in range(1, n):
        running += ranks[t - 1]
        statistic = 2.0 * running - t * (n + 1)
        if abs(statistic) > best_abs:
            best_abs, best_t = abs(statistic), t
    p_value = min(1.0, 2.0 * exp((-6.0 * best_abs * best_abs) / (n**3 + n**2)))
    return best_t, best_abs, p_value


def viterbi(observations: Sequence[int], start_prob: Sequence[float],
            transition: Sequence[Sequence[float]],
            emission: Sequence[Sequence[float]]) -> tuple[list[int], float]:
    """Decode the maximum-probability hidden-state path in log space.

    emission[state][observation_symbol] supplies discrete emission
    probabilities. Rows must be valid probability distributions. Returns the
    state-index path and its log probability; ties resolve to the lowest index.
    """
    if not observations:
        raise ValueError("observations must not be empty")
    states = len(start_prob)
    if states == 0 or len(transition) != states or len(emission) != states:
        raise ValueError("start, transition and emission dimensions must agree")
    symbols = len(emission[0])
    if symbols == 0 or any(len(row) != symbols for row in emission):
        raise ValueError("emission rows must have equal non-zero length")
    if any(len(row) != states for row in transition):
        raise ValueError("transition matrix must be square")
    def valid_row(row):
        return all(isfinite(p) and p >= 0 for p in row) and abs(sum(row) - 1.0) <= 1e-8
    if not valid_row(start_prob) or not all(valid_row(row) for row in transition) or not all(valid_row(row) for row in emission):
        raise ValueError("probability rows must be finite, non-negative and sum to one")
    if any(not isinstance(o, int) or isinstance(o, bool) or o < 0 or o >= symbols for o in observations):
        raise ValueError("observation symbols must be valid non-negative integer indices")
    neg_inf = float("-inf")
    logp = lambda p: log(p) if p > 0 else neg_inf
    scores = [logp(start_prob[s]) + logp(emission[s][observations[0]]) for s in range(states)]
    back = []
    for obs in observations[1:]:
        next_scores, pointers = [], []
        for dest in range(states):
            candidates = [scores[src] + logp(transition[src][dest]) for src in range(states)]
            src = max(range(states), key=lambda i: candidates[i])
            next_scores.append(candidates[src] + logp(emission[dest][obs]))
            pointers.append(src)
        scores, back = next_scores, back + [pointers]
    state = max(range(states), key=lambda i: scores[i])
    best_logp = scores[state]
    path = [state]
    for pointers in reversed(back):
        state = pointers[state]
        path.append(state)
    path.reverse()
    if best_logp == neg_inf:
        raise ValueError("no valid state path has positive probability")
    return path, best_logp
