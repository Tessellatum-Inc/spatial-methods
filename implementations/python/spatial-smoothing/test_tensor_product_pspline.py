import numpy as np
import pytest
from tensor_product_pspline import TensorProductPSpline2D

def grid(nx=9,ny=8):
    x,y=np.meshgrid(np.linspace(0,1,nx),np.linspace(0,1,ny))
    return np.c_[x.ravel(),y.ravel()]

def test_large_penalty_preserves_bilinear_null_space():
    xy=grid();z=2+3*xy[:,0]-1.5*xy[:,1]+.75*xy[:,0]*xy[:,1]
    m=TensorProductPSpline2D((5,5),smoothing=(100.,80.)).fit(xy,z)
    np.testing.assert_allclose(m.predict(xy),z,atol=1e-8)

def test_in_domain_prediction_is_finite():
    xy=grid();z=np.sin(2*np.pi*xy[:,0])+np.cos(np.pi*xy[:,1])
    m=TensorProductPSpline2D((6,5),smoothing=.2).fit(xy,z)
    p=m.predict([[.2,.3],[.7,.8]])
    assert p.shape==(2,) and np.isfinite(p).all()

def test_axis_specific_penalties_and_asymmetric_basis():
    xy=grid(10,9);z=xy[:,0]**2+.1*xy[:,1]
    m=TensorProductPSpline2D((6,4),smoothing=(2.,.1)).fit(xy,z)
    assert m.coefficient_shape_==(6,4) and m.design_rank_==24

def test_extrapolation_is_rejected():
    xy=grid();m=TensorProductPSpline2D((5,5)).fit(xy,xy[:,0]+xy[:,1])
    with pytest.raises(ValueError):m.predict([[1.1,.5]])

@pytest.mark.parametrize("xy,z,kw",[
    (np.ones((4,2)),np.ones(4),{}),(grid()[:3],np.ones(3),{}),
    (grid(),np.ones(4),{}),(grid(),np.ones(len(grid())),{"n_basis":(3,5)}),
    (grid(),np.ones(len(grid())),{"degree":0}),
    (grid(),np.ones(len(grid())),{"smoothing":-1}),
    (grid(),np.full(len(grid()),np.nan),{}),
])
def test_invalid_inputs(xy,z,kw):
    with pytest.raises(ValueError):TensorProductPSpline2D(**kw).fit(xy,z)

def test_predict_before_fit_raises():
    with pytest.raises(RuntimeError):TensorProductPSpline2D().predict([[.5,.5]])
