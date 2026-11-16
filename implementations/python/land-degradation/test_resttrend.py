import numpy as np
import pytest
from resttrend import resttrend


def test_resttrend_recovers_rainfall_response_and_residual_trend():
    years = np.arange(2000., 2012.)
    time = years - years.mean()
    phase = np.arange(len(years), dtype=float)
    raw1 = np.sin(phase*1.7)
    raw2 = np.cos(phase*1.1)
    raw1 -= raw1.mean()
    raw2 -= raw2.mean()
    raw1 -= time * (time @ raw1) / (time @ time)
    raw2 -= time * (time @ raw2) / (time @ time)
    precipitation = np.column_stack((200. + 100.*raw1, 250. + 80.*raw2))
    residual_trend = np.array([-.02, .03])
    ndvi = .2 + .0015*precipitation + (years-years[0])[:,None]*residual_trend
    result = resttrend(ndvi, precipitation, years, min_observations=6)
    np.testing.assert_allclose(result["rainfall_sensitivity"], [.0015,.0015], atol=1e-10)
    np.testing.assert_allclose(result["residual_trend"], residual_trend, atol=1e-10)
    assert np.all(result["residual_r_squared"] > .999999)


def test_resttrend_handles_missing_observations_per_pixel():
    years = np.arange(2000., 2010.)
    p = np.tile(np.linspace(100., 400., 10)[:,None], (1,2))
    y = .3 + .002*p + (years-years[0])[:,None]*np.array([.01,-.01])
    y[::2,0] = np.nan
    result = resttrend(y, p, years, min_observations=5)
    assert result["n_observations"].tolist() == [5,10]
    assert np.isfinite(result["residual_trend"]).all()
    assert np.isnan(result["residuals"][::2,0]).all()


def test_resttrend_leaves_insufficient_or_constant_rainfall_pixels_nan():
    years = np.arange(2000., 2008.)
    p = np.column_stack((np.ones(8), np.arange(8.)))
    y = np.column_stack((np.arange(8.), np.arange(8.)))
    result = resttrend(y, p, years, min_observations=6)
    assert np.isnan(result["residual_trend"][0])
    assert np.isfinite(result["residual_trend"][1])


def test_resttrend_validates_shapes_and_time():
    with pytest.raises(ValueError, match="share"):
        resttrend(np.ones((5,2)), np.ones((4,2)), np.arange(5))
    with pytest.raises(ValueError, match="increasing"):
        resttrend(np.ones((5,2)), np.arange(10.).reshape(5,2), [1,2,3,4,3])
