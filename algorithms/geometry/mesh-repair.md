# Conservative triangular mesh repair

Mesh repair is not one operation: coordinate welding, degenerate-face removal, duplicate-face removal, orientation, hole filling, self-intersection repair and remeshing solve different problems and can change geometry in different ways.

The repository implements a deliberately conservative triangle-mesh cleanup pipeline. It optionally welds nearby vertices, removes faces collapsed by welding or having exactly zero area, removes duplicate triangles, rejects edges with more than two incident faces, propagates consistent orientation through edge-connected face components, and compacts unused vertices.

The orientation invariant is local: two faces sharing an edge traverse it in opposite directions. It does not decide which side is globally outside, so a closed component may still be inward-facing. Open and disconnected components are supported.

See the [implementation and tests](../../implementations/python/mesh-repair/README.md). This is not a general-purpose repair kernel: it does not fill holes, resolve geometric self-intersections, remove spikes, or perform isotropic remeshing. Welding is greedy and input-order dependent, and exact zero-area detection does not remove near-degenerate triangles.
