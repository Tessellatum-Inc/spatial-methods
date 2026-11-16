from collections import Counter
from fractions import Fraction
import math, random, pytest
from constrained_delaunay import (constrained_delaunay_triangulate,
    constrained_delaunay_with_diagonals, triangle_area, _incircle, _edge)
from ear_clipping import orient, polygon_area

def test_convex_count_orientation_area():
    ring=[(0,0),(5,0),(6,3),(3,5),(0,3)]
    tris=constrained_delaunay_triangulate(ring)
    assert len(tris)==len(ring)-2
    assert all(orient(*t)>0 for t in tris)
    assert sum((triangle_area(t) for t in tris),Fraction(0))==polygon_area(ring)

def test_concave_area_and_boundary_constraints():
    ring=[(0,0),(6,0),(6,5),(4,2),(2,4),(0,5)]
    tris=constrained_delaunay_triangulate(ring)
    edges=Counter(_edge(a,b) for tri in tris for a,b in zip(tri,tri[1:]+tri[:1]))
    for a,b in zip(ring,ring[1:]+ring[:1]):
        assert edges[_edge(tuple(map(Fraction,a)),tuple(map(Fraction,b)))]==1
    assert sum((triangle_area(t) for t in tris),Fraction(0))==polygon_area(ring)

def test_all_interior_edges_are_locally_weakly_delaunay():
    ring=[(0,0),(5,0),(6,3),(3,5),(0,3)]
    tris=constrained_delaunay_triangulate(ring)
    incidence={}
    for tri in tris:
        for a,b in zip(tri,tri[1:]+tri[:1]): incidence.setdefault(_edge(a,b),[]).append(tri)
    boundary={_edge(tuple(map(Fraction,a)),tuple(map(Fraction,b))) for a,b in zip(ring,ring[1:]+ring[:1])}
    for edge,owners in incidence.items():
        if len(owners)!=2 or edge in boundary: continue
        u,v=edge; a=next(p for p in owners[0] if p not in edge); b=next(p for p in owners[1] if p not in edge)
        if orient(u,v,a)<0: u,v=v,u
        assert _incircle(u,v,a,b)<=0

def test_clockwise_closed_ring_preserves_area():
    ring=[(0,0),(0,4),(4,4),(4,0),(0,0)]
    tris=constrained_delaunay_triangulate(ring)
    assert len(tris)==2
    assert sum((triangle_area(t) for t in tris),Fraction(0))==16

def test_seeded_radial_simple_polygons():
    rng=random.Random(7741)
    for n in range(5,15):
        angles=sorted(rng.random()*2*math.pi for _ in range(n))
        ring=[(round((2+rng.random())*math.cos(a),5),round((2+rng.random())*math.sin(a),5)) for a in angles]
        area=polygon_area(ring); tris=constrained_delaunay_triangulate(ring)
        assert len(tris)==n-2
        assert sum((triangle_area(t) for t in tris),Fraction(0))==area

def test_repeated_vertex_and_invalid_flip_limit_rejected():
    with pytest.raises(ValueError,match="repeated non-consecutive"):
        constrained_delaunay_triangulate([(0,0),(2,0),(2,2),(0,2),(2,0)])
    with pytest.raises(ValueError):
        constrained_delaunay_triangulate([(0,0),(1,0),(1,1)],max_flips=-1)


def test_collinear_boundary_vertices_are_normalized_before_constraints():
    ring = [(0,0),(2,0),(4,0),(4,4),(0,4),(0,0)]
    tris = constrained_delaunay_triangulate(ring)
    assert len(tris) == 2
    assert sum((triangle_area(t) for t in tris), Fraction(0)) == 16


def test_non_finite_coordinates_are_rejected():
    with pytest.raises(ValueError, match="finite"):
        constrained_delaunay_triangulate([(0,0),(1,0),(1,float("nan"))])
    with pytest.raises(ValueError, match="finite"):
        constrained_delaunay_triangulate([(0,0),(1,0),(1,float("inf"))])


def test_collinear_normalization_preserves_each_normalized_boundary_edge():
    ring = [(0,0),(2,0),(4,0),(4,4),(0,4),(0,0)]
    tris = constrained_delaunay_triangulate(ring)
    incidence = Counter(_edge(a,b) for tri in tris for a,b in zip(tri,tri[1:]+tri[:1]))
    normalized = [(Fraction(0),Fraction(0)),(Fraction(4),Fraction(0)),
                  (Fraction(4),Fraction(4)),(Fraction(0),Fraction(4))]
    for a,b in zip(normalized,normalized[1:]+normalized[:1]):
        assert incidence[_edge(a,b)] == 1


def test_one_shot_iterable_and_self_intersection_validation():
    ring = [(0,0),(5,0),(5,4),(3,2),(0,4)]
    assert len(constrained_delaunay_triangulate(iter(ring))) == len(ring)-2
    with pytest.raises(ValueError, match="simple polygon"):
        constrained_delaunay_triangulate([(0,0),(4,4),(0,4),(4,0)])


def test_interior_diagonal_is_preserved_and_partitions_concave_polygon():
    ring = [(0,0),(5,0),(5,1),(2,1),(2,4),(0,4)]
    constraint = ((0,0),(2,4))
    tris = constrained_delaunay_with_diagonals(ring, [constraint])
    incidence = Counter(_edge(a,b) for tri in tris for a,b in zip(tri,tri[1:]+tri[:1]))
    edge = _edge((Fraction(0),Fraction(0)),(Fraction(2),Fraction(4)))
    assert incidence[edge] == 2
    assert len(tris) == len(ring)-2
    assert sum((triangle_area(t) for t in tris),Fraction(0)) == polygon_area(ring)


def test_multiple_non_crossing_diagonals_can_share_a_vertex():
    ring = [(0,0),(6,0),(6,5),(0,5)]
    constraints = [((0,0),(6,5)), ((0,0),(6,0))]
    tris = constrained_delaunay_with_diagonals(ring, constraints)
    incidence = Counter(_edge(a,b) for tri in tris for a,b in zip(tri,tri[1:]+tri[:1]))
    assert incidence[_edge((Fraction(0),Fraction(0)),(Fraction(6),Fraction(5)))] == 2
    assert incidence[_edge((Fraction(0),Fraction(0)),(Fraction(6),Fraction(0)))] == 1
    assert len(tris) == 2


def test_crossing_constraints_and_exterior_chords_are_rejected():
    square = [(0,0),(4,0),(4,4),(0,4)]
    with pytest.raises(ValueError, match="cross or overlap"):
        constrained_delaunay_with_diagonals(
            square, [((0,0),(4,4)), ((0,4),(4,0))]
        )
    concave = [(0,0),(5,0),(5,1),(2,1),(2,4),(0,4)]
    with pytest.raises(ValueError, match="crosses or touches|interior"):
        constrained_delaunay_with_diagonals(concave, [((0,4),(5,1))])


def test_boundary_edge_can_be_redeclared_as_constraint():
    ring = [(0,0),(4,0),(4,4),(0,4)]
    tris = constrained_delaunay_with_diagonals(ring, [((0,0),(4,0))])
    assert len(tris) == 2

