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
