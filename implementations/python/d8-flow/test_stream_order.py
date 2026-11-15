import numpy as np
import pytest

from stream_order import d8_stream_orders


def test_single_stream_and_outlet_orders_are_one():
    fd = np.array([[1, 1, 0]])
    mask = np.ones((1, 3), dtype=bool)
    strahler, shreve = d8_stream_orders(fd, mask)
    np.testing.assert_array_equal(strahler, [[1, 1, 1]])
    np.testing.assert_array_equal(shreve, [[1, 1, 1]])


def test_strahler_increments_only_when_equal_highest_orders_meet():
    # Two first-order branches meet at cell (2,2), then join a third first-order branch.
    fd = np.array([
        [0, 4, 0, 0, 0],
        [0, 2, 4, 8, 0],
        [0, 1, 1, 16, 0],
        [0, 128, 64, 32, 0],
        [0, 0, 0, 0, 0],
    ], dtype=int)
    mask = np.zeros(fd.shape, dtype=bool)
    # Simpler explicit tributary tree: west and north tributaries meet, then flow east.
    fd = np.array([
        [0, 4, 0, 0],
        [0, 1, 1, 0],
        [0, 0, 0, 0],
    ], dtype=int)
    mask[0, 1] = mask[1, 1] = mask[1, 2] = True
    strahler, shreve = d8_stream_orders(fd, mask)
    assert strahler[1, 1] == 1
    assert strahler[1, 2] == 2
    assert shreve[1, 2] == 2


def test_shreve_adds_magnitudes_at_confluences():
    fd = np.array([[1, 4, 1, 4, 0]], dtype=int)
    mask = np.array([[1, 1, 1, 1, 1]], dtype=bool)
    strahler, shreve = d8_stream_orders(fd, mask)
    assert shreve[0, 4] == 5
    assert strahler[0, 4] == 2


def test_unequal_strahler_orders_do_not_increment():
    fd = np.array([
        [1, 4, 1, 4, 0],
    ], dtype=int)
    mask = np.ones(fd.shape, dtype=bool)
    # This linear chain has no branching: all cells remain first order.
    strahler, _ = d8_stream_orders(fd, mask)
    np.testing.assert_array_equal(strahler, np.ones(fd.shape))


def test_nonstream_cells_are_nan_and_empty_mask_is_supported():
    fd = np.array([[1, 0], [0, 0]], dtype=int)
    mask = np.array([[True, False], [False, False]])
    s, m = d8_stream_orders(fd, mask)
    assert s[0, 0] == 1 and m[0, 0] == 1
    assert np.isnan(s[1, 1]) and np.isnan(m[1, 1])
    empty = d8_stream_orders(fd, np.zeros(fd.shape, dtype=bool))
    assert np.isnan(empty[0]).all()


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
