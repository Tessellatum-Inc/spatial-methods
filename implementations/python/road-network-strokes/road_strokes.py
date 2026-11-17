"""Greedy good-continuation stroke construction for embedded road graphs."""
from __future__ import annotations

from collections import defaultdict
from math import acos, degrees, hypot, isfinite
from typing import Hashable, Iterable, Mapping, Sequence


def generate_strokes(
    nodes: Mapping[Hashable, Sequence[float]],
    edges: Iterable[tuple[Hashable, Hashable, Hashable]],
    *,
    max_deviation_degrees: float = 45.0,
) -> list[dict]:
    """Partition undirected embedded edges into strokes by straightest continuation.

    Each junction greedily pairs incident edges by ascending deviation from a
    180-degree continuation. An edge can be paired at most once at each end.
    """
    if not isfinite(max_deviation_degrees) or not 0 <= max_deviation_degrees <= 180:
        raise ValueError("max_deviation_degrees must be finite and in [0, 180]")
    coords = {}
    for node, point in nodes.items():
        try:
            if len(point) != 2:
                raise ValueError
            x, y = float(point[0]), float(point[1])
        except (TypeError, ValueError, IndexError, OverflowError) as exc:
            raise ValueError("each node coordinate must be a finite x/y pair") from exc
        if not isfinite(x) or not isfinite(y):
            raise ValueError("node coordinates must be finite")
        coords[node] = (x, y)

    edge_records = {}
    incident = defaultdict(list)
    try:
        raw_edges = list(edges)
    except TypeError as exc:
        raise ValueError("edges must be an iterable of (edge_id, u, v) records") from exc
    for record in raw_edges:
        if len(record) != 3:
            raise ValueError("each edge must be (edge_id, u, v)")
        edge_id, u, v = record
        if edge_id in edge_records:
            raise ValueError("edge identifiers must be unique")
        if u not in coords or v not in coords or u == v:
            raise ValueError("edge endpoints must be distinct known nodes")
        if hypot(coords[u][0] - coords[v][0], coords[u][1] - coords[v][1]) == 0:
            raise ValueError("edge endpoints must have distinct coordinates")
        edge_records[edge_id] = (u, v)
        incident[u].append((edge_id, v))
        incident[v].append((edge_id, u))

    adjacency = defaultdict(list)
    pairings = []
    for junction in sorted(incident, key=repr):
        half_edges = incident[junction]
        candidates = []
        for i in range(len(half_edges)):
            edge_a, node_a = half_edges[i]
            ax = coords[node_a][0] - coords[junction][0]
            ay = coords[node_a][1] - coords[junction][1]
            for j in range(i + 1, len(half_edges)):
                edge_b, node_b = half_edges[j]
                bx = coords[node_b][0] - coords[junction][0]
                by = coords[node_b][1] - coords[junction][1]
                cosine = (ax * bx + ay * by) / (hypot(ax, ay) * hypot(bx, by))
                cosine = max(-1.0, min(1.0, cosine))
                angle = degrees(acos(cosine))
                deviation = abs(180.0 - angle)
                if deviation <= max_deviation_degrees:
                    first, second = sorted((edge_a, edge_b), key=repr)
                    candidates.append((deviation, repr(first), repr(second), first, second))
        used = set()
        for deviation, _, __, edge_a, edge_b in sorted(candidates):
            if edge_a in used or edge_b in used:
                continue
            used.update((edge_a, edge_b))
            adjacency[edge_a].append((edge_b, junction))
            adjacency[edge_b].append((edge_a, junction))
            pairings.append({"node": junction, "edge_ids": [edge_a, edge_b], "deviation_degrees": deviation})

    unvisited = set(edge_records)
    strokes = []
    while unvisited:
        component = set()
        stack = [min(unvisited, key=repr)]
        while stack:
            edge_id = stack.pop()
            if edge_id in component:
                continue
            component.add(edge_id)
            stack.extend(other for other, _ in adjacency[edge_id] if other not in component)
        endpoints = [edge_id for edge_id in component if len(adjacency[edge_id]) <= 1]
        start = min(endpoints or list(component), key=repr)
        ordered = []
        transitions = []
        previous = None
        current = start
        while current not in ordered:
            ordered.append(current)
            options = [(other, junction) for other, junction in adjacency[current] if other != previous and other in component]
            if not options:
                break
            nxt, junction = min(options, key=lambda item: repr(item[0]))
            transitions.append(junction)
            previous, current = current, nxt
        if len(ordered) < len(component):
            raise RuntimeError("stroke traversal failed to cover its edge component")

        if len(transitions) == len(ordered):  # closed cycle
            start_node = transitions[-1]
            path_nodes = [start_node] + transitions[:-1] + [start_node]
        elif transitions:
            first_edge = edge_records[ordered[0]]
            start_node = next(node for node in first_edge if node != transitions[0])
            last_edge = edge_records[ordered[-1]]
            end_node = next(node for node in last_edge if node != transitions[-1])
            path_nodes = [start_node] + transitions + [end_node]
        else:
            u, v = edge_records[ordered[0]]
            path_nodes = [u, v]
        strokes.append({"edge_ids": ordered, "node_ids": path_nodes, "closed": path_nodes[0] == path_nodes[-1]})
        unvisited.difference_update(component)

    strokes.sort(key=lambda stroke: tuple(map(repr, stroke["edge_ids"])))
    return strokes
