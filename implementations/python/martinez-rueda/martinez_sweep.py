"""Sweep-line event and segment-splitting core for polygon overlay."""
from dataclasses import dataclass
import heapq
from fractions import Fraction
from math import isfinite
from functools import cmp_to_key

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
    t0: Fraction
    t1: Fraction

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

def _intersection_all(s1,s2,eps):
    """Return exact segment contacts and both endpoints of every overlap.

    Unlike the legacy scalar predicate, this routine never uses epsilon to
    decide whether two segments intersect. Epsilon must not erase a real
    sub-tolerance overlap or turn a near miss into a false contact.
    """
    aa,bb=_fraction_point(s1.a),_fraction_point(s1.b)
    cc,dd=_fraction_point(s2.a),_fraction_point(s2.b)
    rx,ry=bb[0]-aa[0],bb[1]-aa[1]
    sx,sy=dd[0]-cc[0],dd[1]-cc[1]
    qx,qy=cc[0]-aa[0],cc[1]-aa[1]
    den=rx*sy-ry*sx

    def parameter(a,b,p):
        dx,dy=b[0]-a[0],b[1]-a[1]
        axis=0 if abs(dx)>=abs(dy) else 1
        return (p[axis]-a[axis])/(b[axis]-a[axis])

    if den==0:
        if qx*ry-qy*rx!=0:
            return ()
        axis=0 if abs(rx)>=abs(ry) else 1
        low=max(min(aa[axis],bb[axis]),min(cc[axis],dd[axis]))
        high=min(max(aa[axis],bb[axis]),max(cc[axis],dd[axis]))
        if low>high:
            return ()
        def point_at(value):
            if axis==0:
                return (value,aa[1]+(value-aa[0])*ry/rx)
            return (aa[0]+(value-aa[1])*rx/ry,value)
        points=(point_at(low),) if low==high else (point_at(low),point_at(high))
        return tuple(
            (parameter(aa,bb,p),parameter(cc,dd,p),p,False)
            for p in points
        )

    t=(qx*sy-qy*sx)/den
    u=(qx*ry-qy*rx)/den
    if not (0<=t<=1 and 0<=u<=1):
        return ()
    point=(aa[0]+t*rx,aa[1]+t*ry)
    proper=0<t<1 and 0<u<1
    return ((t,u,point,proper),)


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
                    if _intersection_all(s1,s2,eps):
                        raise ValueError('shell and hole boundaries must not touch or cross')
            if i>0 and (_inside(a[0],b) or _inside(b[0],a)):
                raise ValueError('holes must be disjoint and non-nested')
    return rings

def _inside_polygon(point,rings):
    return _inside(point,rings[0]) and not any(_inside(point,hole) for hole in rings[1:])

def _signed_area_exact(ring):
    """Exact signed shoelace area over decimal coordinate representations."""
    total=Fraction(0)
    for i,a in enumerate(ring):
        b=ring[(i+1)%len(ring)]
        ax,ay=_fraction_point(a); bx,by=_fraction_point(b)
        total += ax*by-bx*ay
    return total/2

def _signed_area(ring):
    return float(_signed_area_exact(ring))

def _fraction_value(value):
    return value if isinstance(value,Fraction) else Fraction(str(value))

def _fraction_point(point):
    return (_fraction_value(point[0]),_fraction_value(point[1]))

def _orientation(a,b,c):
    """Exact orientation sign over shortest round-trip decimal coordinates."""
    ax,ay=_fraction_point(a); bx,by=_fraction_point(b); cx,cy=_fraction_point(c)
    value=(bx-ax)*(cy-ay)-(by-ay)*(cx-ax)
    return (value>0)-(value<0)

def _on_segment_exact(a,b,p):
    if _orientation(a,b,p)!=0: return False
    ax,ay=_fraction_point(a); bx,by=_fraction_point(b); px,py=_fraction_point(p)
    return min(ax,bx)<=px<=max(ax,bx) and min(ay,by)<=py<=max(ay,by)

def _segments_intersect_exact(a,b,c,d):
    o1,o2=_orientation(a,b,c),_orientation(a,b,d)
    o3,o4=_orientation(c,d,a),_orientation(c,d,b)
    if o1==0 and _on_segment_exact(a,b,c): return True
    if o2==0 and _on_segment_exact(a,b,d): return True
    if o3==0 and _on_segment_exact(c,d,a): return True
    if o4==0 and _on_segment_exact(c,d,b): return True
    return o1*o2<0 and o3*o4<0

