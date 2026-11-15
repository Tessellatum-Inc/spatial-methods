"""Normalized-Laplacian spectral bisection with a normalized-cut sweep."""
from __future__ import annotations
import math
from collections.abc import Mapping
from numbers import Real
import numpy as np

def _adj(graph):
    nodes=list(graph); seen=set(nodes); directed={}
    for val in graph.values():
        for v in (val.keys() if isinstance(val,Mapping) else val):
            if v not in seen: nodes.append(v); seen.add(v)
    for u,val in graph.items():
        items=val.items() if isinstance(val,Mapping) else ((v,1.) for v in val)
        for v,w in items:
            if u==v: continue
            if isinstance(w,bool) or not isinstance(w,Real) or not math.isfinite(float(w)) or w<0:
                raise ValueError("weights must be finite and non-negative")
            directed[u,v]=float(w)
    adj={u:{} for u in nodes}
    for pair in {frozenset((u,v)) for u,v in directed}:
        u,v=tuple(pair); ws=[x for x in (directed.get((u,v)),directed.get((v,u))) if x is not None]
        w=sum(ws)/len(ws)
        if w: adj[u][v]=w; adj[v][u]=w
    return adj

def spectral_bisection(graph):
    """Split an undirected weighted graph using the normalized Fiedler vector.

    Returns two non-empty sets. Among all sweep cuts induced by sorted Fiedler
    coordinates, selects the minimum normalized cut. Isolates are assigned to
    the currently smaller side after the positive-degree subgraph is split.
    """
    adj=_adj(graph); nodes=list(adj)
    if len(nodes)<2: raise ValueError("at least two vertices are required")
    active=[u for u in nodes if adj[u]]
    isolates=[u for u in nodes if not adj[u]]
    if len(active)<2:
        ordered=sorted(nodes,key=lambda x:(type(x).__name__,repr(x)))
        mid=len(ordered)//2
        return set(ordered[:mid]),set(ordered[mid:])
    index={u:i for i,u in enumerate(active)}; n=len(active)
    a=np.zeros((n,n),dtype=float)
    for u in active:
        for v,w in adj[u].items():
            if v in index: a[index[u],index[v]]=w
    degree=a.sum(axis=1)
    inv=np.diag(1.0/np.sqrt(degree))
    lap=np.eye(n)-inv@a@inv
    values,vectors=np.linalg.eigh(lap)
    fiedler=vectors[:,1]
    order=sorted(range(n),key=lambda i:(float(fiedler[i]),i))
    total=float(degree.sum()); best=None
    for cut in range(1,n):
        left_idx=order[:cut]; right_idx=order[cut:]
        left={active[i] for i in left_idx}; right={active[i] for i in right_idx}
        vol_l=float(sum(degree[i] for i in left_idx)); vol_r=total-vol_l
        if vol_l<=0 or vol_r<=0: continue
        crossing=sum(w for u in left for v,w in adj[u].items() if v in right)
        score=crossing/vol_l+crossing/vol_r
        candidate=(score,abs(len(left)-len(right)),cut,left,right)
        if best is None or candidate[:3]<best[:3]: best=candidate
    if best is None:
        ordered=sorted(active,key=lambda x:(type(x).__name__,repr(x)))
        left,right=set(ordered[:n//2]),set(ordered[n//2:])
    else:
        left,right=set(best[3]),set(best[4])
    for u in isolates:
        (left if len(left)<=len(right) else right).add(u)
    return left,right
