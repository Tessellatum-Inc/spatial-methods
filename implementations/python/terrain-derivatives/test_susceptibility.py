import numpy as np
import pytest
from susceptibility import (
    drastic_index, frequency_ratio, fit_logistic_susceptibility,
    predict_logistic_susceptibility,
)


def test_drastic_weighted_sum_and_validation():
    layers = np.ones((7, 2, 2)) * 5
    result = drastic_index(layers)
    assert result.shape == (2, 2)
    assert np.all(result == 115)
    with pytest.raises(ValueError):
        drastic_index(np.ones((6, 2, 2)))
    with pytest.raises(ValueError):
        drastic_index(np.ones((7, 2, 2)) * 11)


def test_frequency_ratio_balanced_and_enriched_categories():
    predictor = np.array([1, 1, 1, 2, 2, 2])
    event = np.array([1, 1, 0, 0, 0, 0])
    result = frequency_ratio(predictor, event)
    assert result["frequency_ratio"][1] == pytest.approx(2)
    assert result["frequency_ratio"][2] == pytest.approx(0)
    assert result["raster"][0] == pytest.approx(2)


def test_frequency_ratio_masks_invalid_cells():
    result = frequency_ratio(np.array([1., 2., np.nan]), np.array([1, 0, 0]))
    assert np.isnan(result["raster"][2])
    with pytest.raises(ValueError):
        frequency_ratio([1, 2], [0, 0])


def test_logistic_regression_recovers_positive_signal():
    x = np.array([[-2], [-1], [-.5], [.5], [1], [2]], dtype=float)
    y = np.array([0, 0, 0, 1, 1, 1], dtype=float)
    fit = fit_logistic_susceptibility(x, y, ridge=.01)
    assert fit["coefficients"][1] > 0
    p = predict_logistic_susceptibility(x, fit["coefficients"])
    assert np.all(np.diff(p) > 0)
    assert p[0] < .5 < p[-1]


def test_logistic_validation():
    with pytest.raises(ValueError):
        fit_logistic_susceptibility([[1], [2]], [1, 1])
    with pytest.raises(ValueError):
        predict_logistic_susceptibility([[1, 2]], [0, 1])
