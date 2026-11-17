import pytest

from street_address_interpolation import interpolate_street_addresses


def test_even_address_range_interpolates_on_straight_segment():
    result = interpolate_street_addresses([(0, 0), (100, 0)], 100, 108)
    assert [row["number"] for row in result] == [100, 102, 104, 106, 108]
    assert [row["x"] for row in result] == pytest.approx([0, 25, 50, 75, 100])
    assert all(row["y"] == 0 for row in result)


def test_polyline_uses_cumulative_distance_not_chord_distance():
    result = interpolate_street_addresses([(0, 0), (10, 0), (10, 10)], 1, 3, requested_numbers=[1, 2, 3])
    assert (result[1]["x"], result[1]["y"]) == pytest.approx((10, 0))


def test_mixed_parity_range_generates_every_integer_and_descending_ranges_work():
    ascending = interpolate_street_addresses([(0, 0), (4, 0)], 1, 4)
    descending = interpolate_street_addresses([(0, 0), (4, 0)], 4, 1)
    assert [r["number"] for r in ascending] == [1, 2, 3, 4]
    assert [r["number"] for r in descending] == [4, 3, 2, 1]
    assert [r["x"] for r in descending] == pytest.approx([0, 4/3, 8/3, 4])


def test_requested_numbers_and_side_offsets_are_supported():
    left = interpolate_street_addresses([(0, 0), (10, 0)], 10, 20,
                                         requested_numbers=[12, 18], side="left", offset_distance=2)
    assert [r["number"] for r in left] == [12, 18]
    assert [r["y"] for r in left] == pytest.approx([2, 8])
    right = interpolate_street_addresses([(0, 0), (10, 0)], 10, 20,
                                          requested_numbers=[15], side="right", offset_distance=1)
    assert right[0]["y"] == pytest.approx(-1)


@pytest.mark.parametrize("kwargs", [
    {"start_number": 2, "end_number": 2},
    {"start_number": 10, "end_number": 20, "requested_numbers": [9]},
    {"start_number": 10, "end_number": 20, "requested_numbers": [12, 12]},
    {"start_number": 10, "end_number": 20, "side": "center", "offset_distance": 1},
    {"start_number": 10, "end_number": 20, "side": "north"},
])
def test_invalid_ranges_and_controls_are_rejected(kwargs):
    start = kwargs.pop("start_number", 10)
    end = kwargs.pop("end_number", 20)
    with pytest.raises(ValueError):
        interpolate_street_addresses([(0, 0), (1, 0)], start, end, **kwargs)


def test_rejects_duplicate_vertices_and_nonfinite_coordinates():
    with pytest.raises(ValueError):
        interpolate_street_addresses([(0, 0), (0, 0)], 1, 3)
    with pytest.raises(ValueError):
        interpolate_street_addresses([(0, 0), (float("nan"), 1)], 1, 3)
