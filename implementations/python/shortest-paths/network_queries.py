"""Bounded many-to-many and network service-area queries.

These are transparent repeated-Dijkstra baselines for static directed graphs.
They are not contraction-hierarchy or transit-network algorithms.
"""
from __future__ import annotations

from heapq import heappop, heappush
from itertools import count
from math import isfinite
from typing import Hashable, Mapping, Sequence

Node = Hashable
Graph = Mapping[Node, Sequence[tuple[Node, float]]]


def _validate_graph(graph: Graph) -> set[Node]:
    nodes = set(graph)
    for node, outgoing in graph.items():
        for neighbor, weight in outgoing:
            if not isfinite(weight) or weight < 0:
                raise ValueError("Dijkstra queries require finite non-negative edge weights")
            nodes.add(neighbor)
    return nodes


def _single_source_tree(graph: Graph, source: Node, cutoff: float = float("inf")):
    distances = {source: 0.0}
    predecessors: dict[Node, Node] = {}
    serial = count()
    queue = [(0.0, next(serial), source)]
    while queue:
        distance, _order, node = heappop(queue)
        if distance != distances.get(node):
            continue
        for neighbor, weight in graph.get(node, ()):
            candidate = distance + weight
            if candidate <= cutoff and candidate < distances.get(neighbor, float("inf")):
                distances[neighbor] = candidate
                predecessors[neighbor] = node
                heappush(queue, (candidate, next(serial), neighbor))
    return distances, predecessors


def _reconstruct_path(predecessors: Mapping[Node, Node], source: Node, target: Node):
    if target == source:
        return [source]
    if target not in predecessors:
        return None
    path = [target]
    while path[-1] != source:
        parent = predecessors.get(path[-1])
        if parent is None:
            return None
        path.append(parent)
    path.reverse()
    return path


def many_to_many_dijkstra(
    graph: Graph, sources: Sequence[Node], targets: Sequence[Node] | None = None
) -> dict[Node, dict[Node, tuple[list[Node] | None, float]]]:
    """Return shortest paths/costs for each source-target pair.

    One Dijkstra tree is computed per source, then paths are reconstructed for
    requested targets. With T requested targets, reconstruction adds O(TL)
    work per source, where L is returned path length. This baseline does not
    share preprocessing across sources.
    """
    nodes = _validate_graph(graph)
    target_list = list(nodes if targets is None else targets)
    result: dict[Node, dict[Node, tuple[list[Node] | None, float]]] = {}
    for source in sources:
        distances, predecessors = _single_source_tree(graph, source)
        result[source] = {}
        for target in target_list:
            cost = distances.get(target, float("inf"))
            path = _reconstruct_path(predecessors, source, target) if isfinite(cost) else None
            result[source][target] = (path, cost)
    return result


def network_isochrone(
    graph: Graph, source: Node, budget: float
) -> dict[str, object]:
    """Return nodes reachable within a non-negative cost budget.

    The result contains inclusive-budget shortest distances, predecessor
    links, and directed frontier arcs leaving the reachable set. Frontier
    arcs are reported as (from_node, to_node, cumulative_cost_if_traversed).
    """
    _validate_graph(graph)
    if not isfinite(budget) or budget < 0:
        raise ValueError("budget must be finite and non-negative")
    distances, predecessors = _single_source_tree(graph, source, cutoff=budget)
    frontier = []
    for node, distance in distances.items():
        for neighbor, weight in graph.get(node, ()):
            candidate = distance + weight
            if neighbor not in distances and candidate > budget:
                frontier.append((node, neighbor, candidate))
    return {
        "distances": distances,
        "predecessors": predecessors,
        "frontier_edges": frontier,
    }
