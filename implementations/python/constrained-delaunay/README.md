# Constrained Delaunay triangulation

This package triangulates one simple polygon ring. It starts with the exact-predicate ear-clipping implementation and applies Lawson edge flips to unconstrained interior edges that violate the local Delaunay condition. Polygon boundary edges remain constrained.

Returned triangles are counter-clockwise and use exact decimal-rational coordinates. The implementation preserves polygon area and tests local weak-Delaunay legality using an exact incircle determinant. Cocircular edges are left unchanged.

```python
from constrained_delaunay import constrained_delaunay_triangulate
triangles = constrained_delaunay_triangulate([(0,0),(5,0),(6,3),(3,5),(0,3)])
```

## Scope
- One valid simple polygon ring; clockwise and explicitly closed rings are accepted.
- Boundary edges are the constraints.
- No holes, interior constraint segments, Steiner points, quality refinement or mesh-size controls.
- Lawson flips occur only across convex quadrilaterals.
- Exact rational orientation and incircle predicates avoid floating-point sign errors for supplied decimal coordinates.
- Cocircular configurations may have multiple valid triangulations; the existing diagonal is retained.

The worst-case flip count can be quadratic in the number of triangles; edge incidence is rebuilt after each flip. This is a transparent small/medium teaching baseline, not a large-mesh triangulator.

## Tests
Run `python -m pip install -r requirements.txt` then `PYTHONPATH=../ear-clipping python -m pytest -q`.
