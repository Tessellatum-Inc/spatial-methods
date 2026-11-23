# Planar convex hulls: Graham scan, Jarvis march and Quickhull

Three dependency-free teaching implementations solve the same finite 2D convex-hull problem using different strategies.

## Run

~~~bash
python -m pip install -r requirements.txt
python -m pytest -q
~~~

## Algorithms

- **Graham scan** sorts points by polar angle around a guaranteed hull pivot, then maintains a stack of counter-clockwise turns. Time: O(n log n).
- **Jarvis march (gift wrapping)** repeatedly selects the next extreme point around the boundary. Time: O(nh), where h is the number of hull vertices; useful when the hull is small relative to the input.
- **Quickhull** partitions points by the line through the extreme x-coordinates, recursively selecting the farthest point from each current hull edge. Typical time is O(n log n), worst case O(n²).

All return counter-clockwise extreme vertices without repeating the first point at the end. Duplicate coordinates are removed; intermediate collinear boundary points are omitted; empty, singleton, two-point and all-collinear inputs are supported. Non-finite coordinates raise ValueError.

## Example

~~~python
from graham_scan import convex_hull, jarvis_march, quickhull

points = [(0, 0), (2, 0), (2, 2), (0, 2), (1, 1)]
assert convex_hull(points) == jarvis_march(points) == quickhull(points)
~~~

## Verification

The tests cover degeneracies, duplicate and collinear points, non-finite inputs, orientation and 120 seeded random point clouds per algorithm. Randomized outputs are compared against an independently written Andrew monotone-chain reference implementation, rather than comparing the algorithms only with one another.

## Numerical limitations

All three implementations use ordinary floating-point cross products. They are pedagogical and can misclassify near-collinear configurations at extreme coordinate scales. Production geometry should use exact or adaptive-precision orientation predicates.

## References

- Graham, R. L. (1972). [An efficient algorithm for determining the convex hull of a finite planar set](https://doi.org/10.1016/0020-0190(72)90045-2). Information Processing Letters, 1(4), 132–133.
- Jarvis, R. A. (1973). [On the identification of the convex hull of a finite set of points in the plane](https://doi.org/10.1016/0020-0190(73)90020-3). Information Processing Letters, 2(1), 18–21.
- Preparata, F. P. and Shamos, M. I. (1985). Computational Geometry: An Introduction. Springer.
- [CGAL 2D convex hull documentation](https://doc.cgal.org/latest/Convex_hull_2/index.html).

See the [algorithm lesson](../../../algorithms/geometry/convex-hull.md) and [visual lab](../../../notebooks/convex-hull-lab.ipynb).
