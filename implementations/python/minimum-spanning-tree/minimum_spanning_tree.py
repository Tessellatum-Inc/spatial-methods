"""Kruskal minimum spanning tree and forest for weighted undirected graphs."""
from __future__ import annotations

from math import fsum, isfinite
from typing import Hashable, Iterable, Sequence

Node = Hashable


def minimum_spanning_tree(
    nodes: Iterable[Node], edges: Sequence[tuple[Node, Node, float]]
) -> dict[str, object]:
    """Return a minimum spanning forest using Kruskal's algorithm.

    Each input edge is an undirected (u, v, weight) triple. Parallel edges are
    allowed and self-loops are ignored. Negative finite weights are valid.
    For disconnected graphs, the result is a minimum spanning forest.
    """
    ordered_nodes = list(nodes)
    if len(set(ordered_nodes)) != len(ordered_nodes):
        raise ValueError("nodes must be unique")
    node_set = set(ordered_nodes)
    parent = {node: node for node in ordered_nodes}
    rank = dict.fromkeys(ordered_nodes, 0)

    def find(node):
        while parent[node] != node:
            parent[node] = parent[parent[node]]
            node = parent[node]
        return node

    def union(a, b):
        root_a, root_b = find(a), find(b)
        if root_a == root_b:
            return False
        if rank[root_a] < rank[root_b]:
            root_a, root_b = root_b, root_a
        parent[root_b] = root_a
        if rank[root_a] == rank[root_b]:
            rank[root_a] += 1
        return True

    candidates = []
    for index, edge in enumerate(edges):
        if len(edge) != 3:
            raise ValueError("each edge must contain three values: (u, v, weight)")
        u, v, weight = edge
        if u not in node_set or v not in node_set:
            raise ValueError("edge endpoint is not in nodes")
        weight = float(weight)
        if not isfinite(weight):
            raise ValueError("edge weights must be finite")
        if u != v:
            candidates.append((weight, index, u, v))

    chosen = []
    chosen_weights = []
    for weight, index, u, v in sorted(candidates, key=lambda item: (item[0], item[1])):
        if union(u, v):
            chosen.append({"edge_index": index, "u": u, "v": v, "weight": weight})
            chosen_weights.append(weight)
            if len(chosen) == max(0, len(ordered_nodes) - 1):
                break

    roots = {find(node) for node in ordered_nodes}
    try:
        total = fsum(chosen_weights)
    except OverflowError as exc:
        raise OverflowError("minimum spanning forest weight exceeds finite float range") from exc
    return {
        "edges": chosen,
        "total_weight": total,
        "components": len(roots),
        "is_spanning_tree": len(roots) <= 1 and (len(ordered_nodes) == 0 or len(chosen) == len(ordered_nodes) - 1),
    }
