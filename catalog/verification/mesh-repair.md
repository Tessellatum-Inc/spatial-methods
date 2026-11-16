# Mesh repair verification record

**Source mapping:** Section 17, page 35, mesh-processing family (mesh repair).

## Implemented scope

- Optional spatial-hash vertex welding under a Euclidean tolerance.
- Removal of collapsed / exact-zero-area and duplicate triangles.
- Rejection of non-manifold edges.
- BFS parity propagation for consistent face winding per connected component.
- Removal of unreferenced vertices and a structured change report.

## Tests authored

- Duplicate, collapsed and unreferenced cleanup.
- Welding-induced duplicate removal.
- Shared-edge orientation propagation.
- Independent disconnected components.
- Non-manifold edge rejection.
- Invalid coordinate, face, index and tolerance inputs.
- Empty mesh.

Tests are authored but have not been executed in this environment. No CI success is implied.

## Limitations

Welding is greedy and order-dependent; no hole filling, self-intersection repair, spike removal, global outward orientation, near-degenerate thresholding or remeshing is implemented.
