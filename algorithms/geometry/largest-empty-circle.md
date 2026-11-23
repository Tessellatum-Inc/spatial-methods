# Largest empty circle in a point set

## Problem definition

Given a finite set of planar sites, find a circle with no site in its interior whose centre lies inside the convex hull of the sites. The objective is to maximise the distance from the centre to its nearest site:

\[
\max_{x\in\operatorname{conv}(S)}\;\min_{s\in S}\|x-s\|.
\]

The domain constraint matters. Without a bounded domain or a specified centre region, the problem may not have a finite solution. This record uses the sites' convex hull as the domain; it does not silently substitute an arbitrary study polygon.

## Geometric interpretation

The nearest-site distance is the distance to the Voronoi diagram's nearest-site regions. In an exact Voronoi-based solution, candidates arise from Voronoi vertices and relevant intersections with the domain boundary. Degeneracies, cocircular sites and boundary constraints need careful handling.

## Teaching implementation

The [geometry-metrics package](../../implementations/python/geometry-metrics/README.md) provides a transparent approximate baseline:

1. Construct the convex hull of the sites.
2. Start with a square covering the hull's bounding box.
3. Evaluate the nearest-site distance at each cell centre.
4. Use the 1-Lipschitz property of distance-to-a-set to bound every point in a cell by the centre value plus the cell half-diagonal.
5. Subdivide cells whose upper bound can still improve the best feasible centre.
6. Stop when no cell can exceed the current best by more than the requested additive precision.

The routine returns the best centre, its nearest-site clearance and the number of cells examined. It rejects collinear site sets because their convex hull has no two-dimensional interior. A maximum-cell guard bounds resource use.

## What it does not claim

- It is not an exact Voronoi-vertex construction.
- The domain is the convex hull of the sites, not an arbitrary polygon or raster.
- The result is an additive-tolerance approximation subject to floating-point arithmetic.
- It does not account for obstacles, barriers, geodesic distance or weighted sites.

## Exercise and lab

Use the [largest-empty-circle exercise](../../exercises/largest-empty-circle.md) and [geometry metrics lab](../../notebooks/geometry-metrics-lab.ipynb). A square with four corner sites has its largest empty circle at the centre; compare the returned radius with the exact distance to a corner.

## References

- Aurenhammer, F. (1991). Voronoi diagrams — a survey of a fundamental geometric data structure. *ACM Computing Surveys*, 23(3), 345–405.
- Preparata, F. P. and Shamos, M. I. (1985). *Computational Geometry: An Introduction*. Springer.

**Scope:** approximate largest empty circle with centre constrained to the convex hull of a non-collinear planar point set.
