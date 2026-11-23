# Implementation verification — Hilbert-packed R-tree

## Implemented scope
- Discrete 2D Hilbert distance mapping with configurable 1–31 bit grid.
- Centre quantization over the indexed dataset extent.
- Static Hilbert-order bulk loading into bounded-capacity leaf and internal nodes.
- Closed rectangle-intersection queries with original input-index results.

## Independent checks
- The 2x2 grid follows the standard Hilbert traversal sequence with distances 0, 1, 2, 3.
- Seeded random query results are compared with brute-force rectangle intersection for 350 boxes, 150 queries and five node capacities.
- Empty trees, duplicate centres, zero-area boxes, boundary touches and invalid inputs are tested.

## Limitations
Static bulk-loaded teaching implementation only. It does not implement dynamic insert/delete, disk pages, concurrency, exact predicates for arbitrary geometries or the complete family of dynamic Hilbert R-trees. Quantization can create key ties; input index provides deterministic tie-breaking.

## Reproduction
From implementations/python/hilbert-rtree:

    python -m pip install -r requirements.txt
    python -m pytest -q
