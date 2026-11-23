"""SKATER-style spatial regionalization by cutting a feature-weighted MST."""
from __future__ import annotations
from collections.abc import Iterable
import numpy as np


class _DSU:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x):
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a, b):
        a, b = self.find(a), self.find(b)
        if a == b:
            return False
        if self.rank[a] < self.rank[b]:
            a, b = b, a
        self.parent[b] = a
        if self.rank[a] == self.rank[b]:
            self.rank[a] += 1
        return True


def _components(n, forest):
    adjacency = [[] for _ in range(n)]
    for u, v, _ in forest:
        adjacency[u].append(v)
        adjacency[v].append(u)
    labels = np.full(n, -1, dtype=int)
    members = []
    for start in range(n):
        if labels[start] >= 0:
            continue
        label = len(members)
        stack, group = [start], []
        labels[start] = label
        while stack:
            node = stack.pop()
            group.append(node)
            for neighbour in adjacency[node]:
                if labels[neighbour] < 0:
                    labels[neighbour] = label
                    stack.append(neighbour)
        members.append(group)
    order = sorted(range(len(members)), key=lambda j: min(members[j]))
    remap = {old: new for new, old in enumerate(order)}
    labels = np.asarray([remap[int(x)] for x in labels], dtype=int)
    return labels, [members[j] for j in order]


def _objective(x, groups):
    total = 0.0
    for group in groups:
        block = x[group]
        total += float(np.sum((block - block.mean(axis=0)) ** 2))
    return total


def skater(features: np.ndarray, edges: Iterable[tuple[int, int, float]], k: int) -> dict:
    """Partition a connected spatial graph into k connected regions.

    A minimum spanning tree is built from supplied non-negative edge costs.
    At each step, cut the remaining tree edge that most reduces within-region
    feature sum of squares. This is a deterministic greedy SKATER baseline.
    """
    x = np.asarray(features, dtype=float)
    if x.ndim != 2 or x.shape[0] < 2 or x.shape[1] < 1:
        raise ValueError("features must be a 2-D array with at least two rows")
    if not np.isfinite(x).all():
        raise ValueError("features must contain only finite values")
    n = len(x)
    if isinstance(k, (bool, np.bool_)) or not isinstance(k, (int, np.integer)) or not 1 <= k <= n:
        raise ValueError("k must be an integer between 1 and n")

    candidates = []
    for i, edge in enumerate(edges):
        try:
            u, v, raw_cost = edge
        except (TypeError, ValueError) as exc:
            raise ValueError(f"edge {i} must be a (u, v, cost) triple") from exc
        if isinstance(u, bool) or isinstance(v, bool) or not isinstance(u, (int, np.integer)) or not isinstance(v, (int, np.integer)):
            raise ValueError("edge endpoints must be integer row indices")
        u, v = int(u), int(v)
        if not (0 <= u < n and 0 <= v < n) or u == v:
            raise ValueError("edge endpoints must be distinct valid row indices")
        if isinstance(raw_cost, bool):
            raise ValueError("edge costs must be finite and non-negative")
        try:
            cost = float(raw_cost)
        except (TypeError, ValueError) as exc:
            raise ValueError("edge costs must be finite and non-negative") from exc
        if not np.isfinite(cost) or cost < 0:
            raise ValueError("edge costs must be finite and non-negative")
        candidates.append((cost, min(u, v), max(u, v)))
    dsu = _DSU(n)
    mst = []
    for cost, u, v in sorted(candidates):
        if dsu.union(u, v):
            mst.append((u, v, cost))
            if len(mst) == n - 1:
                break
    if len(mst) != n - 1:
        raise ValueError("input graph must be connected")

    forest = mst.copy()
    cuts = []
    labels, groups = _components(n, forest)
    current = _objective(x, groups)
    while len(groups) < int(k):
        best = None
        best_reduction = -np.inf
        for edge in forest:
            trial = [item for item in forest if item is not edge]
            trial_labels, trial_groups = _components(n, trial)
            objective = _objective(x, trial_groups)
            reduction = current - objective
            key = (edge[0], edge[1], edge[2])
            if reduction > best_reduction + 1e-12 or (
                abs(reduction - best_reduction) <= 1e-12 and
                (best is None or key < best[0])
            ):
                best = (key, edge, trial_labels, trial_groups, objective)
                best_reduction = reduction
        _, edge, labels, groups, current = best
        forest.remove(edge)
        cuts.append(edge)

    labels, groups = _components(n, forest)
    return {"labels": labels, "mst_edges": mst, "cuts": cuts,
            "objective": _objective(x, groups), "k": int(k)}
