# Implementation verification — Bowyer–Watson Delaunay triangulation

**Implementation:** [dependency-free Python package](../../implementations/python/bowyer-watson/README.md)  
**Walkthrough:** [incremental cavity construction](../../implementations/python/bowyer-watson/implementation-walkthrough.md)  
**Lesson:** [Voronoi diagrams and Delaunay triangulations](../../algorithms/geometry/voronoi-delaunay.md)

## Verified implementation envelope

- Incremental insertion into a temporary enclosing super-triangle.
- Cavity detection by an exact rational in-circle determinant.
- Cavity boundary extraction by counting undirected edges of removed faces.
- Counter-clockwise output triangles; zero-area replacement faces are discarded.
- Strict in-circle policy: cocircular ties are retained rather than forcing a flip.
- Duplicate, insufficient, non-finite and all-collinear inputs are rejected.
- The super-triangle was widened to 128× the input bounding span after CI exposed a missing-face regression at a 32× scale; the seeded cloud test now asserts both Euler face count and representation of every input site. This is a tested practical margin, not a proof for arbitrarily near-collinear configurations.

## Independent checks

The package tests include:
- orientation of every output face;
- Euler's planar triangle count, 2n - 2 - h, for general-position point sets, where h is the convex-hull vertex count;
- empty circumcircles checked with an exact in-circle predicate;
- seeded point clouds across multiple sizes;
- square/cocircular insertion and deterministic repeatability;
- duplicate, non-finite, insufficient and collinear input rejection;
- boundary-edge incidence of one and interior-edge incidence of two.

## Limitations

The implementation is a teaching baseline, not a robust production geometry kernel. The cavity is found by scanning all triangles and the edge incidence is rebuilt after every insertion. It does not implement constrained segments, holes, Steiner points, quality refinement, a dynamic adjacency mesh, or geodesic distance. Cocircular output is valid but not unique; the strict predicate preserves existing ties for a fixed insertion order.
