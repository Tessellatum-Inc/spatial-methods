import pytest
from vatti_scanbeam import decompose_scanbeams


def test_rectangle_has_two_scanbeams_and_one_local_minimum():
    ring = [(0, 0), (4, 0), (4, 3), (0, 3)]
    result = decompose_scanbeams([ring])
    assert result.scanbeams == (0.0, 3.0)
    assert len(result.bounds) == 2
    assert len(result.horizontals) == 2
    assert len(result.minima) == 1
    minimum = result.minima[0]
    assert minimum.y == 0
    assert minimum.left_bound.lower == (0.0, 0.0)
    assert minimum.right_bound.lower == (4.0, 0.0)
    assert len(minimum.horizontal_edges) == 1


def test_clockwise_reversal_preserves_minimum_geometry():
    ccw = [(0, 0), (5, 0), (5, 4), (0, 4)]
    cw = list(reversed(ccw))
    a, b = decompose_scanbeams([ccw]), decompose_scanbeams([cw])
    assert a.scanbeams == b.scanbeams
    assert len(a.minima) == len(b.minima) == 1
    assert {a.minima[0].left_bound.lower, a.minima[0].right_bound.lower} == {
        b.minima[0].left_bound.lower, b.minima[0].right_bound.lower}


def test_non_horizontal_minimum_has_two_bounds():
    ring = [(2, 0), (5, 3), (4, 6), (0, 5), (-1, 2)]
    result = decompose_scanbeams([ring])
    assert len(result.minima) == 1
    assert result.minima[0].y == 0
    assert result.minima[0].horizontal_edges == ()


def test_horizontal_bottom_plateau_forms_one_minimum():
    ring = [(0, 0), (2, 0), (4, 0), (5, 3), (0, 3)]
    result = decompose_scanbeams([ring])
    assert len(result.minima) == 1
    assert len(result.minima[0].horizontal_edges) == 2
    assert {result.minima[0].left_bound.lower, result.minima[0].right_bound.lower} == {
        (0.0, 0.0), (4.0, 0.0)}


def test_two_local_minima_are_reported():
    ring = [(0, 2), (2, 0), (4, 2), (6, 0), (8, 2), (8, 5), (0, 5)]
    result = decompose_scanbeams([ring])
    assert len(result.minima) == 2


def test_invalid_rings_and_coordinates_are_rejected():
    with pytest.raises(ValueError):
        decompose_scanbeams([[(0, 0), (1, 1)]])
    with pytest.raises(ValueError, match="finite"):
        decompose_scanbeams([[(0, 0), (1, 0), (0, float("nan"))]])
    with pytest.raises(ValueError, match="repeated"):
        decompose_scanbeams([[(0, 0), (2, 0), (2, 2), (0, 2), (2, 0)]])


def test_active_edge_list_is_ordered_at_band_midpoint():
    from vatti_scanbeam import active_edges_for_band
    ring = [(0, 0), (4, 0), (4, 3), (0, 3)]
    decomposition = decompose_scanbeams([ring])
    active = active_edges_for_band(decomposition, 0, 3)
    assert [edge.lower[0] for edge in active] == [0.0, 4.0]


def test_crossing_events_are_exact_and_y_ordered():
    from vatti_scanbeam import active_edges_for_band, crossings_in_band
    bow_tie = [(0, 0), (4, 4), (0, 4), (4, 0)]
    decomposition = decompose_scanbeams([bow_tie])
    active = active_edges_for_band(decomposition, 0, 4)
    events = crossings_in_band(active, 0, 4)
    assert len(events) == 1
    assert (events[0].x, events[0].y) == (2, 2)


def test_active_edge_band_must_use_consecutive_scanbeams():
    from vatti_scanbeam import active_edges_for_band
    ring = [(0, 0), (4, 0), (4, 3), (0, 3)]
    decomposition = decompose_scanbeams([ring])
    with pytest.raises(ValueError, match="consecutive"):
        active_edges_for_band(decomposition, 0, 2)


def test_crossing_scheduler_ignores_parallel_edges():
    from vatti_scanbeam import crossings_in_band, BoundEdge
    first = BoundEdge(0, 0, 0, (0, 0), (2, 4), 1)
    second = BoundEdge(1, 0, 1, (1, 0), (3, 4), 1)
    assert crossings_in_band([first, second], 0, 4) == ()


