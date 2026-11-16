"""Exact Dreyfus-Wagner Steiner tree for small terminal sets."""
from __future__ import annotations

from heapq import heappop, heappush
from itertools import count
from math import isfinite
from typing import Hashable, Iterable, Sequence

Node = Hashable


def steiner_tree(
    nodes: Iterable[Node], edges: Sequence[tuple[Node, Node, float]],
    terminals: Sequence[Node], *, max_terminals: int = 12,
) -> dict[str, object]:
    """Find an exact minimum-weight undirected Steiner tree.

    Uses the Dreyfus-Wagner subset dynamic program with shortest-path closure.
    The algorithm is exponential in the number of terminals; this reference
    implementation deliberately caps that count. Parallel edges are reduced
    to their minimum-weight representative; self-loops are ignored.
    """
    vertices = list(nodes)
    vertex_set = set(vertices)
    if len(vertex_set) != len(vertices):
        raise ValueError("nodes must be unique")
    terminal_list = list(terminals)
    if not terminal_list or len(set(terminal_list)) != len(terminal_list):
        raise ValueError("terminals must be non-empty and unique")
    if any(t not in vertex_set for t in terminal_list):
        raise ValueError("every terminal must be in nodes")
    if isinstance(max_terminals, bool) or not isinstance(max_terminals, int) or max_terminals <= 0:
        raise ValueError("max_terminals must be a positive integer")
    if len(terminal_list) > max_terminals:
        raise ValueError("terminal count exceeds max_terminals")

    edge_weights = {}
    for edge in edges:
        if len(edge) != 3:
            raise ValueError("each edge must be (u, v, weight)")
        u, v, raw_weight = edge
        if u not in vertex_set or v not in vertex_set:
            raise ValueError("edge endpoint is not in nodes")
        weight = float(raw_weight)
        if not isfinite(weight) or weight <= 0:
            raise ValueError("edge weights must be finite and strictly positive")
        if u == v:
            continue
        key = frozenset((u, v))
        edge_weights[key] = min(weight, edge_weights.get(key, float("inf")))

    adjacency = {v: [] for v in vertices}
    for pair, weight in edge_weights.items():
        u, v = tuple(pair)
        adjacency[u].append((v, weight))
        adjacency[v].append((u, weight))

    k = len(terminal_list)
    full = (1 << k) - 1
    infinity = float("inf")
    dp = {}
    parent = {}
    serial = count()

    for mask in range(1, full + 1):
        distances = dict.fromkeys(vertices, infinity)
        parents = {}
        if mask & (mask - 1) == 0:
            terminal_index = mask.bit_length() - 1
            terminal = terminal_list[terminal_index]
            distances[terminal] = 0.0
            parents[terminal] = ("terminal",)
        else:
            subset = (mask - 1) & mask
            while subset:
                other = mask ^ subset
                if subset < other:
                    for vertex in vertices:
                        left = dp[subset][vertex]
                        right = dp[other][vertex]
                        candidate = left + right
                        if candidate < distances[vertex]:
                            distances[vertex] = candidate
                            parents[vertex] = ("merge", subset, other)
                subset = (subset - 1) & mask

        queue = [(distance, next(serial), vertex)
                 for vertex, distance in distances.items() if distance < infinity]
        import heapq
        heapq.heapify(queue)
        while queue:
            distance, _order, u = heappop(queue)
            if distance != distances[u]:
                continue
            for v, weight in adjacency[u]:
                candidate = distance + weight
                if candidate < distances[v]:
                    distances[v] = candidate
                    parents[v] = ("move", u, weight)
                    heappush(queue, (candidate, next(serial), v))
        dp[mask] = distances
        parent[mask] = parents

    root = min(vertices, key=lambda vertex: dp[full][vertex]) if vertices else None
    if root is None or dp[full][root] == infinity:
        raise ValueError("no connected subgraph contains all terminals")

    selected = {}

    def recover(mask, vertex):
        record = parent[mask].get(vertex)
        if record is None:
            raise RuntimeError("Steiner reconstruction encountered a missing predecessor")
        if record[0] == "terminal":
            return
        if record[0] == "merge":
            recover(record[1], vertex)
            recover(record[2], vertex)
            return
        previous, weight = record[1], record[2]
        key = frozenset((previous, vertex))
        selected[key] = (previous, vertex, weight)
        recover(mask, previous)

    recover(full, root)
    tree_edges = list(selected.values())
    total_weight = sum(weight for _u, _v, weight in tree_edges)
    tree_nodes = {root}
    for u, v, _weight in tree_edges:
        tree_nodes.add(u)
        tree_nodes.add(v)
    return {
        "root": root,
        "terminals": terminal_list,
        "nodes": tree_nodes,
        "edges": [{"u": u, "v": v, "weight": weight} for u, v, weight in tree_edges],
        "total_weight": total_weight,
        "dynamic_program_cost": dp[full][root],
    }
