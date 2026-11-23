# Verification record: minimum spanning tree

## Source identity
- Compendium: *Spatial Analysis Algorithms: Complete Compendium*
- Original location: Section 1, page 2
- Source entry: flows and trees — minimum spanning tree

## Implemented scope
- Kruskal's edge-sorting algorithm with disjoint-set union.
- Minimum spanning forest for disconnected graphs.
- Parallel edges, finite negative weights, ignored self-loops and deterministic equal-weight ties.

## Tests
- Known four-node MST and total weight.
- Disconnected forest and component count.
- Negative/parallel/self-loop edge handling.
- Deterministic ties and empty/singleton graphs.
- Invalid endpoints, edge shape, weights and duplicate node identifiers.

## Limits
This is an undirected graph baseline. It does not implement Euclidean MST, Steiner trees, directed arborescences or dynamic graph updates. The grouped source row remains partial because Steiner tree and k-core decomposition are not included.
