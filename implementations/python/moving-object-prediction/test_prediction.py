import pytest
from prediction import predict_position, predictive_range_query, dead_reckoning_update_required


def test_constant_velocity_prediction():
    assert predict_position((1, 2), (3, -1), 4) == (13.0, -2.0)


def test_zero_horizon_preserves_position():
    assert predict_position((3.5, -2), (100, -50), 0) == (3.5, -2.0)


def test_predictive_query_rectangle_edges_are_inclusive():
    result = predictive_range_query({"edge": (-1, 5, 1, 0)}, (0, 0, 10, 10), 1)
    assert result == [("edge", (0.0, 5.0), 0.0)]


def test_predictive_query_uncertainty_disk_and_mapping_order():
    objects = {"near": (-1, 5, 0, 0), "far": (-2, 5, 0, 0)}
    result = predictive_range_query(objects, (0, 0, 10, 10), 0, uncertainty_radius=1)
    assert [r[0] for r in result] == ["near"]
    assert result[0][2] == pytest.approx(1)


def test_uncertainty_disk_tangent_to_corner_is_included():
    result = predictive_range_query({"corner": (-1, -1, 0, 0)}, (0, 0, 10, 10),
                                    0, uncertainty_radius=2 ** 0.5)
    assert len(result) == 1


def test_dead_reckoning_threshold_is_strict():
    assert not dead_reckoning_update_required((0, 0), (1, 0), 5, (5, 1), tolerance=1)
    assert dead_reckoning_update_required((0, 0), (1, 0), 5, (5, 1.01), tolerance=1)


@pytest.mark.parametrize("position,velocity,horizon", [
    ((0,), (1, 2), 1), ((0, 0), (1, 2), -1),
    ((0, 0), (float("nan"), 2), 1), ((True, 0), (1, 2), 1),
    ((1e308, 0), (1e308, 0), 1), ((0, 0), (1e308, 0), 1e308),
])
def test_prediction_rejects_invalid_or_overflowing_input(position, velocity, horizon):
    with pytest.raises(ValueError):
        predict_position(position, velocity, horizon)


def test_predictive_query_rejects_invalid_bounds_states_and_overflow():
    with pytest.raises(ValueError):
        predictive_range_query({}, (2, 0, 1, 1), 1)
    with pytest.raises(ValueError):
        predictive_range_query({"bad": (0, 0, 1)}, (0, 0, 1, 1), 1)
    with pytest.raises(ValueError):
        predictive_range_query({}, (0, 0, 1, 1), -1)
    with pytest.raises(ValueError, match="overflow"):
        predictive_range_query({"fast": (0, 0, 1e308, 0)}, (0, 0, 1, 1), 1e308)


def test_dead_reckoning_rejects_negative_tolerance_and_overflow():
    with pytest.raises(ValueError):
        dead_reckoning_update_required((0, 0), (1, 0), 1, (1, 0), tolerance=-1)
    with pytest.raises(ValueError, match="overflow"):
        dead_reckoning_update_required((0, 0), (1e308, 0), 1, (0, 0), tolerance=1)


def test_invalid_bounds_and_tolerance_nan_are_rejected():
    with pytest.raises(ValueError):
        predictive_range_query({}, (0, 0, float("inf"), 1), 0)
    with pytest.raises(ValueError):
        predictive_range_query({}, (0, 0, 1, 1), 0, uncertainty_radius=float("nan"))
    with pytest.raises(ValueError):
        dead_reckoning_update_required((0, 0), (0, 0), 0, (0, 0), tolerance=float("nan"))

from prediction import continuous_range_query


def test_continuous_query_finds_crossing_even_when_endpoint_is_outside():
    result = continuous_range_query(
        {"crossing": (-5, 5, 2, 0)}, (0, 0, 10, 10), 10
    )
    assert result == [("crossing", (0.0, 5.0), 2.5)]


def test_continuous_query_reports_zero_time_for_initially_inside_object():
    result = continuous_range_query(
        {"inside": (5, 5, 1, 0)}, (0, 0, 10, 10), 5
    )
    assert result == [("inside", (5.0, 5.0), 0.0)]


def test_continuous_query_includes_tangent_and_boundary_contact():
    result = continuous_range_query(
        {"tangent": (-1, 0, 1, 0), "boundary": (10, 5, 1, 0)},
        (0, 0, 10, 10), 2,
    )
    assert [row[0] for row in result] == ["tangent", "boundary"]
    assert result[0][1] == (0.0, 0.0)
    assert result[1][2] == 0.0


def test_continuous_query_rejects_invalid_and_overflowing_states():
    with pytest.raises(ValueError):
        continuous_range_query({}, (2, 0, 1, 1), 1)
    with pytest.raises(ValueError):
        continuous_range_query({"bad": (0, 0, 1)}, (0, 0, 1, 1), 1)
    with pytest.raises(ValueError, match="overflow"):
        continuous_range_query({"fast": (0, 0, 1e308, 0)}, (0, 0, 1, 1), 1e308)
