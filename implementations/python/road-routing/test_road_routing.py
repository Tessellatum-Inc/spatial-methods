import math
import pytest

from road_routing import earliest_arrival, turn_aware_shortest_path


def test_turn_restriction_forces_alternative_route():
    edges = [
        ("ab", "A", "B", 1),
        ("bd", "B", "D", 1),
        ("bc", "B", "C", 2),
        ("cd", "C", "D", 1),
    ]
    path, cost = turn_aware_shortest_path(
        edges, "A", "D", prohibited_turns={("ab", "bd")}
    )
    assert path == ["ab", "bc", "cd"]
    assert cost == pytest.approx(4)


def test_turn_penalty_changes_best_route():
    edges = [
        ("ab", "A", "B", 1),
        ("bd", "B", "D", 1),
        ("bc", "B", "C", 1.5),
        ("cd", "C", "D", 1),
    ]
    path, cost = turn_aware_shortest_path(
        edges, "A", "D", turn_penalties={("ab", "bd"): 2}
    )
    assert path == ["ab", "bc", "cd"]
    assert cost == pytest.approx(3.5)


def test_no_turn_rules_matches_node_graph_shortest_path_cost():
    edges = [("ab", "A", "B", 2), ("bc", "B", "C", 3)]
    assert turn_aware_shortest_path(edges, "A", "C") == (["ab", "bc"], 5)


def test_unreachable_and_start_equals_goal():
    assert turn_aware_shortest_path([], "A", "B") == (None, math.inf)
    assert turn_aware_shortest_path([], "A", "A") == ([], 0.0)


def test_duplicate_edge_ids_rejected():
    with pytest.raises(ValueError, match="unique"):
        turn_aware_shortest_path([("e", "A", "B", 1), ("e", "B", "C", 1)], "A", "C")


def test_invalid_turn_penalty_rejected():
    with pytest.raises(ValueError, match="turn penalties"):
        turn_aware_shortest_path(
            [("ab", "A", "B", 1), ("bc", "B", "C", 1)],
            "A", "C", turn_penalties={("ab", "bc"): -1}
        )


def test_fifo_earliest_arrival_uses_departure_time_at_each_edge():
    graph = {"A": [("B", "ab")], "B": [("C", "bc")], "C": []}
    durations = {"ab": lambda t: 5.0, "bc": lambda t: 2.0 + 0.1 * t}
    path, arrival = earliest_arrival(
        graph, "A", "C", 0.0, lambda edge, t: durations[edge](t)
    )
    assert path == ["A", "B", "C"]
    assert arrival == pytest.approx(7.5)


def test_earliest_arrival_returns_absolute_time_not_elapsed_duration():
    graph = {"A": [("B", "ab")], "B": []}
    path, arrival = earliest_arrival(graph, "A", "B", 10.0, lambda _edge, _t: 3.0)
    assert path == ["A", "B"]
    assert arrival == pytest.approx(13.0)


def test_time_dependent_unreachable_goal():
    assert earliest_arrival({}, "A", "B", 0, lambda _edge, _t: 1) == (None, math.inf)


def test_invalid_time_or_travel_time_rejected():
    graph = {"A": [("B", "ab")], "B": []}
    with pytest.raises(ValueError, match="departure_time"):
        earliest_arrival(graph, "A", "B", math.inf, lambda _edge, _t: 1)
    with pytest.raises(ValueError, match="travel times"):
        earliest_arrival(graph, "A", "B", 0, lambda _edge, _t: -1)



def test_non_fifo_search_waits_for_a_later_faster_departure():
    from road_routing import non_fifo_earliest_arrival
    graph={"S":[("T","st")],"T":[]}
    result=non_fifo_earliest_arrival(graph,{"st":{0:10,1:1}},"S","T",0,10)
    assert result["path"] == ["S","T"]
    assert result["arrival_time"] == 2
    assert result["legs"] == [{"edge_id":"st","from":"S","to":"T",
                               "departure_time":1,"arrival_time":2}]
    assert result["waits"] == [{"node":"S","start":0,"end":1}]


def test_non_fifo_search_can_wait_at_an_intermediate_node():
    from road_routing import non_fifo_earliest_arrival
    graph={"S":[("A","sa")],"A":[("T","at")],"T":[]}
    profiles={"sa":{0:1},"at":{1:8,2:1}}
    result=non_fifo_earliest_arrival(graph,profiles,"S","T",0,10)
    assert result["arrival_time"] == 3
    assert result["path"] == ["S","A","T"]
    assert result["waits"] == [{"node":"A","start":1,"end":2}]


