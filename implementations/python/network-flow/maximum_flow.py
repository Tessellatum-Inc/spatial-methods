"""Dinic maximum flow and minimum s-t cut for directed capacitated graphs."""
from __future__ import annotations

from collections import deque
from math import fsum, isfinite
from typing import Hashable, Mapping, Sequence

Node = Hashable


def maximum_flow_min_cut(
    graph: Mapping[Node, Sequence[tuple[Node, float]]], source: Node, sink: Node
) -> dict[str, object]:
    """Compute a maximum flow and corresponding minimum cut using Dinic.

    Each adjacency tuple is a distinct directed arc (parallel and antiparallel
    arcs are supported). Capacities must be finite and non-negative. Self
    loops are rejected. Returns the maximum flow value, per-input-arc flows,
    source-side residual-reachable nodes, cut arcs and cut capacity.
    """
    if source == sink:
        raise ValueError("source and sink must be different")
    nodes = list(dict.fromkeys(
        list(graph) + [v for edges in graph.values() for v, _ in edges] + [source, sink]
    ))
    adjacency = {node: [] for node in nodes}
    original_edges = []

    for u, edges in graph.items():
        for v, capacity in edges:
            capacity = float(capacity)
            if u == v:
                raise ValueError("self-loop arcs are not supported")
            if not isfinite(capacity) or capacity < 0:
                raise ValueError("capacities must be finite and non-negative")
            forward = [v, len(adjacency[v]), capacity, capacity]
            reverse = [u, len(adjacency[u]), 0.0, 0.0]
            adjacency[u].append(forward)
            adjacency[v].append(reverse)
            original_edges.append((u, v, forward))

    augmentations = []
    while True:
        level = {node: -1 for node in nodes}
        level[source] = 0
        queue = deque([source])
        while queue:
            u = queue.popleft()
            for v, _rev, residual, _original in adjacency[u]:
                if residual > 0 and level[v] < 0:
                    level[v] = level[u] + 1
                    queue.append(v)
        if level[sink] < 0:
            break

        cursor = {node: 0 for node in nodes}

        # Iterative blocking-flow search avoids Python recursion limits on
        # long road/transit networks while retaining Dinic's current-arc rule.
        while True:
            stack = [source]
            path_edges = []
            bottlenecks = [float("inf")]
            pushed = 0.0

            while stack:
                u = stack[-1]
                if u == sink:
                    pushed = bottlenecks[-1]
                    for path_u, edge_index in zip(stack, path_edges):
                        edge = adjacency[path_u][edge_index]
                        v, reverse_index = edge[0], edge[1]
                        edge[2] -= pushed
                        adjacency[v][reverse_index][2] += pushed
                    break

                while cursor[u] < len(adjacency[u]):
                    edge = adjacency[u][cursor[u]]
                    v, _reverse_index, residual, _original = edge
                    if residual > 0 and level[v] == level[u] + 1:
                        break
                    cursor[u] += 1

                if cursor[u] == len(adjacency[u]):
                    stack.pop()
                    bottlenecks.pop()
                    if path_edges:
                        path_edges.pop()
                        if stack:
                            cursor[stack[-1]] += 1
                    continue

                edge = adjacency[u][cursor[u]]
                v, _reverse_index, residual, _original = edge
                path_edges.append(cursor[u])
                stack.append(v)
                bottlenecks.append(min(bottlenecks[-1], residual))

            if pushed <= 0:
                break
            augmentations.append(pushed)

    source_side = set()
    queue = deque([source])
    source_side.add(source)
    while queue:
        u = queue.popleft()
        for v, _rev, residual, _original in adjacency[u]:
            if residual > 0 and v not in source_side:
                source_side.add(v)
                queue.append(v)

    edge_flows = []
    cut_edges = []
    cut_capacities = []
    for index, (u, v, forward) in enumerate(original_edges):
        flow = forward[3] - forward[2]
        edge_flows.append({"edge_index": index, "from": u, "to": v,
                           "capacity": forward[3], "flow": flow})
        if u in source_side and v not in source_side:
            cut_edges.append({"edge_index": index, "from": u, "to": v,
                              "capacity": forward[3]})
            cut_capacities.append(forward[3])

    try:
        total_flow = fsum(augmentations)
        cut_capacity = fsum(cut_capacities)
    except OverflowError as exc:
        raise OverflowError("maximum flow or minimum cut capacity exceeds finite float range") from exc

    return {
        "value": total_flow,
        "edge_flows": edge_flows,
        "source_side": source_side,
        "sink_side": set(nodes) - source_side,
        "cut_edges": cut_edges,
        "cut_capacity": cut_capacity,
    }
