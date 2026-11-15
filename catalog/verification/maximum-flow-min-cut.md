# Verification record: maximum flow and minimum cut

## Source identity
- Compendium: *Spatial Analysis Algorithms: Complete Compendium*
- Original location: Section 1, page 2
- Source entry: flows and trees — max flow and min cut

## Implemented scope
- Dinic level-graph and blocking-flow algorithm for directed finite non-negative capacities.
- Independent residual arcs for parallel and antiparallel edges.
- Per-input-arc flows, residual source/sink partition and minimum cut edges/capacity.

## Tests
- Classic six-node network with known maximum flow 23 and matching cut.
- Parallel and antiparallel arcs.
- Zero-capacity and disconnected sink.
- Flow conservation and capacity feasibility.
- Invalid capacities, self-loops and identical terminals.

## Limits
This is a teaching baseline. It does not implement min-cost flow, multi-commodity flow, lower bounds, capacity scaling, push-relabel or dynamic network updates. Minimum spanning tree, Steiner tree and k-core remain separate algorithms in the grouped source entry.


## Second independent implementation and oracle

A separate Edmonds–Karp package is available at `implementations/python/max-flow-min-cut/`. Its seeded small-graph tests compare the returned value and cut capacity with exhaustive cut enumeration. This provides an independent algorithmic implementation and a separate optimality oracle; it does not replace the Dinic per-input-arc flow verification.
