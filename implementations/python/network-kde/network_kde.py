"""Vertex-sampled network kernel density estimation."""
from __future__ import annotations
from collections.abc import Hashable, Iterable, Sequence
from heapq import heappop, heappush
import math


def _finite(value: object, name: str, *, positive: bool = False) -> float:
    if isinstance(value, bool):
        raise ValueError(f"{name} must be a finite number")
    try:
        result = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{name} must be a finite number") from exc
    if not math.isfinite(result) or (positive and result <= 0):
        raise ValueError(f"{name} must be finite" + (" and positive" if positive else ""))
    return result


def network_kde(edges: Iterable[tuple[Hashable, Hashable, float]],
                event_nodes: Sequence[Hashable], *, bandwidth: float,
                target_nodes: Sequence[Hashable] | None = None,
                event_weights: Sequence[float] | None = None) -> dict:
    """Evaluate a 1-D Gaussian kernel over undirected network shortest paths.

    Events and targets are graph vertices. Edge lengths and bandwidth share a
    linear unit. This vertex-sampled baseline does not integrate edge interiors
    or apply network edge correction.
    """
    h = _finite(bandwidth, "bandwidth", positive=True)
    graph: dict[Hashable, dict[Hashable, float]] = {}
    for i, edge in enumerate(edges):
        try:
            u, v, raw_length = edge
        except (TypeError, ValueError) as exc:
            raise ValueError(f"edge {i} must be a (u, v, length) triple") from exc
        if u == v:
            raise ValueError(f"edge {i} must connect distinct nodes")
        length = _finite(raw_length, f"edge {i} length", positive=True)
        graph.setdefault(u, {})
        graph.setdefault(v, {})
        graph[u][v] = min(length, graph[u].get(v, math.inf))
        graph[v][u] = min(length, graph[v].get(u, math.inf))
    if not graph:
        raise ValueError("edges must contain at least one edge")
    events = list(event_nodes)
    if not events:
        raise ValueError("event_nodes must contain at least one network node")
    if any(node not in graph for node in events):
        raise ValueError("every event node must occur in the network")
    if event_weights is None:
        weights = [1.0] * len(events)
    else:
        if len(event_weights) != len(events):
            raise ValueError("event_weights must match event_nodes length")
        weights = [_finite(w, f"event_weights[{j}]") for j, w in enumerate(event_weights)]
        if any(w < 0 for w in weights):
            raise ValueError("event weights must be non-negative")
    targets = list(graph) if target_nodes is None else list(target_nodes)
    if not targets:
        raise ValueError("target_nodes must not be empty")
    if any(node not in graph for node in targets):
        raise ValueError("every target node must occur in the network")
    density = []
    for target in targets:
        distances = {target: 0.0}
        queue = [(0.0, 0, target)]
        serial = 0
        while queue:
            distance, _, node = heappop(queue)
            if distance != distances[node]:
                continue
            for neighbour, length in graph[node].items():
                candidate = distance + length
                if candidate < distances.get(neighbour, math.inf):
                    distances[neighbour] = candidate
                    serial += 1
                    heappush(queue, (candidate, serial, neighbour))
        total = sum(weight * math.exp(-0.5 * (distances[event] / h) ** 2)
                    for event, weight in zip(events, weights) if event in distances)
        density.append(total / (math.sqrt(2.0 * math.pi) * h))
    return {"nodes": targets, "density": density, "bandwidth": h,
            "kernel": "gaussian", "distance": "undirected network shortest path",
            "normalization": "one-dimensional Gaussian; no edge correction"}
