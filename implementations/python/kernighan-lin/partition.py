"""Balanced Kernighan-Lin graph bisection for undirected weighted graphs."""
from __future__ import annotations
from collections.abc import Iterable, Mapping
from numbers import Real
from typing import Hashable

Node = Hashable

def kernighan_lin_bisection(
    graph: Mapping[Node, Mapping[Node, Real] | Iterable[Node]], *,
    initial: tuple[Iterable[Node], Iterable[Node]] | None = None,
    max_passes: int = 100,
) -> tuple[set[Node], set[Node]]:
    """Return a locally improved equal-size bipartition.

    Mapping-valued adjacency supplies non-negative edge weights; iterable
    adjacency assigns unit weights. The undirected graph is symmetrised and
    reciprocal weights are averaged. Odd node counts and empty graphs are
    rejected because this implementation targets balanced bisection.
    """
    if isinstance(max_passes, bool) or not isinstance(max_passes, int) or max_passes <= 0:
        raise ValueError("max_passes must be a positive integer")
    nodes = list(graph)
    seen = set(nodes)
    for value in graph.values():
        ns = value.keys() if isinstance(value, Mapping) else value
        for v in ns:
            if v not in seen:
                nodes.append(v); seen.add(v)
    if not nodes or len(nodes) % 2:
        raise ValueError("balanced bisection requires a non-empty even number of nodes")

    directed: dict[tuple[Node, Node], float] = {}
    for u, value in graph.items():
        items = value.items() if isinstance(value, Mapping) else ((v, 1.0) for v in value)
        for v, raw in items:
            if u == v:
                continue
            if isinstance(raw, bool) or not isinstance(raw, Real) or raw < 0:
                raise ValueError("edge weights must be finite and non-negative")
            weight = float(raw)
            if not __import__("math").isfinite(weight):
                raise ValueError("edge weights must be finite and non-negative")
            directed[(u, v)] = weight
    weights: dict[frozenset, float] = {}
    pairs = {frozenset((u, v)) for u, v in directed}
    for pair in pairs:
        u, v = tuple(pair)
        a, b = directed.get((u, v)), directed.get((v, u))
        values = [x for x in (a, b) if x is not None]
        weights[pair] = sum(values) / len(values)

    if initial is None:
        ordered = sorted(nodes, key=lambda x: (type(x).__name__, repr(x)))
        half = len(ordered) // 2
        left, right = set(ordered[:half]), set(ordered[half:])
    else:
        left, right = set(initial[0]), set(initial[1])
        if left & right or left | right != seen or len(left) != len(right):
            raise ValueError("initial partition must split all nodes into equal disjoint sets")

    def weight(u: Node, v: Node) -> float:
        return weights.get(frozenset((u, v)), 0.0)

    for _ in range(max_passes):
        a, b = set(left), set(right)
        gains: list[tuple[float, Node, Node]] = []
        while a and b:
            d_a = {u: sum(weight(u, x) for x in b) - sum(weight(u, x) for x in a)
                   for u in a}
            d_b = {v: sum(weight(v, x) for x in a) - sum(weight(v, x) for x in b)
                   for v in b}
            best = max(
                ((d_a[u] + d_b[v] - 2 * weight(u, v), u, v) for u in a for v in b),
                key=lambda item: (item[0], repr(item[1]), repr(item[2])),
            )
            gain, u, v = best
            gains.append((gain, u, v))
            a.remove(u); b.remove(v)
        cumulative = 0.0
        best_gain, best_prefix = 0.0, 0
        for i, (gain, _, _) in enumerate(gains, 1):
            cumulative += gain
            if cumulative > best_gain:
                best_gain, best_prefix = cumulative, i
        if best_prefix == 0:
            break
        for _, u, v in gains[:best_prefix]:
            left.remove(u); right.remove(v)
            left.add(v); right.add(u)
    return left, right
