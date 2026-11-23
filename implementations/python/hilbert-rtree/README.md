# Hilbert-packed R-tree

An immutable two-dimensional R-tree bulk-loaded by sorting rectangle centres along a discrete Hilbert space-filling curve. It provides closed-envelope intersection queries and returns original input indices.

## Run

    python -m pip install -r requirements.txt
    python -m pytest -q

## Method

1. Validate each finite axis-aligned rectangle.
2. Compute its centre and quantize the centre into a fixed-resolution integer grid over the dataset extent.
3. Compute the 2D Hilbert distance for each quantized centre.
4. Sort entries by Hilbert distance, with original index as a deterministic tie-break.
5. Pack consecutive entries into leaf nodes; recursively pack parent nodes until one root remains.
6. Query by pruning node MBRs that do not intersect the query rectangle.

The Hilbert key is a locality heuristic, not a guarantee that all nearby rectangles are adjacent in storage. The tree is static: updates require rebuilding. Query results are envelope candidates; apply exact geometry predicates to non-rectangular source geometries.

## Complexity and scope

Hilbert key computation is O(b) for b grid bits per item. Sorting dominates bulk loading at O(n log n); tree storage is O(n). Query performance depends on MBR overlap and can degrade to O(n) in the worst case. This implementation is a static Hilbert-ordered packed R-tree baseline, not the full dynamic Hilbert R-tree family.

The finite grid resolution can map distinct centres to the same key. Stable input-index tie-breaking preserves deterministic output. Coordinates are normalized using the dataset's centre extent, and degenerate extents are handled.

## Verification

Tests check the 2x2 Hilbert traversal order, boundary-touch semantics, empty and degenerate rectangles, invalid controls, and 750 seeded random rectangle queries against brute-force intersection for five node capacities.

## References

- Kamel, I. and Faloutsos, C. (1994). Hilbert R-tree: An improved R-tree using fractals. Proceedings of VLDB, 500–509.
- Moon, B., Jagadish, H. V., Faloutsos, C. and Saltz, J. H. (2001). Analysis of the clustering properties of the Hilbert space-filling curve. IEEE Transactions on Knowledge and Data Engineering, 13(1), 124–141.
