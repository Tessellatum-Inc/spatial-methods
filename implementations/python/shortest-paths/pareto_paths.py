"""Pareto label-setting for multi-criteria shortest paths."""
from __future__ import annotations

import heapq
import itertools
from math import isfinite
from numbers import Integral


def pareto_shortest_paths(
    graph,
    source,
    target,
    *,
    n_objectives,
    max_labels_per_node=None,
):
    """Return nondominated simple paths for nonnegative additive vector costs.

    graph maps each node to an iterable of (neighbour, cost_vector) edges.
    Labels are ordered lexicographically in the queue and pruned by
    componentwise dominance. Equal-cost labels retain the first discovered path.
    """
    if (
        isinstance(n_objectives, bool)
        or not isinstance(n_objectives, Integral)
        or n_objectives < 1
    ):
        raise ValueError("n_objectives must be a positive integer")
    n_objectives = int(n_objectives)
    if max_labels_per_node is not None and (
        isinstance(max_labels_per_node, bool)
        or not isinstance(max_labels_per_node, Integral)
        or max_labels_per_node < 1
    ):
        raise ValueError("max_labels_per_node must be a positive integer or None")
    if max_labels_per_node is not None:
        max_labels_per_node = int(max_labels_per_node)
    try:
        hash(source)
        hash(target)
    except TypeError as exc:
        raise ValueError("source and target nodes must be hashable") from exc
    if not isinstance(graph, dict) or source not in graph:
        raise ValueError("graph must be an adjacency mapping containing source")

    adjacency = {}
    for node, edges in graph.items():
        try:
            iter(edges)
        except TypeError as exc:
            raise ValueError("each adjacency value must be iterable") from exc
        parsed_edges = []
        for edge in edges:
            if not isinstance(edge, (tuple, list)) or len(edge) != 2:
                raise ValueError("each edge must be (neighbour, cost_vector)")
            neighbour, raw_costs = edge
            try:
                hash(neighbour)
            except TypeError as exc:
                raise ValueError("neighbour nodes must be hashable") from exc
            try:
                costs = tuple(float(value) for value in raw_costs)
            except (TypeError, ValueError) as exc:
                raise ValueError("edge costs must be numeric vectors") from exc
            if (
                len(costs) != n_objectives
                or not all(isfinite(value) and value >= 0 for value in costs)
            ):
                raise ValueError(
                    "each edge cost must be a finite nonnegative vector of n_objectives"
                )
            parsed_edges.append((neighbour, costs))
        adjacency[node] = parsed_edges

    # Entries are (unique id, cost vector, complete node path).
    labels = {source: [(0, (0.0,) * n_objectives, (source,))]}
    serial = itertools.count(1)
    queue = [((0.0,) * n_objectives, 0, source, (source,))]

    while queue:
        costs, label_id, node, path = heapq.heappop(queue)
        current = labels.get(node, [])
        if not any(
            item[0] == label_id and item[1] == costs and item[2] == path
            for item in current
        ):
            continue
        if node == target:
            continue

        for neighbour, edge_costs in adjacency.get(node, []):
            # With nonnegative costs, removing a cycle cannot worsen a path.
            if neighbour in path:
                continue
            candidate = tuple(a + b for a, b in zip(costs, edge_costs))
            if not all(isfinite(value) for value in candidate):
                raise ValueError("path cost accumulation overflowed")

            existing = labels.get(neighbour, [])
            if any(
                all(a <= b for a, b in zip(item[1], candidate))
                for item in existing
            ):
                continue

            survivors = [
                item for item in existing
                if not all(a <= b for a, b in zip(candidate, item[1]))
            ]
            if (
                max_labels_per_node is not None
                and len(survivors) + 1 > max_labels_per_node
            ):
                raise RuntimeError(
                    "max_labels_per_node exceeded; Pareto frontier was not truncated"
                )

            new_id = next(serial)
            new_path = path + (neighbour,)
            labels[neighbour] = survivors + [(new_id, candidate, new_path)]
            heapq.heappush(queue, (candidate, new_id, neighbour, new_path))

    return [
        {"costs": costs, "path": path}
        for _, costs, path in sorted(labels.get(target, []), key=lambda item: item[1])
    ]
