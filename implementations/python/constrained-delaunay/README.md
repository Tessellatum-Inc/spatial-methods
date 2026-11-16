# Constrained Delaunay triangulation

This package triangulates one simple polygon ring. It starts with the exact-predicate ear-clipping implementation and applies Lawson edge flips to unconstrained interior edges that violate the local Delaunay condition. Polygon boundary edges remain constrained. Consecutive duplicate and exactly collinear intermediate boundary vertices are normalized using the shared ear-clipping ring cleaner before the constraint set is built; non-finite coordinates are rejected.

Returned triangles are counter-clockwise and use exact decimal-rational coordinates. The implementation preserves polygon area and tests local weak-Delaunay legality using an exact incircle determinant. Cocircular edges are left unchanged.

```python
from constrained_delaunay import (
    constrained_delaunay_triangulate,
    constrained_delaunay_with_diagonals,
)
ring = [(0,0),(5,0),(5,1),(2,1),(2,4),(0,4)]
triangles = constrained_delaunay_with_diagonals(ring, [((0,0),(2,4))])
```

## Scope
- One valid simple polygon ring; clockwise and explicitly closed rings are accepted.
- Boundary edges are the constraints.
- Non-crossing interior constraints are supported when each segment joins existing normalized polygon vertices; each constraint partitions the polygon, and all resulting piece boundaries remain constrained. Crossing constraints, holes, Steiner points, quality refinement and mesh-size controls are unsupported.
- Lawson flips occur only across convex quadrilaterals. The separate `constrained_delaunay_with_diagonals` entry point accepts a non-crossing set of interior diagonals and triangulates each resulting simple piece independently.
- Exact rational orientation and incircle predicates avoid floating-point sign errors for supplied decimal coordinates.
- Cocircular configurations may have multiple valid triangulations; the existing diagonal is retained.

The worst-case flip count can be quadratic in the number of triangles; edge incidence is rebuilt after each flip. This is a transparent small/medium teaching baseline, not a large-mesh triangulator.

## Tests
Run `python -m pip install -r requirements.txt` then `PYTHONPATH=../ear-clipping python -m pytest -q`.
