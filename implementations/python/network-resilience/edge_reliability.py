"""Edge-failure resilience and small-graph reliability baselines."""
from __future__ import annotations
from itertools import combinations
import random

def _graph(adjacency):
    g={u:set(vs) for u,vs in adjacency.items()}
    if not g: raise ValueError("graph must contain at least one node")
    for u,vs in g.items():
        if u in vs: raise ValueError("self-loops are not supported")
        if any(v not in g for v in vs): raise ValueError("unknown neighbor")
        if any(u not in g[v] for v in vs): raise ValueError("adjacency must be symmetric")
    return g

def _key(u,v):
    return (u,v) if (type(u).__name__,repr(u)) <= (type(v).__name__,repr(v)) else (v,u)

def _edges(g):
    return sorted({_key(u,v) for u,vs in g.items() for v in vs},
        key=lambda e:(type(e[0]).__name__,repr(e[0]),type(e[1]).__name__,repr(e[1])))

def _components(g):
    unseen=set(g); out=[]
    while unseen:
        start=unseen.pop(); comp={start}; stack=[start]
        while stack:
            u=stack.pop()
            for v in g[u]:
                if v in unseen: unseen.remove(v); comp.add(v); stack.append(v)
        out.append(comp)
    return out

def _remove(g, edges):
    active={u:set(vs) for u,vs in g.items()}
    for u,v in edges: active[u].discard(v); active[v].discard(u)
    return active

def largest_component_size_after_edge_removal(adjacency, removed_edges=()):
    g=_graph(adjacency); removed=set()
    for edge in removed_edges:
        if len(edge)!=2: raise ValueError("each edge needs two endpoints")
        u,v=edge
        if u not in g or v not in g or v not in g[u]: raise ValueError(f"unknown edge: {edge!r}")
        removed.add(_key(u,v))
    return max(map(len,_components(_remove(g,removed))))

def random_edge_attack_order(adjacency, seed=0):
    edges=_edges(_graph(adjacency)); random.Random(seed).shuffle(edges); return edges

def edge_betweenness_attack_order(adjacency):
    """Static unweighted Brandes edge-betweenness ranking, highest first."""
    g=_graph(adjacency); edges=_edges(g); score={e:0.0 for e in edges}
    for source in g:
        stack=[]; pred={v:[] for v in g}; sigma=dict.fromkeys(g,0.0); dist=dict.fromkeys(g,-1)
        sigma[source]=1.0; dist[source]=0; queue=[source]
        for v in queue:
            stack.append(v)
            for w in g[v]:
                if dist[w]<0: queue.append(w); dist[w]=dist[v]+1
                if dist[w]==dist[v]+1: sigma[w]+=sigma[v]; pred[w].append(v)
        dep=dict.fromkeys(g,0.0)
        while stack:
            w=stack.pop()
            for v in pred[w]:
                c=(sigma[v]/sigma[w])*(1+dep[w]); score[_key(v,w)]+=c; dep[v]+=c
    score={e:s/2 for e,s in score.items()}
    return sorted(edges,key=lambda e:(-score[e],edges.index(e)))

def edge_attack_curve(adjacency, removal_order):
    """Fractions are normalized by original node/edge counts."""
    g=_graph(adjacency); edges=_edges(g); order=[_key(*e) for e in removal_order]
    if len(order)!=len(edges) or set(order)!=set(edges):
        raise ValueError("order must contain every undirected edge exactly once")
    n,m=len(g),len(edges); failed=set()
    giant=[max(map(len,_components(g)))/n]; remain=[1.0 if m else 0.0]
    for e in order:
        failed.add(e); active=_remove(g,failed)
        giant.append(max(map(len,_components(active)))/n)
        remain.append((m-len(failed))/m if m else 0.0)
    return {"removed_edges":order,"removed_fraction":[i/m for i in range(m+1)] if m else [0.0],
            "remaining_edge_fraction":remain,"largest_component_fraction":giant}

def _connected(g, terminals=None):
    if terminals is None: return len(_components(g))==1
    t=tuple(terminals)
    if len(t)<2 or any(x not in g for x in t): raise ValueError("terminals must contain at least two graph nodes")
    seen={t[0]}; stack=[t[0]]
    while stack:
        u=stack.pop()
        for v in g[u]-seen: seen.add(v); stack.append(v)
    return all(x in seen for x in t)

def monte_carlo_reliability(adjacency, edge_survival_probability, trials=10000, terminals=None, seed=0):
    """Estimate all-terminal or k-terminal reliability under IID edge survival."""
    g=_graph(adjacency); p=float(edge_survival_probability)
    if not 0<=p<=1: raise ValueError("probability must be in [0,1]")
    if isinstance(trials,bool) or int(trials)!=trials or trials<1: raise ValueError("trials must be a positive integer")
    if terminals is not None:
        terminals=tuple(terminals)
        if len(terminals)<2 or any(t not in g for t in terminals): raise ValueError("invalid terminals")
    edges=_edges(g); rng=random.Random(seed); success=0
    for _ in range(int(trials)):
        failed=[e for e in edges if rng.random()>p]
        success+=int(_connected(_remove(g,failed),terminals))
    estimate=success/trials; se=(estimate*(1-estimate)/trials)**0.5
    return {"estimate":estimate,"standard_error":se,
        "confidence_interval_95":(max(0,estimate-1.96*se),min(1,estimate+1.96*se)),
        "successes":success,"trials":int(trials),"edge_survival_probability":p,"seed":seed,
        "reliability_type":"all-terminal" if terminals is None else "k-terminal"}

def minimal_edge_cut_sets(adjacency, terminals=None, max_edges=20):
    """Exhaustive inclusion-minimal cut enumeration; exponential, small graphs only."""
    g=_graph(adjacency); edges=_edges(g)
    if isinstance(max_edges,bool) or int(max_edges)!=max_edges or max_edges<0: raise ValueError("max_edges must be nonnegative integer")
    if len(edges)>max_edges: raise ValueError(f"{len(edges)} edges exceeds limit {max_edges}")
    if terminals is not None:
        terminals=tuple(terminals)
        if len(terminals)<2 or any(t not in g for t in terminals): raise ValueError("invalid terminals")
    if not _connected(g,terminals): raise ValueError("intact graph must satisfy requested connectivity")
    cuts=[]
    for k in range(1,len(edges)+1):
        for candidate in combinations(edges,k):
            cs=set(candidate)
            if any(set(c).issubset(cs) for c in cuts): continue
            if not _connected(_remove(g,cs),terminals): cuts.append(candidate)
    return cuts
