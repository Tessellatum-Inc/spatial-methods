# Maximum flow and minimum cut: Edmonds–Karp

Dependency-free implementation of the Edmonds–Karp augmenting-path algorithm for directed capacitated networks.

## Run

```bash
python -m pip install -r requirements.txt
python -m pytest -q
```

## API

```python
from max_flow import edmonds_karp, minimum_cut

edges = [("s", "a", 3), ("s", "b", 2),
         ("a", "b", 1), ("a", "t", 2), ("b", "t", 3)]
value, edge_flows = edmonds_karp(edges, "s", "t")
cut_capacity, source_side, sink_side = minimum_cut(edges, "s", "t")
```

Capacities must be finite, non-negative numbers. Parallel directed edges are combined. Self-loops are rejected. The returned edge-flow map reports aggregate net flow for each ordered pair; where both directions exist, this is a signed net value rather than a decomposition into separate physical parallel arcs.

## Algorithm

Each iteration runs breadth-first search over positive residual-capacity arcs to find a shortest augmenting path (fewest edges). It augments by the path bottleneck, updates forward and reverse residual capacities, and repeats until no augmenting path remains. With integral capacities, the algorithm terminates with an integral maximum flow. Its standard worst-case complexity is O(V E²).

The minimum-cut routine identifies vertices reachable from the source in the final residual network. The cut capacity is the sum of original capacities crossing from the reachable side to its complement. By max-flow/min-cut duality, this equals the maximum-flow value.

## GIS relevance

Maximum flow/minimum cut supports capacity-constrained transport assignment, evacuation bottlenecks, network vulnerability, water and utility distribution, and graph partitioning. A road network needs a defensible capacity model: edge capacities are not automatically travel times or observed flows. Directed arcs are important for one-way streets and asymmetric infrastructure.

## Verification

The tests include the canonical six-node network (maximum flow 23), parallel and antiparallel arcs, zero-flow/disconnected cases, invalid capacities, and 100 seeded small directed graphs. For each random graph, the computed flow is compared with an independent exhaustive enumeration of every s-t cut. This brute-force oracle is deliberately limited to small graphs.

## Limitations

This implementation is for teaching and small/medium graphs, not production-scale routing. It uses floating-point capacities and a small residual tolerance in cut reachability; for exact integer guarantees, an integer-capacity specialization is preferable. It does not model lower bounds, node capacities, multicommodity flow, or min-cost flow.

## References

- Edmonds, J. and Karp, R. M. (1972). Theoretical improvements in algorithmic efficiency for network flow problems. *Journal of the ACM*, 19(2), 248–264.
- Ford, L. R. and Fulkerson, D. R. (1956). Maximal flow through a network. *Canadian Journal of Mathematics*, 8, 399–404.
