import pytest
from prediction import predict_position, predictive_range_query, dead_reckoning_update_required

def test_constant_velocity_prediction():
    assert predict_position((1, 2), (3, -1), 4) == (13.0, -2.0)

def test_predictive_query_returns_future_positions_inside_rectangle():
    objects = {"approaching": (-2, 5, 1, 0), "leaving": (2, 5, 1, 0), "stationary": (20, 20, 0, 0)}
    result = predictive_range_query(objects, (0, 0, 10, 10), 3)
    assert [row[0] for row in result] == ["approaching", "leaving"]
    assert result[0][1] == (1.0, 5.0)
    assert result[1][1] == (5.0, 5.0)

def test_uncertainty_disk_intersects_rectangle_when_center_is_outside():
    objects = {"near": (-1, 5, 0, 0), "far": (-2, 5, 0, 0)}
    result = predictive_range_query(objects, (0, 0, 10, 10), 0, uncertainty_radius=1.0)
    assert [row[0] for row in result] == ["near"]
    assert result[0][2] == pytest.approx(1.0)

def test_uncertainty_disk_tangent_to_corner_is_included():
    result = predictive_range_query({"corner": (-1, -1, 0, 0)}, (0, 0, 10, 10), 0, uncertainty_radius=2 ** 0.5)
    assert len(result) == 1

def test_dead_reckoning_update_uses_strict_error_threshold():
    assert not dead_reckoning_update_required((0, 0), (1, 0), 5, (5, 0), tolerance=0)
    assert not dead_reckoning_update_required((0, 0), (1, 0), 5, (5, 1), tolerance=1)
    assert dead_reckoning_update_required((0, 0), (1, 0), 5, (5, 1.01), tolerance=1)

@pytest.mark.parametrize("position,velocity,horizon", [
    ((0,), (1, 2), 1), ((0, 0), (1, 2), -1),
    ((0, 0), (float("nan"), 2), 1), ((True, 0), (1, 2), 1),
])
def test_prediction_rejects_invalid_input(position, velocity, horizon):
    with pytest.raises(ValueError):
        predict_position(position, velocity, horizon)

def test_predictive_query_rejects_invalid_bounds_and_states():
    with pytest.raises(ValueError):
        predictive_range_query({}, (2, 0, 1, 1), 1)
    with pytest.raises(ValueError):
        predictive_range_query({"bad": (0, 0, 1)}, (0, 0, 1, 1), 1)
    with pytest.raises(ValueError):
        predictive_range_query({}, (0, 0, 1, 1), -1)

def test_dead_reckoning_rejects_negative_tolerance():
    with pytest.raises(ValueError):
        dead_reckoning_update_required((0, 0), (1, 0), 1, (1, 0), tolerance=-1)
