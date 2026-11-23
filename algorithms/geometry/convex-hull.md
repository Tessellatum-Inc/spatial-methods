# Convex hulls: find the outside boundary of a point set

A convex hull is the smallest convex set containing a finite point set. Imagine stretching a tight rubber band around nails on a board: the contact points form the hull, while interior points do not affect its boundary.

## Geometric definition

A set is convex when the segment joining any two of its points lies entirely inside it. For a finite planar set P,

$$
\operatorname{CH}(P)=\bigcap\{C\mid P\subseteq C,\ C\text{ is convex}\}.
$$

For non-degenerate inputs, the boundary is a convex polygon. Empty, singleton, two-point and collinear inputs produce the corresponding lower-dimensional result.

## Orientation predicate

For points O, A and B, the signed cross product is

$$
\operatorname{cross}(O,A,B)=(A_x-O_x)(B_y-O_y)-(A_y-O_y)(B_x-O_x).
$$

Positive means counter-clockwise, negative clockwise, and zero collinear. All implementations here use this predicate and ordinary floating-point arithmetic; they are not exact-predicate geometry kernels.

## Three algorithms

### Graham scan

Choose the lowest-then-leftmost point as pivot, sort the other points by polar angle, and scan them with a stack. Pop while the most recent turn is clockwise or collinear. Each point is pushed once and popped at most once after sorting, so the total time is O(n log n).

### Jarvis march (gift wrapping)

Start at the leftmost point and repeatedly select the point that makes the most counter-clockwise wrap, resolving collinear candidates by choosing the farthest. It visits only hull vertices but scans all input points at each step: O(nh), where h is the number of hull vertices. It can be attractive when h is small.

### Quickhull

Start with the leftmost and rightmost points. Partition the remaining points on either side of their baseline. For each directed edge, choose the point with greatest signed distance (equivalently greatest cross-product magnitude on that side), then recurse on the two subproblems. Typical distributions often give O(n log n), but the worst case is O(n²).

## Output policy and edge cases

The implementations return a counter-clockwise, unclosed ring of extreme vertices. Duplicates are removed and intermediate collinear points on hull edges are omitted. Empty input returns an empty list; one point returns that point; two or more collinear points return the two extremes. Non-finite coordinates are rejected.

Some GIS tasks need every collinear boundary point retained. That is a different output policy and should be implemented explicitly rather than silently changing the hull definition.

## Verification

The test suite compares each algorithm against an independently implemented Andrew monotone-chain oracle on 120 seeded random integer point clouds, and checks degenerate inputs, duplicate points, collinear edges, orientation and invalid coordinates. The algorithms' agreement is useful but is not itself the oracle: the independent implementation provides a separate construction.

## GIS uses and limitations

Convex hulls summarize extents and support collision reasoning, clustering descriptors and geometric preprocessing. They fill concavities, so they are not concave hulls or faithful boundaries of irregular study areas. Alpha shapes provide a parameterized family of more detailed envelopes, but require separate choices about scale and topology.

Floating-point orientation can fail for nearly collinear coordinates. Use exact or adaptive-precision predicates for high-assurance overlays, topology or adversarial inputs. Coordinates must also be in an appropriate planar coordinate system if distances and areas are interpreted metrically.

## References

- Graham, R. L. (1972). [An efficient algorithm for determining the convex hull of a finite planar set](https://doi.org/10.1016/0020-0190(72)90045-2). Information Processing Letters, 1(4), 132–133.
- Jarvis, R. A. (1973). [On the identification of the convex hull of a finite set of points in the plane](https://doi.org/10.1016/0020-0190(73)90020-3). Information Processing Letters, 2(1), 18–21.
- Preparata, F. P. and Shamos, M. I. (1985). Computational Geometry: An Introduction. Springer.
- [CGAL 2D convex hull documentation](https://doc.cgal.org/latest/Convex_hull_2/index.html).

**Evidence state:** Graham scan, Jarvis march and Quickhull are described as distinct algorithms with their standard complexity qualifications. The repository versions are transparent floating-point teaching implementations; the tests add an independent monotone-chain comparison but do not establish robust predicates.
