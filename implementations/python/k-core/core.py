"""Undirected k-core decomposition by degree peeling."""
from __future__ import annotations
import heapq
from collections.abc import Iterable, Mapping
from typing import Hashable

Node = Hashable

def _adjacency(graph: Mapping[Node, Iterable[Node]]) -> dict[Node, set[Node]]:
    nodes = list(graph)
    known = set(nodes)
    for ns in graph.values():
        for v in ns:
            if v not in known:
                nodes.append(v)
                known.add(v)
    adj = {u: set() for u in nodes}
    for u, ns in graph.items():
        for v in ns:
            if u != v:
                adj[u].add(v)
                adj[v].add(u)
    return adj

def core_numbers(graph: Mapping[Node, Iterable[Node]]) -> dict[Node, int]:
    """Return core number per node; heap-based complexity O((V+E) log V)."""
    adj = _adjacency(graph)
    degree = {u: len(ns) for u, ns in adj.items()}
    order = {u: i for i, u in enumerate(adj)}
    heap = [(d, order[u], u) for u, d in degree.items()]
    heapq.heapify(heap)
    removed = set()
    result = {}
    while heap:
        d, _, u = heapq.heappop(heap)
        if u in removed or d != degree[u]:
            continue
        removed.add(u)
        result[u] = d
        for v in adj[u]:
            if v not in removed and degree[v] > d:
                degree[v] -= 1
                heapq.heappush(heap, (degree[v], order[v], v))
    return result

def k_core(graph: Mapping[Node, Iterable[Node]], k: int) -> dict[Node, set[Node]]:
    """Return adjacency of the maximal induced subgraph with minimum degree k."""
    if isinstance(k, bool) or not isinstance(k, int) or k < 0:
        raise ValueError("k must be a non-negative integer")
    adj = _adjacency(graph)
    numbers = core_numbers(graph)
    keep = {u for u, c in numbers.items() if c >= k}
    return {u: adj[u] & keep for u in adj if u in keep}
