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
    for insertion_index, (corridor, splits) in enumerate(zip(
        locator.insertion_corridors, locator.insertion_splits
    )):
        sid = locator.insertion_order[insertion_index]
        assert corridor
        assert len(corridor) == len(splits)
        assert corridor[0].x_left < source[sid][0][0] < corridor[0].x_right
        assert corridor[-1].x_left < source[sid][1][0] < corridor[-1].x_right
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


def test_corridor_cells_have_reciprocal_neighbor_links():
    locator = RandomizedTrapezoidalMap(segments(), (0, 0, 10, 10), seed=19)
    by_id = {cell.id: cell for cell in locator.trapezoids}
    for cell in locator.trapezoids:
        for neighbor_id in cell.right_neighbors:
            assert cell.id in by_id[neighbor_id].left_neighbors
        for neighbor_id in cell.left_neighbors:
            assert cell.id in by_id[neighbor_id].right_neighbors
    for corridor in locator.insertion_corridors:
        for left, right in zip(corridor, corridor[1:]):
            assert right.id in left.right_neighbors


def _trapezoid_area(locator, cell):
    xmin, ymin, xmax, ymax = locator.bounds
    def height(x):
        bottom = ymin if cell.bottom_segment is None else (
            locator.segments[cell.bottom_segment][0][1]
            + (x-locator.segments[cell.bottom_segment][0][0])
            * (locator.segments[cell.bottom_segment][1][1]
               - locator.segments[cell.bottom_segment][0][1])
            / (locator.segments[cell.bottom_segment][1][0]
               - locator.segments[cell.bottom_segment][0][0])
        )
        top = ymax if cell.top_segment is None else (
            locator.segments[cell.top_segment][0][1]
            + (x-locator.segments[cell.top_segment][0][0])
            * (locator.segments[cell.top_segment][1][1]
               - locator.segments[cell.top_segment][0][1])
            / (locator.segments[cell.top_segment][1][0]
               - locator.segments[cell.top_segment][0][0])
        )
        return top-bottom
    return (cell.x_right-cell.x_left) * (
        height(cell.x_left)+height(cell.x_right)
    ) / 2


def test_persistent_corridor_replacements_preserve_full_domain_and_reciprocity():
    locator = RandomizedTrapezoidalMap(segments(), (0, 0, 10, 10), seed=19)
    assert len(locator.insertion_replacements) == len(segments())
    assert len(locator.replacement_graph_snapshots) == len(segments())
    for replacement, snapshot in zip(
        locator.insertion_replacements, locator.replacement_graph_snapshots
    ):
        by_id = {cell.id: cell for cell in snapshot}
        assert not (set(replacement.removed_cell_ids) & set(by_id))
        assert set(cell.id for cell in replacement.added_cells) <= set(by_id)
        assert all(cell.x_left < cell.x_right for cell in snapshot)
        for cell in snapshot:
            for neighbor_id in cell.right_neighbors:
                assert cell.id in by_id[neighbor_id].left_neighbors
            for neighbor_id in cell.left_neighbors:
                assert cell.id in by_id[neighbor_id].right_neighbors
        assert sum(_trapezoid_area(locator, cell) for cell in snapshot) == pytest.approx(100.0)

    # Compare every persistent snapshot with an independently rebuilt static
    # decomposition of exactly the same insertion prefix.
    for insertion_index, snapshot in enumerate(locator.replacement_graph_snapshots):
        prefix = locator.insertion_order[:insertion_index + 1]
        locator._build(prefix)
        signature = lambda cells: sorted(
            (cell.x_left, cell.x_right,
             -1 if cell.bottom_segment is None else cell.bottom_segment,
             -1 if cell.top_segment is None else cell.top_segment)
            for cell in cells
        )
        assert signature(snapshot) == signature(locator.trapezoids)


