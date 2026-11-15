# Half-edge mesh data structure

A half-edge structure represents each oriented mesh edge as a record linked to the next and previous edge around a face. An interior edge has a symmetric twin with reversed direction. The representation makes local traversal explicit: face boundaries, adjacent faces, and edges incident to a vertex can be followed through pointers rather than reconstructed from triangle arrays.

## Indexed triangular implementation

The repository implementation builds a half-edge structure from consistently oriented triangular faces. It stores origin vertex, incident face, next, previous and optional twin indices. Boundary edges have no twin; an explicit exterior-face cycle is not synthesized.

The constructor rejects repeated vertices in a face, invalid indices, duplicate geometric faces, repeated directed edges, inconsistent winding across a shared edge, and edges incident to more than two faces. It exposes face cycles, boundary-edge enumeration, adjacent-face lookup and incident-face lookup.

This is a practical manifold-edge baseline, not a full mesh-repair or topology kernel. In particular, it does not prove that each vertex link is a single connected fan, detect geometric self-intersections, support edits, or implement winged-edge / quad-edge representations. The implementation also checks each non-isolated vertex link is one connected path or cycle, rejecting disconnected bow-tie fans.

See the [implementation and tests](../../implementations/python/half-edge-mesh/README.md). The source compendium also names winged-edge and quad-edge structures; those remain separate implementations.
