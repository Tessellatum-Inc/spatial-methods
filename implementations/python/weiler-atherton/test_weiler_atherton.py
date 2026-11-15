import random
import pytest
from weiler_atherton import weiler_atherton_intersection, _area


def area(rings):
    return sum(abs(_area(r)) for r in rings)


def test_overlapping_rectangles():
    a=[(0,0),(6,0),(6,4),(0,4)]
    b=[(2,-1),(5,-1),(5,5),(2,5)]
    out=weiler_atherton_intersection(a,b)
    assert len(out)==1
    assert area(out)==pytest.approx(12)


def test_concave_intersection_can_be_disconnected():
    u=[(0,0),(6,0),(6,6),(4,6),(4,2),(2,2),(2,6),(0,6)]
    strip=[(-1,3),(7,3),(7,5),(-1,5)]
    out=weiler_atherton_intersection(u,strip)
    assert len(out)==2
    assert area(out)==pytest.approx(8)


def test_containment_and_disjoint():
    outer=[(0,0),(8,0),(8,8),(0,8)]
    inner=[(2,2),(4,2),(4,4),(2,4)]
    assert area(weiler_atherton_intersection(outer,inner))==pytest.approx(4)
    far=[(10,10),(11,10),(11,11),(10,11)]
    assert weiler_atherton_intersection(outer,far)==[]


def test_clockwise_inputs():
    a=[(0,0),(6,0),(6,4),(0,4)]
    b=[(2,-1),(5,-1),(5,5),(2,5)]
    assert area(weiler_atherton_intersection(a[::-1],b[::-1]))==pytest.approx(12)


def test_rejects_vertex_touch_and_collinear_overlap():
    a=[(0,0),(2,0),(2,2),(0,2)]
    touch=[(2,2),(4,2),(4,4),(2,4)]
    shared=[(1,0),(3,0),(3,2),(1,2)]
    with pytest.raises(NotImplementedError):
        weiler_atherton_intersection(a,touch)
    with pytest.raises(NotImplementedError):
        weiler_atherton_intersection(a,shared)


def test_rejects_self_crossing():
    bow=[(0,0),(2,2),(0,2),(2,0)]
    sq=[(-1,-1),(3,-1),(3,3),(-1,3)]
    with pytest.raises(ValueError,match="simple ring"):
        weiler_atherton_intersection(bow,sq)


def test_seeded_rectangle_oracle():
    rng=random.Random(117)
    for _ in range(250):
        ax, bx=sorted((rng.uniform(-10,10),rng.uniform(-10,10)))
        ay, by=sorted((rng.uniform(-10,10),rng.uniform(-10,10)))
        cx, dx=sorted((rng.uniform(-10,10),rng.uniform(-10,10)))
        cy, dy=sorted((rng.uniform(-10,10),rng.uniform(-10,10)))
        if min(bx-ax,by-ay,dx-cx,dy-cy)<1e-3: continue
        a=[(ax,ay),(bx,ay),(bx,by),(ax,by)]
        b=[(cx,cy),(dx,cy),(dx,dy),(cx,dy)]
        expected=max(0,min(bx,dx)-max(ax,cx))*max(0,min(by,dy)-max(ay,cy))
        assert area(weiler_atherton_intersection(a,b))==pytest.approx(expected,abs=1e-7)
