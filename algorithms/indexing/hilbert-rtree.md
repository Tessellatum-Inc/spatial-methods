# Hilbert-packed R-tree

A Hilbert-packed R-tree is a static spatial index that orders entries by the Hilbert distance of their bounding-box centres before grouping them into tree nodes. The Hilbert curve maps a two-dimensional grid to a one-dimensional order while tending to keep nearby grid cells close in that order.

## Hilbert ordering

For each rectangle, calculate its centre. Normalize the centre coordinates over the indexed dataset extent and quantize them to an integer grid. The discrete Hilbert mapping converts the grid coordinate (x,y) to an integer distance. Entries are sorted by that distance, with original input index as a stable tie-break.

This implementation uses a configurable 1–31 bit grid per axis. Quantization can map distinct centres to the same cell; deterministic tie-breaking preserves reproducibility.

## Bulk loading

1. Compute Hilbert keys for all entry centres.
2. Sort entries by key and original index.
3. Group consecutive entries into leaf nodes up to the node capacity.
4. Compute each node's minimum bounding rectangle.
5. Sort and group nodes at each successive level until one root remains.

The result is a balanced, immutable hierarchy. A range query prunes any node whose MBR does not intersect the query rectangle, then checks leaf entries and returns original input indices.

## Complexity and limitations

Hilbert key computation is O(b) for b grid bits per entry. Sorting dominates bulk loading at O(n log n); storage is O(n). Query cost depends on bounding-box overlap and can degrade to O(n) in the worst case.

The package is a static Hilbert-ordered packed R-tree baseline. It does not implement dynamic insertion/deletion, disk pages, persistence, concurrency or exact predicates for arbitrary geometries. Rebuild the tree when the indexed collection changes. Use an exact geometry predicate to refine envelope candidates.

## Verification

Tests check the standard 2x2 Hilbert traversal, empty and singleton trees, closed-boundary touching, duplicate centres, degenerate rectangles, invalid controls, and seeded brute-force differential queries over 350 rectangles and 150 query windows at five node capacities.

## Implementation

See the [Python implementation and tests](../../implementations/python/hilbert-rtree/README.md).

## References

- Kamel, I. and Faloutsos, C. (1994). Hilbert R-tree: An improved R-tree using fractals. Proceedings of VLDB, 500–509.
- Moon, B., Jagadish, H. V., Faloutsos, C. and Saltz, J. H. (2001). Analysis of the clustering properties of the Hilbert space-filling curve. IEEE Transactions on Knowledge and Data Engineering, 13(1), 124–141.
