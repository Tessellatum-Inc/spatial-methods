import numpy as np
import pytest
from variogram_models import variogram_model,directional_semivariogram,fit_variogram,genton_semivariance,dowd_semivariance,anisotropic_distance,fit_variogram_reml

@pytest.mark.parametrize("model",["spherical","exponential","gaussian"])
def test_models_are_zero_at_origin_and_approach_sill(model):
    y=variogram_model([0,1e9],model=model,nugget=0.2,partial_sill=1.3,range_=5)
    assert y[0]==pytest.approx(0.0)
    assert variogram_model([1e-9],model=model,nugget=0.2,partial_sill=1.3,range_=5)[0] >= 0.2
    assert y[1]==pytest.approx(1.5)

@pytest.mark.parametrize("nu", [0.5, 1.5, 2.5])
def test_matern_covariance_matches_closed_form_special_cases(nu):
    h = np.array([0.0, 1.0, 2.0])
    r = h / 2.0
    if nu == 0.5:
        correlation = np.exp(-r)
    elif nu == 1.5:
        q = np.sqrt(3.0) * r
        correlation = (1.0 + q) * np.exp(-q)
    else:
        q = np.sqrt(5.0) * r
        correlation = (1.0 + q + q*q/3.0) * np.exp(-q)
    expected = 0.2 + 1.7 * (1.0 - correlation)
    assert variogram_model(h, model="matern", nugget=0.2,
                           partial_sill=1.7, range_=2.0, nu=nu) == pytest.approx(expected)


def test_matern_rejects_invalid_smoothness():
    with pytest.raises(ValueError):
        variogram_model([0, 1], model="matern", nu=0)


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
    assert result[0]["semivariance"] == pytest.approx(0.0)


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



def test_reml_fits_finite_bounded_covariance_parameters():
    rng = np.random.default_rng(41)
    points = np.array([(x, y) for x in range(5) for y in range(4)], dtype=float)
    distances = np.linalg.norm(points[:, None, :] - points[None, :, :], axis=2)
    covariance = 0.15 * np.exp(-distances / 1.8)
    covariance.flat[::len(points) + 1] += 0.85
    values = rng.multivariate_normal(np.full(len(points), 7.0), covariance)
    fit = fit_variogram_reml(points, values, model="exponential")
    assert fit["model"] == "exponential"
    assert fit["nugget"] > 0
    assert fit["partial_sill"] > 0
    assert fit["range"] > 0
    assert np.isfinite(fit["reml_objective"])
    assert fit["observations"] == len(points)


def test_reml_rejects_degenerate_inputs():
    with pytest.raises(ValueError):
        fit_variogram_reml([(0, 0), (1, 0), (2, 0)], [1, 2, 3])
    with pytest.raises(ValueError):
        fit_variogram_reml([(0, 0), (1, 0), (0, 1), (0, 0)], [1, 2, 3, 4])
    with pytest.raises(ValueError):
        fit_variogram_reml([(0, 0), (1, 0), (0, 1), (1, 1)], [2, 2, 2, 2])



def test_dowd_estimator_matches_median_scale_formula_and_is_robust_to_sign():
    expected = 1.099 * 1.5 ** 2
    assert dowd_semivariance([0, 1, 2, 3]) == pytest.approx(expected)
    assert dowd_semivariance([0, -1, -2, -3]) == pytest.approx(expected)
    assert dowd_semivariance([0, 1, 2, 3, 1e9]) == pytest.approx(1.099 * 2 ** 2)


def test_dowd_directional_estimator_and_validation():
    out = directional_semivariogram(
        [(0, 0), (1, 0), (2, 0)], [0, 1, 3],
        [0, 1.5, 2.5], azimuth_deg=90, tolerance_deg=1, estimator="dowd"
    )
    assert out[0]["pairs"] == 2
    assert out[0]["semivariance"] == pytest.approx(1.099 * 1.5 ** 2)
    with pytest.raises(ValueError):
        dowd_semivariance([float("nan")])
    with pytest.raises(ValueError):
        directional_semivariogram([(0, 0), (1, 0)], [0, 1], [0, 2], estimator="bad")


