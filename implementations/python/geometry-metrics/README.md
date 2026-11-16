# Geometry metrics: Hausdorff, discrete Fréchet and smallest enclosing circle

Dependency-free teaching implementations for planar point sets and ordered polylines.

- Directed and symmetric Hausdorff distance for finite point sets.
- Discrete Fréchet distance for ordered vertex sequences, using an O(mn)-time, O(n)-space dynamic program.
- Continuous Fréchet decision via Alt–Godau free-space reachability, with distance approximation by bisection to an absolute tolerance.
- Smallest enclosing circle using randomized iterative incremental construction with a reproducible local seed, local-frame circumcircle predicates and ULP-scaled containment checks.
- Convex-hull diameter using a rotating-calipers antipodal-pair sweep.
- Approximate polygon pole of inaccessibility (Polylabel-style best-first subdivision), supporting holes and an explicit distance precision.
- Approximate largest empty circle for point sites, with its centre constrained to the sites' convex hull and a Lipschitz branch-and-bound error bound.
- Minimum-area oriented bounding rectangle using both a transparent O(h²) baseline and a four-support O(h) rotating-calipers sweep after hull construction.

## Run

~~~bash
python -m pytest -q
~~~

Coordinates must use one planar Cartesian CRS and consistent linear units. Hausdorff treats inputs as sets of sampled vertices; it does not measure distance to continuous line segments. Discrete Fréchet respects vertex order and is not the continuous Fréchet distance. The smallest-circle routine uses floating-point predicates and a randomized iterative incremental construction; it avoids recursion-depth limits but remains a teaching implementation, not certified exact geometry.

The diameter routine builds a monotone-chain hull in O(n log n) and sweeps antipodal pairs in O(h). It returns a farthest pair, not a minimum-area oriented bounding rectangle. Polylabel maximises signed boundary clearance with a best-first square-cell search and returns an approximate point and radius; polygon rings must be valid.

See the [minimum-area rectangle lesson](../../../algorithms/geometry/minimum-area-bounding-rectangle.md), [intern walkthrough](implementation-walkthrough.md), [Hausdorff/Fréchet lesson](../../../algorithms/geometry/hausdorff-frechet.md), [smallest-circle lesson](../../../algorithms/geometry/smallest-enclosing-circle.md), [Polylabel lesson](../../../algorithms/geometry/pole-of-inaccessibility-polylabel.md), [largest empty circle lesson](../../../algorithms/geometry/largest-empty-circle.md), [test suite](test_geometry_metrics.py) and [interactive lab](../../../notebooks/geometry-metrics-lab.ipynb).


The continuous Fréchet decision routine uses the free-space diagram for polygonal curves. The distance routine bisects the decision threshold and returns an upper bound within the requested tolerance (subject to floating-point arithmetic); it is distinct from the discrete vertex-sequence dynamic program.


The largest-empty-circle routine searches the convex hull of a non-collinear site set and maximises distance to the nearest site. It is an additive-tolerance branch-and-bound baseline, not an exact Voronoi-vertex construction for arbitrary domains.


The four-support rotating-calipers rectangle routine advances the extrema along the edge direction and its normal monotonically around the convex hull. Its sweep is O(h) after the O(n log n) hull construction; seeded tests compare its area against the transparent O(h²) orientation scan.


- Minimum width of a point set using a rotating antipodal-support pointer,
  O(n log n) including hull construction and O(h) for the caliper sweep.
  This returns the minimum distance between parallel support lines; it is
  distinct from minimum-area bounding rectangle and diameter.
