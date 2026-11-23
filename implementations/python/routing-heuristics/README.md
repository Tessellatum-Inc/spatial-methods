# Euclidean TSP and CVRP heuristics

Dependency-free reference implementations for two classical routing heuristics.

## Install and test

```bash
python -m pip install -r requirements.txt
python -m pytest -q
```

## Algorithms

- `two_opt(points, route=None, max_passes=100)`: deterministic closed-tour 2-opt local search. It fixes point 0 to remove rotational symmetry and accepts strictly improving edge exchanges. Complexity is O(passes × n²) distance comparisons; it is a heuristic and has no optimality guarantee.
- `clarke_wright_cvrp(points, demands, capacity, depot=0)`: parallel Clarke–Wright savings construction for symmetric Euclidean CVRP with indivisible nonnegative demands, a single depot and homogeneous vehicle capacity. Returns depot-closed routes. Savings ties are deterministic.
- `validate_cvrp_routes(...)`: checks exact customer coverage and vehicle capacities.

Coordinates are planar Cartesian coordinates in a consistent linear unit. Do not pass longitude/latitude directly for large regions; project appropriately or replace the distance model. These are teaching baselines, not dispatch-ready optimizers. They omit time windows, fleet limits, heterogeneous vehicles, road-network travel costs, split deliveries, stochastic demand and pickup/delivery precedence.

## Worked example

```python
from routing_heuristics import two_opt, route_length, clarke_wright_cvrp

points = [(0, 0), (2, 0), (2, 2), (0, 2), (1, 1)]
tour = two_opt(points)
print(tour, route_length(tour, points))

demands = [0, 2, 2, 1, 1]
routes = clarke_wright_cvrp(points, demands, capacity=3, depot=0)
print(routes)
```

The first result is a locally improved closed TSP tour. The second is a
capacity-feasible set of depot-closed delivery routes; neither is guaranteed
to be globally optimal.


## Vehicle routing with time windows

\`greedy_vrptw\` builds depot-closed routes while respecting one vehicle capacity, customer service-start windows, service durations and a depot return deadline:

\`\`\`python
from routing_heuristics import greedy_vrptw

result = greedy_vrptw(
    points=[(0, 0), (1, 0), (2, 0)],
    demands=[0, 1, 1],
    time_windows=[(0, 20), (5, 8), (0, 20)],
    capacity=2,
    service_times=[0, 2, 0],
)
for route in result.routes:
    print(route.nodes, route.load, route.distance)
    print([(stop.arrival, stop.service_start, stop.departure) for stop in route.stops])
print("unserved:", result.unserved)
\`\`\`

This deterministic nearest-detour construction allows waiting and checks whether each tentative customer can still return to the depot before closing. Each route exposes stop schedules; customers that cannot be inserted are returned in \`result.unserved\`. It is a small-instance heuristic, not an exact VRPTW solver or a road-network dispatch engine. See the [VRPTW method note](../../../algorithms/optimization/vrptw-greedy-insertion.md) for its contract and limitations.