def test_non_fifo_search_matches_exhaustive_time_expanded_oracle():
    from road_routing import non_fifo_earliest_arrival
    graph={"S":[("A","sa"),("B","sb")],"A":[("T","at")],
           "B":[("T","bt")],"T":[]}
    profiles={"sa":{0:1,1:4,2:1,3:2},
              "sb":{0:3,1:1,2:3,3:1},
              "at":{1:5,2:1,3:4,4:1,5:1},
              "bt":{1:1,2:4,3:1,4:2,5:1}}
    start, horizon = 0, 8
    reachable={("S",start)}
    for tick in range(start,horizon+1):
        for node in ("S","A","B","T"):
            if (node,tick) not in reachable:
                continue
            if tick<horizon:
                reachable.add((node,tick+1))
            for neighbour,edge in graph.get(node,()):
                duration=profiles.get(edge,{}).get(tick)
                if duration is not None and tick+duration<=horizon:
                    reachable.add((neighbour,tick+duration))
    expected=min((tick for node,tick in reachable if node=="T"),default=None)
    actual=non_fifo_earliest_arrival(graph,profiles,"S","T",start,horizon)
    assert actual["arrival_time"] == expected


def test_non_fifo_search_handles_unreachable_and_same_node():
    from road_routing import non_fifo_earliest_arrival
    assert non_fifo_earliest_arrival({"S":[("T","st")]} ,{},"S","T",0,3)["path"] is None
    same=non_fifo_earliest_arrival({},{},"S","S",2,3)
    assert same["path"] == ["S"] and same["arrival_time"] == 2


def test_non_fifo_search_rejects_invalid_profiles_and_horizon():
    from road_routing import non_fifo_earliest_arrival
    graph={"S":[("T","st")]}
    with pytest.raises(ValueError,match="horizon"):
        non_fifo_earliest_arrival(graph,{},"S","T",3,2)
    with pytest.raises(ValueError,match="integer"):
        non_fifo_earliest_arrival(graph,{"st":{0.5:1}},"S","T",0,3)
    with pytest.raises(ValueError,match="integer"):
        non_fifo_earliest_arrival(graph,{"st":{0:-1}},"S","T",0,3)
    with pytest.raises(ValueError,match="unknown edge"):
        non_fifo_earliest_arrival(graph,{"other":{0:1}},"S","T",0,3)


def test_non_fifo_restricted_waiting_caps_consecutive_wait_at_each_visit():
    from road_routing import non_fifo_earliest_arrival
    graph={"S":[("T","st")],"T":[]}
    profile={"st":{0:10,1:8,2:1}}
    unrestricted=non_fifo_earliest_arrival(graph,profile,"S","T",0,10)
    no_wait=non_fifo_earliest_arrival(graph,profile,"S","T",0,10,max_wait=0)
    one_tick=non_fifo_earliest_arrival(graph,profile,"S","T",0,10,max_wait=1)
    assert unrestricted["arrival_time"]==3
    assert no_wait["arrival_time"]==10 and no_wait["waits"]==[]
    assert one_tick["arrival_time"]==9
    assert one_tick["waits"]==[{"node":"S","start":0,"end":1}]


def test_non_fifo_wait_limit_resets_after_traversing_an_edge():
    from road_routing import non_fifo_earliest_arrival
    graph={"S":[("A","sa")],"A":[("T","at")],"T":[]}
    profiles={"sa":{0:1},"at":{1:9,2:1}}
    result=non_fifo_earliest_arrival(graph,profiles,"S","T",0,10,max_wait=1)
    assert result["arrival_time"]==3
    assert result["waits"]==[{"node":"A","start":1,"end":2}]


@pytest.mark.parametrize("max_wait",[-1,1.5,True])
def test_non_fifo_rejects_invalid_wait_limit(max_wait):
    from road_routing import non_fifo_earliest_arrival
    with pytest.raises(ValueError,match="max_wait"):
        non_fifo_earliest_arrival({"S":[("T","st")]},{"st":{0:1}},
                                  "S","T",0,3,max_wait=max_wait)
