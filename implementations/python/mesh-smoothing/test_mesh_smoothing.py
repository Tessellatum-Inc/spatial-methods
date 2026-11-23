import numpy as np
import pytest
from mesh_smoothing import laplacian_smooth, taubin_smooth
V=np.array([[1.,1.,1.],[-1.,-1.,1.],[-1.,1.,-1.],[1.,-1.,-1.]])
F=np.array([[0,1,2],[0,3,1],[0,2,3],[1,3,2]])
def radius(p): return float(np.sqrt(np.mean(np.sum(p*p,axis=1))))
def test_zero_iterations_are_identity():
    assert np.array_equal(laplacian_smooth(V,F,iterations=0),V)
    assert np.array_equal(taubin_smooth(V,F,iterations=0),V)
def test_one_step_matches_independent_one_ring_calculation():
    v=np.array([[0.,0.,0.],[2.,0.,0.],[0.,2.,0.],[0.,0.,2.]])
    f=np.array([[0,1,2],[0,1,3]])
    r=laplacian_smooth(v,f,iterations=1,lam=.5)
    assert r[0] == pytest.approx([1/3,1/3,1/3])
    assert r[1] == pytest.approx([1.,1/3,1/3])
def test_laplacian_shrinks_closed_tetrahedron():
    assert radius(laplacian_smooth(V,F,iterations=2,lam=.25)) < radius(V)
def test_taubin_counteracts_shrinkage():
    ordinary=laplacian_smooth(V,F,iterations=5,lam=.4)
    taubin=taubin_smooth(V,F,iterations=5,lam=.4,mu=-.43)
    assert abs(radius(taubin)-radius(V)) < abs(radius(ordinary)-radius(V))
def test_fixed_vertices_remain_unchanged():
    r=laplacian_smooth(V,F,iterations=3,fixed_vertices=[0,2])
    assert np.array_equal(r[[0,2]],V[[0,2]])
def test_boundary_pinning():
    f=np.array([[0,1,2],[0,2,3]])
    assert np.array_equal(laplacian_smooth(V,f,iterations=2,fix_boundary=True),V)
def test_connectivity_shape_is_preserved():
    assert taubin_smooth(V,F,iterations=3).shape == V.shape
@pytest.mark.parametrize("fn,kw",[(laplacian_smooth,{"iterations":-1}),(laplacian_smooth,{"lam":1.1}),(taubin_smooth,{"mu":.1})])
def test_invalid_parameters(fn,kw):
    with pytest.raises(ValueError): fn(V,F,**kw)
def test_repeated_face_vertex_rejected():
    with pytest.raises(ValueError,match="distinct"): laplacian_smooth(V,[[0,0,1]])
def test_out_of_range_index_rejected():
    with pytest.raises(ValueError,match="outside"): laplacian_smooth(V,[[0,1,9]])
def test_nonmanifold_edge_rejected():
    v=[[0,0,0],[1,0,0],[0,1,0],[0,-1,0],[0,0,1]]
    f=[[0,1,2],[1,0,3],[0,1,4]]
    with pytest.raises(ValueError,match="non-manifold"): laplacian_smooth(v,f)
def test_nonfinite_vertices_rejected():
    bad=V.copy(); bad[0,0]=np.nan
    with pytest.raises(ValueError,match="finite"): laplacian_smooth(bad,F)
