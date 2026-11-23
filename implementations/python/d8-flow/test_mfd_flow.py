import numpy as np
import pytest

from mfd_flow import mfd_flow_accumulation, mfd_flow_weights


def test_mfd_weights_split_flow_between_two_lower_neighbours():
    dem = np.array([[1.0, 2.0, 1.0]])
    weights = mfd_flow_weights(dem, exponent=1.0)
    assert weights[0, 1, 4] == pytest.approx(0.5)  # west
    assert weights[0, 1, 0] == pytest.approx(0.5)  # east
    assert weights[0, 1].sum() == pytest.approx(1.0)


def test_power_exponent_controls_convergence_toward_steeper_neighbour():
    dem = np.array([[1.0, 2.0, 0.0]])
    linear = mfd_flow_weights(dem, exponent=1.0)
    concentrated = mfd_flow_weights(dem, exponent=2.0)
    assert concentrated[0, 1, 0] > linear[0, 1, 0]
    assert concentrated[0, 1, 4] < linear[0, 1, 4]


def test_rectangular_cell_spacing_changes_slope_weights():
    dem = np.array([[10.0, 9.0], [8.0, 10.0]])
    square = mfd_flow_weights(dem, cell_size=(1.0, 1.0))
    rectangular = mfd_flow_weights(dem, cell_size=(3.0, 1.0))
    assert square[0, 0, 2] > rectangular[0, 0, 2]
    assert rectangular[0, 0, 0] > square[0, 0, 0]


def test_mfd_sink_and_nodata_cells_have_zero_weights():
    dem = np.array([[5.0, -9999.0, 5.0], [5.0, 1.0, 5.0], [5.0, 5.0, 5.0]])
    weights = mfd_flow_weights(dem, nodata=-9999)
    assert np.all(weights[1, 1] == 0)
    assert np.all(weights[0, 1] == 0)


def test_mfd_accumulation_conserves_total_at_terminal_sink():
    dem = np.array([[3.0, 3.0, 3.0], [3.0, 2.0, 3.0], [3.0, 3.0, 3.0]])
    weights = mfd_flow_weights(dem)
    accumulation = mfd_flow_accumulation(dem, weights)
    assert accumulation[1, 1] == pytest.approx(9.0)


def test_mfd_accumulation_splits_contribution_conservatively():
    dem = np.array([[1.0, 2.0, 1.0]])
    weights = mfd_flow_weights(dem, exponent=1.0)
    accumulation = mfd_flow_accumulation(dem, weights)
    assert accumulation[0, 0] == pytest.approx(1.5)
    assert accumulation[0, 1] == pytest.approx(1.0)
    assert accumulation[0, 2] == pytest.approx(1.5)


def test_mfd_accumulation_supports_weighted_initial_contributions():
    dem = np.array([[3.0, 2.0]])
    weights = mfd_flow_weights(dem)
    result = mfd_flow_accumulation(
        dem, weights, initial_contribution=np.array([[2.0, 5.0]])
    )
    assert result[0, 1] == pytest.approx(7.0)


def test_mfd_rejects_invalid_weights_and_uphill_edges():
    dem = np.array([[2.0, 1.0]])
    with pytest.raises(ValueError):
        mfd_flow_accumulation(dem, np.ones((1, 2, 8)))
    bad = np.zeros((1, 2, 8))
    bad[0, 1, 4] = 1.0
    with pytest.raises(ValueError, match="strictly downhill"):
        mfd_flow_accumulation(dem, bad)


def test_mfd_rejects_invalid_exponent_spacing_and_mask():
    with pytest.raises(ValueError):
        mfd_flow_weights([[2.0, 1.0]], exponent=0.0)
    with pytest.raises(ValueError):
        mfd_flow_weights([[2.0, 1.0]], cell_size=(1.0, 0.0))
    with pytest.raises(ValueError):
        mfd_flow_weights([[2.0, 1.0]], valid_mask=np.ones((2, 2)))


def test_random_dem_topological_accumulation_conserves_total_at_sinks():
    rng = np.random.default_rng(55)
    for _ in range(10):
        dem = rng.integers(0, 100, size=(8, 9)).astype(float)
        valid = rng.random(dem.shape) > 0.1
        weights = mfd_flow_weights(dem, valid_mask=valid, exponent=1.3)
        initial = np.where(valid, rng.uniform(0.1, 2.0, size=dem.shape), 0.0)
        result = mfd_flow_accumulation(
            dem, weights, valid_mask=valid, initial_contribution=initial
        )
        sinks = valid & (weights.sum(axis=2) == 0)
        assert np.nansum(result[sinks]) == pytest.approx(initial[valid].sum())
        assert np.isnan(result[~valid]).all()
