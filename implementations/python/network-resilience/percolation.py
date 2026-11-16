"""Node-failure and targeted-attack resilience on undirected graphs."""
from __future__ import annotations
import random

def _graph(adjacency):
    graph={node:set(neighbors) for node,neighbors in adjacency.items()}
    if not graph:
        raise ValueError("graph must contain at least one node")
    for node,neighbors in graph.items():
        if node in neighbors:
            raise ValueError("self-loops are not supported")
        if any(neighbor not in graph for neighbor in neighbors):
            raise ValueError("every neighbor must be a graph node")
        if any(node not in graph[neighbor] for neighbor in neighbors):
            raise ValueError("adjacency must describe an undirected graph symmetrically")
    return graph

def largest_component_size(adjacency):
    graph=_graph(adjacency); unseen=set(graph); largest=0
    while unseen:
        start=unseen.pop(); stack=[start]; size=1
        while stack:
            node=stack.pop()
            for neighbor in graph[node]:
                if neighbor in unseen:
                    unseen.remove(neighbor); stack.append(neighbor); size+=1
        largest=max(largest,size)
    return largest

def degree_targeted_order(adjacency):
    """Static degree attack order, ties broken by string representation."""
    graph=_graph(adjacency)
    return sorted(graph,key=lambda node:(-len(graph[node]),str(node)))

def random_attack_order(adjacency, seed=0):
    graph=_graph(adjacency); nodes=list(graph)
    random.Random(seed).shuffle(nodes)
    return nodes

def node_attack_curve(adjacency, removal_order):
    """Return largest-component and remaining-node fractions after each removal.

    Fractions are normalized by the original node count, not the remaining
    network. Recomputes connected components after every node removal.
    """
    original=_graph(adjacency); order=list(removal_order); nodes=set(original)
    if len(order)!=len(nodes) or set(order)!=nodes:
        raise ValueError("removal_order must contain every node exactly once")
    active={node:set(neighbors) for node,neighbors in original.items()}
    n=len(nodes); removed=[0]; giant=[largest_component_size(active)/n]
    remaining=[1.0]
    for node in order:
        for neighbor in list(active[node]):
            active[neighbor].discard(node)
        del active[node]
        removed.append(len(removed))
        remaining.append(len(active)/n)
        giant.append(largest_component_size(active)/n if active else 0.0)
    return {"removed_fraction":[k/n for k in removed],
            "remaining_fraction":remaining,"largest_component_fraction":giant}
