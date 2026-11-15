"""Sweep-line event and segment-splitting core for polygon overlay."""
from dataclasses import dataclass
from fractions import Fraction
from math import isfinite, atan2, pi

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

@dataclass
class _IntervalNode:
    low: float
    high: float
    sid: int
    priority: int
    left: object = None
    right: object = None
    max_high: float = 0.0

def _refresh(node):
    if node is not None:
        node.max_high=max(node.high,
            node.left.max_high if node.left is not None else float('-inf'),
            node.right.max_high if node.right is not None else float('-inf'))
    return node

def _priority(sid):
    # SplitMix64 finalizer gives reproducible, well-dispersed treap priorities.
    x=(sid+0x9E3779B97F4A7C15)&0xFFFFFFFFFFFFFFFF
    x=((x^(x>>30))*0xBF58476D1CE4E5B9)&0xFFFFFFFFFFFFFFFF
    x=((x^(x>>27))*0x94D049BB133111EB)&0xFFFFFFFFFFFFFFFF
    return x^(x>>31)

def _rotate_right(root):
    child=root.left; root.left=child.right; child.right=_refresh(root)
    return _refresh(child)

def _rotate_left(root):
    child=root.right; root.right=child.left; child.left=_refresh(root)
    return _refresh(child)

def _interval_insert(root,node):
    if root is None: return node
    if (node.low,node.sid)<(root.low,root.sid):
        root.left=_interval_insert(root.left,node)
        if root.left.priority<root.priority: root=_rotate_right(root)
    else:
        root.right=_interval_insert(root.right,node)
        if root.right.priority<root.priority: root=_rotate_left(root)
    return _refresh(root)

def _interval_merge(left,right):
    if left is None: return right
    if right is None: return left
    if left.priority<right.priority:
        left.right=_interval_merge(left.right,right); return _refresh(left)
    right.left=_interval_merge(left,right.left); return _refresh(right)

def _interval_delete(root,key):
    if root is None: return None
    here=(root.low,root.sid)
    if key<here: root.left=_interval_delete(root.left,key)
    elif key>here: root.right=_interval_delete(root.right,key)
    else: return _interval_merge(root.left,root.right)
    return _refresh(root)

class _YIntervalStatus:
    """Dynamic interval treap; overlap reporting is expected O(log n + k)."""
    def __init__(self): self.root=None; self.keys={}
    def insert(self,sid,low,high):
        node=_IntervalNode(low,high,sid,_priority(sid),max_high=high)
        self.root=_interval_insert(self.root,node); self.keys[sid]=(low,sid)
    def remove(self,sid):
        key=self.keys.pop(sid); self.root=_interval_delete(self.root,key)
    def overlaps(self,low,high):
        found=[]
        def visit(node):
            if node is None or node.max_high<low: return
            if node.left is not None and node.left.max_high>=low: visit(node.left)
            if node.low<=high and node.high>=low: found.append(node.sid)
            if node.low<=high: visit(node.right)
        visit(self.root)
        return found

def _left_right(a,b):
    return (a,b) if a<=b else (b,a)

def _intersection(s1,s2,eps):
    """Exact-rational segment predicate for decimal-coordinate input.

    Coordinates are interpreted as their shortest round-trip decimal strings.
    Determinants and intersection parameters are exact; epsilon is used only
    for endpoint/overlap tolerance and proper-crossing classification.
    """
    a,b,c,d=s1.a,s1.b,s2.a,s2.b
    aa=tuple(Fraction(str(v)) for v in a)
    bb=tuple(Fraction(str(v)) for v in b)
    cc=tuple(Fraction(str(v)) for v in c)
    dd=tuple(Fraction(str(v)) for v in d)
    r=(bb[0]-aa[0],bb[1]-aa[1])
    q=(dd[0]-cc[0],dd[1]-cc[1])
    den=r[0]*q[1]-r[1]*q[0]
    ca=(cc[0]-aa[0],cc[1]-aa[1])
    tolerance=Fraction(str(eps))
    if den==0:
        if ca[0]*r[1]-ca[1]*r[0]==0:
            axis=0 if abs(r[0])>=abs(r[1]) else 1
            overlap_length=min(max(aa[axis],bb[axis]),max(cc[axis],dd[axis]))-max(min(aa[axis],bb[axis]),min(cc[axis],dd[axis]))
            if overlap_length>tolerance:
                raise NotImplementedError("collinear segment overlap is unsupported")
            if overlap_length>=-tolerance:
                candidates=set((aa,bb)) & set((cc,dd))
                if candidates:
                    p=next(iter(candidates))
                    return (Fraction(0) if p==aa else Fraction(1),
                            Fraction(0) if p==cc else Fraction(1),
                            (float(p[0]),float(p[1])),False)
        return None
    t=(ca[0]*q[1]-ca[1]*q[0])/den
    u=(ca[0]*r[1]-ca[1]*r[0])/den
    if -tolerance<=t<=1+tolerance and -tolerance<=u<=1+tolerance:
        t=max(Fraction(0),min(Fraction(1),t))
        u=max(Fraction(0),min(Fraction(1),u))
        p=(aa[0]+t*r[0],aa[1]+t*r[1])
        proper=tolerance<t<1-tolerance and tolerance<u<1-tolerance
        return t,u,(float(p[0]),float(p[1])),proper
    return None

