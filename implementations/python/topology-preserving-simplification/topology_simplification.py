"""Topology-checked Visvalingam simplification for one simple polygon ring."""
from __future__ import annotations
from fractions import Fraction
from heapq import heappop, heappush
from math import isfinite
from typing import Sequence

Point = tuple[float, float]

def _orient(a, b, c):
    ax,ay,bx,by,cx,cy = (Fraction(str(v)) for p in (a,b,c) for v in p)
    q=(bx-ax)*(cy-ay)-(by-ay)*(cx-ax)
    return (q>0)-(q<0)

def _on(a,b,p):
    return _orient(a,b,p)==0 and min(a[0],b[0])<=p[0]<=max(a[0],b[0]) and min(a[1],b[1])<=p[1]<=max(a[1],b[1])

def _hit(a,b,c,d):
    o1,o2,o3,o4=_orient(a,b,c),_orient(a,b,d),_orient(c,d,a),_orient(c,d,b)
    if (o1==0 and _on(a,b,c)) or (o2==0 and _on(a,b,d)) or (o3==0 and _on(c,d,a)) or (o4==0 and _on(c,d,b)): return True
    return o1*o2<0 and o3*o4<0

def _area2(p):
    q=[(Fraction(str(x)),Fraction(str(y))) for x,y in p]
    return sum(q[i][0]*q[(i+1)%len(q)][1]-q[(i+1)%len(q)][0]*q[i][1] for i in range(len(q)))

def _simple(p):
    n=len(p)
    if n<3 or len(set(p))!=n or _area2(p)==0: return False
    for i in range(n):
        for j in range(i+1,n):
            if j==i+1 or (i==0 and j==n-1): continue
            if _hit(p[i],p[(i+1)%n],p[j],p[(j+1)%n]): return False
    return True

def _tri(a,b,c):
    return abs((b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0]))/2

def simplify_ring(points: Sequence[Sequence[float]], area_threshold: float) -> list[Point]:
    """Simplify a simple ring; threshold is triangle area in squared units.

    Exact rational orientation predicates reject topology-changing chords.
    This is a single-ring method, not polygon coverage or shell-hole
    simplification. Worst-case complexity is O(n^2 log n).
    """
    if not isfinite(area_threshold) or area_threshold<0: raise ValueError("area_threshold must be finite and non-negative")
    raw=[]
    for p in points:
        if len(p)!=2: raise ValueError("each coordinate must contain x and y")
        q=(float(p[0]),float(p[1]))
        if not all(isfinite(v) for v in q): raise ValueError("coordinates must be finite")
        raw.append(q)
    closed=len(raw)>1 and raw[0]==raw[-1]
    p=raw[:-1] if closed else raw
    if not p: return []
    if not _simple(p): raise ValueError("input must be a simple non-zero-area ring")
    n=len(p); prev=[(i-1)%n for i in range(n)]; nxt=[(i+1)%n for i in range(n)]
    alive=[True]*n; version=[0]*n; heap=[]; count=n
    def push(i,floor):
        if not alive[i] or count<=3: return
        version[i]+=1
        heappush(heap,(max(floor,_tri(p[prev[i]],p[i],p[nxt[i]])),i,version[i]))
    for i in range(n): push(i,0.0)
    floor=0.0; original_sign=_area2(p)>0
    while heap and count>3:
        area,i,v=heappop(heap)
        if not alive[i] or version[i]!=v: continue
        if area>area_threshold: break
        left,right=prev[i],nxt[i]; blocked=False
        for j in range(n):
            if not alive[j]: continue
            k=nxt[j]
            if not alive[k] or j in (left,i,right) or k in (left,i,right): continue
            if _hit(p[left],p[right],p[j],p[k]): blocked=True; break
        if blocked: continue
        trial=[p[j] for j in range(n) if alive[j] and j!=i]
        area2=_area2(trial)
        if area2==0 or (area2>0)!=original_sign: continue
        alive[i]=False; count-=1; nxt[left]=right; prev[right]=left
        floor=max(floor,area); push(left,floor); push(right,floor)
    result=[p[i] for i in range(n) if alive[i]]
    return result+[result[0]] if closed else result
