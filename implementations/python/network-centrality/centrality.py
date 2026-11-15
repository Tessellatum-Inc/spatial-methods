"""Directed weighted/unweighted graph centrality reference algorithms.

Betweenness uses Brandes' dependency accumulation; weighted mode uses
Dijkstra and therefore requires strictly positive finite edge weights.
Closeness uses the Wasserman-Faust reachability correction. PageRank uses
weighted outgoing transition probabilities and redistributes dangling mass
according to the selected personalization vector.
"""
from __future__ import annotations

from heapq import heappop, heappush
from itertools import count
from math import isfinite
from typing import Hashable, Mapping, Sequence

Node = Hashable
Graph = Mapping[Node, Sequence[tuple[Node, float]]]


def _normalise_graph(graph: Graph, weighted: bool):
    nodes = list(dict.fromkeys(
        list(graph) + [v for edges in graph.values() for v, _ in edges]
    ))
    adjacency = {u: list(graph.get(u, ())) for u in nodes}
    for u, edges in adjacency.items():
        for v, w in edges:
            if v not in adjacency:
                raise ValueError("graph contains an unknown endpoint")
            if not isfinite(w) or w < 0 or (weighted and w <= 0):
                requirement = "strictly positive" if weighted else "non-negative"
                raise ValueError(f"edge weights must be finite and {requirement}")
    return nodes, adjacency


def _brandes_source(source: Node, nodes: list[Node], adjacency, weighted: bool):
    predecessors = {v: [] for v in nodes}
    sigma = dict.fromkeys(nodes, 0.0)
    sigma[source] = 1.0
    distance = dict.fromkeys(nodes, float("inf"))
    distance[source] = 0.0
    stack = []

    if weighted:
        serial = count()
        queue = [(0.0, next(serial), source)]
        settled = set()
        while queue:
            dist_v, _order, v = heappop(queue)
            if dist_v != distance[v] or v in settled:
                continue
            settled.add(v)
            stack.append(v)
            for w, weight in adjacency[v]:
                candidate = dist_v + float(weight)
                if candidate < distance[w]:
                    distance[w] = candidate
                    heappush(queue, (candidate, next(serial), w))
                    sigma[w] = sigma[v]
                    predecessors[w] = [v]
                elif candidate == distance[w]:
                    sigma[w] += sigma[v]
                    predecessors[w].append(v)
    else:
        from collections import deque
        queue = deque([source])
        while queue:
            v = queue.popleft()
            stack.append(v)
            for w, _weight in adjacency[v]:
                if distance[w] == float("inf"):
                    distance[w] = distance[v] + 1
                    queue.append(w)
                if distance[w] == distance[v] + 1:
                    sigma[w] += sigma[v]
                    predecessors[w].append(v)

    dependency = dict.fromkeys(nodes, 0.0)
    while stack:
        w = stack.pop()
        if sigma[w]:
            coefficient = (1.0 + dependency[w]) / sigma[w]
            for v in predecessors[w]:
                dependency[v] += sigma[v] * coefficient
        if w != source:
            yield w, dependency[w]


def betweenness_centrality(
    graph: Graph, *, weighted: bool = False, normalized: bool = True
) -> dict[Node, float]:
    """Return directed node betweenness centrality using Brandes' algorithm.

    Endpoints are excluded. For normalized directed graphs with n > 2,
    scores are divided by (n-1)(n-2). Disconnected nodes receive zero.
    """
    nodes, adjacency = _normalise_graph(graph, weighted)
    centrality = dict.fromkeys(nodes, 0.0)
    n = len(nodes)
    if n <= 2:
        return centrality
    for source in nodes:
        for node, contribution in _brandes_source(source, nodes, adjacency, weighted):
            centrality[node] += contribution
    if normalized:
        scale = 1.0 / ((n - 1) * (n - 2))
        centrality = {v: value * scale for v, value in centrality.items()}
    return centrality


def closeness_centrality(graph: Graph) -> dict[Node, float]:
    """Return directed inward closeness with the Wasserman-Faust correction.

    For each node v, distances are measured from every node that can reach v
    by running BFS on the reversed graph. Score is (r/(n-1))*(r/sum_dist),
    where r is the number of other reachable nodes.
    """
    nodes, adjacency = _normalise_graph(graph, weighted=False)
    reverse = {v: [] for v in nodes}
    for u, edges in adjacency.items():
        for v, _weight in edges:
            reverse[v].append(u)
    n = len(nodes)
    scores = {}
    from collections import deque
    for target in nodes:
        distances = {target: 0}
        queue = deque([target])
        while queue:
            v = queue.popleft()
            for predecessor in reverse[v]:
                if predecessor not in distances:
                    distances[predecessor] = distances[v] + 1
                    queue.append(predecessor)
        reachable = len(distances) - 1
        total = sum(distances.values())
        scores[target] = (reachable / (n - 1)) * (reachable / total) if n > 1 and total else 0.0
    return scores


def pagerank(
    graph: Graph, *, alpha: float = 0.85, max_iter: int = 200,
    tolerance: float = 1e-12, personalization: Mapping[Node, float] | None = None,
) -> dict[Node, float]:
    """Return weighted directed PageRank using power iteration.

    Dangling nodes redistribute their rank using the personalization vector.
    The returned scores sum to one (up to floating-point error).
    """
    nodes, adjacency = _normalise_graph(graph, weighted=False)
    if not isfinite(alpha) or not 0 <= alpha < 1:
        raise ValueError("alpha must be finite and in [0, 1)")
    if isinstance(max_iter, bool) or not isinstance(max_iter, int) or max_iter <= 0:
        raise ValueError("max_iter must be a positive integer")
    if not isfinite(tolerance) or tolerance <= 0:
        raise ValueError("tolerance must be finite and positive")
    n = len(nodes)
    if n == 0:
        return {}
    if personalization is None:
        teleport = {v: 1.0 / n for v in nodes}
    else:
        if set(personalization) - set(nodes):
            raise ValueError("personalization contains nodes outside the graph")
        raw = {v: float(personalization.get(v, 0.0)) for v in nodes}
        if any(not isfinite(x) or x < 0 for x in raw.values()) or sum(raw.values()) <= 0:
            raise ValueError("personalization weights must be finite, non-negative and not all zero")
        total = sum(raw.values())
        teleport = {v: raw[v] / total for v in nodes}
    transitions = {}
    for u, edges in adjacency.items():
        total = sum(float(weight) for _v, weight in edges)
        if total > 0:
            transitions[u] = [(v, float(weight) / total) for v, weight in edges]
        else:
            transitions[u] = []
    rank = dict(teleport)
    for _ in range(max_iter):
        dangling_mass = sum(rank[u] for u in nodes if not transitions[u])
        updated = {v: (1.0 - alpha) * teleport[v] + alpha * dangling_mass * teleport[v]
                   for v in nodes}
        for u, outgoing in transitions.items():
            for v, probability in outgoing:
                updated[v] += alpha * rank[u] * probability
        error = sum(abs(updated[v] - rank[v]) for v in nodes)
        rank = updated
        if error < tolerance:
            break
    else:
        raise RuntimeError("PageRank power iteration did not converge within max_iter")
    return rank