def _validate_polygon_rings(rings,eps):
    if not rings: raise ValueError('each polygon source needs one shell ring')
    shell=rings[0]
    for hole in rings[1:]:
        if not all(_inside(p,shell) for p in hole):
            raise ValueError('every hole vertex must lie strictly inside the shell')
    for i in range(len(rings)):
        for j in range(i+1,len(rings)):
            a,b=rings[i],rings[j]
            for k in range(len(a)):
                s1=Segment(0,i,k,a[k],a[(k+1)%len(a)])
                for m in range(len(b)):
                    s2=Segment(1,j,m,b[m],b[(m+1)%len(b)])
                    try: hit=_intersection(s1,s2,eps)
                    except NotImplementedError: raise ValueError('rings in one polygon may not share collinear boundary segments')
                    if hit is not None: raise ValueError('shell and hole boundaries must not touch or cross')
            if i>0 and (_inside(a[0],b) or _inside(b[0],a)):
                raise ValueError('holes must be disjoint and non-nested')
    return rings

def _inside_polygon(point,rings):
    return _inside(point,rings[0]) and not any(_inside(point,hole) for hole in rings[1:])

def _signed_area(ring):
    return 0.5*sum(ring[i][0]*ring[(i+1)%len(ring)][1] - ring[(i+1)%len(ring)][0]*ring[i][1] for i in range(len(ring)))

def _cross(a,b,c):
    return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])

def _on_segment(a,b,p,eps):
    return (min(a[0],b[0])-eps<=p[0]<=max(a[0],b[0])+eps and min(a[1],b[1])-eps<=p[1]<=max(a[1],b[1])+eps)

def _ring_is_simple(ring,eps):
    n=len(ring)
    for i in range(n):
        a,b=ring[i],ring[(i+1)%n]
        for j in range(i+1,n):
            if j==i or j==(i+1)%n or (j+1)%n==i: continue
            d,e=ring[j],ring[(j+1)%n]
            o1,o2=_cross(a,b,d),_cross(a,b,e)
            o3,o4=_cross(d,e,a),_cross(d,e,b)
            proper=((o1>eps and o2< -eps) or (o1< -eps and o2>eps)) and ((o3>eps and o4< -eps) or (o3< -eps and o4>eps))
            touch=((abs(o1)<=eps and _on_segment(a,b,d,eps)) or (abs(o2)<=eps and _on_segment(a,b,e,eps)) or (abs(o3)<=eps and _on_segment(d,e,a,eps)) or (abs(o4)<=eps and _on_segment(d,e,b,eps)))
            if proper or touch: return False
    return True

def _inside(point, ring):
    x,y=point; inside=False
    for i,a in enumerate(ring):
        b=ring[(i+1)%len(ring)]
        if (a[1]>y)!=(b[1]>y):
            xcross=a[0]+(y-a[1])*(b[0]-a[0])/(b[1]-a[1])
            if x<xcross: inside=not inside
    return inside

