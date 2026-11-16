# Implementation verification — polygon-boundary constrained Delaunay triangulation

The package starts from a simple-polygon ear-clipping triangulation and applies Lawson edge flips until every unconstrained interior edge is locally weakly Delaunay. Polygon boundary edges remain fixed. Orientation and incircle tests use exact rational arithmetic.

Tests check:
- (n-2) triangle count and positive orientation;
- exact polygon-area conservation for convex, concave and clockwise rings;
- each normalized polygon boundary edge appears exactly once, including redundant collinear boundary inputs;
- every unconstrained two-triangle edge satisfies an exact incircle legality check;
- seeded radial simple polygons across multiple vertex counts;
- non-crossing interior diagonals preserved as two-sided edges, including concave polygon partitions;
- multiple non-crossing constraints sharing an endpoint, boundary-edge constraints, and rejection of crossing constraints and exterior chords.

This is not a general constrained mesh package. Interior constraints are limited to non-crossing diagonals between existing normalized polygon vertices; arbitrary segment recovery, holes, Steiner points and quality refinement are not implemented. The flip loop rebuilds edge incidence after each change and is not optimized for large meshes.

Reproduce with `python -m pip install -r requirements.txt && PYTHONPATH=../ear-clipping python -m pytest -q`.
