"""Weiler–Atherton polygon intersection for simple non-degenerate rings.

Supports proper transverse crossings, concavity and disconnected area outputs.
Touching/collinear events and holes are rejected explicitly.
"""
from dataclasses import dataclass
from math import isfinite, hypot
from collections.abc import Sequence

Point = tuple[float, float]


@dataclass
class Node:
    point: Point
    crossing: bool = False
    entry: bool = False
    visited: bool = False
    next: "Node | None" = None
    prev: "Node | None" = None
    partner: "Node | None" = None


def _cross(a, b, c):
    return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])


def _area(ring):
    return sum(ring[i][0]*ring[(i+1)%len(ring)][1] -
               ring[(i+1)%len(ring)][0]*ring[i][1]
               for i in range(len(ring))) / 2


def _inside(p, ring):
    x,y=p
    inside=False
    for i,a in enumerate(ring):
        b=ring[(i+1)%len(ring)]
        if (a[1]>y)!=(b[1]>y):
            xi=a[0]+(y-a[1])*(b[0]-a[0])/(b[1]-a[1])
            if x < xi:
                inside=not inside
    return inside


def _prepare(points, label, eps):
    ring=[]
    for p in points:
        if len(p)!=2 or not all(isfinite(float(x)) for x in p):
            raise ValueError(f"{label} must contain finite 2D points")
        q=(float(p[0]),float(p[1]))
        if not ring or hypot(q[0]-ring[-1][0],q[1]-ring[-1][1])>eps:
            ring.append(q)
    if len(ring)>1 and hypot(ring[0][0]-ring[-1][0],ring[0][1]-ring[-1][1])<=eps:
        ring.pop()
    if len(ring)<3 or len(set(ring))!=len(ring):
        raise ValueError(f"{label} must be a simple ring with at least three vertices")
    n=len(ring)
    for i in range(n):
        for j in range(i+1,n):
            if j==i+1 or (i==0 and j==n-1):
                continue
            if _segment_event(ring[i],ring[(i+1)%n],ring[j],ring[(j+1)%n],eps,True):
                raise ValueError(f"{label} must be a simple ring")
    area=_area(ring)
    if abs(area)<=eps:
        raise ValueError(f"{label} must have non-zero area")
    return ring if area>0 else ring[::-1]


def _segment_event(a,b,c,d,eps,allow_touch=False):
    r=(b[0]-a[0],b[1]-a[1]); s=(d[0]-c[0],d[1]-c[1])
    den=r[0]*s[1]-r[1]*s[0]
    q=(c[0]-a[0],c[1]-a[1])
    if abs(den)<=eps:
        col=abs(q[0]*r[1]-q[1]*r[0])<=eps
        if col and allow_touch:
            if (max(min(a[0],b[0]),min(c[0],d[0])) <= min(max(a[0],b[0]),max(c[0],d[0]))+eps
                and max(min(a[1],b[1]),min(c[1],d[1])) <= min(max(a[1],b[1]),max(c[1],d[1]))+eps):
                return ("touch",)
        return None
    t=(q[0]*s[1]-q[1]*s[0])/den
    u=(q[0]*r[1]-q[1]*r[0])/den
    if -eps<=t<=1+eps and -eps<=u<=1+eps:
        if t<=eps or t>=1-eps or u<=eps or u>=1-eps:
            return ("touch",)
        return (t,u,(a[0]+t*r[0],a[1]+t*r[1]))
    return None


def _ring_nodes(points):
    nodes=[Node(p) for p in points]
    for i,n in enumerate(nodes):
        n.next=nodes[(i+1)%len(nodes)]
        n.prev=nodes[(i-1)%len(nodes)]
    return nodes


def _walk(start):
    node=start
    while True:
        yield node
        node=node.next
        if node is start:
            break


def _insert(base, events):
    for i, items in enumerate(events):
        previous=base[i]
        for t,node in sorted(items,key=lambda x:x[0]):
            following=previous.next
            previous.next=node; node.prev=previous
            node.next=following; following.prev=node
            previous=node


def _clean(points,eps):
    out=[]
    for p in points:
        if not out or hypot(p[0]-out[-1][0],p[1]-out[-1][1])>eps:
            out.append(p)
    if len(out)>1 and hypot(out[0][0]-out[-1][0],out[0][1]-out[-1][1])<=eps:
        out.pop()
    if len(out)>=3 and _area(out)<0:
        out.reverse()
    return out


def weiler_atherton_intersection(subject: Sequence[Point],
                                  clip: Sequence[Point], *,
                                  epsilon: float=1e-9) -> list[list[Point]]:
    """Return CCW intersection components for two simple polygon rings.

    Handles concave polygons, proper crossings, containment and disjointness.
    Point/edge touches, collinear overlaps, self-intersections and holes are
    outside this implementation's contract and raise explicit exceptions.
    """
    if not isfinite(epsilon) or epsilon<=0:
        raise ValueError("epsilon must be finite and positive")
    a=_prepare(subject,"subject",epsilon); b=_prepare(clip,"clip",epsilon)
    an,bn=_ring_nodes(a),_ring_nodes(b)
    ae=[[] for _ in a]; be=[[] for _ in b]
    intersections=0
    for i,p in enumerate(a):
        for j,q in enumerate(b):
            event=_segment_event(p,a[(i+1)%len(a)],q,b[(j+1)%len(b)],epsilon)
            if event is None:
                continue
            if event[0]=="touch":
                raise NotImplementedError("vertex touches and collinear overlaps are unsupported")
            ta,tb,point=event
            x,y=Node(point,True),Node(point,True)
            x.partner=y; y.partner=x
            ae[i].append((ta,x)); be[j].append((tb,y))
            intersections+=1
    if intersections==0:
        if _inside(a[0],b): return [a]
        if _inside(b[0],a): return [b]
        return []
    _insert(an,ae); _insert(bn,be)

    # Entry/exit classification is determined by the immediately following
    # arc, avoiding orientation assumptions about the input rings.
    for n in _walk(an[0]):
        if n.crossing:
            mid=((n.point[0]+n.next.point[0])/2,(n.point[1]+n.next.point[1])/2)
            n.entry=_inside(mid,b)
    for n in _walk(bn[0]):
        if n.crossing:
            mid=((n.point[0]+n.next.point[0])/2,(n.point[1]+n.next.point[1])/2)
            n.entry=_inside(mid,a)

    # Weiler–Atherton traversal: follow an interior boundary arc to the next
    # crossing, transfer to the paired boundary, and continue its interior arc.
    outputs=[]
    for start in _walk(an[0]):
        if not start.crossing or not start.entry or start.visited:
            continue
        ring=[]; current=start; forward=True
        while True:
            if current.visited:
                break
            ring.append(current.point)
            current.visited=True
            if current.crossing:
                paired=current.partner
                if paired is None or paired.visited:
                    break
                paired.visited=True
                current=paired
                # The paired event's following arc determines whether the
                # interior clip/subject boundary is traversed forward or back.
                forward=current.entry
            current=current.next if forward else current.prev
            if current is start:
                break
        cleaned=_clean(ring,epsilon)
        if len(cleaned)>=3 and abs(_area(cleaned))>epsilon:
            outputs.append(cleaned)
    return outputs
