import numpy as np
import pytest

from stream_order import d8_stream_orders


def test_single_stream_chain_has_first_order_and_unit_magnitude():
    fd = np.array([[1, 1, 1, 0]], dtype=int)
    mask = np.ones(fd.shape, dtype=bool)
    strahler, shreve = d8_stream_orders(fd, mask)
    np.testing.assert_array_equal(strahler, [[1, 1, 1, 1]])
    np.testing.assert_array_equal(shreve, [[1, 1, 1, 1]])


def test_three_headwaters_converge_to_second_order_and_magnitude_three():
    fd = np.array([
        [0, 4, 0],
        [1, 1, 0],
        [0, 64, 0],
    ], dtype=int)
    mask = np.zeros(fd.shape, dtype=bool)
    mask[0, 1] = mask[1, 0] = mask[1, 1] = mask[2, 1] = mask[1, 2] = True
    strahler, shreve = d8_stream_orders(fd, mask)
    assert strahler[1, 1] == 2
    assert shreve[1, 1] == 3


def test_first_order_tributary_does_not_raise_second_order_stream():
    fd = np.array([
        [0, 4, 4],
        [1, 1, 0],
    ], dtype=int)
    mask = np.zeros(fd.shape, dtype=bool)
    mask[0, 1] = mask[1, 0] = mask[1, 1] = mask[0, 2] = mask[1, 2] = True
    strahler, shreve = d8_stream_orders(fd, mask)
    assert strahler[1, 1] == 2
    assert shreve[1, 1] == 2
    assert strahler[1, 2] == 2
    assert shreve[1, 2] == 3


def test_nonstream_cells_are_nan_and_empty_mask_is_supported():
    fd = np.array([[0, 0], [0, 0]], dtype=int)
    mask = np.array([[True, False], [False, False]])
    s, m = d8_stream_orders(fd, mask)
    assert s[0, 0] == 1 and m[0, 0] == 1
    assert np.isnan(s[1, 1]) and np.isnan(m[1, 1])
    empty = d8_stream_orders(fd, np.zeros(fd.shape, dtype=bool))
    assert np.isnan(empty).all()


def test_rejects_stream_links_into_nonstream_cells_and_bad_codes():
    with pytest.raises(ValueError, match="receiver"):
        d8_stream_orders(np.array([[1, 0]]), np.array([[True, False]]))
    with pytest.raises(ValueError, match="unsupported"):
        d8_stream_orders(np.array([[3]]), np.array([[True]]))


def test_rejects_cycle_in_stream_graph():
    fd = np.array([[1, 16]], dtype=int)
    mask = np.ones(fd.shape, dtype=bool)
    with pytest.raises(ValueError, match="cycle"):
        d8_stream_orders(fd, mask)


def test_rejects_invalid_shapes_and_nodata_stream_cells():
    with pytest.raises(ValueError, match="match"):
        d8_stream_orders(np.zeros((2, 2), dtype=int), np.ones((3, 3), dtype=bool))
    with pytest.raises(ValueError, match="NoData"):
        d8_stream_orders(np.array([[-1]]), np.array([[True]]))


def test_accepts_integer_valued_float_codes_and_rejects_fractional_codes():
    d8_stream_orders(np.array([[1.0, 0.0]]), np.array([[True, True]]))
    with pytest.raises(ValueError, match="integer"):
        d8_stream_orders(np.array([[1.5]]), np.array([[True]]))
