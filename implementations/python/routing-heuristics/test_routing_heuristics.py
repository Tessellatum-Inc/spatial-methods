import math
import random
import pytest
from routing_heuristics import two_opt, route_length, clarke_wright_cvrp, validate_cvrp_routes


def test_two_opt_improves_crossing_tour_and_preserves_cycle():
    pts=[(0,0),(1,1),(0,1),(1,0),(2,0)]
    start=[0,1,2,3,4]
    got=two_opt(pts,start)
    assert got[0]==0 and sorted(got)==list(range(len(pts)))
    assert route_length(got,pts)<=route_length(start,pts)


def test_two_opt_seeded_random_never_worsens():
    rng=random.Random(31)
    for n in range(4,30):
        pts=[(rng.random()*100,rng.random()*100) for _ in range(n)]
        initial=list(range(n))
        assert route_length(two_opt(pts,initial),pts)<=route_length(initial,pts)+1e-9


def test_two_opt_validation_and_small_cases():
    assert two_opt([(0,0),(1,0),(0,1)])==[0,1,2]
    with pytest.raises(ValueError): two_opt([(0,0),(1,0)], [0,0])
    with pytest.raises(ValueError): two_opt([(0,0)], max_passes=0)
    with pytest.raises(ValueError): two_opt([(math.nan,0)])


def test_clarke_wright_capacity_and_coverage():
    pts=[(0,0),(1,0),(2,0),(0,2),(2,2)]
    demands=[0,2,2,2,2]
    routes=clarke_wright_cvrp(pts,demands,4)
    assert validate_cvrp_routes(routes,demands,4)
    assert sorted(i for r in routes for i in r[1:-1])==[1,2,3,4]


def test_clarke_wright_custom_depot_and_determinism():
    pts=[(9,9),(0,0),(1,0),(0,1)]
    demands=[0,1,1,1]
    a=clarke_wright_cvrp(pts,demands,2,depot=0)
    assert a==clarke_wright_cvrp(pts,demands,2,depot=0)
    assert validate_cvrp_routes(a,demands,2,depot=0)


@pytest.mark.parametrize("demands,capacity", [([0,3],2),([0,-1],2),([1,1],2)])
def test_cvrp_invalid_inputs(demands,capacity):
    with pytest.raises(ValueError): clarke_wright_cvrp([(0,0),(1,0)],demands,capacity)


from routing_heuristics import greedy_vrptw


def test_greedy_vrptw_respects_capacity_windows_and_returns():
    points = [(0, 0), (1, 0), (2, 0), (0, 2)]
    result = greedy_vrptw(
        points,
        [0, 1, 1, 1],
        [(0, 10), (0, 3), (0, 10), (0, 2.5)],
        capacity=2,
    )
    assert result.unserved == ()
    assert [route.nodes for route in result.routes] == [(0, 1, 2, 0), (0, 3, 0)]
    for route in result.routes:
        assert route.load <= 2
        assert route.stops[0].node == route.stops[-1].node == 0
        assert route.stops[-1].arrival <= 10


def test_greedy_vrptw_waits_and_accounts_for_service_time():
    result = greedy_vrptw(
        [(0, 0), (1, 0)],
        [0, 1],
        [(0, 20), (5, 6)],
        capacity=1,
        service_times=[0, 2],
    )
    route = result.routes[0]
    assert route.stops[1].arrival == pytest.approx(1)
    assert route.stops[1].service_start == pytest.approx(5)
    assert route.stops[1].departure == pytest.approx(7)
    assert route.stops[-1].arrival == pytest.approx(8)


def test_greedy_vrptw_reports_unserviceable_customers_and_vehicle_limit():
    result = greedy_vrptw(
        [(0, 0), (1, 0), (2, 0), (3, 0)],
        [0, 1, 1, 1],
        [(0, 20), (0, 20), (0, 20), (0, 20)],
        capacity=1,
        vehicle_limit=2,
    )
    assert len(result.routes) == 2
    assert result.unserved == (3,)


def test_greedy_vrptw_reports_window_infeasibility():
    result = greedy_vrptw(
        [(0, 0), (1, 0)],
        [0, 1],
        [(0, 20), (0, 0.5)],
        capacity=1,
    )
    assert result.routes == ()
    assert result.unserved == (1,)


@pytest.mark.parametrize(
    "kwargs",
    [
        {"capacity": 0},
        {"capacity": 1, "time_windows": [(0, 1)]},
        {"capacity": 1, "vehicle_limit": 0},
        {"capacity": 1, "start_time": float("nan")},
    ],
)
def test_greedy_vrptw_rejects_invalid_controls(kwargs):
    base = {
        "points": [(0, 0), (1, 0)],
        "demands": [0, 1],
        "time_windows": [(0, 10), (0, 10)],
        "capacity": 1,
    }
    base.update(kwargs)
    with pytest.raises(ValueError):
        greedy_vrptw(**base)


def test_greedy_vrptw_rejects_invalid_demands_windows_and_service():
    with pytest.raises(ValueError):
        greedy_vrptw([(0, 0), (1, 0)], [1, 1], [(0, 10), (0, 10)], 2)
    with pytest.raises(ValueError):
        greedy_vrptw([(0, 0), (1, 0)], [0, 1], [(0, 10), (2, 1)], 1)
    with pytest.raises(ValueError):
        greedy_vrptw([(0, 0), (1, 0)], [0, 1], [(0, 10), (0, 10)], 1, [0, -1])
