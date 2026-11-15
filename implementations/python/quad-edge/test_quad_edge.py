import pytest
from quad_edge import QuadEdgeSubdivision


def test_make_edge_rotation_and_origin_rings():
    sub = QuadEdgeSubdivision()
    e = sub.make_edge("a", "b")
    assert e.sym.origin == "b"
    assert e.destination == "b"
    assert e.rot.rot.rot.rot is e
    assert e.onext is e
    assert sub.validate()


def test_splice_merges_origin_rings_and_is_involutive():
    sub = QuadEdgeSubdivision()
    a = sub.make_edge("a", "b")
    b = sub.make_edge("a", "c")
    sub.splice(a, b)
    assert a.onext is b and b.onext is a
    sub.splice(a, b)
    assert a.onext is a and b.onext is b


def test_connect_builds_diagonal_between_face_boundaries():
    sub = QuadEdgeSubdivision()
    a = sub.make_edge("a", "b")
    b = sub.make_edge("c", "d")
    diagonal = sub.connect(a, b)
    assert diagonal.origin == "b"
    assert diagonal.destination == "c"
    assert len(sub.edges) == 3
    assert sub.validate()


def test_delete_edge_detaches_both_primal_directions():
    sub = QuadEdgeSubdivision()
    e = sub.make_edge(0, 1)
    sub.delete_edge(e)
    assert e.origin is None and e.sym.origin is None
    assert e.onext is e and e.sym.onext is e.sym


def test_rejects_dual_dart_deletion():
    sub = QuadEdgeSubdivision()
    e = sub.make_edge(0,1)
    with pytest.raises(ValueError):
        sub.delete_edge(e.rot)
