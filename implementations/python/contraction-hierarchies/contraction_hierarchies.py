"""Reference implementation of static contraction hierarchies."""
from __future__ import annotations

import heapq
from math import inf, isfinite
from numbers import Integral


class ContractionHierarchy:
    """Static directed contraction hierarchy with shortcut unpacking.

    Nodes are integers in [0, n_nodes). Edge weights must be finite and
    nonnegative. A user-supplied contraction order is preferred; the default
    is a deterministic static degree order, not a dynamic importance heuristic.
    """

    def __init__(self, n_nodes, edges, *, order=None):
        if isinstance(n_nodes, bool) or not isinstance(n_nodes, Integral) or n_nodes < 1:
            raise ValueError("n_nodes must be a positive integer")
        self.n_nodes = int(n_nodes)
        self.edges = []
        self.out_edges = [[] for _ in range(self.n_nodes)]
        self.in_edges = [[] for _ in range(self.n_nodes)]
        best = {}
        for input_index, item in enumerate(edges):
            if len(item) != 3:
                raise ValueError("each edge must be (tail, head, weight)")
            u, v, weight = item
            if (isinstance(u, bool) or not isinstance(u, Integral)
                    or isinstance(v, bool) or not isinstance(v, Integral)
                    or not 0 <= u < self.n_nodes or not 0 <= v < self.n_nodes):
                raise ValueError("edge endpoints must be valid integer node ids")
            weight = float(weight)
            if not isfinite(weight) or weight < 0:
                raise ValueError("edge weights must be finite and nonnegative")
            if u == v:
                raise ValueError("self-loop edges are not supported")
            pair = (int(u), int(v))
            old = best.get(pair)
            if old is not None and self.edges[old]["weight"] <= weight:
                continue
            edge_id = len(self.edges)
            self.edges.append({
                "tail": int(u), "head": int(v), "weight": weight,
                "left": None, "right": None, "original_id": input_index,
            })
            self.out_edges[int(u)].append(edge_id)
            self.in_edges[int(v)].append(edge_id)
            best[pair] = edge_id

        if order is None:
            degree = [len(self.out_edges[i]) + len(self.in_edges[i])
                      for i in range(self.n_nodes)]
            order = sorted(range(self.n_nodes), key=lambda node: (degree[node], node))
        else:
            order = list(order)
            if (len(order) != self.n_nodes
                    or any(isinstance(v, bool) or not isinstance(v, Integral) for v in order)
                    or sorted(map(int, order)) != list(range(self.n_nodes))):
                raise ValueError("order must be a permutation of all node ids")
            order = list(map(int, order))

        self.order = tuple(order)
        self.rank = [-1] * self.n_nodes
        contracted = set()
        for level, vertex in enumerate(order):
            incoming = [eid for eid in self.in_edges[vertex]
                        if self.edges[eid]["tail"] not in contracted]
            outgoing = [eid for eid in self.out_edges[vertex]
                        if self.edges[eid]["head"] not in contracted]
            for in_id in incoming:
                u = self.edges[in_id]["tail"]
                for out_id in outgoing:
                    w = self.edges[out_id]["head"]
                    if u == w:
                        continue
                    candidate = self.edges[in_id]["weight"] + self.edges[out_id]["weight"]
                    existing = best.get((u, w))
                    if existing is not None and self.edges[existing]["weight"] <= candidate:
                        continue
                    # Keep every candidate shortcut in this small-graph reference.
                    # Avoiding witness pruning trades index size for a simpler exactness
                    # argument and prevents an over-aggressive witness search from
                    # suppressing a path needed by the upward query.
                    shortcut_id = len(self.edges)
                    self.edges.append({
                        "tail": u, "head": w, "weight": candidate,
                        "left": in_id, "right": out_id, "original_id": None,
                    })
                    self.out_edges[u].append(shortcut_id)
                    self.in_edges[w].append(shortcut_id)
                    best[(u, w)] = shortcut_id
            contracted.add(vertex)
            self.rank[vertex] = level

        self.original_edge_count = sum(e["original_id"] is not None for e in self.edges)
        self.shortcut_count = sum(e["left"] is not None for e in self.edges)

    def _witness_exists(self, source, target, avoid, cutoff, contracted):
        distances = {source: 0.0}
        queue = [(0.0, source)]
        while queue:
            distance, node = heapq.heappop(queue)
            if distance != distances.get(node):
                continue
            if distance > cutoff:
                return False
            if node == target:
                return True
            for edge_id in self.out_edges[node]:
                edge = self.edges[edge_id]
                neighbour = edge["head"]
                if neighbour == avoid or neighbour in contracted:
                    continue
                candidate = distance + edge["weight"]
                if candidate <= cutoff and candidate < distances.get(neighbour, inf):
                    distances[neighbour] = candidate
                    heapq.heappush(queue, (candidate, neighbour))
        return False

    def _upward_search(self, start, *, reverse=False):
        distances = {start: 0.0}
        parents = {}
        queue = [(0.0, start)]
        while queue:
            distance, node = heapq.heappop(queue)
            if distance != distances.get(node):
                continue
            edge_ids = self.in_edges[node] if reverse else self.out_edges[node]
            for edge_id in edge_ids:
                edge = self.edges[edge_id]
                neighbour = edge["tail"] if reverse else edge["head"]
                # Forward search follows upward original edges; reverse search
                # follows upward edges in the reversed graph (originally downward).
                upward = self.rank[node] < self.rank[neighbour]
                if not upward:
                    continue
                candidate = distance + edge["weight"]
                if candidate < distances.get(neighbour, inf):
                    distances[neighbour] = candidate
                    parents[neighbour] = edge_id
                    heapq.heappush(queue, (candidate, neighbour))
        return distances, parents

    def _expand(self, edge_id):
        edge = self.edges[edge_id]
        if edge["left"] is None:
            return [edge_id]
        return self._expand(edge["left"]) + self._expand(edge["right"])

    def query(self, source, target, *, return_path=True):
        """Return exact distance and, optionally, an unpacked original-edge path."""
        for node in (source, target):
            if isinstance(node, bool) or not isinstance(node, Integral) or not 0 <= node < self.n_nodes:
                raise ValueError("source and target must be valid integer node ids")
        if not isinstance(return_path, bool):
            raise ValueError("return_path must be boolean")
        source, target = int(source), int(target)
        if source == target:
            return {"distance": 0.0, "path": [source] if return_path else [],
                    "edge_ids": [], "meeting_node": source}
        forward, forward_parent = self._upward_search(source)
        backward, backward_parent = self._upward_search(target, reverse=True)
        candidates = [(distance + backward[node], node)
                      for node, distance in forward.items() if node in backward]
        if not candidates:
            return {"distance": inf, "path": [], "edge_ids": [], "meeting_node": None}
        distance, meeting = min(candidates)
        if not return_path:
            return {"distance": float(distance), "path": [], "edge_ids": [],
                    "meeting_node": meeting}

        left, node = [], meeting
        while node != source:
            edge_id = forward_parent[node]
            left.append(edge_id)
            node = self.edges[edge_id]["tail"]
        left.reverse()
        right, node = [], meeting
        while node != target:
            edge_id = backward_parent[node]
            right.append(edge_id)
            node = self.edges[edge_id]["head"]
        original_edges = []
        for edge_id in left + right:
            original_edges.extend(self._expand(edge_id))
        path = [source]
        original_ids = []
        for edge_id in original_edges:
            edge = self.edges[edge_id]
            if path[-1] != edge["tail"]:
                raise RuntimeError("shortcut unpacking produced a discontinuous path")
            path.append(edge["head"])
            original_ids.append(edge["original_id"])
        return {"distance": float(distance), "path": path,
                "edge_ids": original_ids, "meeting_node": meeting}
