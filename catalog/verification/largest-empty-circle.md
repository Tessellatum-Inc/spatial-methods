# Source verification — largest empty circle

## Identity

The largest-empty-circle problem is a standard Voronoi geometry problem. The objective and candidate structure depend on the centre domain; a bounded convex-hull domain is not interchangeable with an arbitrary study polygon.

## Implemented scope

The geometry-metrics package constructs the convex hull of a non-collinear site set and searches for a centre inside that hull. It uses nearest-site distance as the objective and a 1-Lipschitz branch-and-bound upper bound: the distance at a cell centre plus the cell half-diagonal. The search returns a feasible centre and an additive precision bound, subject to floating-point arithmetic.

## Verification

Tests cover the square-corner case with a known centre and radius, feasibility inside a convex hull, nearest-site clearance, collinear-site rejection, invalid parameters and the cell-budget guard.

## Limitations

This is an approximate baseline, not an exact Voronoi-vertex construction. It does not support arbitrary domains, obstacles, weighted sites or geodesic distance. Exact candidate enumeration and robust degeneracy handling remain open.

## Rights

The method is independently implemented from its mathematical description. No source code or figures are reproduced.
