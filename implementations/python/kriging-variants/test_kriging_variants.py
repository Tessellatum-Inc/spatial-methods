import numpy as np
import pytest

from kriging_variants import kriging_predict


def test_simple_kriging_matches_one_observation_closed_form():
    result = kriging_predict(
        [(0, 0)], [5], [(1, 0)], drift="simple", known_mean=2,
        model="exponential", nugget=0.5, partial_sill=2, range_=1,
    )
    covariance = 2 * np.exp(-3)
    expected_weight = covariance / 2.5
    assert result["prediction"][0] == pytest.approx(2 + expected_weight * 3)
    assert result["variance"][0] == pytest.approx(2 - covariance**2 / 2.5)


def test_ordinary_kriging_reproduces_constant_field_and_unit_sum_weights():
    points = [(0, 0), (1, 0), (0, 1), (1, 1)]
    result = kriging_predict(
        points, [7, 7, 7, 7], [(0.2, 0.3), (0.8, 0.6)],
        drift="ordinary", model="spherical", partial_sill=2, range_=2,
    )
    np.testing.assert_allclose(result["prediction"], [7, 7], atol=1e-10)
    np.testing.assert_allclose(result["weights"].sum(axis=1), [1, 1], atol=1e-10)
    assert np.all(result["variance"] >= 0)


def test_universal_linear_drift_reproduces_a_planar_trend():
    points = [(x, y) for x in range(4) for y in range(3)]
    values = [3 + 2*x - 4*y for x, y in points]
    targets = [(0.5, 0.5), (2.2, 1.7), (4.0, -1.0)]
    expected = [3 + 2*x - 4*y for x, y in targets]
    result = kriging_predict(
        points, values, targets, drift="linear",
        model="exponential", nugget=0, partial_sill=1.5, range_=2.5,
    )
    np.testing.assert_allclose(result["prediction"], expected, atol=1e-9)
    np.testing.assert_allclose(result["weights"].sum(axis=1), 1.0, atol=1e-9)
    assert np.all(result["variance"] >= 0)


def test_zero_nugget_kriging_reproduces_sampled_values():
    points = [(0, 0), (1, 0), (0, 1), (1, 1)]
    values = [1, 2, 3, 5]
    result = kriging_predict(
        points, values, points, drift="ordinary",
        model="exponential", nugget=0, partial_sill=1, range_=2,
    )
    np.testing.assert_allclose(result["prediction"], values, atol=1e-9)
    np.testing.assert_allclose(result["variance"], 0, atol=1e-9)


def test_universal_prediction_matches_independent_block_system():
    points = np.array([(0, 0), (1, 0), (0, 1), (1, 1), (2, 0)], dtype=float)
    values = np.array([1, 2, 3, 5, 4], dtype=float)
    target = np.array([[0.4, 0.7]])
    result = kriging_predict(points, values, target, drift="linear",
                             model="gaussian", partial_sill=1.2, range_=2.0)
    d = np.linalg.norm(points[:, None] - points[None, :], axis=2)
    c = 1.2 * np.exp(-3 * (d / 2.0)**2)
    f = np.column_stack((np.ones(len(points)), points[:, 0], points[:, 1]))
    dt = np.linalg.norm(points - target[0], axis=1)
    c0 = 1.2 * np.exp(-3 * (dt / 2.0)**2)
    f0 = np.array([1.0, 0.4, 0.7])
    system = np.block([[c, f], [f.T, np.zeros((3, 3))]])
    oracle = np.linalg.solve(system, np.r_[c0, f0])
    assert result["prediction"][0] == pytest.approx(oracle[:5] @ values)
    assert result["variance"][0] == pytest.approx(
        1.2 - oracle[:5] @ c0 - oracle[5:] @ f0
    )


def test_invalid_and_rank_deficient_kriging_inputs_are_rejected():
    with pytest.raises(ValueError, match="rank deficient"):
        kriging_predict([(0, 0), (1, 0), (2, 0)], [1, 2, 3],
                        [(0.5, 1)], drift="linear")
    with pytest.raises(ValueError, match="finite"):
        kriging_predict([(0, 0), (1, 0)], [1, np.nan], [(0, 1)])
    with pytest.raises(ValueError, match="positive"):
        kriging_predict([(0, 0)], [1], [(1, 0)], partial_sill=0)
    with pytest.raises(ValueError, match="drift"):
        kriging_predict([(0, 0)], [1], [(1, 0)], drift="unknown")
