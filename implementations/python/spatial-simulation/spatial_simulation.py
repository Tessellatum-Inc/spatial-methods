"""Small, explicit spatial cellular-automata and Schelling model baselines."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import numpy as np
from numpy.typing import NDArray


def _validate_grid(grid: NDArray, *, binary: bool = False) -> NDArray:
    arr = np.asarray(grid)
    if arr.ndim != 2 or min(arr.shape, default=0) < 1:
        raise ValueError("grid must be a non-empty two-dimensional array")
    if not np.issubdtype(arr.dtype, np.integer):
        raise TypeError("grid values must be integers")
    if binary and not np.isin(arr, [0, 1]).all():
        raise ValueError("binary cellular automaton grid must contain only 0 and 1")
    return arr


def _offsets(neighborhood: str) -> tuple[tuple[int, int], ...]:
    if neighborhood == "moore":
        return tuple((dr, dc) for dr in (-1, 0, 1)
                     for dc in (-1, 0, 1) if (dr, dc) != (0, 0))
    if neighborhood == "von_neumann":
        return ((-1, 0), (1, 0), (0, -1), (0, 1))
    raise ValueError("neighborhood must be 'moore' or 'von_neumann'")


def _shift(arr: NDArray, dr: int, dc: int, periodic: bool) -> NDArray:
    if periodic:
        return np.roll(arr, shift=(-dr, -dc), axis=(0, 1))
    out = np.zeros_like(arr)
    rows, cols = arr.shape
    src_r0, src_r1 = max(0, -dr), min(rows, rows - dr)
    src_c0, src_c1 = max(0, -dc), min(cols, cols - dc)
    dst_r0, dst_r1 = max(0, dr), min(rows, rows + dr)
    dst_c0, dst_c1 = max(0, dc), min(cols, cols + dc)
    out[dst_r0:dst_r1, dst_c0:dst_c1] = arr[src_r0:src_r1, src_c0:src_c1]
    return out


def live_neighbor_count(
    grid: NDArray, *, neighborhood: str = "moore", periodic: bool = False
) -> NDArray[np.int64]:
    """Count live (value 1) neighbors for each cell; the center is excluded."""
    arr = _validate_grid(grid, binary=True)
    count = np.zeros(arr.shape, dtype=np.int64)
    for dr, dc in _offsets(neighborhood):
        count += _shift(arr, dr, dc, periodic)
    return count


def life_like_step(
    grid: NDArray,
    *,
    birth: Iterable[int] = (3,),
    survive: Iterable[int] = (2, 3),
    neighborhood: str = "moore",
    periodic: bool = False,
) -> NDArray[np.uint8]:
    """Apply a synchronous binary B/S cellular-automaton update."""
    arr = _validate_grid(grid, binary=True)
    birth_set, survive_set = set(birth), set(survive)
    degree = len(_offsets(neighborhood))
    if any(not isinstance(x, (int, np.integer)) or x < 0 or x > degree
           for x in birth_set | survive_set):
        raise ValueError(f"neighbor counts must be integers from 0 to {degree}")
    neighbors = live_neighbor_count(
        arr, neighborhood=neighborhood, periodic=periodic
    )
    born = (arr == 0) & np.isin(neighbors, tuple(birth_set))
    lives = (arr == 1) & np.isin(neighbors, tuple(survive_set))
    return (born | lives).astype(np.uint8)


def simulate_life_like(
    grid: NDArray,
    steps: int,
    *,
    birth: Iterable[int] = (3,),
    survive: Iterable[int] = (2, 3),
    neighborhood: str = "moore",
    periodic: bool = False,
) -> NDArray[np.uint8]:
    """Run a B/S cellular automaton for a fixed number of synchronous steps."""
    if not isinstance(steps, (int, np.integer)) or steps < 0:
        raise ValueError("steps must be a non-negative integer")
    state = _validate_grid(grid, binary=True).astype(np.uint8, copy=True)
    for _ in range(steps):
        state = life_like_step(
            state, birth=birth, survive=survive,
            neighborhood=neighborhood, periodic=periodic,
        )
    return state


def same_group_share(
    grid: NDArray,
    row: int,
    col: int,
    *,
    neighborhood: str = "moore",
    periodic: bool = False,
) -> float:
    """Return same-group share among occupied neighboring cells.

    A cell with no occupied neighbors has share 1.0 by convention and is
    therefore not classified as unhappy by a positive tolerance.
    """
    arr = _validate_grid(grid)
    if np.any(arr < 0):
        raise ValueError("Schelling group labels must be non-negative")
    if not (0 <= row < arr.shape[0] and 0 <= col < arr.shape[1]):
        raise IndexError("cell coordinates are outside the grid")
    group = arr[row, col]
    if group == 0:
        raise ValueError("share is undefined for an empty cell")
    values = []
    for dr, dc in _offsets(neighborhood):
        rr, cc = row + dr, col + dc
        if periodic:
            rr %= arr.shape[0]
            cc %= arr.shape[1]
        elif not (0 <= rr < arr.shape[0] and 0 <= cc < arr.shape[1]):
            continue
        value = arr[rr, cc]
        if value != 0:
            values.append(value)
    if not values:
        return 1.0
    return float(np.count_nonzero(np.asarray(values) == group) / len(values))


def schelling_step(
    grid: NDArray,
    *,
    tolerance: float = 0.5,
    neighborhood: str = "moore",
    periodic: bool = False,
    seed: int | None = None,
    max_moves: int | None = None,
) -> tuple[NDArray, int]:
    """Move unhappy agents to distinct cells that were empty at step start.

    Unhappiness is evaluated against the initial state; relocation is then
    processed in a seeded random order. This is a transparent one-pass
    relocation rule, not a claim to reproduce every Schelling variant.
    """
    arr = _validate_grid(grid)
    if np.any(arr < 0):
        raise ValueError("Schelling group labels must be non-negative")
    if not 0.0 <= tolerance <= 1.0:
        raise ValueError("tolerance must be between 0 and 1")
    if max_moves is not None and (
        not isinstance(max_moves, (int, np.integer)) or max_moves < 0
    ):
        raise ValueError("max_moves must be a non-negative integer or None")
    _offsets(neighborhood)  # validate topology before doing any work
    rng = np.random.default_rng(seed)
    unhappy = [
        (r, c) for r in range(arr.shape[0]) for c in range(arr.shape[1])
        if arr[r, c] != 0 and same_group_share(
            arr, r, c, neighborhood=neighborhood, periodic=periodic
        ) < tolerance
    ]
    if not unhappy or max_moves == 0:
        return arr.copy(), 0
    order = rng.permutation(len(unhappy))
    empty = np.argwhere(arr == 0)
    if empty.size == 0:
        return arr.copy(), 0
    empty_order = rng.permutation(len(empty))
    state = arr.copy()
    moves = 0
    limit = len(empty) if max_moves is None else min(max_moves, len(empty))
    for idx, empty_idx in zip(order[:limit], empty_order[:limit]):
        source = unhappy[int(idx)]
        target = tuple(int(x) for x in empty[int(empty_idx)])
        state[target] = state[source]
        state[source] = 0
        moves += 1
    return state, moves


@dataclass(frozen=True)
class SchellingResult:
    grid: NDArray
    moves_per_step: tuple[int, ...]
    converged: bool


def simulate_schelling(
    grid: NDArray,
    *,
    tolerance: float = 0.5,
    max_iterations: int = 100,
    neighborhood: str = "moore",
    periodic: bool = False,
    seed: int | None = None,
) -> SchellingResult:
    """Iterate seeded Schelling relocations until stable or iteration limit."""
    if not isinstance(max_iterations, (int, np.integer)) or max_iterations < 0:
        raise ValueError("max_iterations must be a non-negative integer")
    state = _validate_grid(grid).copy()
    if np.any(state < 0):
        raise ValueError("Schelling group labels must be non-negative")
    if not 0.0 <= tolerance <= 1.0:
        raise ValueError("tolerance must be between 0 and 1")
    rng = np.random.default_rng(seed)
    history: list[int] = []
    for _ in range(max_iterations):
        # Draw a fresh deterministic child seed from the caller's generator.
        child_seed = int(rng.integers(0, np.iinfo(np.int32).max))
        state, moves = schelling_step(
            state, tolerance=tolerance, neighborhood=neighborhood,
            periodic=periodic, seed=child_seed,
        )
        history.append(moves)
        if moves == 0:
            return SchellingResult(state, tuple(history), True)
    return SchellingResult(state, tuple(history), False)


def sample_site_percolation(
    shape: tuple[int, int], probability: float, *, seed: int | None = None
) -> NDArray[np.bool_]:
    """Sample independent occupied sites on a 2D lattice."""
    if (not isinstance(shape, (tuple, list)) or len(shape) != 2
            or any(not isinstance(n, (int, np.integer)) or isinstance(n, bool) or n < 1
                   for n in shape)):
        raise ValueError("shape must contain two positive integers")
    if not 0.0 <= probability <= 1.0:
        raise ValueError("probability must be between 0 and 1")
    return np.random.default_rng(seed).random(shape) < probability


def percolates(
    occupied: NDArray,
    *,
    neighborhood: str = "von_neumann",
) -> bool:
    """Return whether occupied sites connect the top and bottom grid edges."""
    grid = np.asarray(occupied)
    if grid.ndim != 2 or min(grid.shape, default=0) < 1:
        raise ValueError("occupied must be a non-empty two-dimensional array")
    if not np.isin(grid, [False, True, 0, 1]).all():
        raise ValueError("occupied grid must be boolean or binary")
    offsets = _offsets(neighborhood)
    rows, cols = grid.shape
    seen = np.zeros(grid.shape, dtype=bool)
    stack = [(0, c) for c in range(cols) if bool(grid[0, c])]
    for cell in stack:
        seen[cell] = True
    while stack:
        r, c = stack.pop()
        if r == rows - 1:
            return True
        for dr, dc in offsets:
            rr, cc = r + dr, c + dc
            if (0 <= rr < rows and 0 <= cc < cols
                    and bool(grid[rr, cc]) and not seen[rr, cc]):
                seen[rr, cc] = True
                stack.append((rr, cc))
    return False


def forest_fire_step(
    grid: NDArray,
    *,
    growth_probability: float,
    lightning_probability: float,
    neighborhood: str = "von_neumann",
    periodic: bool = False,
    seed: int | None = None,
) -> NDArray[np.uint8]:
    """Advance a stochastic forest-fire cellular automaton synchronously.

    States are 0=empty, 1=tree and 2=burning. Burning cells become empty;
    trees ignite from a burning neighbor or lightning; empty cells grow trees.
    """
    arr = np.asarray(grid)
    if arr.ndim != 2 or min(arr.shape, default=0) < 1:
        raise ValueError("grid must be a non-empty two-dimensional array")
    if not np.issubdtype(arr.dtype, np.integer):
        raise TypeError("forest-fire states must be integers")
    if not np.isin(arr, [0, 1, 2]).all():
        raise ValueError("forest-fire states must be 0, 1 or 2")
    if not 0.0 <= growth_probability <= 1.0:
        raise ValueError("growth_probability must be between 0 and 1")
    if not 0.0 <= lightning_probability <= 1.0:
        raise ValueError("lightning_probability must be between 0 and 1")
    offsets = _offsets(neighborhood)
    burning_neighbors = np.zeros(arr.shape, dtype=np.int64)
    burning = (arr == 2).astype(np.uint8)
    for dr, dc in offsets:
        burning_neighbors += _shift(burning, dr, dc, periodic)
    rng = np.random.default_rng(seed)
    random_values = rng.random(arr.shape)
    result = arr.astype(np.uint8, copy=True)
    result[arr == 2] = 0
    trees = arr == 1
    ignited = trees & (
        (burning_neighbors > 0) | (random_values < lightning_probability)
    )
    result[ignited] = 2
    empty = arr == 0
    result[empty & (random_values < growth_probability)] = 1
    return result


def distance_decay_preferential_attachment(
    coordinates: NDArray,
    *,
    m: int,
    distance_scale: float,
    degree_exponent: float = 1.0,
    seed: int | None = None,
) -> NDArray[np.bool_]:
    """Generate an undirected spatial preferential-attachment graph.

    The first m+1 vertices form a clique. Each later vertex selects m distinct
    earlier vertices with probability proportional to
    degree**degree_exponent * exp(-distance / distance_scale).
    """
    points = np.asarray(coordinates, dtype=float)
    if points.ndim != 2 or points.shape[1] < 1 or points.shape[0] < 2:
        raise ValueError("coordinates must be an n-by-d array with n >= 2")
    if not np.isfinite(points).all():
        raise ValueError("coordinates must be finite")
    n = points.shape[0]
    if not isinstance(m, (int, np.integer)) or isinstance(m, bool) or m < 1 or n < m + 1:
        raise ValueError("m must be a positive integer and n must be at least m+1")
    if not np.isfinite(distance_scale) or distance_scale <= 0:
        raise ValueError("distance_scale must be finite and positive")
    if not np.isfinite(degree_exponent):
        raise ValueError("degree_exponent must be finite")
    rng = np.random.default_rng(seed)
    adjacency = np.zeros((n, n), dtype=bool)
    for i in range(m + 1):
        for j in range(i):
            adjacency[i, j] = adjacency[j, i] = True
    degrees = adjacency.sum(axis=0).astype(float)
    for node in range(m + 1, n):
        distances = np.linalg.norm(points[:node] - points[node], axis=1)
        log_weights = (
            degree_exponent * np.log(np.maximum(degrees[:node], 1.0))
            - distances / distance_scale
        )
        log_weights -= np.max(log_weights)
        weights = np.exp(log_weights)
        total = weights.sum()
        if not np.isfinite(total) or total <= 0:
            raise FloatingPointError("spatial attachment weights are not normalisable")
        probabilities = weights / total
        targets = rng.choice(node, size=m, replace=False, p=probabilities)
        adjacency[node, targets] = True
        adjacency[targets, node] = True
        degrees[node] = m
        degrees[targets] += 1
    return adjacency


def watts_strogatz_graph(
    n: int,
    *,
    k: int,
    beta: float,
    seed: int | None = None,
) -> NDArray[np.bool_]:
    """Generate a Watts-Strogatz small-world graph from a ring lattice."""
    if not isinstance(n, (int, np.integer)) or isinstance(n, bool) or n < 3:
        raise ValueError("n must be an integer of at least 3")
    if not isinstance(k, (int, np.integer)) or isinstance(k, bool) or k < 2 or k >= n or k % 2:
        raise ValueError("k must be an even integer with 2 <= k < n")
    if not 0.0 <= beta <= 1.0:
        raise ValueError("beta must be between 0 and 1")
    rng = np.random.default_rng(seed)
    adjacency = np.zeros((n, n), dtype=bool)
    half = k // 2
    for node in range(n):
        for distance in range(1, half + 1):
            other = (node + distance) % n
            adjacency[node, other] = adjacency[other, node] = True
    for node in range(n):
        for distance in range(1, half + 1):
            old = (node + distance) % n
            if not adjacency[node, old] or rng.random() >= beta:
                continue
            candidates = np.flatnonzero(~adjacency[node])
            candidates = candidates[candidates != node]
            candidates = candidates[candidates != old]
            if candidates.size == 0:
                continue
            new = int(rng.choice(candidates))
            adjacency[node, old] = adjacency[old, node] = False
            adjacency[node, new] = adjacency[new, node] = True
    return adjacency


@dataclass(frozen=True)
class SIRResult:
    states: NDArray[np.uint8]
    counts: tuple[tuple[int, int, int], ...]


def sir_step(
    states: NDArray,
    adjacency: NDArray,
    *,
    infection_probability: float,
    recovery_probability: float,
    seed: int | None = None,
) -> NDArray[np.uint8]:
    """Advance a discrete-time network SIR model synchronously.

    State codes are 0=susceptible, 1=infected and 2=recovered. Each susceptible
    with k infected neighbors is infected with probability 1-(1-beta)**k.
    Each currently infected node independently recovers with probability gamma.
    """
    state = np.asarray(states)
    graph = np.asarray(adjacency)
    if state.ndim != 1 or state.size < 1 or not np.issubdtype(state.dtype, np.integer):
        raise ValueError("states must be a non-empty one-dimensional integer array")
    if not np.isin(state, [0, 1, 2]).all():
        raise ValueError("SIR states must be 0, 1 or 2")
    if graph.shape != (state.size, state.size) or graph.ndim != 2:
        raise ValueError("adjacency must be a square matrix matching states")
    if not np.isin(graph, [False, True, 0, 1]).all():
        raise ValueError("adjacency must be binary")
    graph = graph.astype(bool, copy=False)
    if np.diag(graph).any() or not np.array_equal(graph, graph.T):
        raise ValueError("adjacency must be symmetric and have no self-loops")
    if not 0.0 <= infection_probability <= 1.0:
        raise ValueError("infection_probability must be between 0 and 1")
    if not 0.0 <= recovery_probability <= 1.0:
        raise ValueError("recovery_probability must be between 0 and 1")
    infected_neighbors = graph @ (state == 1).astype(np.int64)
    infection_risk = 1.0 - np.power(1.0 - infection_probability, infected_neighbors)
    rng = np.random.default_rng(seed)
    draws = rng.random(state.size)
    next_state = state.astype(np.uint8, copy=True)
    susceptible = state == 0
    infected = state == 1
    next_state[susceptible & (draws < infection_risk)] = 1
    next_state[infected & (draws < recovery_probability)] = 2
    return next_state


def simulate_sir(
    states: NDArray,
    adjacency: NDArray,
    *,
    infection_probability: float,
    recovery_probability: float,
    steps: int,
    seed: int | None = None,
) -> SIRResult:
    """Run network SIR and return final states plus S/I/R counts per step."""
    if not isinstance(steps, (int, np.integer)) or isinstance(steps, bool) or steps < 0:
        raise ValueError("steps must be a non-negative integer")
    state = np.asarray(states).copy()
    history = [(int(np.count_nonzero(state == 0)),
                int(np.count_nonzero(state == 1)),
                int(np.count_nonzero(state == 2)))]
    rng = np.random.default_rng(seed)
    for _ in range(steps):
        child_seed = int(rng.integers(0, np.iinfo(np.int32).max))
        state = sir_step(
            state, adjacency,
            infection_probability=infection_probability,
            recovery_probability=recovery_probability,
            seed=child_seed,
        )
        history.append((int(np.count_nonzero(state == 0)),
                        int(np.count_nonzero(state == 1)),
                        int(np.count_nonzero(state == 2))))
    return SIRResult(state.astype(np.uint8), tuple(history))