def test_geometric_anisotropy_scales_minor_axis_only():
    # Azimuth 90 degrees is east-west: the north-south range is halved.
    assert anisotropic_distance(4, 0, azimuth_deg=90, ratio=0.5) == pytest.approx(4)
    assert anisotropic_distance(0, 4, azimuth_deg=90, ratio=0.5) == pytest.approx(8)
    assert anisotropic_distance(0, 4, azimuth_deg=90, ratio=1.0) == pytest.approx(4)
    with pytest.raises(ValueError):
        anisotropic_distance(1, 1, ratio=0)
    with pytest.raises(ValueError):
        anisotropic_distance(1, 1, ratio=1.1)


def test_directional_semivariogram_accepts_fixed_geometric_anisotropy():
    points=[(0, 0), (1, 0), (0, 1)]
    values=[0, 1, 2]
    isotropic=directional_semivariogram(points,values,[0,1.5,2.5],azimuth_deg=90,tolerance_deg=90)
    stretched=directional_semivariogram(points,values,[0,1.5,2.5],azimuth_deg=90,tolerance_deg=90,
                                        anisotropy_azimuth_deg=90,anisotropy_ratio=0.5)
    assert sum(x["pairs"] for x in isotropic) == 3
    assert [x["pairs"] for x in stretched] == [1, 2]


def test_reml_accepts_fixed_geometric_anisotropy():
    rng=np.random.default_rng(43)
    points=np.array([(x,y) for x in range(4) for y in range(4)],dtype=float)
    values=rng.normal(size=len(points))
    fit=fit_variogram_reml(points,values,anisotropy_azimuth_deg=90,anisotropy_ratio=0.6)
    assert fit["anisotropy_azimuth_deg"] == pytest.approx(90)
    assert fit["anisotropy_ratio"] == pytest.approx(0.6)
    with pytest.raises(ValueError):
        fit_variogram_reml(points,values,anisotropy_ratio=0)



def test_reml_automatic_anisotropy_is_bounded_and_no_worse_than_fixed_start():
    rng = np.random.default_rng(84)
    points = np.array([(x, y) for x in range(5) for y in range(5)], dtype=float)
    delta = points[:, None, :] - points[None, :, :]
    angle = np.deg2rad(35.0)
    along = delta[:, :, 0] * np.sin(angle) + delta[:, :, 1] * np.cos(angle)
    across = delta[:, :, 0] * np.cos(angle) - delta[:, :, 1] * np.sin(angle)
    distance = np.hypot(along, across / 0.45)
    covariance = 0.12 * np.exp(-distance / 2.2)
    covariance.flat[::len(points) + 1] += 0.88
    values = rng.multivariate_normal(np.full(len(points), 3.0), covariance)
    fixed = fit_variogram_reml(points, values, model="exponential",
                               anisotropy_azimuth_deg=0, anisotropy_ratio=1)
    fitted = fit_variogram_reml(points, values, model="exponential",
                                anisotropy_azimuth_deg=0, anisotropy_ratio=1,
                                fit_anisotropy=True)
    assert fitted["anisotropy_fitted"] is True
    assert 0.0 <= fitted["anisotropy_azimuth_deg"] < 180.0
    assert 0.1 <= fitted["anisotropy_ratio"] <= 1.0
    assert fitted["reml_objective"] <= fixed["reml_objective"] + 1e-6


def test_reml_rejects_non_boolean_anisotropy_flag():
    points = np.array([(x, y) for x in range(2) for y in range(2)], dtype=float)
    with pytest.raises(ValueError):
        fit_variogram_reml(points, [0, 1, 2, 4], fit_anisotropy=1)


def test_matern_reml_returns_finite_covariance_fit():
    rng = np.random.default_rng(96)
    points = np.array([(x, y) for x in range(4) for y in range(4)], dtype=float)
    delta = points[:, None, :] - points[None, :, :]
    distance = np.sqrt(np.sum(delta * delta, axis=2))
    q = np.sqrt(3.0) * distance / 1.7
    covariance = 0.25 * (1.0 + q) * np.exp(-q)
    covariance.flat[::len(points) + 1] += 0.75
    values = rng.multivariate_normal(np.full(len(points), 2.0), covariance)
    fit = fit_variogram_reml(points, values, model="matern", nu=1.5)
    assert fit["model"] == "matern"
    assert fit["nu"] == pytest.approx(1.5)
    assert fit["nugget"] > 0
    assert fit["partial_sill"] > 0
    assert np.isfinite(fit["reml_objective"])
