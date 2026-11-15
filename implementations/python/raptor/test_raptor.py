import pytest
from raptor import Route, Trip, raptor

def route(stops, times):
    return Route(tuple(stops), tuple(Trip(tuple(a), tuple(d)) for a, d in times))

def test_direct_trip_and_departure_constraint():
    r = route(("A", "B", "C"), [((0, 10, 20), (0, 10, 20)), ((30, 40, 50), (30, 40, 50))])
    result = raptor([r], {"A": 5}, max_transfers=0)
    assert result["rounds"][1]["B"] == 40
    assert result["rounds"][1]["C"] == 50

def test_cannot_board_trip_that_has_departed():
    r = route(("A", "B"), [((0, 10), (0, 10))])
    result = raptor([r], {"A": 1}, max_transfers=0)
    assert "B" not in result["rounds"][1]

def test_transfer_requires_an_extra_round():
    first = route(("A", "B"), [((0, 10), (0, 10))])
    second = route(("B", "C"), [((15, 25), (15, 25))])
    one = raptor([first, second], {"A": 0}, max_transfers=0)
    two = raptor([first, second], {"A": 0}, max_transfers=1)
    assert "C" not in one["rounds"][1]
    assert two["rounds"][2]["C"] == 25

def test_footpath_transfer_and_chain():
    r = route(("A", "C"), [((0, 20), (0, 20))])
    result = raptor([r], {"A": 0}, max_transfers=0,
                    footpaths={"C": [("D", 3)], "D": [("E", 2)]})
    assert result["rounds"][1]["E"] == 25

def test_route_choice_uses_earliest_arrival():
    r = route(("A", "B"), [((0, 20), (0, 20)), ((5, 12), (5, 12))])
    result = raptor([r], {"A": 0}, max_transfers=0)
    assert result["rounds"][1]["B"] == 12

def test_validation():
    with pytest.raises(ValueError):
        raptor([], {"A": 0}, max_transfers=-1)
    with pytest.raises(ValueError):
        raptor([route(("A", "B"), [((10, 5), (10, 5))])], {"A": 0})
    with pytest.raises(ValueError):
        raptor([], {})

def test_overtaking_trip_order_is_rejected():
    r = route(("A", "B"), [((0, 20), (0, 20)), ((5, 12), (5, 12))])
    with pytest.raises(ValueError, match="overtaking"):
        raptor([r], {"A": 0})