def test_active_edges_swap_order_across_crossing_event():
    from vatti_scanbeam import active_edges_for_band, sweep_active_edge_slices
    bow_tie = [(0, 0), (4, 4), (0, 4), (4, 0)]
    decomposition = decompose_scanbeams([bow_tie])
    active = active_edges_for_band(decomposition, 0, 4)
    slices = sweep_active_edge_slices(active, 0, 4)
    assert len(slices) == 2
    assert (slices[0].lower_y, slices[0].upper_y) == (0, 2)
    assert (slices[1].lower_y, slices[1].upper_y) == (2, 4)
    assert [e.edge_id for e in slices[0].edges] == [0, 2]
    assert [e.edge_id for e in slices[1].edges] == [2, 0]


def test_winding_states_are_cumulative_in_active_edge_order():
    from vatti_scanbeam import BoundEdge, winding_states
    edges = [
        BoundEdge(0, 0, 0, (0, 0), (1, 2), 1),
        BoundEdge(1, 1, 0, (2, 0), (3, 2), -1),
        BoundEdge(2, 2, 0, (4, 0), (5, 2), 1),
    ]
    assert winding_states(edges) == (1, 0, 1)


def test_horizontal_events_include_bound_endpoint_contacts():
    from vatti_scanbeam import horizontal_events_at
    result = decompose_scanbeams([[(0, 0), (4, 0), (4, 3), (0, 3)]])
    events = horizontal_events_at(result, 0)
    bound_events = [event for event in events if event.other_kind == "bound"]
    assert [(event.x_start, event.x_end) for event in bound_events] == [(0, 0), (4, 4)]
    assert all(event.kind == "point" for event in bound_events)


def test_horizontal_events_find_interior_crossings():
    from vatti_scanbeam import horizontal_events_at
    vertical_rect = [(0, 0), (4, 0), (4, 4), (0, 4)]
    horizontal_rect = [(-1, 2), (5, 2), (5, 3), (-1, 3)]
    result = decompose_scanbeams([vertical_rect, horizontal_rect])
    events = horizontal_events_at(result, 2)
    subject_bound_ids = {edge.edge_id for edge in result.bounds if edge.ring_id == 0}
    crossings = [event for event in events
                 if event.other_kind == "bound"
                 and event.other_edge_id in subject_bound_ids
                 and event.horizontal_edge_id in {
                     edge.edge_id for edge in result.horizontals
                     if edge.ring_id == 1 and edge.a[1] == 2
                 }]
    assert [(event.x_start, event.x_end) for event in crossings] == [(0, 0), (4, 4)]


def test_horizontal_horizontal_overlap_is_classified():
    from vatti_scanbeam import horizontal_events_at
    first = [(0, 0), (4, 0), (4, 2), (0, 2)]
    second = [(2, 0), (6, 0), (6, -2), (2, -2)]
    result = decompose_scanbeams([first, second])
    overlaps = [event for event in horizontal_events_at(result, 0)
                if event.other_kind == "horizontal"]
    assert len(overlaps) == 1
    assert (overlaps[0].x_start, overlaps[0].x_end) == (2, 4)
    assert overlaps[0].kind == "overlap"


def test_horizontal_horizontal_point_contact_is_not_overlap():
    from vatti_scanbeam import horizontal_events_at
    first = [(0, 0), (2, 0), (2, 2), (0, 2)]
    second = [(2, 0), (4, 0), (4, -2), (2, -2)]
    result = decompose_scanbeams([first, second])
    contacts = [event for event in horizontal_events_at(result, 0)
                if event.other_kind == "horizontal"]
    assert len(contacts) == 1
    assert (contacts[0].x_start, contacts[0].x_end) == (2, 2)
    assert contacts[0].kind == "point"


def test_horizontal_events_are_empty_off_their_scanbeam():
    from vatti_scanbeam import horizontal_events_at
    result = decompose_scanbeams([[(0, 0), (4, 0), (4, 3), (0, 3)]])
    assert horizontal_events_at(result, 1) == ()


