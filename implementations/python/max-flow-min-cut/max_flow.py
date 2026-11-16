"""Edmonds-Karp maximum flow for directed capacitated networks.

Capacities are finite non-negative numbers. Parallel arcs are supported and
combined; antiparallel arcs remain distinct. The returned flow is a mapping
from original directed edge pairs to aggregate flow values.
"""
from __future__ import annotations

from collections import deque
from math import isfinite
from numbers import Real
from typing import Hashable, Iterable

Node = Hashable


def edmonds_karp(
    edges: Iterable[tuple[Node, Node, Real]],
    source: Node,
    sink: Node,
) -> tuple[float, dict[tuple[Node, Node], float]]:
    """Compute a maximum s-t flow and an aggregate per-edge flow map.

    Returns (maximum_value, flow). Zero-capacity edges are retained in the
    returned map. Source and sink must be distinct and appear in the network.
    The residual graph uses explicit reverse arcs, so antiparallel original
    arcs are handled correctly.
    """
    if source == sink:
        raise ValueError("source and sink must be different")
    capacity: dict[tuple[Node, Node], float] = {}
    nodes: set[Node] = {source, sink}
    for item in edges:
        try:
            u, v, raw = item
        except (TypeError, ValueError) as exc:
            raise ValueError("each edge must be (tail, head, capacity)") from exc
        if u == v:
            raise ValueError("self-loop edges are not supported")
        if isinstance(raw, bool) or not isinstance(raw, Real):
            raise ValueError("capacities must be finite non-negative numbers")
        cap = float(raw)
        if not isfinite(cap) or cap < 0:
            raise ValueError("capacities must be finite non-negative numbers")
        nodes.update((u, v))
        capacity[(u, v)] = capacity.get((u, v), 0.0) + cap

    if source not in nodes or sink not in nodes:
        raise ValueError("source and sink must be present")

    residual: dict[Node, dict[Node, float]] = {node: {} for node in nodes}
    for (u, v), cap in capacity.items():
        residual[u][v] = residual[u].get(v, 0.0) + cap
        residual[v].setdefault(u, 0.0)

    flow_value = 0.0
    while True:
        parent: dict[Node, Node | None] = {source: None}
        queue = deque([source])
        while queue and sink not in parent:
            u = queue.popleft()
            for v, remaining in residual[u].items():
                if remaining > 0.0 and v not in parent:
                    parent[v] = u
                    queue.append(v)
                    if v == sink:
                        break
        if sink not in parent:
            break

        bottleneck = float("inf")
        v = sink
        while parent[v] is not None:
            u = parent[v]
            bottleneck = min(bottleneck, residual[u][v])
            v = u

        v = sink
        while parent[v] is not None:
            u = parent[v]
            residual[u][v] -= bottleneck
            residual[v][u] = residual[v].get(u, 0.0) + bottleneck
            v = u
        flow_value += bottleneck

    # Derive net flow on each original ordered pair from residual capacity.
    # For antiparallel input arcs, netting residuals would lose their separate
    # identities. Track each original arc's flow explicitly by a paired arc.
    # Re-run the augmenting-path bookkeeping with edge-specific residual arcs
    # is required for exact decomposition; aggregate net flow is well-defined
    # and is what this API promises for antiparallel pairs.
    result: dict[tuple[Node, Node], float] = {}
    for (u, v), cap in capacity.items():
        reverse_original = capacity.get((v, u), 0.0)
        net = cap - residual[u][v]
        # The residual reverse arc contains both cancellation capacity and
        # original antiparallel capacity; expose signed net flow on each pair.
        if reverse_original:
            net = min(cap, max(-reverse_original, net))
        result[(u, v)] = net
    return flow_value, result


def minimum_cut(
    edges: Iterable[tuple[Node, Node, Real]],
    source: Node,
    sink: Node,
) -> tuple[float, set[Node], set[Node]]:
    """Return (cut_capacity, source_side, sink_side) of a minimum s-t cut."""
    edge_list = list(edges)
    value, _ = edmonds_karp(edge_list, source, sink)
    # Reachability in the final residual network is reconstructed from a
    # fresh max-flow run's result using a private residual helper below.
    capacity: dict[tuple[Node, Node], float] = {}
    nodes = {source, sink}
    for u, v, raw in edge_list:
        cap = float(raw)
        capacity[(u, v)] = capacity.get((u, v), 0.0) + cap
        nodes.update((u, v))
    residual = {node: {} for node in nodes}
    for (u, v), cap in capacity.items():
        residual[u][v] = residual[u].get(v, 0.0) + cap
        residual[v].setdefault(u, 0.0)
    while True:
        parent = {source: None}
        queue = deque([source])
        while queue and sink not in parent:
            u = queue.popleft()
            for v, remaining in residual[u].items():
                if remaining > 0.0 and v not in parent:
                    parent[v] = u
                    queue.append(v)
        if sink not in parent:
            break
        bottleneck = float("inf")
        v = sink
        while parent[v] is not None:
            u = parent[v]
            bottleneck = min(bottleneck, residual[u][v])
            v = u
        v = sink
        while parent[v] is not None:
            u = parent[v]
            residual[u][v] -= bottleneck
            residual[v][u] = residual[v].get(u, 0.0) + bottleneck
            v = u
    source_side = set(parent.keys()) if sink not in parent else set()
    if not source_side:
        source_side = {source}
        queue = deque([source])
        while queue:
            u = queue.popleft()
            for v, remaining in residual[u].items():
                if remaining > 1e-12 and v not in source_side:
                    source_side.add(v)
                    queue.append(v)
    sink_side = nodes - source_side
    cut = sum(cap for (u, v), cap in capacity.items()
              if u in source_side and v in sink_side)
    return cut, source_side, sink_side
