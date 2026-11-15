# Geometry metrics: Hausdorff, discrete Fréchet and smallest enclosing circle

Dependency-free teaching implementations for planar point sets and ordered polylines.

- Directed and symmetric Hausdorff distance for finite point sets.
- Discrete Fréchet distance for ordered vertex sequences, using an O(mn)-time, O(n)-space dynamic program.
- Smallest enclosing circle using randomized Welzl recursion with a reproducible local seed.
- Convex-hull diameter using a rotating-calipers antipodal-pair sweep.

## Run

~~~bash
python -m pytest -q
~~~

Coordinates must use one planar Cartesian CRS and consistent linear units. Hausdorff treats inputs as sets of sampled vertices; it does not measure distance to continuous line segments. Discrete Fréchet respects vertex order and is not the continuous Fréchet distance. The smallest-circle routine uses floating-point predicates and recursive Welzl construction; it is intended for modest point sets, not adversarially large input or certified exact geometry.

The diameter routine builds a monotone-chain hull in O(n log n) and sweeps antipodal pairs in O(h). It returns a farthest pair, not a minimum-area oriented bounding rectangle.

See the [intern walkthrough](implementation-walkthrough.md), [Hausdorff/Fréchet lesson](../../../algorithms/geometry/hausdorff-frechet.md), [smallest-circle lesson](../../../algorithms/geometry/smallest-enclosing-circle.md), [test suite](test_geometry_metrics.py) and [interactive lab](../../../notebooks/geometry-metrics-lab.ipynb).
