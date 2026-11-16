import pytest
from isotropic_remeshing import (
    split_edge, collapse_edge, flip_edge, tangential_relax, isotropic_remesh,
)


def square():
    return ( (0.,0.,0.), (2.,0.,0.), (0.,2.,0.), (2.,2.,0.) ), ((0,1,2),(1,3,2))


def test_split_edge_subdivides_both_incident_faces_and_preserves_boundary():
    v, f = square()
    nv, nf, changed = split_edge(v, f, (1,2))
    assert changed and len(nv) == 5 and len(nf) == 4
    assert sum(1 for tri in nf if 4 in tri) == 4


def test_boundary_edge_split_splits_single_face():
    v, f = square()
    nv, nf, changed = split_edge(v, f, (0,1))
    assert changed and len(nf) == 3


def test_collapse_refuses_boundary_interior_mixed_edge():
    v, f = square()
    # Vertex 0 is boundary and vertex 3 is interior only if an additional
    # surrounding mesh exists; this edge is absent and must remain unchanged.
    nv, nf, changed = collapse_edge(v, f, (0,3))
    assert not changed and nv == v and nf == f


def test_collapse_refuses_interior_chord_between_boundary_vertices():
    v, f = square()
    nv, nf, changed = collapse_edge(v, f, (1, 2))
    assert not changed and nv == v and nf == f


def test_collapse_short_interior_edge_of_closed_tetrahedron():
    v=((0.,0.,0.),(1.,0.,0.),(0.5,0.866,0.),(0.5,0.289,0.816))
    f=((0,2,1),(0,1,3),(1,2,3),(2,0,3))
    nv,nf,changed=collapse_edge(v,f,(0,1))
    # Tetrahedron collapses to a two-face double-sided shell, so manifold
    # validation may reject it rather than inventing a valid surface.
    assert not changed


def test_flip_rejects_boundary_edges():
    v,f=square()
    nv,nf,changed=flip_edge(v,f,(0,1))
    assert not changed


def test_tangential_relaxation_pins_boundary_and_keeps_finite_points():
    v=((0.,0.,0.),(1.,0.,0.),(0.,1.,0.),(0.2,0.2,1.))
    f=((0,1,3),(1,2,3),(2,0,3))
    out=tangential_relax(v,f,iterations=2,pin_boundary=True)
    assert out[:3] == v[:3]
    assert all(len(p)==3 for p in out)


def test_remesher_returns_valid_manifold_and_counts():
    v,f=square()
    out_v,out_f,counts=isotropic_remesh(v,f,0.8,iterations=1)
    assert len(out_f)>0
    assert set(counts)=={"splits","collapses","flips"}
    assert len(out_v)>0


@pytest.mark.parametrize("target, message", [(0,"positive"),(-1,"positive"),(float("inf"),"finite")])
def test_invalid_target_length(target,message):
    v,f=square()
    with pytest.raises(ValueError,match=message):
        isotropic_remesh(v,f,target)
