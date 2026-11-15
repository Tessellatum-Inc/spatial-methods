# Source verification — maximum flow and minimum cut

## Source identity
The compendium's network-analysis inventory explicitly includes maximum flow and minimum cut.

## Implemented
A dependency-free Edmonds–Karp implementation builds a residual network, finds shortest augmenting paths with BFS, and computes a maximum s-t flow. A companion routine extracts a minimum cut from residual reachability.

## Independent verification
The canonical six-node example returns flow and cut capacity 23. A seeded test suite checks 100 small directed graphs against exhaustive enumeration of all possible s-t cuts, independently of the augmenting-path implementation. Parallel and antiparallel arcs, disconnected sinks, zero capacities and invalid capacities are covered.

## Limitations
The implementation uses floating-point capacities. The public edge-flow result for antiparallel input pairs is aggregate net flow, not per-physical-arc decomposition. The exhaustive test oracle is restricted to small graphs. No claim is made for multicommodity or min-cost flow.
