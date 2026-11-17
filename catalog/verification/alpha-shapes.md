# Implementation verification — planar alpha shapes

## Implemented scope

- SciPy/Qhull Delaunay triangulation of finite 2D sites.
- Circumradius thresholding of Delaunay triangles.
- Boundary extraction by single-incidence undirected edges.
- Directed ring tracing, with counter-clockwise outer boundaries and clockwise holes when the boundary is manifold.
- Duplicate-site removal and explicit lower-dimensional behavior.

## Independent checks

- A square's two Delaunay triangles have circumradius sqrt(2); a threshold below sqrt(2) retains none, while the exact threshold retains the square boundary.
- A U-shaped point fixture produces a concave ring with area 9 at threshold 2 and a convex-hull ring with area 16 at threshold 5.
- Translation and uniform scaling preserve ring vertex count and scale area by the square of the scale factor.
- Tests cover duplicate points, collinear and lower-dimensional inputs, invalid thresholds and coordinates, and outer-ring orientation.

## Limitations

This computes the boundary of the retained triangle union, not the complete alpha complex with isolated edges and vertices. Delaunay construction is delegated to SciPy/Qhull. Floating-point circumradius comparisons and Qhull degeneracy behavior are not exact-predicate guarantees. Non-manifold/open boundaries are rejected. Weighted and 3D alpha shapes are not implemented.

## Reproduction

From implementations/python/alpha-shapes:

    python -m pip install -r requirements.txt
    python -m pytest -q

A GitHub Actions run is triggered by the implementation commits; record its final result before marking the entry fully CI-verified.


## 3D boundary-mesh extension
- Delaunay tetrahedra are retained by circumsphere radius and single-incidence oriented faces are extracted.
- Tests cover a regular tetrahedron's analytic circumradius and outward face orientation, a cube's convex-hull surface area, lower-dimensional inputs and translation/scaling invariance.
- Limits: this is the boundary of the retained tetrahedron union, not the full alpha complex with isolated faces/edges/vertices; weighted 3D alpha shapes remain open.
