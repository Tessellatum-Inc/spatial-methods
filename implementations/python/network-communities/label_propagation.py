"""Seeded asynchronous label-propagation community detection.

The input is an adjacency mapping for an unweighted graph. Each listed edge
is treated as undirected, so asymmetric adjacency lists are symmetrised.
"""
from __future__ import annotations

from collections import Counter
from numbers import Integral
import random
from typing import Hashable, Mapping, Sequence

Node = Hashable


def label_propagation(
    graph: Mapping[Node, Sequence[Node]], *, max_iter: int = 100, seed: int = 0
) -> dict[Node, Node]:
    """Assign each node the label of its local majority community.

    Nodes are visited in a seeded random order and updated asynchronously.
    Ties are broken randomly. Isolates retain their own labels. The algorithm
    stops after a sweep with no label changes or after max_iter sweeps.
    Community labels are representative node identifiers, not consecutive
    integer IDs. Results are reproducible for a fixed graph iteration order
    and seed, but different seeds can produce different valid partitions.
    """
    if isinstance(max_iter, bool) or not isinstance(max_iter, Integral) or max_iter <= 0:
        raise ValueError("max_iter must be a positive integer")
    if isinstance(seed, bool) or not isinstance(seed, Integral):
        raise ValueError("seed must be an integer")

    nodes = list(graph)
    seen = set(nodes)
    for neighbours in graph.values():
        for neighbour in neighbours:
            if neighbour not in seen:
                nodes.append(neighbour)
                seen.add(neighbour)
    adjacency = {node: set() for node in nodes}
    for node, neighbours in graph.items():
        for neighbour in neighbours:
            if neighbour == node:
                continue
            adjacency[node].add(neighbour)
            adjacency[neighbour].add(node)

    labels = {node: node for node in nodes}
    rng = random.Random(int(seed))
    for _iteration in range(int(max_iter)):
        order = list(nodes)
        rng.shuffle(order)
        changed = False
        for node in order:
            if not adjacency[node]:
                continue
            frequencies = Counter(labels[neighbour] for neighbour in adjacency[node])
            maximum = max(frequencies.values())
            candidates = [label for label, frequency in frequencies.items()
                          if frequency == maximum]
            selected = rng.choice(candidates)
            if selected != labels[node]:
                labels[node] = selected
                changed = True
        if not changed:
            break
    return labels