def _ring_is_simple(ring,eps):
    """Reject non-adjacent edge intersections using exact decimal predicates.

    eps remains in the signature for API compatibility; exact orientation
    signs are not compared to a dimensionally incompatible area tolerance.
    """
    n=len(ring)
    for i in range(n):
        previous,current,following=ring[i-1],ring[i],ring[(i+1)%n]
        if (_orientation(previous,current,following)==0 and
                (_on_segment_exact(previous,current,following) or
                 _on_segment_exact(current,following,previous))):
            return False
    for i in range(n):
        a,b=ring[i],ring[(i+1)%n]
        for j in range(i+1,n):
            if j==(i+1)%n or (j+1)%n==i: continue
            c,d=ring[j],ring[(j+1)%n]
            if _segments_intersect_exact(a,b,c,d): return False
    return True

def _inside(point, ring):
    """Exact even-odd point-in-ring test; boundary points are outside.

    Coordinates are interpreted as their shortest round-trip decimal strings.
    This strict-boundary convention is used for shell/hole containment.
    """
    px,py=_fraction_point(point); inside=False
    for i,a in enumerate(ring):
        b=ring[(i+1)%len(ring)]
        ax,ay=_fraction_point(a); bx,by=_fraction_point(b)
        if _on_segment_exact(a,b,point): return False
        if (ay>py)!=(by>py):
            lhs=(px-ax)*(by-ay)
            rhs=(py-ay)*(bx-ax)
            crosses_right = lhs<rhs if by>ay else lhs>rhs
            if crosses_right: inside=not inside
    return inside