@pytest.mark.parametrize("rule,values,expected", [
    ("even_odd", [-2, -1, 0, 1, 2], [False, True, False, True, False]),
    ("non_zero", [-2, -1, 0, 1, 2], [True, True, False, True, True]),
    ("positive", [-2, -1, 0, 1, 2], [False, False, False, True, True]),
    ("negative", [-2, -1, 0, 1, 2], [True, True, False, False, False]),
])
def test_fill_rule_winding_predicates(rule, values, expected):
    from vatti_scanbeam import is_filled
    assert [is_filled(value, rule) for value in values] == expected


@pytest.mark.parametrize("operation,expected", [
    ("intersection", True),
    ("union", True),
    ("difference", False),
    ("xor", False),
])
def test_boolean_truth_table_when_both_inputs_filled(operation, expected):
    from vatti_scanbeam import boolean_result
    assert boolean_result(1, 1, operation) is expected


@pytest.mark.parametrize("operation,expected", [
    ("intersection", False),
    ("union", True),
    ("difference", True),
    ("xor", True),
])
def test_boolean_truth_table_subject_only(operation, expected):
    from vatti_scanbeam import boolean_result
    assert boolean_result(1, 0, operation) is expected


def test_boolean_truth_table_clip_only():
    from vatti_scanbeam import boolean_result
    assert [boolean_result(0, 1, operation) for operation in
            ("intersection", "union", "difference", "xor")] == [
                False, True, False, True]


def test_fill_rule_and_boolean_operation_names_are_validated():
    from vatti_scanbeam import boolean_result, is_filled
    with pytest.raises(ValueError, match="fill rule"):
        is_filled(1, "mystery")
    with pytest.raises(ValueError, match="operation"):
        boolean_result(1, 1, "symmetric")


def test_subject_clip_fill_states_propagate_across_active_edge_order():
    from vatti_scanbeam import BoundEdge, fill_transitions
    edges = [
        BoundEdge(0, 10, 0, (0, 0), (0, 4), 1),
        BoundEdge(1, 20, 0, (1, 0), (1, 4), 1),
        BoundEdge(2, 10, 1, (3, 0), (3, 4), -1),
        BoundEdge(3, 20, 1, (4, 0), (4, 4), -1),
    ]
    states = fill_transitions(edges, {10}, {20}, "intersection")
    assert [(s.subject_after, s.clip_after) for s in states] == [
        (1, 0), (1, 1), (0, 1), (0, 0)]
    assert [s.result_after for s in states] == [False, True, False, False]
    assert [s.result_before for s in states] == [False, False, True, False]


def test_fill_transitions_support_all_boolean_operations():
    from vatti_scanbeam import BoundEdge, fill_transitions
    edges = [
        BoundEdge(0, 0, 0, (0, 0), (0, 1), 1),
        BoundEdge(1, 1, 0, (1, 0), (1, 1), 1),
    ]
    expected = {
        "intersection": [False, True],
        "union": [True, True],
        "difference": [True, False],
        "xor": [True, False],
    }
    for operation, values in expected.items():
        states = fill_transitions(edges, {0}, {1}, operation)
        assert [state.result_after for state in states] == values


def test_fill_transitions_reject_ambiguous_ring_ownership():
    from vatti_scanbeam import BoundEdge, fill_transitions
    edge = BoundEdge(0, 3, 0, (0, 0), (0, 1), 1)
    with pytest.raises(ValueError, match="disjoint"):
        fill_transitions([edge], {3}, {3})
    with pytest.raises(ValueError, match="every active edge"):
        fill_transitions([edge], {1}, {2})


def _cell_area(cell):
    vertices = cell.vertices
    return abs(sum(
        vertices[i][0] * vertices[(i + 1) % len(vertices)][1]
        - vertices[(i + 1) % len(vertices)][0] * vertices[i][1]
        for i in range(len(vertices))
    )) / 2


def _overlapping_rectangles():
    subject = [(0, 0), (4, 0), (4, 4), (0, 4)]
    clip = [(2, -1), (6, -1), (6, 3), (2, 3)]
    return decompose_scanbeams([subject, clip])


@pytest.mark.parametrize("operation,expected_area", [
    ("intersection", 6),
    ("union", 26),
    ("difference", 10),
    ("xor", 20),
])
def test_full_scanbeam_sweep_decomposes_boolean_areas(operation, expected_area):
    from vatti_scanbeam import sweep_boolean
    result = sweep_boolean(_overlapping_rectangles(), {0}, {1}, operation)
    assert sum(_cell_area(cell) for cell in result.cells) == expected_area
    assert result.band_slice_count >= 3
    assert len(result.levels) == 4


