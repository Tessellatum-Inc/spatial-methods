"""Spatially constrained Ward zoning and scale-effect summaries."""
from __future__ import annotations
import numpy as np


def spatially_constrained_ward(attributes, adjacency_edges, *, n_zones):
    """Greedily merge adjacent zones by minimum Ward increase in SSE.

    Attributes have shape (units, variables). Adjacency edges are undirected
    integer unit pairs. The graph must have at least n_zones connected
    components; merging never crosses a missing adjacency edge.
    """
    x = np.asarray(attributes, dtype=float)
    edges = np.asarray(adjacency_edges)
    if x.ndim != 2 or x.shape[0] == 0 or x.shape[1] == 0 or not np.all(np.isfinite(x)):
        raise ValueError("attributes must be a non-empty finite units-by-variables matrix")
    n = len(x)
    if edges.ndim != 2 or edges.shape[1] != 2 or not np.issubdtype(edges.dtype, np.integer):
        raise ValueError("adjacency_edges must be an integer (m, 2) array")
    if np.any(edges < 0) or np.any(edges >= n) or np.any(edges[:,0] == edges[:,1]):
        raise ValueError("adjacency_edges contain invalid unit IDs")
    if isinstance(n_zones, (bool, np.bool_)) or not isinstance(n_zones, (int, np.integer)) or not 1 <= n_zones <= n:
        raise ValueError("n_zones must be an integer between one and the number of units")
    active = set(range(n))
    sizes = {i: 1 for i in range(n)}
    means = {i: x[i].copy() for i in range(n)}
    members = {i: [i] for i in range(n)}
    neighbours = {i: set() for i in range(n)}
    for i, j in edges:
        neighbours[int(i)].add(int(j))
        neighbours[int(j)].add(int(i))
    merge_costs = []
    next_id = n
    while len(active) > n_zones:
        best = None
        for a in sorted(active):
            for b in sorted(neighbours[a] & active):
                if a >= b:
                    continue
                cost = (sizes[a]*sizes[b]/(sizes[a]+sizes[b])) * float(np.sum((means[a]-means[b])**2))
                candidate = (cost, a, b)
                if best is None or candidate < best:
                    best = candidate
        if best is None:
            raise ValueError("adjacency graph is disconnected at the requested zone count")
        cost, a, b = best
        new = next_id
        next_id += 1
        size = sizes[a]+sizes[b]
        mean = (sizes[a]*means[a]+sizes[b]*means[b])/size
        merged_members = members[a]+members[b]
        merged_neighbours = (neighbours[a] | neighbours[b]) - {a,b}
        active.remove(a); active.remove(b); active.add(new)
        for neighbour in merged_neighbours:
            neighbours[neighbour].discard(a)
            neighbours[neighbour].discard(b)
            neighbours[neighbour].add(new)
        neighbours[new] = merged_neighbours
        sizes[new] = size; means[new] = mean; members[new] = merged_members
        merge_costs.append(float(cost))
    labels = np.zeros(n, dtype=np.int32)
    final_clusters = sorted(active, key=lambda cluster: min(members[cluster]))
    for label_id, cluster in enumerate(final_clusters):
        labels[members[cluster]] = label_id
    return {"labels": labels, "zone_sizes": np.asarray([sizes[c] for c in final_clusters]),
            "within_zone_sse": float(np.sum(merge_costs)),
            "merge_costs": np.asarray(merge_costs),
            "n_zones": int(n_zones)}


def zoning_scale_effect(attributes, adjacency_edges, zone_counts):
    """Evaluate spatial Ward within-zone SSE over a sequence of zone counts."""
    counts = list(zone_counts)
    if not counts or any(isinstance(k, (bool, np.bool_)) or not isinstance(k, (int, np.integer)) for k in counts):
        raise ValueError("zone_counts must be a non-empty sequence of integers")
    results = [spatially_constrained_ward(attributes, adjacency_edges, n_zones=int(k))
               for k in counts]
    return {"zone_counts": np.asarray(counts, dtype=np.int32),
            "within_zone_sse": np.asarray([r["within_zone_sse"] for r in results]),
            "mean_zone_sse": np.asarray([r["within_zone_sse"]/r["n_zones"] for r in results]),
            "solutions": results}