def sweep_split_segments(polygons, *, epsilon=1e-10):
    """Return x-ordered endpoint events, proper crossings and split fragments.

    polygons is [source][ring][point]. An x-ordered sweep maintains a dynamic
    y-interval status and tests only cross-source bounding-box overlaps. This
    broad-phase status can still be quadratic in dense/overlapping data; it is
    not the complete Martinez–Rueda neighbour-event sweep.
    """
    if not isfinite(epsilon) or epsilon<=0: raise ValueError("epsilon must be finite and positive")
    segments=[]
    for source,rings in enumerate(polygons):
        prepared=[]
        for rid,ring in enumerate(rings):
            pts=[]
            for p in ring:
                if len(p)!=2 or not all(isfinite(float(v)) for v in p):
                    raise ValueError("rings require finite 2D coordinates")
                pts.append((float(p[0]),float(p[1])))
            if len(pts)<3 or len(set(pts))<3: raise ValueError("rings need three distinct points")
            if abs(_signed_area(pts))<=epsilon: raise ValueError("ring area must be non-zero")
            if not _ring_is_simple(pts,epsilon): raise ValueError("input rings must be simple and non-self-touching")
            prepared.append(pts)
        _validate_polygon_rings(prepared,epsilon)
        for rid,pts in enumerate(prepared):
            area=_signed_area(pts)
            # First ring is the shell (CCW); subsequent rings are holes (CW).
            if (rid==0 and area<0) or (rid>0 and area>0): pts.reverse()
            for i,a in enumerate(pts):
                b=pts[(i+1)%len(pts)]
                if a==b: raise ValueError("zero-length edges are unsupported")
                segments.append(Segment(source,rid,i,a,b))
    bounds=[]; events=[]; by_id={}
    for sid,s in enumerate(segments):
        left,right=_left_right(s.a,s.b)
        ymin,ymax=sorted((s.a[1],s.b[1]))
        item=(left[0],right[0],sid,left,right,ymin,ymax); bounds.append(item); by_id[sid]=item
        events.extend((Event(left,"left",(sid,)),Event(right,"right",(sid,))))
    bounds.sort(key=lambda x:(x[0],x[3][1],x[1],x[2]))
    # Dynamic y-interval treap prunes active segments whose vertical bounds
    # cannot overlap the entering segment. Exact predicates run on candidates.
    active_status=_YIntervalStatus(); active_by_id={}
    params=[[(0.,s.a),(1.,s.b)] for s in segments]; crossings=[]; candidate_pairs=0
    for xmin,xmax,sid,left,right,ymin,ymax in bounds:
        expired=[other for other,item in active_by_id.items() if item[0]<xmin-epsilon]
        for other in expired:
            active_status.remove(other); active_by_id.pop(other)
        for other in active_status.overlaps(ymin-epsilon,ymax+epsilon):
            s1,s2=segments[sid],segments[other]
            if s1.source==s2.source: continue
            candidate_pairs+=1
            hit=_intersection(s1,s2,epsilon)
            if hit is None: continue
            t,u,p,proper=hit
            params[sid].append((t,p)); params[other].append((u,p))
            if proper: crossings.append(Event(p,"intersection",tuple(sorted((sid,other)))))
        active_status.insert(sid,ymin,ymax); active_by_id[sid]=(xmax,ymin,ymax)
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
            "intersection_events":tuple(crossings),"split_segments":tuple(fragments),
            "candidate_pairs_tested":candidate_pairs}

def classify_boundary_fragments(polygons, *, operation='intersection', epsilon=1e-10):
    """Select directed fragments for two polygons, each with one shell and optional holes.
    Fragment stitching is performed by boolean_overlay_rings.
    """
    if operation not in {'intersection','union','difference','symmetric_difference'}:
        raise ValueError('unsupported Boolean operation')
    if len(polygons)!=2 or any(len(source)<1 for source in polygons):
        raise NotImplementedError('classification requires two polygon sources with one shell each')
    result=sweep_split_segments(polygons,epsilon=epsilon)
    rings=[]
    for source in polygons:
        source_rings=[[(float(p[0]),float(p[1])) for p in ring] for ring in source]
        for rid,ring in enumerate(source_rings):
            area=_signed_area(ring)
            if (rid==0 and area<0) or (rid>0 and area>0): ring.reverse()
        rings.append(source_rings)
    selected=[]
    for f in result['split_segments']:
        midpoint=((f.a[0]+f.b[0])/2,(f.a[1]+f.b[1])/2)
        inside=_inside_polygon(midpoint,rings[1-f.source])
        if operation=='intersection':
            keep=inside
        elif operation=='union':
            keep=not inside
        elif operation=='difference':
            keep=(not inside if f.source==0 else inside)
        else:
            keep=True
        if keep:
            reverse=(operation=='difference' and f.source==1) or (operation=='symmetric_difference' and inside)
            a,b=(f.b,f.a) if reverse else (f.a,f.b)
            t0,t1=(f.t1,f.t0) if reverse else (f.t0,f.t1)
            selected.append(SplitSegment(f.source,f.ring,f.index,a,b,t0,t1))
    return {'operation':operation,'selected_fragments':tuple(selected),
            'intersection_events':result['intersection_events']}

