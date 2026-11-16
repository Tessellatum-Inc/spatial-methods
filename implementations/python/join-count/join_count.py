"""Binary join-count statistics with conditional randomisation inference."""
from __future__ import annotations
from dataclasses import dataclass
import random
from math import isfinite
from typing import Sequence


@dataclass(frozen=True)
class JoinCountResult:
    observed: tuple[int, int, int]
    expected: tuple[float, float, float]
    p_upper: tuple[float, float, float]
    p_lower: tuple[float, float, float]
    n_edges: int
    n_black: int
    n_white: int


def _validate(labels, weights):
    raw = list(labels)
    n = len(raw)
    if n < 2:
        raise ValueError("at least two binary labels are required")
    clean_labels = []
    for value in raw:
        if isinstance(value, bool):
            clean_labels.append(int(value))
            continue
        try:
            number = float(value)
        except (TypeError, ValueError):
            raise ValueError("labels must contain only binary 0/1 values") from None
        if not isfinite(number) or number not in (0.0, 1.0):
            raise ValueError("labels must contain only binary 0/1 values")
        clean_labels.append(int(number))
    if len(weights) != n:
        raise ValueError("weights must have one row per label")
    matrix = []
    for i, row in enumerate(weights):
        if len(row) != n:
            raise ValueError("weights must be a square n-by-n matrix")
        clean = []
        for j, raw_weight in enumerate(row):
            try:
                value = float(raw_weight)
            except (TypeError, ValueError):
                raise ValueError("weights must be finite and binary") from None
            if not isfinite(value) or value not in (0.0, 1.0):
                raise ValueError("weights must be finite and binary")
            if i == j and value != 0:
                raise ValueError("weights must have a zero diagonal")
            clean.append(int(value))
        matrix.append(clean)
    for i in range(n):
        for j in range(i + 1, n):
            if matrix[i][j] != matrix[j][i]:
                raise ValueError("weights must be symmetric and undirected")
    edges = [(i, j) for i in range(n) for j in range(i + 1, n) if matrix[i][j]]
    if not edges:
        raise ValueError("weights must contain at least one undirected edge")
    return clean_labels, edges


def _counts(labels, edges):
    black_black = white_white = black_white = 0
    for i, j in edges:
        a, b = labels[i], labels[j]
        if a == b == 1:
            black_black += 1
        elif a == b == 0:
            white_white += 1
        else:
            black_white += 1
    return black_black, white_white, black_white


def join_count_test(
    labels: Sequence[int],
    weights: Sequence[Sequence[int]],
    *,
    permutations: int = 999,
    seed: int | None = 0,
) -> JoinCountResult:
    """Compute BB, WW and BW joins and conditional permutation p-values.

    The undirected binary weights matrix is counted once per edge (i < j).
    Randomisation holds the graph and the number of black/white labels fixed,
    shuffling labels across vertices without replacement. p_upper and p_lower
    are one-sided plus-one Monte Carlo tail estimates for unusually many or
    few joins of each type. They are not multiplicity-adjusted.
    """
    values, edges = _validate(labels, weights)
    if isinstance(permutations, bool) or not isinstance(permutations, int) or permutations < 0:
        raise ValueError("permutations must be a non-negative integer")
    observed = _counts(values, edges)
    n = len(values)
    black = sum(values)
    white = n - black
    m = len(edges)
    expected = (
        m * black * (black - 1) / (n * (n - 1)),
        m * white * (white - 1) / (n * (n - 1)),
        m * 2 * black * white / (n * (n - 1)),
    )
    if permutations == 0:
        return JoinCountResult(observed, expected, (1.0, 1.0, 1.0),
                               (1.0, 1.0, 1.0), m, black, white)
    rng = random.Random(seed)
    simulated = [[], [], []]
    shuffled = values[:]
    for _ in range(permutations):
        shuffled = values[:]
        rng.shuffle(shuffled)
        counts = _counts(shuffled, edges)
        for k, value in enumerate(counts):
            simulated[k].append(value)
    upper = tuple((sum(value >= observed[k] for value in simulated[k]) + 1)
                  / (permutations + 1) for k in range(3))
    lower = tuple((sum(value <= observed[k] for value in simulated[k]) + 1)
                  / (permutations + 1) for k in range(3))
    return JoinCountResult(observed, expected, upper, lower, m, black, white)
