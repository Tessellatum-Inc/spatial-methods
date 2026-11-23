# Implementation verification — TIN barycentric interpolation

The implementation evaluates linear barycentric interpolation over a
caller-supplied planar triangular mesh. It checks vertex/value alignment,
integer triangle indices, repeated indices, duplicate faces, zero-area
triangles and finite query coordinates.

Synthetic tests verify exact affine-plane reproduction, vertices, shared
edges, mesh holes and outside-mesh results. This is not a triangulation
generator and does not certify global mesh topology, non-overlap, breakline
handling or geospatial dataset accuracy. The mesh validity assumption is
therefore part of the caller contract.
