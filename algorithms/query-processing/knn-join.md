# Point k-nearest-neighbour join

A kNN join relates each point in a left relation to its (k) nearest points
in a right relation. Unlike an all-pairs distance join, it returns a bounded
number of right-side matches per left-side record.

## Indexed plan

1. Build a static 2D k-d tree over the right relation once.
2. For each left point, issue an exact k-nearest query.
3. Emit the original left and right record IDs and squared Euclidean distance.

The reference implementation uses the existing repository k-d tree, so its
deterministic tie rule (right-side input index) is preserved. If (n) is the
right relation size and (m) the left relation size, the index is built once;
query cost is data-dependent and can be linear in the worst case. The current
implementation handles planar points only, not geometry-to-geometry joins,
spherical distance, temporal constraints or mutual kNN joins.
