import numpy as np
import pytest
from universal_kriging import universal_kriging


def test_linear_universal_kriging_reproduces_linear_drift():
    x, y = np.meshgrid(np.linspace(0,4,4), np.linspace(0,3,3))
    obs = np.column_stack((x.ravel(),y.ravel()))
    values = 2. + 3.*obs[:,0] - 1.5*obs[:,1]
    targets = np.array([[.5,.5],[2.2,1.1],[3.5,2.5]])
    expected = 2. + 3.*targets[:,0] - 1.5*targets[:,1]
    result = universal_kriging(obs, values, targets, drift_order=1,
                               nugget=0., partial_sill=1., range_=3.)
    np.testing.assert_allclose(result["prediction"], expected, atol=1e-9)
    assert np.all(result["variance"] >= 0)


def test_quadratic_universal_kriging_reproduces_quadratic_drift():
    x, y = np.meshgrid(np.linspace(-2,2,5), np.linspace(-2,2,5))
    obs = np.column_stack((x.ravel(),y.ravel()))
    values = 1. + obs[:,0] - 2*obs[:,1] + .4*obs[:,0]**2 + .2*obs[:,0]*obs[:,1] - .3*obs[:,1]**2
    targets = np.array([[-1.2,.7],[.4,-.8],[1.5,1.1]])
    expected = 1. + targets[:,0] - 2*targets[:,1] + .4*targets[:,0]**2 + .2*targets[:,0]*targets[:,1] - .3*targets[:,1]**2
    result = universal_kriging(obs, values, targets, drift_order=2,
                               variogram="exponential", partial_sill=1., range_=4.)
    np.testing.assert_allclose(result["prediction"], expected, atol=1e-8)


def test_ordinary_kriging_constant_drift_and_exact_sample_prediction():
    obs = np.array([[0.,0.],[1.,0.],[0.,1.],[1.,1.]])
    values = np.full(4, 7.5)
    result = universal_kriging(obs, values, obs, drift_order=0,
                               nugget=0., partial_sill=1., range_=2.)
    np.testing.assert_allclose(result["prediction"], values, atol=1e-9)
    np.testing.assert_allclose(result["variance"], 0., atol=1e-8)


def test_universal_kriging_validates_drift_geometry_and_variogram():
    with pytest.raises(ValueError, match="not enough"):
        universal_kriging([[0.,0.],[1.,0.]], [1.,2.], [[.5,.5]], drift_order=2)
    with pytest.raises(ValueError, match="rank deficient"):
        universal_kriging([[0.,0.],[1.,0.],[2.,0.]], [1.,2.,3.], [[1.,1.]], drift_order=1)
    with pytest.raises(ValueError, match="variogram"):
        universal_kriging([[0.,0.],[1.,0.],[0.,1.]], [1.,2.,3.], [[.5,.5]], variogram="bad")
