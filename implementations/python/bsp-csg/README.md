# BSP tree constructive solid geometry

This module implements the classic binary-space-partition (BSP) approach to
boundary-representation CSG. It exposes union, intersection and difference
for closed solids supplied as polygon soups.

## Input contract and limitations

- Each input solid is a closed, consistently outward-wound boundary.
- Every face must be planar and convex. Concave faces must be triangulated or
  decomposed before use.
- The implementation uses floating-point coordinates and a caller-visible
  classification tolerance (default `1e-8`).
- It is a teaching baseline for polygon splitting and BSP clipping, not a
  robust production mesh Boolean kernel. Near-coplanar features, slivers,
  non-manifold input, self-intersections and tolerance-sensitive topology
  require stronger exact or adaptive predicates and mesh validation.
- Output is a polygon soup; it does not build a DCEL/half-edge mesh or repair
  non-manifold results.

## API

```python
from bsp_csg import box, union, intersection, difference

a = box((0, 0, 0), (2, 2, 2))
b = box((1, 1, 1), (3, 3, 3))
common = intersection(a, b)
combined = union(a, b)
remainder = difference(a, b)
```

## Verification

Tests measure signed boundary volume independently by triangulating each
output polygon as a fan. Overlapping, disjoint and nested axis-aligned boxes
exercise all three Boolean operations; invalid convexity and planarity are
also checked. These cases are useful regression tests but do not establish
robustness for arbitrary triangle meshes.
