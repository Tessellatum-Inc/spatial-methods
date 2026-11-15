# Maximum flow and minimum cut

For a directed network with non-negative capacities, the maximum-flow problem seeks the greatest feasible source-to-sink flow subject to capacity constraints and flow conservation. The max-flow min-cut theorem states that this value equals the capacity of a minimum source-sink cut.

The included implementation uses Dinic's algorithm: BFS constructs a residual level graph and repeated DFS sends a blocking flow. Once the sink is unreachable in the residual network, residual reachability identifies a minimum cut. Parallel and antiparallel arcs are kept distinct.

See the [tested implementation](../../implementations/python/network-flow/README.md), [tests](../../implementations/python/network-flow/test_maximum_flow.py) and [verification record](../../catalog/verification/maximum-flow-min-cut.md).


## Alternative implementation: Edmonds–Karp

The repository also contains a dependency-free Edmonds–Karp implementation. Unlike Dinic's blocking-flow phases, Edmonds–Karp uses BFS to find one shortest augmenting path per iteration, with O(VE²) worst-case complexity. Its implementation and tests are in [max-flow-min-cut](../../implementations/python/max-flow-min-cut/README.md). Seeded small directed graphs are checked against exhaustive enumeration of every s-t cut, providing an independent optimality oracle alongside the Dinic package's own tests.

The Edmonds–Karp package reports aggregate net flow per ordered vertex pair; the Dinic implementation remains the better choice when per-input-arc decomposition is required.
