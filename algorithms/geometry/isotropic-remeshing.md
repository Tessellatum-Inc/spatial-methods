# Isotropic-style triangular surface remeshing

The implementation provides a bounded local-edit remeshing baseline for consistently oriented manifold triangle meshes. It splits overlong edges, attempts safe short-edge collapses, flips interior edges when the local minimum angle improves, and applies tangential vertex relaxation. Boundary edges are protected from collapse and boundary vertices can be pinned.

Every topology-changing operation is checked by rebuilding the indexed half-edge structure. This favours conservative correctness over speed and makes the implementation unsuitable for large production meshes without a more efficient mutable topology kernel.

The implementation does not provide feature-aware sizing, constrained Delaunay guarantees, reference-surface projection, Hausdorff error bounds, or exact target edge lengths. It is not a substitute for a production remeshing library.

See the [implementation and tests](../../implementations/python/isotropic-remeshing/README.md).
