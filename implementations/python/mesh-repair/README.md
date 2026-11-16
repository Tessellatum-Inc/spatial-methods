# Conservative triangular mesh repair

This utility performs bounded, auditable cleanup on triangle meshes:

1. validates finite 3D coordinates and triangle indices;
2. optionally welds vertices within a Euclidean tolerance using a spatial hash;
3. removes faces collapsed by welding and exactly zero-area triangles;
4. removes duplicate triangles irrespective of orientation;
5. rejects edges incident to more than two faces;
6. propagates consistent face orientation over each edge-connected component;
7. compacts unreferenced vertices and reports each change.

```python
from mesh_repair import repair_triangle_mesh
vertices, faces, report = repair_triangle_mesh(
    [(0,0,0), (1,0,0), (0,1,0), (1e-8,0,0)],
    [(0,1,2)], weld_tolerance=1e-6,
)
```

## Important scope

Welding is greedy and input-order dependent: a vertex maps to the first accepted representative within tolerance. This is not transitive clustering and does not promise that every pair of points in a welded cluster is within tolerance. A zero tolerance disables welding. The exact-zero-area test is intentionally conservative; near-degenerate triangles are not removed.

The orientation pass makes adjacent faces traverse each shared edge in opposite directions, but does not choose a globally outward orientation. Open surfaces and disconnected components are supported. Non-manifold edges are rejected rather than guessed or split.

This does not fill holes, resolve self-intersections, remove spikes, preserve sharp features during remeshing, infer missing geometry, or repair arbitrary non-manifold vertex configurations beyond what can be detected from edge incidence and orientation constraints. Treat the report as an audit trail and inspect outputs before using them downstream.

Run `python -m pytest -q` in this directory.
