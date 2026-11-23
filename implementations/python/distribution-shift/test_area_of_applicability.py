import numpy as np
import pytest
from area_of_applicability import fit_applicability_envelope, predict_applicability


def test_training_points_are_inside_leave_one_out_envelope():
    x = np.array([[0, 0], [1, 0], [0, 1], [1, 1], [.5, .5]], dtype=float)
    model = fit_applicability_envelope(x, quantile=.95)
    result = predict_applicability(model, x)
    assert result["applicable"].all()
    assert np.all(result["dissimilarity"] <= model["threshold"])


def test_far_extrapolation_is_outside_envelope():
    x = np.array([[0, 0], [1, 0], [0, 1], [1, 1], [.5, .5]], dtype=float)
    model = fit_applicability_envelope(x)
    result = predict_applicability(model, [[20, 20]])
    assert not result["applicable"][0]


def test_feature_weights_change_distance_and_are_normalised():
    x = np.array([[0, 0], [1, 0], [0, 1], [1, 1], [.5, .5]], dtype=float)
    model = fit_applicability_envelope(x, feature_weights=[9, 1])
    assert model["feature_weights"].sum() == pytest.approx(1)
    a = predict_applicability(model, [[1.1, .5]])
    b = predict_applicability(model, [[.5, 1.1]])
    assert a["dissimilarity"][0] != pytest.approx(b["dissimilarity"][0])


def test_constant_predictor_is_handled_without_division_by_zero():
    x = np.array([[0, 1], [1, 1], [2, 1], [3, 1]], dtype=float)
    model = fit_applicability_envelope(x)
    result = predict_applicability(model, [[2.5, 1]])
    assert np.isfinite(result["dissimilarity"]).all()


@pytest.mark.parametrize("bad", [np.array([[1.0], [1.0]]), np.array([[1.0], [np.nan], [2.0]])])
def test_invalid_training_data_rejected(bad):
    with pytest.raises(ValueError):
        fit_applicability_envelope(bad)


def test_invalid_weights_and_quantile_rejected():
    x = np.array([[0, 0], [1, 0], [0, 1]], dtype=float)
    with pytest.raises(ValueError):
        fit_applicability_envelope(x, feature_weights=[0, 0])
    with pytest.raises(ValueError):
        fit_applicability_envelope(x, quantile=1)
