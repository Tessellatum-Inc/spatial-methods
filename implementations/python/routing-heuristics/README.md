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
