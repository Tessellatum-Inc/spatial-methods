# Shortest-path teaching implementation

Implements seven shortest-path methods for explicit weighted graphs: Dijkstra, A*, bidirectional Dijkstra and directed ALT landmark heuristics and Yen's k-shortest loopless paths for non-negative edge weights, Bellman–Ford for negative edges, and Floyd–Warshall for all-pairs shortest distances.

The companion `network_queries.py` adds:
- repeated-Dijkstra many-to-many shortest paths for selected source and target sets;
- cutoff-Dijkstra network isochrones with directed frontier arcs.

These are reference baselines. The many-to-many method repeats a single-source search for each source; it is not a shared-preprocessing production engine. The isochrone is a set of reachable graph nodes and frontier arcs, not a polygon.

## Run

~~~bash
python -m pip install -r requirements.txt
python -m pytest -q
~~~

## Example

~~~python
from shortest_paths import dijkstra, astar, bidirectional_dijkstra, ALTHeuristic

graph = {
    "A": [("B", 2), ("C", 1)],
    "B": [("D", 2)],
    "C": [("B", 0.5)],
    "D": [],
}
print(dijkstra(graph, "A", "D"))
print(astar(graph, "A", "D", lambda node, goal: 0))
print(bidirectional_dijkstra(graph, "A", "D"))
landmarks = ALTHeuristic(graph, landmarks=["A", "D"])
print(astar(graph, "A", "D", landmarks))
~~~

A* requires an admissible heuristic for optimality. A consistent heuristic is recommended. Dijkstra and A* require finite non-negative edge weights. Bellman–Ford and Floyd–Warshall accept finite negative edges but detect and reject negative cycles. The caller is responsible for representing one-way edges, access rules, turn restrictions and the chosen cost model.

Yen's algorithm returns up to k distinct loopless paths in non-decreasing cost order; this teaching graph model represents paths as node sequences and uses the minimum weight for parallel arcs. Bidirectional Dijkstra uses a reversed directed graph and a lower-bound stopping condition. ALT preprocesses distances from and to selected landmarks and applies directed triangle-inequality lower bounds. These are static-graph teaching baselines. This is not a production routing engine; it does not include contraction hierarchies, hub labels, customizable route planning, turn-expanded state, time-dependent costs or transit routing.

## Pareto multi-criteria paths

The companion `pareto_paths.py` module stores multiple labels per node. Each label contains an accumulated cost vector and a node path. Componentwise dominance removes labels that cannot be Pareto-optimal; equal cost vectors retain the first discovered path.

~~~python
from pareto_paths import pareto_shortest_paths

frontier = pareto_shortest_paths(
    graph, source, target, n_objectives=2,
    max_labels_per_node=10_000,
)
~~~

The optional per-node label cap raises an error instead of silently truncating the frontier. The number of nondominated labels can grow exponentially, so this exact output-sensitive method is intended for small and medium teaching graphs. Edge costs must be finite and nonnegative. It does not automatically model turn restrictions, time-dependent costs, multimodal transfers or stochastic route choice. See the [canonical lesson](../../../algorithms/networks/multi-criteria-shortest-paths.md), [Pareto walkthrough](implementation-walkthrough.md), [test suite](test_pareto_paths.py) and [interactive lab](../../../notebooks/pareto-multi-criteria-routing-lab.ipynb).
