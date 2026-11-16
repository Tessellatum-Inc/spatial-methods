import numpy as np
import pytest
from cpue import fit_cpue_model, predict_cpue


def test_poisson_cpue_recovers_effort_offset_and_covariate_direction():
    rng = np.random.default_rng(22)
    n = 5000
    x = rng.normal(size=n)
    effort = rng.uniform(.5, 3., size=n)
    mu = effort*np.exp(.4 + .7*x)
    y = rng.poisson(mu)
    model = fit_cpue_model(y, effort, x[:,None], distribution="poisson")
    assert model["converged"]
    assert model["coefficients"][0] == pytest.approx(.4, abs=.07)
    assert model["coefficients"][1] == pytest.approx(.7, abs=.04)
    assert model["standardized_cpue"] == pytest.approx(np.exp(.4), rel=.08)


def test_nb2_cpue_estimates_overdispersion_and_predicts():
    rng = np.random.default_rng(8)
    n = 6000
    x = rng.normal(size=n)
    effort = rng.uniform(.5, 2., size=n)
    mu = effort*np.exp(.2 + .35*x)
    alpha = .45
    size = 1/alpha
    y = rng.negative_binomial(size, size/(size+mu))
    model = fit_cpue_model(y, effort, x[:,None], distribution="nb2")
    assert model["converged"]
    assert model["dispersion"] == pytest.approx(alpha, abs=.12)
    pred = predict_cpue(model, [[0.]], effort=2.)
    assert pred[0] == pytest.approx(2*np.exp(.2), rel=.1)


def test_cpue_validates_counts_effort_and_distribution():
    with pytest.raises(ValueError, match="integer"):
        fit_cpue_model([1., 1.5, 2., 1.], [1.,1.,1.,1.], np.zeros((4,1)))
    with pytest.raises(ValueError, match="positive"):
        fit_cpue_model([1., 2., 3., 4.], [1.,0.,1.,1.], np.zeros((4,1)))
    with pytest.raises(ValueError, match="distribution"):
        fit_cpue_model([1.,2.,3.,4.], [1.,1.,1.,1.], np.zeros((4,1)), distribution="gamma")


def test_cpue_prediction_validates_feature_count():
    model = fit_cpue_model([1,2,3,4,5], [1,1,1,1,1], np.arange(5.)[:,None])
    with pytest.raises(ValueError, match="feature"):
        predict_cpue(model, [[1.,2.]])
