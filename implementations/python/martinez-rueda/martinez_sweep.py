"""Sweep-line event and segment-splitting core for polygon overlay."""
from dataclasses import dataclass
from math import isfinite

@dataclass(frozen=True)
class Segment:
    source: int
    ring: int
    index: int
    a: tuple
    b: tuple

@dataclass(frozen=True)
class Event:
    point: tuple
    kind: str
    segment_ids: tuple

@dataclass(frozen=True)
class SplitSegment:
    source: int
    ring: int
    index: int
    a: tuple
    b: tuple
    t0: float
    t1: float

def _left_right(a,b):
    return (a,b) if a<=b else (b,a)

def _intersection(s1,s2,eps):
    a,b,c,d=s1.a,s1.b,s2.a,s2.b
    r=(b[0]-a[0],b[1]-a[1]); q=(d[0]-c[0],d[1]-c[1])
    den=r[0]*q[1]-r[1]*q[0]; ca=(c[0]-a[0],c[1]-a[1])
    if abs(den)<=eps:
        if abs(ca[0]*r[1]-ca[1]*r[0])<=eps:
            overlap=(max(min(a[0],b[0]),min(c[0],d[0])) <= min(max(a[0],b[0]),max(c[0],d[0]))+eps and
                     max(min(a[1],b[1]),min(c[1],d[1])) <= min(max(a[1],b[1]),max(c[1],d[1]))+eps)
            if overlap: raise NotImplementedError("collinear segment overlap is unsupported")
        return None
    t=(ca[0]*q[1]-ca[1]*q[0])/den
    u=(ca[0]*r[1]-ca[1]*r[0])/den
    if -eps<=t<=1+eps and -eps<=u<=1+eps:
        t=max(0.,min(1.,t)); u=max(0.,min(1.,u))
        p=(a[0]+t*r[0],a[1]+t*r[1])
        proper=eps<t<1-eps and eps<u<1-eps
        return t,u,p,proper
    return None

def sweep_split_segments(polygons, *, epsilon=1e-10):
    """Return x-ordered endpoint events, proper crossings and split fragments.

    polygons is [source][ring][point]. Active x-overlap pairs are tested on
    insertion. This transparent front end is quadratic in the worst case;
    it is not the complete Martinez–Rueda neighbour-updating algorithm.
    """
    if not isfinite(epsilon) or epsilon<=0: raise ValueError("epsilon must be finite and positive")
    segments=[]
    for source,rings in enumerate(polygons):
        for rid,ring in enumerate(rings):
            pts=[]
            for p in ring:
                if len(p)!=2 or not all(isfinite(float(v)) for v in p):
                    raise ValueError("rings require finite 2D coordinates")
                pts.append((float(p[0]),float(p[1])))
            if len(pts)<3 or len(set(pts))<3: raise ValueError("rings need three distinct points")
            for i,a in enumerate(pts):
                b=pts[(i+1)%len(pts)]
                if a==b: raise ValueError("zero-length edges are unsupported")
                segments.append(Segment(source,rid,i,a,b))
    bounds=[]; events=[]; by_id={}
    for sid,s in enumerate(segments):
        left,right=_left_right(s.a,s.b)
        item=(left[0],right[0],sid,left,right); bounds.append(item); by_id[sid]=item
        events.extend((Event(left,"left",(sid,)),Event(right,"right",(sid,))))
    bounds.sort(key=lambda x:(x[0],x[3][1],x[1],x[2]))
    active=set(); params=[[(0.,s.a),(1.,s.b)] for s in segments]; crossings=[]
    for xmin,xmax,sid,left,right in bounds:
        active={other for other in active if by_id[other][1]>=xmin-epsilon}
        for other in sorted(active):
            s1,s2=segments[sid],segments[other]
            if s1.source==s2.source: continue
            hit=_intersection(s1,s2,epsilon)
            if hit is None: continue
            t,u,p,proper=hit
            params[sid].append((t,p)); params[other].append((u,p))
            if proper: crossings.append(Event(p,"intersection",tuple(sorted((sid,other)))))
        active.add(sid)
    fragments=[]
    for sid,s in enumerate(segments):
        ordered=sorted(params[sid],key=lambda z:z[0]); unique=[]
        for t,p in ordered:
            if not unique or abs(t-unique[-1][0])>epsilon: unique.append((t,p))
        for (t0,a),(t1,b) in zip(unique,unique[1:]):
            if t1-t0>epsilon and a!=b:
                fragments.append(SplitSegment(s.source,s.ring,s.index,a,b,t0,t1))
    crossings.sort(key=lambda e:(e.point[0],e.point[1],e.segment_ids))
    events.sort(key=lambda e:(e.point[0],e.point[1],0 if e.kind=="left" else 1))
    return {"segments":tuple(segments),"events":tuple(events),
            "intersection_events":tuple(crossings),"split_segments":tuple(fragments)}