def test_full_scanbeam_sweep_carries_horizontal_events_and_local_minima():
    from vatti_scanbeam import sweep_boolean
    result = sweep_boolean(_overlapping_rectangles(), {0}, {1}, "intersection")
    bottom = result.levels[0]
    assert bottom.y == -1
    assert bottom.horizontal_edges
    assert bottom.local_minima
    assert bottom.horizontal_events


def test_full_scanbeam_sweep_splits_cells_at_edge_crossings():
    from vatti_scanbeam import sweep_boolean
    bow_tie = [(0, 0), (4, 4), (0, 4), (4, 0)]
    clip = [(-1, -1), (5, -1), (5, 5), (-1, 5)]
    result = sweep_boolean(decompose_scanbeams([bow_tie, clip]), {0}, {1},
                           "intersection")
    assert result.band_slice_count >= 3
    assert result.cells
    assert all(cell.lower_y < cell.upper_y for cell in result.cells)


def test_full_scanbeam_sweep_rejects_unassigned_rings_and_invalid_operands():
    from vatti_scanbeam import sweep_boolean
    with pytest.raises(ValueError, match="every bound edge"):
        sweep_boolean(_overlapping_rectangles(), {0}, {2})
    with pytest.raises(ValueError, match="non-empty"):
        sweep_boolean(_overlapping_rectangles(), {0}, set())


def _signed_ring_area(ring):
    core = ring[:-1]
    return sum(
        core[i][0] * core[(i+1) % len(core)][1]
        - core[(i+1) % len(core)][0] * core[i][1]
        for i in range(len(core))
    ) / 2


@pytest.mark.parametrize("operation,expected_area,expected_rings", [
    ("intersection", 6, 1),
    ("union", 26, 1),
    ("difference", 10, 1),
    ("xor", 20, 2),
])
def test_contour_clipper_stitches_all_boolean_operations(
    operation, expected_area, expected_rings
):
    from vatti_scanbeam import clip_rings
    result = clip_rings(_overlapping_rectangles(), {0}, {1}, operation)
    assert len(result.rings) == expected_rings
    assert result.boundary_edge_count > 0
    assert all(ring[0] == ring[-1] for ring in result.rings)
    assert sum(_signed_ring_area(ring) for ring in result.rings) == expected_area
    assert all(_signed_ring_area(ring) > 0 for ring in result.rings)


def test_contour_stitching_preserves_a_hole_and_a_disconnected_shell():
    from vatti_scanbeam import clip_rings
    outer = [(0, 0), (10, 0), (10, 10), (0, 10)]
    hole_cw = [(3, 3), (3, 7), (7, 7), (7, 3)]
    separate_clip = [(20, 20), (22, 20), (22, 22), (20, 22)]
    decomposition = decompose_scanbeams([outer, hole_cw, separate_clip])
    result = clip_rings(decomposition, {0, 1}, {2}, "union")
    signed_areas = sorted((_signed_ring_area(ring) for ring in result.rings))
    assert signed_areas == [-16, 4, 100]
    assert len(result.rings) == 3
    assert all(ring[0] == ring[-1] for ring in result.rings)


def test_stitch_filled_cells_returns_empty_for_no_filled_cells():
    from vatti_scanbeam import stitch_filled_cells
    assert stitch_filled_cells(()).rings == ()


def test_contour_stitching_nodes_unequal_shared_edge_subdivisions():
    from fractions import Fraction
    from vatti_scanbeam import FilledCell, stitch_filled_cells
    # Two adjacent CCW rectangles; the left cell's right edge is split at y=1.
    cells = (
        FilledCell(Fraction(0), Fraction(2), 0, 1, (
            (Fraction(0), Fraction(0)), (Fraction(1), Fraction(0)),
            (Fraction(1), Fraction(1)), (Fraction(1), Fraction(2)),
            (Fraction(0), Fraction(2)))),
        FilledCell(Fraction(0), Fraction(2), 1, 2, (
            (Fraction(1), Fraction(0)), (Fraction(2), Fraction(0)),
            (Fraction(2), Fraction(2)), (Fraction(1), Fraction(2)))),
    )
    result = stitch_filled_cells(cells)
    assert len(result.rings) == 1
    assert _signed_ring_area(result.rings[0]) == 4


