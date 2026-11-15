# Mutable R*-style tree

Dependency-free incremental 2D bounding-box index. It uses overlap-enlargement subtree selection, R*-style split-axis selection by summed margins, then minimum-overlap/minimum-area distribution selection. Record IDs are stable; duplicate and zero-area boxes are retained; queries use closed-envelope intersection.

**Scope:** this is not a complete Beckmann et al. R*-tree. Forced reinsertion, deletion/condensation, bulk loading, kNN, disk pages, persistence and robust exact arithmetic are omitted. For non-rectangular geometries, refine envelope candidates with exact predicates. Use suitable planar coordinates.

Run tests with `pytest -q`.
