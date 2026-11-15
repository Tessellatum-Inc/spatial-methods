# Maximum flow and minimum cut

For a directed network with non-negative capacities, the maximum-flow problem seeks the greatest feasible source-to-sink flow subject to capacity constraints and flow conservation. The max-flow min-cut theorem states that this value equals the capacity of a minimum source-sink cut.

The included implementation uses Dinic's algorithm: BFS constructs a residual level graph and repeated DFS sends a blocking flow. Once the sink is unreachable in the residual network, residual reachability identifies a minimum cut. Parallel and antiparallel arcs are kept distinct.

See the [tested implementation](../../implementations/python/network-flow/README.md), [tests](../../implementations/python/network-flow/test_maximum_flow.py) and [verification record](../../catalog/verification/maximum-flow-min-cut.md).
