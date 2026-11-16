# BSP trees and constructive solid geometry

A binary space partition (BSP) recursively divides 3D space by polygon planes.
For CSG, polygons are classified as coplanar, in front of, behind, or spanning
a splitter plane. Spanning polygons are split at plane intersections. The
resulting front/back fragments are clipped through two BSP trees, and a
sequence of tree inversions and clips implements union, intersection and
difference.

## Operations

The implementation follows the classic polygon-BSP CSG construction:

- **Union:** retain exterior fragments from both boundaries and merge the
  clipped polygon sets.
- **Intersection:** invert and clip the two trees so only their common
  boundary fragments remain.
- **Difference:** invert the first tree, clip against the second, then restore
  the resulting boundary orientation.

The implementation is at
[implementations/python/bsp-csg](../../implementations/python/bsp-csg/README.md).

## Contract and limitations

Inputs are closed, consistently outward-wound polygon soups. Every face must
be convex and planar. Coordinates and plane classifications use floating
point with an explicit tolerance. The current implementation is a teaching
baseline, not a production robust Boolean kernel: it does not repair
self-intersections or non-manifold input, and near-coplanar/sliver cases can
be tolerance-sensitive. Output is not assembled into a DCEL or validated as
a watertight manifold.

The reference tests use independent signed-volume calculations on overlapping,
disjoint and nested boxes. Broader verification should add randomized convex
polyhedra, coplanar face/edge contacts, transformed solids, and manifold
edge-incidence checks.
