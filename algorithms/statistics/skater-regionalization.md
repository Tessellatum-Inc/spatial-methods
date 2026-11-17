# SKATER spatial regionalization

SKATER (Spatial 'K'luster Analysis by Tree Edge Removal) constructs a
minimum spanning tree from a spatial adjacency graph, then prunes tree edges
to create connected regions. The tree ensures that every resulting region
remains connected in the supplied graph.

This reference implementation uses supplied non-negative edge costs to
construct a deterministic minimum spanning tree. It greedily removes the
remaining edge that maximizes the reduction in within-region sum of squares
over supplied feature vectors. The result is a connected k-partition.

## Scope

The implementation is a bounded greedy baseline for small connected graphs.
It does not implement automatic k selection, minimum region-size constraints,
alternative regional objectives, or the full range of SKATER software options.
Feature scaling is the caller's responsibility.

See the [Python package](../../implementations/python/skater/README.md)
and [tests](../../implementations/python/skater/test_skater.py).
