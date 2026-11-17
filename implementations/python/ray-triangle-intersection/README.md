# 3D geometry: ray intersection, BVH and frustum culling

A dependency-free 3D geometry reference package: Möller–Trumbore ray/triangle intersection, AABB slab tests, a binary bounding-volume hierarchy (BVH) built with exact-centroid surface-area-heuristic (SAH) split scans, a spatial triangle kd-tree with straddler duplication and near-first traversal, and conservative AABB/frustum-plane culling.

## Run

    python -m pip install -r requirements.txt
    python -m pytest -q

## Input and numerical contract

- Coordinates are finite Cartesian 3D values in one consistent frame and unit.
- The ray is o + t*d. The parameter t is Euclidean distance only if d is unit length.
- Default policy is two-sided intersection; back-face culling is opt-in.
- Edges and vertices are included within the configurable tolerance.
- Degenerate triangles and near-parallel ray/triangle pairs return no hit.
- This floating-point teaching implementation is not an exact/adaptive geometric predicate.
- The BVH builder scans every centroid split. It is deterministic and inspectable, but slower than binned SAH on large meshes.

Do not pass longitude/latitude directly as Cartesian 3D coordinates. Transform vertices and rays into an appropriate local/projected 3D engineering frame first. CRS transformation, ellipsoidal geometry occlusion culling, clip-matrix plane extraction, production SAH kd-tree construction, SIMD/GPU execution and production binned SAH are outside scope.


## Spatial kd-tree

The triangle kd-tree partitions the node's spatial AABB along its longest axis at a median centroid. Triangle bounds crossing the split are referenced in both children; query traversal clips the ray against child cells and deduplicates triangle tests. Empty/non-progressing splits become leaves and a maximum depth bounds replication. This is a median-split reference, not a production SAH kd-tree.
