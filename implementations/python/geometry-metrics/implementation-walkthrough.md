# Geometry metrics — implementation walkthrough

## 1. Directed and symmetric Hausdorff distance

For finite point sets A and B, the directed distance is the maximum over a in A of the nearest-neighbour distance from a to B. The symmetric Hausdorff distance is the maximum of both directed values. The direct implementation is O(|A||B|) and intentionally transparent rather than spatially indexed.

## 2. Discrete Fréchet distance

The dynamic program evaluates the leash distance at each pair of vertices. Each cell is the maximum of the current pair distance and the minimum predecessor value (up, diagonal or left). The rolling-row implementation uses O(mn) time and O(n) memory. The result depends on vertex order and sampling density; it is not the continuous Fréchet distance between piecewise-linear curves.

## 3. Smallest enclosing circle

Welzl's randomized algorithm maintains a boundary set of at most three points. If the next point lies inside the current circle, the circle remains valid. Otherwise the point joins the boundary and the recursive subproblem is solved with that constraint. One or two boundary points define a midpoint circle; three non-collinear points define a circumcircle. Collinear triples reduce to the farthest pair's diameter circle.

## 4. Polygon pole of inaccessibility

The Polylabel routine evaluates signed distance to the exterior and hole boundaries. A square cell's centre distance plus its half-diagonal is an upper bound on the best distance anywhere inside the cell. A max-priority queue subdivides only cells whose upper bound can still improve the current best by more than the requested precision. The output is approximate and depends on the absolute coordinate-unit precision.

## 5. Minimum-area oriented rectangle

The rectangle baseline constructs the convex hull, then tests each hull-edge orientation. It projects hull vertices onto the edge direction and its perpendicular, computes the enclosing extents and transforms the four corners back. This transparent method is O(h²) after hull construction; it is not the optimal linear-time rotating-calipers rectangle algorithm.

## 6. Validation and limitations

Tests cover known distances, symmetry, order sensitivity, singleton and empty cases, collinear triples, reproducibility and containment of all input points. Floating-point tolerances are explicit and are not a substitute for exact predicates. For large point sets use spatial indexes or established computational-geometry libraries; for continuous curve distances use a continuous Fréchet algorithm.
