import pytest
from csa import Connection, earliest_arrival

def test_basic_connection_chain():
    cs = [Connection("T1", "A", "B", 5, 10),
          Connection("T1", "B", "C", 10, 15)]
    result = earliest_arrival(cs, {"A": 0})
    assert result["arrival_times"]["C"] == 15

def test_transfer_and_minimum_change_time():
    cs = [Connection("T1", "A", "B", 5, 10),
          Connection("T2", "B", "C", 13, 20)]
    result = earliest_arrival(cs, {"A": 0}, minimum_transfer={"B": 3})
    assert result["arrival_times"]["C"] == 20

def test_transfer_too_short_is_rejected_but_same_trip_continues():
    cs = [Connection("T1", "A", "B", 5, 10),
          Connection("T2", "B", "C", 12, 20)]
    result = earliest_arrival(cs, {"A": 0}, minimum_transfer={"B": 3})
    assert "C" not in result["arrival_times"]
    same = [Connection("T1", "A", "B", 5, 10),
            Connection("T1", "B", "C", 10, 15)]
    assert earliest_arrival(same, {"A": 0}, minimum_transfer={"B": 3})["arrival_times"]["C"] == 15

def test_earliest_of_competing_trips():
    cs = [Connection("slow", "A", "B", 2, 20),
          Connection("fast", "A", "B", 5, 10)]
    assert earliest_arrival(cs, {"A": 0})["arrival_times"]["B"] == 10

def test_unreachable_and_access_label():
    result = earliest_arrival([Connection("T", "X", "Y", 1, 2)], {"A": 0})
    assert result["arrival_times"] == {"A": 0}

def test_validation():
    with pytest.raises(ValueError):
        earliest_arrival([], {})
    with pytest.raises(ValueError):
        earliest_arrival([Connection("T", "A", "B", 3, 2)], {"A": 0})
    with pytest.raises(ValueError):
        earliest_arrival([Connection("T", "A", "B", 2, 3),
                          Connection("U", "A", "B", 1, 2)], {"A": 0})
    with pytest.raises(ValueError):
        earliest_arrival([], {"A": 0}, minimum_transfer={"A": -1})


def test_minimum_transfer_does_not_delay_initial_access_boarding():
    cs = [Connection("T1", "A", "B", 5, 10)]
    result = earliest_arrival(cs, {"A": 0}, minimum_transfer={"A": 30})
    assert result["arrival_times"]["B"] == 10


def test_transfer_minimum_applies_after_a_ride():
    cs = [Connection("T1", "A", "B", 5, 10),
          Connection("T2", "B", "C", 12, 20)]
    blocked = earliest_arrival(cs, {"A": 0}, minimum_transfer={"B": 3})
    assert "C" not in blocked["arrival_times"]
    allowed = earliest_arrival(
        [cs[0], Connection("T2", "B", "C", 13, 20)],
        {"A": 0}, minimum_transfer={"B": 3}
    )
    assert allowed["arrival_times"]["C"] == 20


def test_access_label_remains_boardable_after_earlier_transit_arrival():
    connections = [
        Connection("T1", "A", "B", 1, 2),
        Connection("T2", "B", "C", 6, 7),
    ]
    result = earliest_arrival(
        connections, {"A": 0, "B": 5}, minimum_transfer={"B": 5}
    )
    # Access at B is ready at 5; the later transfer penalty must not apply.
    assert result["arrival_times"]["C"] == 7


def test_transit_transfer_penalty_still_applies_without_access_path():
    connections = [
        Connection("T1", "A", "B", 1, 2),
        Connection("T2", "B", "C", 6, 7),
    ]
    result = earliest_arrival(
        connections, {"A": 0}, minimum_transfer={"B": 5}
    )
    assert "C" not in result["arrival_times"]
