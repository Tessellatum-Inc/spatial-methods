import random

import pytest

from hand import height_above_nearest_drainage


def test_linear_drainage_path_and_stream_cells_have_zero_hand():
    elevation = [[9, 8, 7, 6, 5]]
    directions = [[1, 1, 1, 1, 0]]
    streams = [[False, False, True, False, True]]
    assert height_above_nearest_drainage(elevation, directions, streams) == [
        [2.0, 1.0, 0.0, 1.0, 0.0]
    ]


def test_branching_paths_reach_their_first_downstream_stream_cell():
    elevation = [
        [8, 7, 6],
        [9, 6, 4],
        [10, 5, 3],
    ]
    directions = [
        [2, 4, 4],
        [1, 1, 4],
        [1, 1, 0],
    ]
    streams = [
        [False, False, True],
        [False, False, True],
        [False, False, True],
    ]
    hand = height_above_nearest_drainage(elevation, directions, streams)
    assert hand[0][0] == 4.0  # 8 -> 6 -> first stream elevation 4
    assert hand[1][0] == 5.0  # 9 -> 6 -> first stream elevation 4
    assert hand[2][0] == 7.0  # 10 -> 5 -> first stream elevation 3


def test_paths_without_a_stream_return_none_and_nodata_is_preserved():
    elevation = [[5, 4, None], [6, 3, 2]]
    directions = [[1, 0, None], [1, 1, 0]]
    streams = [[False, False, False], [False, False, False]]
    result = height_above_nearest_drainage(elevation, directions, streams)
    assert result == [[None, None, None], [None, None, None]]


def test_nodata_terminates_a_flow_path():
    elevation = [[5, None, 1]]
    directions = [[1, None, 0]]
    streams = [[False, False, True]]
    assert height_above_nearest_drainage(elevation, directions, streams) == [
        [None, None, 0.0]
    ]


def test_cycle_is_rejected():
    elevation = [[4, 3]]
    directions = [[1, 16]]
    streams = [[False, False]]
    # Strict downhill validation rejects this cyclic receiver pair before
    # traversal; any valid strictly descending D8 graph is necessarily acyclic.
    with pytest.raises(ValueError):
        height_above_nearest_drainage(elevation, directions, streams)


def test_uphill_receiver_is_rejected():
    with pytest.raises(ValueError, match="strictly downhill"):
        height_above_nearest_drainage([[1, 2]], [[1, 0]], [[False, True]])


def test_invalid_shapes_codes_and_stream_masks_are_rejected():
    with pytest.raises(ValueError, match="match elevation"):
        height_above_nearest_drainage([[2]], [[0, 0]], [[False]])
    with pytest.raises(ValueError, match="unsupported"):
        height_above_nearest_drainage([[2]], [[3]], [[False]])
    with pytest.raises(ValueError, match="boolean"):
        height_above_nearest_drainage([[2]], [[0]], [[1]])
    with pytest.raises(ValueError, match="valid elevations"):
        height_above_nearest_drainage([[None]], [[None]], [[True]])


def test_seeded_random_eastward_drainage_matches_hand_oracle():
    rng = random.Random(20261115)
    rows, cols = 18, 25
    elevation = [
        [float(1000 - 3 * c - r) + rng.random() * 0.01 for c in range(cols)]
        for r in range(rows)
    ]
    directions = [[1 if c < cols - 1 else 0 for c in range(cols)]
                  for _ in range(rows)]
    streams = [[c == cols - 1 for c in range(cols)] for _ in range(rows)]
    result = height_above_nearest_drainage(elevation, directions, streams)
    for r in range(rows):
        for c in range(cols):
            assert result[r][c] == pytest.approx(elevation[r][c] - elevation[r][-1])
