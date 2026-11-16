import math, random
from collections.abc import Mapping
from numbers import Real

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
    out={u:{} for u in nodes}
    for pair in {frozenset((u,v)) for u,v in directed}:
        u,v=tuple(pair); ws=[x for x in (directed.get((u,v)),directed.get((v,u))) if x is not None]
        w=sum(ws)/len(ws)
        if w: out[u][v]=w; out[v][u]=w
    return out

def _move(adj,gamma,rng,passes):
    ns=list(adj); deg={u:sum(adj[u].values()) for u in ns}; m2=sum(deg.values())
    labels={u:i for i,u in enumerate(ns)}
    if not m2: return labels
    totals={labels[u]:deg[u] for u in ns}
    for _ in range(passes):
        changed=False; order=ns[:]; rng.shuffle(order)
        for u in order:
            old=labels[u]; ku=deg[u]; links={}
            for v,w in adj[u].items():
                c=labels[v]; links[c]=links.get(c,0.)+w
            totals[old]-=ku; best=old; best_gain=0.
            for c,kin in links.items():
                gain=kin-gamma*ku*totals.get(c,0.)/m2
                if gain>best_gain+1e-12: best,best_gain=c,gain
            labels[u]=best; totals[best]=totals.get(best,0.)+ku
            changed |= best!=old
        if not changed: break
    return labels

def louvain_communities(graph,*,resolution=1.,seed=0,max_levels=100,max_passes=100):
    if isinstance(resolution,bool) or not isinstance(resolution,Real) or not math.isfinite(float(resolution)) or resolution<=0:
        raise ValueError("resolution must be finite and positive")
    for name,n in (("max_levels",max_levels),("max_passes",max_passes)):
        if isinstance(n,bool) or not isinstance(n,int) or n<=0: raise ValueError(name+" must be positive")
    adj=_adj(graph); members={u:{u} for u in adj}
    if not adj: return []
    rng=random.Random(seed)
    for _ in range(max_levels):
        labels=_move(adj,float(resolution),rng,max_passes); groups={}
        for u,c in labels.items(): groups.setdefault(c,[]).append(u)
        if len(groups)==len(adj): break
        newmem={c:set().union(*(members[u] for u in group)) for c,group in groups.items()}
        newadj={c:{} for c in groups}
        for u,edges in adj.items():
            cu=labels[u]
            for v,w in edges.items():
                cv=labels[v]
                if cu!=cv:
                    newadj[cu][cv]=newadj[cu].get(cv,0.)+w
                else:
                    # Preserve contracted internal edges as doubled self-loop
                    # weight so supernode strength and modularity are conserved.
                    newadj[cu][cu]=newadj[cu].get(cu,0.)+w
        adj,members=newadj,newmem
    result=list(members.values())
    result.sort(key=lambda g:min((type(x).__name__,repr(x)) for x in g))
    return result

def modularity(graph,communities,resolution=1.):
    if isinstance(resolution,bool) or not isinstance(resolution,Real) or not math.isfinite(float(resolution)) or resolution<=0:
        raise ValueError("resolution must be finite and positive")
    adj=_adj(graph); groups=[set(c) for c in communities]; flat=[u for c in groups for u in c]
    if len(flat)!=len(set(flat)) or set(flat)!=set(adj): raise ValueError("communities must partition all nodes")
    m2=sum(sum(e.values()) for e in adj.values())
    if not m2: return 0.
    deg={u:sum(e.values()) for u,e in adj.items()}; q=0.
    for group in groups:
        internal=sum(w for u in group for v,w in adj[u].items() if v in group)
        volume=sum(deg[u] for u in group)
        q+=internal/m2-resolution*(volume/m2)**2
    return q