def _rect(x0, y0, x1, y1, ccw=True):
    ring = [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
    return ring if ccw else list(reversed(ring))


@pytest.mark.parametrize("operation,expected_area,expected_rings", [
    ("intersection", 4, 1),
    ("union", 4, 1),
    ("difference", 0, 0),
    ("xor", 0, 0),
])
def test_coincident_identical_rings_are_bundled(operation, expected_area,
                                                 expected_rings):
    from vatti_scanbeam import clip_rings
    d = decompose_scanbeams([_rect(0, 0, 2, 2), _rect(0, 0, 2, 2)])
    result = clip_rings(d, {0}, {1}, operation)
    assert len(result.rings) == expected_rings
    assert sum(_signed_ring_area(r) for r in result.rings) == expected_area


@pytest.mark.parametrize("operation,expected_area,expected_rings", [
    ("union", 8, 1),
    ("intersection", 0, 0),
    ("difference", 4, 1),
    ("xor", 8, 1),
])
def test_shared_vertical_boundary_is_not_double_counted(operation, expected_area,
                                                          expected_rings):
    from vatti_scanbeam import clip_rings
    d = decompose_scanbeams([_rect(0, 0, 2, 2), _rect(2, 0, 4, 2)])
    result = clip_rings(d, {0}, {1}, operation)
    assert len(result.rings) == expected_rings
    assert sum(_signed_ring_area(r) for r in result.rings) == expected_area


def test_partial_collinear_shared_boundary_and_horizontal_events():
    from vatti_scanbeam import clip_rings, sweep_boolean
    d = decompose_scanbeams([_rect(0, 0, 2, 4), _rect(2, 1, 4, 3)])
    result = clip_rings(d, {0}, {1}, "union")
    assert len(result.rings) == 1
    assert sum(_signed_ring_area(r) for r in result.rings) == 12
    assert any(event.kind == "point" and event.other_kind == "bound"
               for level in sweep_boolean(d, {0}, {1}, "union").levels
               for event in level.horizontal_events)
    horizontal_shared = decompose_scanbeams([
        _rect(0, 0, 2, 2), _rect(0, 2, 2, 4)
    ])
    assert any(event.kind == "overlap" and event.other_kind == "horizontal"
               for level in sweep_boolean(
                   horizontal_shared, {0}, {1}, "union"
               ).levels for event in level.horizontal_events)


def test_vertex_touching_components_remain_separate_shells():
    from vatti_scanbeam import clip_rings
    d = decompose_scanbeams([_rect(0, 0, 2, 2), _rect(2, 2, 4, 4)])
    result = clip_rings(d, {0}, {1}, "union")
    assert len(result.rings) == 2
    assert sum(_signed_ring_area(r) for r in result.rings) == 8


def test_opposite_orientation_coincident_operand_rings_remain_filled():
    from vatti_scanbeam import clip_rings
    d = decompose_scanbeams([
        _rect(0, 0, 2, 2), _rect(0, 0, 2, 2, ccw=False)
    ])
    result = clip_rings(d, {0}, {1}, "union", fill_rule="non_zero")
    assert len(result.rings) == 1
    assert _signed_ring_area(result.rings[0]) == 4


def test_neighbour_event_sweep_orders_three_way_crossing_atomically():
    from vatti_scanbeam import (
        BoundEdge, bundle_active_edges, sweep_neighbour_ordered_bundles
    )
    edges = [
        BoundEdge(0, 0, 0, (0, 0), (4, 4), 1),
        BoundEdge(1, 0, 1, (2, 0), (2, 4), 1),
        BoundEdge(2, 1, 0, (4, 0), (0, 4), 1),
    ]
    bundles = bundle_active_edges(edges, {0}, {1})
    slices = sweep_neighbour_ordered_bundles(bundles, 0, 4)
    assert len(slices) >= 2
    assert slices[0].upper_y == 2
    assert [b.representative.edge_id for b in slices[0].bundles] == [0, 1, 2]
    assert [b.representative.edge_id for b in slices[1].bundles] == [2, 1, 0]


def test_shapely_differential_boolean_oracle():
    shapely = pytest.importorskip("shapely.geometry")
    from shapely.ops import unary_union
    from vatti_scanbeam import clip_rings
    fixtures = [
        (_rect(0, 0, 4, 4), _rect(2, -1, 6, 3)),
        (_rect(0, 0, 2, 2), _rect(2, 0, 4, 2)),
        (_rect(0, 0, 2, 4), _rect(2, 1, 4, 3)),
        (_rect(0, 0, 2, 2), _rect(2, 2, 4, 4)),
        (_rect(0, 0, 3, 3), _rect(1, 1, 4, 4)),
    ]
    # Seeded axis-aligned cases broaden the independent comparison without
    # making the regression suite dependent on nondeterministic randomness.
    import random
    rng = random.Random(20261116)
    for _ in range(24):
        x0, y0 = rng.randint(-8, 8), rng.randint(-8, 8)
        x1, y1 = x0 + rng.randint(1, 7), y0 + rng.randint(1, 7)
        u0, v0 = rng.randint(-8, 8), rng.randint(-8, 8)
        u1, v1 = u0 + rng.randint(1, 7), v0 + rng.randint(1, 7)
        fixtures.append((_rect(x0, y0, x1, y1), _rect(u0, v0, u1, v1)))
    operations = {
        "intersection": lambda a, b: a.intersection(b),
        "union": lambda a, b: a.union(b),
        "difference": lambda a, b: a.difference(b),
        "xor": lambda a, b: a.symmetric_difference(b),
    }
    for subject, clip in fixtures:
        d = decompose_scanbeams([subject, clip])
        a, b = shapely.Polygon(subject), shapely.Polygon(clip)
        for operation, oracle in operations.items():
            expected = oracle(a, b)
            actual = clip_rings(d, {0}, {1}, operation)
            actual_geom = unary_union([
                shapely.Polygon(ring[:-1]) for ring in actual.rings
            ]) if actual.rings else shapely.GeometryCollection()
            assert abs(sum(_signed_ring_area(r) for r in actual.rings)
                       - expected.area) < 1e-9
            assert actual_geom.symmetric_difference(expected).area < 1e-9
            if expected.geom_type == "Polygon":
                expected_components = 0 if expected.is_empty else 1
            elif expected.geom_type == "MultiPolygon":
                expected_components = len(expected.geoms)
            else:
                expected_components = 0
            assert len(actual.rings) == expected_components


def test_neighbour_scheduler_handles_distinct_crossings_at_same_y():
    from vatti_scanbeam import (
        BoundEdge, bundle_active_edges, sweep_neighbour_ordered_bundles
    )
    edges = [
        BoundEdge(0, 0, 0, (0, 0), (2, 4), 1),
        BoundEdge(1, 0, 1, (2, 0), (0, 4), 1),
        BoundEdge(2, 1, 0, (10, 0), (12, 4), 1),
        BoundEdge(3, 1, 1, (12, 0), (10, 4), 1),
    ]
    bundles = bundle_active_edges(edges, {0}, {1})
    slices = sweep_neighbour_ordered_bundles(bundles, 0, 4)
    assert len(slices) == 2
    assert slices[0].upper_y == 2
    assert [b.representative.edge_id for b in slices[0].bundles] == [0, 1, 2, 3]
    assert [b.representative.edge_id for b in slices[1].bundles] == [1, 0, 3, 2]

def test_horizontal_fill_transitions_compare_both_sides_of_scanbeam():
    from fractions import Fraction
    from vatti_scanbeam import sweep_boolean
    result = sweep_boolean(
        _overlapping_rectangles(), {0}, {1}, "intersection"
    )
    transitions = {level.y: level.fill_transitions for level in result.levels}
    assert [(item.x_start, item.x_end, item.below_filled, item.above_filled)
            for item in transitions[Fraction(0)]] == [
                (Fraction(2), Fraction(4), False, True)
            ]
    assert [(item.x_start, item.x_end, item.below_filled, item.above_filled)
            for item in transitions[Fraction(3)]] == [
                (Fraction(2), Fraction(4), True, False)
            ]


def test_shared_horizontal_edge_has_no_false_union_fill_transition():
    from vatti_scanbeam import sweep_boolean
    d = decompose_scanbeams([
        _rect(0, 0, 2, 2), _rect(0, 2, 2, 4)
    ])
    result = sweep_boolean(d, {0}, {1}, "union")
    shared_level = next(level for level in result.levels if level.y == 2)
    assert shared_level.horizontal_events
    assert shared_level.fill_transitions == ()
