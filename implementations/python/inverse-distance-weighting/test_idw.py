import pytest
from idw import idw_interpolate

def test_exact_sample_location_returns_observed_value():
    assert idw_interpolate([(0,0),(1,0)], [4,8], [(0,0)]) == [4]

def test_duplicate_exact_samples_are_averaged():
    assert idw_interpolate([(0,0),(0,0),(1,0)], [2,4,9], [(0,0)]) == [3]

def test_equal_distance_samples_receive_equal_weights():
    result = idw_interpolate([(-1,0),(1,0)], [2,6], [(0,0)])
    assert result == pytest.approx([4])

def test_inverse_square_weights_match_hand_calculation():
    result = idw_interpolate([(1,0),(2,0)], [10,20], [(0,0)], power=2)
    expected = (10/1**2 + 20/2**2) / (1/1**2 + 1/2**2)
    assert result == pytest.approx([expected])

def test_max_neighbors_uses_nearest_samples_with_stable_ties():
    result = idw_interpolate([(1,0),(-1,0),(5,0)], [2,6,100], [(0,0)], max_neighbors=2)
    assert result == pytest.approx([4])

def test_radius_excludes_distant_samples_and_returns_none_when_empty():
    result = idw_interpolate([(1,0),(10,0)], [3,9], [(0,0),(20,20)], radius=2)
    assert result[0] == pytest.approx(3)
    assert result[1] is None

def test_empty_queries_return_empty_result():
    assert idw_interpolate([(0,0)], [1], []) == []

@pytest.mark.parametrize("kwargs", [
    {"power": 0}, {"max_neighbors": 0}, {"radius": 0}
])
def test_invalid_controls_are_rejected(kwargs):
    with pytest.raises(ValueError):
        idw_interpolate([(0,0)], [1], [(1,1)], **kwargs)

@pytest.mark.parametrize("samples,values,queries", [
    ([], [], [(0,0)]), ([(0,0)], [], [(0,0)]),
    ([(0,0,1)], [1], [(0,0)]), ([(0,0)], [float("nan")], [(0,0)]),
    ([(0,0)], [1], [(float("inf"),0)])
])
def test_invalid_samples_values_and_queries_are_rejected(samples,values,queries):
    with pytest.raises(ValueError):
        idw_interpolate(samples, values, queries)

def test_non_sequence_values_are_rejected():
    with pytest.raises(ValueError):
        idw_interpolate([(0, 0)], None, [(1, 1)])
