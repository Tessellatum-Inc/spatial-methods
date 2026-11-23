"""Shortest-path point-pattern summaries on finite undirected linear networks."""
from __future__ import annotations

from heapq import heappop, heappush
from itertools import count
from math import hypot, isfinite
from numbers import Integral
from typing import Hashable, Sequence


def _network(edges):
    if not edges:
        raise ValueError("edges must contain at least one (u, v, length) tuple")
    adjacency = {}
    normalized = []
    total = 0.0
    for index, edge in enumerate(edges):
        if len(edge) != 3:
            raise ValueError("each edge must be (u, v, positive_length)")
        u, v, length = edge
        try:
            hash(u); hash(v)
        except TypeError:
            raise ValueError("network node identifiers must be hashable") from None
        length = float(length)
        if u == v or not isfinite(length) or length <= 0:
            raise ValueError("edges must join distinct nodes with positive finite lengths")
        adjacency.setdefault(u, []).append((v, length))
        adjacency.setdefault(v, []).append((u, length))
        normalized.append((u, v, length))
        total += length
    return normalized, adjacency, total


def _all_pairs_shortest_paths(adjacency):
    result = {}
    for source in adjacency:
        distances = {source: 0.0}
        sequence = count()
        queue = [(0.0, next(sequence), source)]
        while queue:
            distance, _, node = heappop(queue)
            if distance != distances[node]:
                continue
            for neighbour, weight in adjacency[node]:
                candidate = distance + weight
                if candidate < distances.get(neighbour, float("inf")):
                    distances[neighbour] = candidate
                    heappush(queue, (candidate, next(sequence), neighbour))
        result[source] = distances
    return result


def network_event_distance_matrix(edges, events):
    """Shortest-path distances for events encoded as (edge_index, offset_from_u).

    Edges are undirected tuples (u, v, length). Event offsets are measured
    from the first endpoint u and must lie in [0, edge_length]. Distances are
    shortest paths over the full network, including alternate routes around
    cycles and the direct segment when events share an edge.
    """
    network, adjacency, _ = _network(edges)
    if len(events) < 2:
        raise ValueError("at least two network events are required")
    locations = []
    for event in events:
        if len(event) != 2:
            raise ValueError("each event must be (edge_index, offset)")
        edge_index, offset = event
        if isinstance(edge_index, bool) or not isinstance(edge_index, Integral) or not 0 <= edge_index < len(network):
            raise ValueError("event edge_index must reference an existing edge")
        u, v, length = network[int(edge_index)]
        offset = float(offset)
        if not isfinite(offset) or offset < 0 or offset > length:
            raise ValueError("event offset must be finite and within its edge")
        locations.append((int(edge_index), offset, u, v, length))
    node_distances = _all_pairs_shortest_paths(adjacency)
    n = len(locations)
    matrix = [[0.0] * n for _ in range(n)]
    for i in range(n):
        ei, oi, ui, vi, li = locations[i]
        for j in range(i + 1, n):
            ej, oj, uj, vj, lj = locations[j]
            best = abs(oi - oj) if ei == ej else float("inf")
            access_i = ((ui, oi), (vi, li-oi))
            access_j = ((uj, oj), (vj, lj-oj))
            for ni, di in access_i:
                for nj, dj in access_j:
                    best = min(best, di + node_distances[ni].get(nj, float("inf")) + dj)
            matrix[i][j] = matrix[j][i] = best
    return matrix


def network_ripley_k(edges, events, radii: Sequence[float]):
    """Uncorrected network K using shortest-path distances on a finite graph.

    K_net(r) = L/[n(n-1)] * sum_{i != j} 1[d_net(i,j) <= r], where L is
    total network length. This is a descriptive finite-network estimator,
    not an edge-corrected or intensity-reweighted estimator. Disconnected
    event pairs have infinite distance and do not contribute at finite r.
    """
    network, _, total_length = _network(edges)
    distances = network_event_distance_matrix(network, events)
    rs = [float(r) for r in radii]
    if not rs or any(not isfinite(r) or r < 0 for r in rs):
        raise ValueError("radii must be a non-empty finite nonnegative sequence")
    n = len(events)
    values = []
    for radius in rs:
        pairs = sum(distances[i][j] <= radius
                    for i in range(n) for j in range(n) if i != j)
        values.append(total_length * pairs / (n * (n-1)))
    return {"radii": rs, "k_values": values, "network_length": total_length,
            "event_count": n, "distance_matrix": distances,
            "edge_correction": "none"}
