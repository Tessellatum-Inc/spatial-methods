"""Motter–Lai-style overload cascades on undirected unweighted graphs."""
from __future__ import annotations
from collections import deque
import math

def _graph(adjacency):
    g={u:set(vs) for u,vs in adjacency.items()}
    if not g: raise ValueError("graph must contain at least one node")
    for u,vs in g.items():
        if u in vs or any(v not in g for v in vs): raise ValueError("invalid self-loop or unknown neighbor")
        if any(u not in g[v] for v in vs): raise ValueError("adjacency must be symmetric")
    return g

def node_betweenness_load(adjacency):
    """Unnormalized undirected node betweenness; endpoints are excluded."""
    g=_graph(adjacency); load=dict.fromkeys(g,0.0)
    for source in g:
        stack=[]; pred={v:[] for v in g}; sigma=dict.fromkeys(g,0.0); dist=dict.fromkeys(g,-1)
        sigma[source]=1.0; dist[source]=0; queue=deque([source])
        while queue:
            v=queue.popleft(); stack.append(v)
            for w in g[v]:
                if dist[w]<0: dist[w]=dist[v]+1; queue.append(w)
                if dist[w]==dist[v]+1: sigma[w]+=sigma[v]; pred[w].append(v)
        dependency=dict.fromkeys(g,0.0)
        while stack:
            w=stack.pop()
            for v in pred[w]: dependency[v]+=(sigma[v]/sigma[w])*(1+dependency[w])
            if w!=source: load[w]+=dependency[w]
    return {v:value/2 for v,value in load.items()}

def motter_lai_cascade(adjacency, attacked_nodes, *, tolerance=0.2, max_rounds=None):
    """Simulate synchronous overload failures after an initial node attack.

    Initial node load is unnormalized shortest-path betweenness. Capacity is
    (1+tolerance)*initial_load. At each synchronous round, loads are recomputed
    on the surviving graph and every node strictly exceeding capacity fails
    together. Disconnected pairs contribute no paths. This is a structural
    shortest-path load model, not a power-flow or traffic assignment solver.
    """
    original=_graph(adjacency); attacked=list(attacked_nodes)
    if not attacked or len(set(attacked))!=len(attacked) or any(v not in original for v in attacked):
        raise ValueError("attacked_nodes must be a nonempty unique subset of graph nodes")
    if not math.isfinite(tolerance) or tolerance<0: raise ValueError("tolerance must be finite and nonnegative")
    if max_rounds is not None and (isinstance(max_rounds,bool) or int(max_rounds)!=max_rounds or max_rounds<1):
        raise ValueError("max_rounds must be a positive integer or None")
    baseline=node_betweenness_load(original)
    capacity={v:(1+tolerance)*baseline[v] for v in original}
    active={v:set(ns) for v,ns in original.items()}
    failed=set(attacked)
    for v in attacked:
        for u in active[v]: active[u].discard(v)
        del active[v]
    rounds=[tuple(sorted(attacked,key=lambda x:(type(x).__name__,repr(x))))]
    step=0
    while active:
        current=node_betweenness_load(active)
        overloaded=[v for v in active if current[v]>capacity[v]+1e-12]
        if not overloaded: break
        step+=1
        if max_rounds is not None and step>max_rounds: raise RuntimeError("cascade exceeded max_rounds")
        batch=set(overloaded); rounds.append(tuple(sorted(batch,key=lambda x:(type(x).__name__,repr(x)))))
        for v in batch:
            for u in active[v]: active[u].discard(v)
        for v in batch: del active[v]
        failed.update(batch)
    return {"initial_load":baseline,"capacity":capacity,"failure_rounds":rounds,
            "failed_nodes":failed,"surviving_nodes":set(active),
            "cascade_size":len(failed),"cascade_fraction":len(failed)/len(original),
            "additional_failures":len(failed)-len(attacked),"rounds":len(rounds)-1}
