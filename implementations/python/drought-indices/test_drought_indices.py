import numpy as np
import pytest
from drought_indices import growing_degree_days,standardized_precipitation_index,temperature_condition_index,vegetation_condition_index,vegetation_health_index

def test_vci_tci_vhi():
    np.testing.assert_allclose(vegetation_condition_index([.2,.5,.8],[.1]*3,[.9]*3),[12.5,50,87.5])
    np.testing.assert_allclose(temperature_condition_index([30,20,10],[10]*3,[30]*3),[0,50,100])
    np.testing.assert_allclose(vegetation_health_index([0,100],[100,0]),[50,50])
    assert vegetation_health_index([0],[100],alpha=.8)[0]==pytest.approx(20)
def test_constant_range_and_bad_order():
    assert np.isnan(vegetation_condition_index([1],[1],[1])[0])
    with pytest.raises(ValueError): vegetation_condition_index([1],[2],[1])
def test_spi_gamma_standardization_and_missing():
    rng=np.random.default_rng(7);x=rng.gamma(2,20,120);x[::17]=0;x[5]=np.nan;z=standardized_precipitation_index(x)
    assert np.isnan(z[5]) and np.isfinite(z).sum()==119
    assert np.mean(z[np.isfinite(z)])==pytest.approx(0,abs=.35)
    assert np.std(z[np.isfinite(z)])==pytest.approx(1,abs=.35)
def test_spi_spatial_axis():
    rng=np.random.default_rng(8);x=rng.gamma(2,10,(60,2,3));x[0,0,0]=np.nan
    z=standardized_precipitation_index(x,axis=0);assert z.shape==x.shape and np.isnan(z[0,0,0])
    zz=standardized_precipitation_index(np.moveaxis(x,0,-1),axis=-1);np.testing.assert_allclose(z,np.moveaxis(zz,-1,0),equal_nan=True)
def test_spi_validation():
    with pytest.raises(ValueError): standardized_precipitation_index([-1]*40)
    assert np.isnan(standardized_precipitation_index([1,2,3,4],min_samples=10)).all()


def test_growing_degree_days_mean_method_and_upper_cap():
    np.testing.assert_allclose(
        growing_degree_days([5, 10, 20], [15, 20, 30], base_temperature=10),
        [0, 5, 15],
    )
    np.testing.assert_allclose(
        growing_degree_days([10, 20], [30, 40], base_temperature=10,
                            upper_temperature=30),
        [10, 20],
    )


def test_growing_degree_days_preserves_missing_and_validates():
    values = growing_degree_days([5, np.nan], [15, 20], base_temperature=10)
    assert values[0] == pytest.approx(0)
    assert np.isnan(values[1])
    with pytest.raises(ValueError):
        growing_degree_days([20], [10], base_temperature=5)
    with pytest.raises(ValueError):
        growing_degree_days([5], [10], base_temperature=12,
                            upper_temperature=10)
