import math
import random

import pytest

from randomized_trapezoidal_map import BOUNDARY, RandomizedTrapezoidalMap, Trapezoid


def segments():
    return [
        ((1.0, 2.0), (7.0, 3.0)),
        ((2.0, 6.0), (8.0, 5.0)),
        ((3.0, 8.0), (6.0, 9.0)),
    ]


def test_randomized_build_is_reproducible_for_seed_and_covers_every_slab():
    a = RandomizedTrapezoidalMap(segments(), (0, 0, 10, 10), seed=41)
    b = RandomizedTrapezoidalMap(segments(), (0, 0, 10, 10), seed=41)
    assert a.insertion_order == b.insertion_order
    assert a.insertion_rebuild_sizes == b.insertion_rebuild_sizes
    assert len(a.slabs) == len(a.x_events) - 1
    assert a.search_node_count > 0
    assert len({id(cell) for slab in a.slabs for cell in slab[1]}) == len(a.trapezoids)


def test_query_returns_a_trapezoid_with_correct_vertical_interval():
    locator = RandomizedTrapezoidalMap(segments(), (0, 0, 10, 10), seed=3)
    for x in (0.5, 1.5, 2.5, 3.5, 5.5, 6.5, 7.5, 8.5, 9.5):
        for y in (0.5, 1.5, 4.0, 5.5, 7.0, 9.5):
            cell = locator.locate(x, y)
            assert isinstance(cell, Trapezoid)
            if cell.bottom_segment is None:
                bottom = 0.0
            else:
                bottom = (lambda s: s[0][1] + (x-s[0][0])*(s[1][1]-s[0][1])/(s[1][0]-s[0][0]))(locator.segments[cell.bottom_segment])
            if cell.top_segment is None:
                top = 10.0
            else:
                top = (lambda s: s[0][1] + (x-s[0][0])*(s[1][1]-s[0][1])/(s[1][0]-s[0][0]))(locator.segments[cell.top_segment])
            assert bottom - 1e-10 <= y <= top + 1e-10


def test_original_segment_queries_return_boundary():
    locator = RandomizedTrapezoidalMap(segments(), (0, 0, 10, 10))
    assert locator.locate(4.0, 2.5) == BOUNDARY
    assert locator.locate(5.0, 5.5) == BOUNDARY


def test_artificial_vertical_walls_use_deterministic_right_side_convention():
    locator = RandomizedTrapezoidalMap(segments(), (0, 0, 10, 10))
    left = locator.locate(2.0, 1.0)
    right = locator.locate(2.0 + 1e-7, 1.0)
    assert isinstance(left, Trapezoid)
    assert isinstance(right, Trapezoid)
    assert left.id[0] == right.id[0]


def test_outside_bounding_box_returns_none_and_nonfinite_rejected():
    locator = RandomizedTrapezoidalMap(segments(), (0, 0, 10, 10))
    assert locator.locate(-1, 2) is None
    assert locator.locate(2, 11) is None
    with pytest.raises(ValueError):
        locator.locate(math.nan, 2)


@pytest.mark.parametrize("bad", [
    [((2, 2), (2, 5))],  # vertical
    [((1, 1), (1, 1))],  # zero length
    [((1, 1), (5, 5)), ((1, 5), (5, 1))],  # crossing
    [((1, 1), (5, 5)), ((3, 3), (7, 1))],  # touching
    [((0, 1), (5, 2))],  # outside strict bounding box
])
def test_rejects_unsupported_or_invalid_segment_sets(bad):
    with pytest.raises(ValueError):
        RandomizedTrapezoidalMap(bad, (0, 0, 10, 10))


def test_seeded_random_disjoint_segments_against_independent_cell_scan():
    rng = random.Random(20261116)
    source = []
    for i in range(12):
        x0 = 0.5 + i * 0.7
        x1 = x0 + 0.3
        y = 1.0 + i * 0.6
        source.append(((x0, y), (x1, y + rng.uniform(-0.1, 0.1))))
    locator = RandomizedTrapezoidalMap(source, (0, 0, 10, 10), seed=2026)
    for _ in range(1000):
        x, y = rng.uniform(0, 10), rng.uniform(0, 10)
        result = locator.locate(x, y)
        if result == BOUNDARY:
            assert any(
                min(a[0], b[0]) <= x <= max(a[0], b[0]) and
                abs((a[1] + (x-a[0])*(b[1]-a[1])/(b[0]-a[0])) - y) < 1e-8
                for a, b in source
            )
        else:
            assert isinstance(result, Trapezoid)
            assert result.x_left <= x <= result.x_right



def test_adjacent_slab_intervals_are_merged_into_shared_trapezoids():
    locator = RandomizedTrapezoidalMap(
        [((1, 2), (8, 2.5)), ((2, 6), (9, 6.5))],
        (0, 0, 10, 10), seed=7,
    )
    left = locator.locate(1.5, 1.0)
    right = locator.locate(2.5, 1.0)
    assert isinstance(left, Trapezoid)
    assert left is right
    assert left.x_left == 1.0
    assert left.x_right == 8.0
    assert len(locator.trapezoids) < sum(len(slab[1]) for slab in locator.slabs)



def test_randomized_insertions_trace_corridors_and_form_local_split_pieces():
    source = segments()
    locator = RandomizedTrapezoidalMap(source, (0, 0, 10, 10), seed=19)
    assert len(locator.insertion_corridors) == len(source)
    assert len(locator.insertion_splits) == len(source)
    for sid, (corridor, splits) in enumerate(zip(
        locator.insertion_corridors, locator.insertion_splits
    )):
        assert corridor
        assert len(corridor) == len(splits)
        for cell, split in zip(corridor, splits):
            assert split.source_trapezoid is cell
            assert split.lower.bottom_segment == cell.bottom_segment
            assert split.lower.top_segment == sid
            assert split.upper.bottom_segment == sid
            assert split.upper.top_segment == cell.top_segment
            assert split.lower.x_left == split.upper.x_left
            assert split.lower.x_right == split.upper.x_right
            probe = (split.lower.x_left + split.lower.x_right) / 2
            line_y = (
                source[sid][0][1]
                + (probe-source[sid][0][0])
                * (source[sid][1][1]-source[sid][0][1])
                / (source[sid][1][0]-source[sid][0][0])
            )
            if cell.bottom_segment is not None:
                bottom = (
                    locator.segments[cell.bottom_segment][0][1]
                    + (probe-locator.segments[cell.bottom_segment][0][0])
                    * (locator.segments[cell.bottom_segment][1][1]
                       - locator.segments[cell.bottom_segment][0][1])
                    / (locator.segments[cell.bottom_segment][1][0]
                       - locator.segments[cell.bottom_segment][0][0])
                )
                assert line_y > bottom
            if cell.top_segment is not None:
                top = (
                    locator.segments[cell.top_segment][0][1]
                    + (probe-locator.segments[cell.top_segment][0][0])
                    * (locator.segments[cell.top_segment][1][1]
                       - locator.segments[cell.top_segment][0][1])
                    / (locator.segments[cell.top_segment][1][0]
                       - locator.segments[cell.top_segment][0][0])
                )
                assert line_y < top