def test_endpoint_cells_keep_uncrossed_caps_in_replacement_record():
    locator = RandomizedTrapezoidalMap(segments(), (0, 0, 10, 10), seed=19)
    for sid, corridor, replacement in zip(
        locator.insertion_order, locator.insertion_corridors,
        locator.insertion_replacements
    ):
        x0, x1 = locator.segments[sid][0][0], locator.segments[sid][1][0]
        caps = [
            cell for cell in replacement.added_cells
            if (cell.top_segment, cell.bottom_segment) == (
                corridor[0].top_segment, corridor[0].bottom_segment
            ) or (cell.top_segment, cell.bottom_segment) == (
                corridor[-1].top_segment, corridor[-1].bottom_segment
            )
        ]
        assert any(cell.x_right == x0 for cell in caps) or corridor[0].x_left == x0
        assert any(cell.x_left == x1 for cell in caps) or corridor[-1].x_right == x1


def test_persistent_history_dag_matches_rebuilt_locator_on_seeded_queries():
    rng = random.Random(20261116)
    locator = RandomizedTrapezoidalMap(segments(), (0, 0, 10, 10), seed=19)
    assert locator.history_node_count > 0
    queries = [(rng.uniform(-1, 11), rng.uniform(-1, 11)) for _ in range(2000)]
    queries.extend((a[0], a[1]) for a, _b in locator.segments)
    queries.extend((b[0], b[1]) for _a, b in locator.segments)
    for x, y in queries:
        expected = locator._locate_slab(x, y)
        actual = locator._locate_history(x, y)
        if expected == BOUNDARY or expected is None:
            assert actual == expected
        else:
            assert isinstance(actual, Trapezoid)
            assert (
                actual.x_left, actual.x_right,
                actual.bottom_segment, actual.top_segment
            ) == (
                expected.x_left, expected.x_right,
                expected.bottom_segment, expected.top_segment
            )


@pytest.mark.parametrize("source", [
    [((2.0, 2.0), (8.0, 7.0))],
    [],
    [((1.0, 5.0), (9.0, 5.0))],
])
def test_history_dag_handles_empty_single_and_horizontal_inputs(source):
    locator = RandomizedTrapezoidalMap(source, (0, 0, 10, 10), seed=23)
    rng = random.Random(90210)
    queries = [(rng.uniform(0, 10), rng.uniform(0, 10)) for _ in range(500)]
    for segment in source:
        queries.extend([segment[0], segment[1]])
        x0, x1 = segment[0][0], segment[1][0]
        queries.extend([(x0, 1.0), (x0, 9.0), (x1, 1.0), (x1, 9.0)])
    for x, y in queries:
        expected = locator._locate_slab(x, y)
        actual = locator._locate_history(x, y)
        if expected == BOUNDARY or expected is None:
            assert actual == expected
        else:
            assert isinstance(actual, Trapezoid)
            assert (
                actual.x_left, actual.x_right,
                actual.bottom_segment, actual.top_segment
            ) == (
                expected.x_left, expected.x_right,
                expected.bottom_segment, expected.top_segment
            )


@pytest.mark.parametrize("seed", range(16))
def test_history_dag_differential_across_insertion_orders(seed):
    rng = random.Random(7000 + seed)
    locator = RandomizedTrapezoidalMap(segments(), (0, 0, 10, 10), seed=seed)
    assert sorted(locator.insertion_order) == list(range(len(segments())))
    for _ in range(250):
        x, y = rng.uniform(-0.5, 10.5), rng.uniform(-0.5, 10.5)
        expected = locator._locate_slab(x, y)
        actual = locator._locate_history(x, y)
        if expected == BOUNDARY or expected is None:
            assert actual == expected
        else:
            assert isinstance(actual, Trapezoid)
            assert (
                actual.x_left, actual.x_right,
                actual.bottom_segment, actual.top_segment
            ) == (
                expected.x_left, expected.x_right,
                expected.bottom_segment, expected.top_segment
            )


def test_public_query_uses_the_persistent_history_dag():
    locator = RandomizedTrapezoidalMap(segments(), (0, 0, 10, 10), seed=31)
    for point in [(0.5, 0.5), (4.0, 2.5), (5.0, 5.5), (9.5, 9.5)]:
        public = locator.locate(*point)
        history = locator._locate_history(*point)
        reference = locator._locate_slab(*point)
        assert public == history
        if reference == BOUNDARY or reference is None:
            assert public == reference
        else:
            assert isinstance(public, Trapezoid)
            assert (public.x_left, public.x_right,
                    public.bottom_segment, public.top_segment) == (
                reference.x_left, reference.x_right,
                reference.bottom_segment, reference.top_segment
            )