def fragment_area_contribution(fragments):
    """Signed shoelace contribution; meaningful when selected fragments close."""
    return 0.5*sum(f.a[0]*f.b[1]-f.b[0]*f.a[1] for f in fragments)

def stitch_boundary_fragments(fragments, *, epsilon=1e-10):
    """Stitch directed fragments into closed rings using a planar face walk.
    Raises rather than returning open or degenerate chains.
    """
    if not isfinite(epsilon) or epsilon<=0: raise ValueError('epsilon must be finite and positive')
    edges=list(fragments)
    if not edges: return tuple()
    def key(p): return (round(p[0]/epsilon),round(p[1]/epsilon))
    outgoing={}
    for i,e in enumerate(edges): outgoing.setdefault(key(e.a),[]).append(i)
    used=set(); rings=[]
    for first in range(len(edges)):
        if first in used: continue
        ring=[edges[first].a]; current=first; start_key=key(edges[first].a)
        for _ in range(len(edges)+1):
            if current in used: raise ValueError('fragment graph enters an already-used edge')
            used.add(current); edge=edges[current]; ring.append(edge.b)
            end_key=key(edge.b)
            if end_key==start_key:
                ring.pop(); break
            candidates=[i for i in outgoing.get(end_key,()) if i not in used]
            if not candidates: raise ValueError('selected boundary fragments contain an open chain')
            reverse_angle=atan2(edge.a[1]-edge.b[1],edge.a[0]-edge.b[0])
            def turn(i):
                nxt=edges[i]; angle=atan2(nxt.b[1]-nxt.a[1],nxt.b[0]-nxt.a[0])
                return ((reverse_angle-angle)%(2*pi),i)
            current=min(candidates,key=turn)
        else: raise ValueError('boundary traversal exceeded fragment count')
        if len(ring)<3 or abs(_signed_area(ring))<=epsilon: raise ValueError('stitched boundary is degenerate')
        rings.append(tuple(ring))
    if len(used)!=len(edges): raise ValueError('not all selected fragments were stitched')
    return tuple(rings)

def assemble_polygon_components(rings):
    """Group CCW shell rings with their directly contained CW hole rings.

    Positive rings become polygon shells. Each negative ring is assigned to
    the smallest-area shell that strictly contains one of its vertices.
    Islands inside holes remain independent polygon components.
    """
    shells=[ring for ring in rings if _signed_area(ring)>0]
    holes=[ring for ring in rings if _signed_area(ring)<0]
    components=[{'shell':shell,'holes':[]} for shell in shells]
    for hole in holes:
        probe=hole[0]
        parents=[(abs(_signed_area(item['shell'])),item)
                 for item in components if _inside(probe,item['shell'])]
        if not parents:
            raise ValueError('clockwise ring has no containing shell')
        min(parents,key=lambda item:item[0])[1]['holes'].append(hole)
    return tuple({'shell':item['shell'],'holes':tuple(item['holes'])}
                 for item in components)


def boolean_overlay_rings(polygons, *, operation='intersection', epsilon=1e-10):
    """Return oriented rings and explicit polygon components for two inputs."""
    classified=classify_boundary_fragments(polygons,operation=operation,epsilon=epsilon)
    rings=stitch_boundary_fragments(classified['selected_fragments'],epsilon=epsilon)
    components=assemble_polygon_components(rings)
    return {'operation':operation,'rings':rings,'polygons':components,
            'area':sum(_signed_area(ring) for ring in rings),
            'intersection_events':classified['intersection_events']}
