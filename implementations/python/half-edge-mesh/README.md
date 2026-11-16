# Half-edge mesh topology

A dependency-free indexed half-edge representation for oriented triangular surface meshes.

## Build

```python
from half_edge_mesh import HalfEdgeMesh

mesh = HalfEdgeMesh.from_triangles(
    4,
    [(0, 1, 2), (2, 1, 3)],
)
print(mesh.adjacent_faces(0))  # (1,)
print(mesh.boundary_edges())   # boundary half-edge indices
```

Each input triangle creates three directed half-edges. Each half-edge stores its origin, incident face, next and previous edge in the face cycle, and its symmetric twin when the edge is interior. Boundary edges have `twin=None`. Isolated vertices are permitted.

## Contract and limits

- Input is an oriented triangle soup; faces must be consistently wound across shared edges.
- Every undirected edge has one or two incident faces. Edges with more than two incident faces are rejected.
- Duplicate geometric faces (including reversed duplicates), repeated vertices within a face, out-of-range indices and duplicate directed edges are rejected.
- The constructor checks each non-isolated vertex link is one connected path (boundary) or cycle (interior), rejecting disconnected bow-tie fans. This is a combinatorial manifold check; it does not detect geometric self-intersections.
- It does not construct explicit exterior boundary faces, support polygonal faces, edit topology, repair meshes, or guarantee geometric non-self-intersection.
- Construction is expected O(F) time and O(F+V) storage using hash maps, where F is triangle count and V is vertex count. Python dictionary costs are expected-case, not worst-case guarantees.

Run tests with `python -m pytest -q` from this directory.
