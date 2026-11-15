# Smallest enclosing circle

The smallest enclosing circle (minimum enclosing circle) is the minimum-radius Euclidean circle containing every point in a finite planar point set. Its centre is not generally the centroid or mean coordinate.

## Boundary characterisation

A minimum circle is determined by at most three input points:

- One point when all points coincide.
- Two points when the circle's diameter is defined by a farthest pair.
- Three non-collinear points when the defining points lie on the circle's boundary.

For a two-point boundary, the centre is the midpoint and the radius is half their separation. For three non-collinear boundary points, the centre is their circumcentre. Collinear triples reduce to the farthest pair.

## Welzl's randomized algorithm

Welzl's algorithm randomly orders the points and incrementally maintains the minimum circle for the processed prefix. When a point falls outside, nested passes constrain it and up to two earlier points on the boundary. If the next point is already enclosed, it does not change the solution. Otherwise it becomes a required boundary point and the subproblem is solved again. Randomization gives expected linear time under the standard model, although the recursive teaching implementation here is not designed for very large or adversarial inputs.

The implementation uses a local seed for reproducibility, an iterative nested-loop construction and a scale-aware floating-point containment tolerance. The iterative form avoids Python recursion-depth failures. This is a practical numerical baseline, not an exact-arithmetic certificate.

## Applications and cautions

The circle is useful for compactness summaries, geometric bounding, sensor placement and preliminary facility or camera coverage. It is not a substitute for an oriented minimum bounding rectangle, a geodesic enclosing circle or a robust ellipsoidal solution. Longitude/latitude coordinates should not be passed directly to a planar Euclidean routine.

## Reference

Welzl, E. (1991). Smallest enclosing disks (balls and ellipsoids). In *New Results and New Trends in Computer Science*, LNCS 555, 359–370.

See the [tested Python implementation](../../implementations/python/geometry-metrics/README.md), [verification note](../../catalog/verification/smallest-enclosing-circle.md) and [interactive lab](../../notebooks/geometry-metrics-lab.ipynb).
