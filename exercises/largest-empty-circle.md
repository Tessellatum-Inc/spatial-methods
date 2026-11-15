# Exercise: largest empty circle

## Goal

Find a high-clearance centre inside the convex hull of a finite set of sites.

## Tasks

1. Use four sites at the corners of a 10-by-10 square. Predict the centre and radius before running the implementation.
2. Add a fifth site at the centre. Explain why the largest empty circle changes.
3. Move one corner site inward. Compare the best centre and nearest-site clearance.
4. Tighten the additive precision. Record the number of cells examined and the change in returned radius.
5. Try collinear sites and explain why the two-dimensional domain assumption fails.
6. Explain why an arbitrary study-area polygon would define a different problem from the convex hull of the sites.

## Interpretation

The branch-and-bound upper bound uses the fact that distance to the nearest site is 1-Lipschitz. The returned centre is feasible and the best possible radius is no more than the requested precision above it, subject to floating-point arithmetic. This is an approximate convex-hull-domain method, not an exact Voronoi construction.

See the [canonical lesson](../algorithms/geometry/largest-empty-circle.md) and [geometry metrics lab](../notebooks/geometry-metrics-lab.ipynb).
