import numpy as np
import pytest
from ross_li_brdf import fit_ross_li_brdf, ross_li_kernels


def test_kernels_are_finite_and_hotspot_geometry_changes_geometric_term():
    kv, kg = ross_li_kernels([0.3, 0.3], [0.0, 0.0], [0.0, np.pi])
    assert np.all(np.isfinite(kv)) and np.all(np.isfinite(kg))
    assert kg[0] > kg[1]


def test_kernel_validation():
    with pytest.raises(ValueError):
        ross_li_kernels([np.pi/2], [0.1], [0.0])
    with pytest.raises(ValueError):
        ross_li_kernels([0.1], [0.1], [0.0], height_to_width=0)


def test_multiband_coefficients_and_reference_normalization():
    ts=np.array([.15,.25,.35,.45,.55,.65,.4,.3])
    tv=np.array([0,.1,.2,.3,.15,.25,.4,.05])
    phi=np.array([0,.5,1,1.5,2,2.5,3,4])
    kv,kg=ross_li_kernels(ts,tv,phi)
    truth=np.array([[.2,.3],[.04,.02],[.01,.03]])
    rho=np.column_stack((np.ones(ts.size),kv,kg))@truth
    out=fit_ross_li_brdf(rho,ts,tv,phi,reference_solar_zenith=.35)
    np.testing.assert_allclose(out["coefficients"],truth,atol=1e-11)
    assert np.all(out["r_squared"]>1-1e-12)
    rkv,rkg=ross_li_kernels(.35,0.,0.)
    np.testing.assert_allclose(out["normalized"][:,0],.2+.04*rkv+.01*rkg,atol=1e-11)
    np.testing.assert_allclose(out["normalized"][:,1],.3+.02*rkv+.03*rkg,atol=1e-11)


def test_single_band_and_rank_deficient_geometry():
    ts=np.array([.1,.2,.3,.4,.5]); tv=np.array([0,.1,.2,.1,0]); phi=np.array([0,.5,1,2,3])
    kv,kg=ross_li_kernels(ts,tv,phi); rho=.25+.03*kv+.02*kg
    out=fit_ross_li_brdf(rho,ts,tv,phi,reference_solar_zenith=.3)
    assert out["normalized"].shape==rho.shape and out["coefficients"].shape==(3,)
    with pytest.raises(ValueError):
        fit_ross_li_brdf(np.ones(4),np.full(4,.2),np.zeros(4),np.zeros(4),reference_solar_zenith=.2)


def test_rejects_invalid_shapes():
    with pytest.raises(ValueError):
        fit_ross_li_brdf(np.ones((2,1)),[0,1],[0,0],[0,1],reference_solar_zenith=.2)
    with pytest.raises(ValueError):
        fit_ross_li_brdf(np.ones(4),[0,1],[0,0,0,0],[0,1,2,3],reference_solar_zenith=.2)
