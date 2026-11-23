# Isotropic-style triangular remeshing baseline

A dependency-free local-edit remesher for consistently oriented manifold triangle meshes.

Each iteration:
1. splits edges longer than `split_ratio * target_length`;
2. collapses edges shorter than `collapse_ratio * target_length`, subject to boundary constraints and a full combinatorial manifold rebuild check;
3. flips interior edges only when the minimum angle of the two incident triangles strictly improves;
4. performs tangential vertex relaxation, optionally pinning boundary vertices.

```python
from isotropic_remeshing import isotropic_remesh
new_vertices, new_faces, counts = isotropic_remesh(
    vertices, faces, target_length=10.0, iterations=3
)
```

## Scope and limitations

This is a conservative educational baseline, not a production isotropic remesher. Local edits rebuild and validate topology, so runtime is high. Candidate edges are processed from per-pass snapshots; an edge changed by an earlier operation may no longer be eligible later in that pass. Collapses are rejected when they create duplicate faces or violate manifold validation. Boundary edges are protected from collapse by default, and boundary vertices are pinned during relaxation by default.

The flip criterion is a local minimum-angle improvement, not constrained Delaunay optimization. Tangential relaxation uses area-weighted vertex normals and neighbour averages; it is not curvature-flow integration. There is no feature/crease preservation, adaptive sizing field, projection to a reference surface, error bound, Hausdorff guarantee, or robust exact predicates. It does not guarantee every output edge lies within the target-length band, and a pass can leave short or long edges when a topology-safe edit is unavailable.

Run `python -m pytest -q` in this directory.