def sweep_split_segments(polygons, *, epsilon=1e-10):
    """Return x-ordered endpoint events, proper crossings and split fragments.

    polygons is [source][ring][point]. An x-ordered sweep maintains a dynamic
    y-interval status and an expiry heap, testing cross-source bounding-box
    overlaps. This broad-phase status can still be quadratic in dense/overlapping
    data; it is not the complete Martinez–Rueda neighbour-event sweep.
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
                pts.append(_fraction_point(p))
            if len(pts)<3 or len(set(pts))<3: raise ValueError("rings need three distinct points")
            if _signed_area_exact(pts)==0: raise ValueError("ring area must be non-zero")
            if not _ring_is_simple(pts,epsilon): raise ValueError("input rings must be simple and non-self-touching")
            prepared.append(pts)
        _validate_polygon_rings(prepared,epsilon)
        for rid,pts in enumerate(prepared):
            area=_signed_area_exact(pts)
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
    active_status=_YIntervalStatus(); active_by_id={}; expiry=[]
    params=[[(Fraction(0),s.a),(Fraction(1),s.b)] for s in segments]
    crossings=[]; contacts=[]; candidate_pairs=0
    for xmin,xmax,sid,left,right,ymin,ymax in bounds:
        # Expire by a min-heap, not by scanning every active segment for every
        # new left endpoint. This keeps x-window maintenance O(log n) per edge.
        epsq=Fraction(str(epsilon))
        while expiry and expiry[0][0]<xmin-epsq:
            _,other=heapq.heappop(expiry)
            if other in active_by_id:
                active_status.remove(other); active_by_id.pop(other)
        for other in active_status.overlaps(ymin-epsq,ymax+epsq):
            s1,s2=segments[sid],segments[other]
            if s1.source==s2.source: continue
            candidate_pairs+=1
            for t,u,p,proper in _intersection_all(s1,s2,epsilon):
                params[sid].append((t,p)); params[other].append((u,p))
                pair=tuple(sorted((sid,other)))
                if proper:
                    crossings.append(Event(p,"intersection",pair))
                else:
                    contacts.append(Event(p,"contact",pair))
        active_status.insert(sid,ymin,ymax); active_by_id[sid]=(xmax,ymin,ymax)
        heapq.heappush(expiry,(xmax,sid))
    fragments=[]
    for sid,s in enumerate(segments):
        ordered=sorted(params[sid],key=lambda z:z[0]); unique=[]
        for t,p in ordered:
            # Parameters are exact Fractions: distinct intersections must not
            # be merged merely because their separation is smaller than epsilon.
            if not unique or t!=unique[-1][0]: unique.append((t,p))
        for (t0,a),(t1,b) in zip(unique,unique[1:]):
            if t1>t0 and a!=b:
                fragments.append(SplitSegment(s.source,s.ring,s.index,a,b,t0,t1))
    crossings.sort(key=lambda e:(e.point[0],e.point[1],e.segment_ids))
    # Coalesce pairwise reports at the same exact coordinate into one
    # multiway node event. Keep the legacy proper-crossing list unchanged.
    grouped={}
    for event in crossings+contacts:
        entry=grouped.setdefault(event.point,{"kinds":set(),"segments":set()})
        entry["kinds"].add(event.kind)
        entry["segments"].update(event.segment_ids)
    node_events=tuple(
        Event(point,"intersection" if "intersection" in data["kinds"] else "contact",
              tuple(sorted(data["segments"])))
        for point,data in sorted(grouped.items(),key=lambda item:(item[0][0],item[0][1]))
    )
    events.sort(key=lambda e:(e.point[0],e.point[1],0 if e.kind=="left" else 1))
    return {"segments":tuple(segments),"events":tuple(events),
            "intersection_events":tuple(crossings),"node_events":node_events,
            "split_segments":tuple(fragments),
            "candidate_pairs_tested":candidate_pairs}

def _point_segment_distance_squared(point, a, b):
    """Exact squared distance from a rational point to a closed segment."""
    px,py=point; ax,ay=_fraction_point(a); bx,by=_fraction_point(b)
    dx,dy=bx-ax,by-ay
    length2=dx*dx+dy*dy
    if length2==0:
        return (px-ax)**2+(py-ay)**2
    dot=(px-ax)*dx+(py-ay)*dy
    if dot<=0:
        return (px-ax)**2+(py-ay)**2
    if dot>=length2:
        return (px-bx)**2+(py-by)**2
    cross=dx*(py-ay)-dy*(px-ax)
    return cross*cross/length2


def _safe_side_probe_offset(midpoint, dx, dy, polygons):
    """Choose an exact side-probe distance below every non-collinear boundary.

    The midpoint is in the relative interior of an atomic fragment. Any
    boundary through it must therefore be collinear with that fragment.
    Those coincident bundle members are ignored; all other boundaries provide
    a positive clearance. The returned offset is strictly smaller than one
    quarter of that clearance and is independent of the user epsilon.
    """
    scale=max(abs(dx),abs(dy))
    if scale==0:
        return Fraction(0)
    clearance2=None
    for rings in polygons:
        for ring in rings:
            for i,a in enumerate(ring):
                b=ring[(i+1)%len(ring)]
                ax,ay=_fraction_point(a); bx,by=_fraction_point(b)
                if (bx-ax)*dy-(by-ay)*dx==0:
                    # Parallel edges need not be coincident; the distance
                    # calculation below still protects against nearby ones.
                    pass
                distance2=_point_segment_distance_squared(midpoint,a,b)
                if distance2==0:
                    # A zero-distance non-collinear contact is an unresolved
                    # event at the fragment interior, not a safe probe case.
                    if (bx-ax)*dy-(by-ay)*dx!=0:
                        raise ValueError("non-collinear boundary event remains inside an atomic fragment")
                    continue
                if clearance2 is None or distance2<clearance2:
                    clearance2=distance2
    # A finite rational fallback is used only when every boundary is collinear
    # with the current fragment (e.g. identical coincident polygon edges).
    offset=scale/Fraction(2**40)
    if clearance2 is not None:
        offset=min(offset,clearance2/(8*scale))
    return offset


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
        source_rings=[[(p[0],p[1]) for p in ring] for ring in source]
        for rid,ring in enumerate(source_rings):
            area=_signed_area_exact(ring)
            if (rid==0 and area<0) or (rid>0 and area>0): ring.reverse()
        rings.append(source_rings)
    selected=[]
    def result_filled(point):
        subject=_inside_polygon(point,rings[0])
        clip=_inside_polygon(point,rings[1])
        if operation=='intersection': return subject and clip
        if operation=='union': return subject or clip
        if operation=='difference': return subject and not clip
        return subject != clip
    for f in result['split_segments']:
        ax,ay=_fraction_point(f.a); bx,by=_fraction_point(f.b)
        dx,dy=bx-ax,by-ay
        scale=max(abs(dx),abs(dy))
        if scale==0: continue
        # The offset is bounded by the exact clearance to every
        # non-collinear source boundary. Unlike an epsilon-only probe, this
        # cannot jump across a narrow face merely because its width is below
        # the public tolerance.
        midpoint=((ax+bx)/2,(ay+by)/2)
        offset=_safe_side_probe_offset(midpoint,dx,dy,polygons)
        nx,ny=-dy*offset/scale,dx*offset/scale
        left=(midpoint[0]+nx,midpoint[1]+ny)
        right=(midpoint[0]-nx,midpoint[1]-ny)
        left_filled=result_filled(left)
        right_filled=result_filled(right)
        if left_filled==right_filled:
            continue
        reverse=not left_filled
        a,b=(f.b,f.a) if reverse else (f.a,f.b)
        t0,t1=(f.t1,f.t0) if reverse else (f.t0,f.t1)
        selected.append(SplitSegment(f.source,f.ring,f.index,a,b,t0,t1))
    # Coincident source boundaries can generate the same oriented result edge
    # from both operands. Keep one geometric representative before stitching.
    unique=[]; seen=set()
    for edge in selected:
        signature=(_fraction_point(edge.a),_fraction_point(edge.b))
        if signature in seen: continue
        seen.add(signature); unique.append(edge)
    selected=unique
    return {'operation':operation,'selected_fragments':tuple(selected),
            'intersection_events':result['intersection_events']}

def fragment_area_contribution(fragments):
    """Signed shoelace contribution; meaningful when selected fragments close."""
    return 0.5*sum(f.a[0]*f.b[1]-f.b[0]*f.a[1] for f in fragments)

def _polar_half(vector):
    x,y=vector
    return 0 if (y>0 or (y==0 and x>=0)) else 1


def _polar_compare(first,second):
    """Exact counter-clockwise polar ordering for non-zero rational vectors."""
    h1,h2=_polar_half(first),_polar_half(second)
    if h1!=h2:
        return -1 if h1<h2 else 1
    cross=first[0]*second[1]-first[1]*second[0]
    if cross>0: return -1
    if cross<0: return 1
    return 0


def stitch_boundary_fragments(fragments, *, epsilon=1e-10):
    """Stitch directed fragments into closed rings using a planar face walk.
    Raises rather than returning open or degenerate chains.
    """
    if not isfinite(epsilon) or epsilon<=0: raise ValueError('epsilon must be finite and positive')
    edges=list(fragments)
    if not edges: return tuple()
    def key(p): return _fraction_point(p)
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
            if not candidates:
                detail=[(tuple(map(str,edge.a)),tuple(map(str,edge.b))) for edge in edges]
                raise ValueError(f'selected boundary fragments contain an open chain at {tuple(map(str,edge.b))}; edges={detail}')
            reverse=(edge.a[0]-edge.b[0],edge.a[1]-edge.b[1])
            def vector(i):
                nxt=edges[i]
                return (nxt.b[0]-nxt.a[0],nxt.b[1]-nxt.a[1])
            ordered=sorted(candidates,key=cmp_to_key(
                lambda first,second: _polar_compare(vector(first),vector(second))
                or (first>second)-(first<second)
            ))
            predecessor=None
            for candidate in ordered:
                if _polar_compare(vector(candidate),reverse)<=0:
                    predecessor=candidate
                else:
                    break
            current=predecessor if predecessor is not None else ordered[-1]
        else: raise ValueError('boundary traversal exceeded fragment count')
        if len(ring)<3 or _signed_area_exact(ring)==0: raise ValueError('stitched boundary is degenerate')
        rings.append(tuple(ring))
    if len(used)!=len(edges): raise ValueError('not all selected fragments were stitched')
    return tuple(rings)

def assemble_polygon_components(rings):
    """Group CCW shell rings with their directly contained CW hole rings.

    Positive rings become polygon shells. Each negative ring is assigned to
    the smallest-area shell that strictly contains one of its vertices.
    Islands inside holes remain independent polygon components.
    """
    shells=[ring for ring in rings if _signed_area_exact(ring)>0]
    holes=[ring for ring in rings if _signed_area_exact(ring)<0]
    components=[{'shell':shell,'holes':[]} for shell in shells]
    for hole in holes:
        probe=hole[0]
        parents=[(abs(_signed_area_exact(item['shell'])),item)
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
