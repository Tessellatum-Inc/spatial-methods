"""Path-size logit choice probabilities for overlapping route alternatives."""
from __future__ import annotations
from collections import Counter
import math
import numpy as np

def path_size_factors(paths, edge_lengths=None):
    """PS_k = sum((length_a / path_length_k) / n_a) over edges in path k."""
    alternatives=[tuple(path) for path in paths]
    if not alternatives or any(not p for p in alternatives): raise ValueError("paths must contain non-empty alternatives")
    for p in alternatives:
        try: set(p)
        except TypeError as exc: raise ValueError("edge identifiers must be hashable") from exc
        if len(set(p))!=len(p): raise ValueError("a path may not repeat an edge")
    if edge_lengths is None: lengths={e:1.0 for p in alternatives for e in p}
    else:
        lengths={}
        for e in {e for p in alternatives for e in p}:
            if e not in edge_lengths: raise ValueError(f"missing length for edge {e!r}")
            value=float(edge_lengths[e])
            if not math.isfinite(value) or value<=0: raise ValueError("edge lengths must be finite and positive")
            lengths[e]=value
    counts=Counter(e for p in alternatives for e in set(p))
    result=np.empty(len(alternatives))
    for i,p in enumerate(alternatives):
        total=sum(lengths[e] for e in p)
        result[i]=sum((lengths[e]/total)/counts[e] for e in p)
    return result

def path_size_logit_probabilities(systematic_utilities,paths,*,scale=1.0,overlap_coefficient=1.0,edge_lengths=None):
    """Stable softmax of scaled systematic utility plus log path-size correction."""
    v=np.asarray(systematic_utilities,dtype=float)
    if v.ndim!=1 or v.size==0 or not np.isfinite(v).all(): raise ValueError("utilities must be a non-empty finite vector")
    if len(paths)!=v.size: raise ValueError("one path is required per utility")
    if not math.isfinite(scale) or scale<=0: raise ValueError("scale must be finite and positive")
    if not math.isfinite(overlap_coefficient) or overlap_coefficient<0: raise ValueError("overlap_coefficient must be finite and non-negative")
    ps=path_size_factors(paths,edge_lengths)
    z=scale*(v+overlap_coefficient*np.log(ps));z-=z.max()
    w=np.exp(z)
    return w/w.sum()

def path_size_log_likelihood(systematic_utilities,paths,chosen_index,*,scale=1.0,overlap_coefficient=1.0,edge_lengths=None):
    """Log probability of the observed alternative index."""
    if not isinstance(chosen_index,(int,np.integer)) or not 0<=chosen_index<len(paths): raise ValueError("chosen_index is outside alternatives")
    p=path_size_logit_probabilities(systematic_utilities,paths,scale=scale,overlap_coefficient=overlap_coefficient,edge_lengths=edge_lengths)
    return float(np.log(p[chosen_index]))
