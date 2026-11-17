import numpy as np
import pytest
from variogram_models import variogram_model,directional_semivariogram,fit_variogram,genton_semivariance

@pytest.mark.parametrize("model",["spherical","exponential","gaussian"])
def test_models_are_zero_at_origin_and_approach_sill(model):
    y=variogram_model([0,1e9],model=model,nugget=0.2,partial_sill=1.3,range_=5)
    assert y[0]==pytest.approx(0.0)
    assert variogram_model([1e-9],model=model,nugget=0.2,partial_sill=1.3,range_=5)[0] >= 0.2
    assert y[1]==pytest.approx(1.5)

def test_spherical_model_reaches_sill_at_range():
    assert variogram_model([10],model="spherical",nugget=0.1,partial_sill=2,range_=10)[0]==pytest.approx(2.1)

def test_directional_filter_selects_east_west_pairs():
    pts=[(0,0),(1,0),(2,0),(0,1),(0,2)]
    result=directional_semivariogram(pts,[0,1,3,5,9],[0,1.5,3],azimuth_deg=90,tolerance_deg=5)
    assert sum(x["pairs"] for x in result)==3

def test_cressie_estimator_is_finite_and_nonnegative():
    result=directional_semivariogram([(0,0),(1,0),(2,0)],[0,1,4],[0,1.5,2.5],azimuth_deg=90,estimator="cressie")
    assert all(x["semivariance"] is None or x["semivariance"]>=0 for x in result)

def test_genton_qn_estimator_matches_hand_computed_order_statistic():
    expected = 0.5 * (2.2191 ** 2)
    assert genton_semivariance([0, 1, 2, 3]) == pytest.approx(expected)
    assert genton_semivariance([13, 12, 11, 10]) == pytest.approx(expected)


def test_directional_genton_estimator_uses_increment_differences():
    result = directional_semivariogram(
        [(0, 0), (1, 0), (2, 0), (3, 0)],
        [0, 1, 2, 3], [0, 1.5, 3.5],
        azimuth_deg=90, tolerance_deg=1, estimator="genton"
    )
    assert result[0]["pairs"] == 3
    assert result[0]["semivariance"] == pytest.approx(0.5 * (2.2191 ** 2))


def test_genton_requires_two_finite_increments():
    for values in ([1], [1, float("nan")], [[1, 2]]):
        with pytest.raises(ValueError):
            genton_semivariance(values)


def test_fit_recovers_spherical_parameters():
    h=np.linspace(1,20,20)
    g=variogram_model(h,model="spherical",nugget=0.15,partial_sill=2.4,range_=12)
    fit=fit_variogram(h,g,model="spherical")
    assert fit["success"]
    assert fit["nugget"]==pytest.approx(.15,abs=1e-3)
    assert fit["partial_sill"]==pytest.approx(2.4,abs=1e-3)
    assert fit["range"]==pytest.approx(12,abs=1e-2)

def test_fixed_nugget_fit_and_pair_weights():
    h=np.linspace(1,20,20); g=variogram_model(h,model="exponential",nugget=.3,partial_sill=1.8,range_=7)
    fit=fit_variogram(h,g,model="exponential",fit_nugget=False,initial=(.3,1.5,8),pairs=np.arange(1,21))
    assert fit["nugget"]==pytest.approx(.3)
    assert fit["partial_sill"]==pytest.approx(1.8,abs=1e-3)

def test_invalid_inputs_are_rejected():
    with pytest.raises(ValueError): variogram_model([-1])
    with pytest.raises(ValueError): directional_semivariogram([(0,0),(1,1)],[1,2],[0,2],estimator="bad")
    with pytest.raises(ValueError): fit_variogram([1,2],[1,2])
