# Linear interpolation on a triangulated irregular network

A TIN represents a piecewise planar surface over a triangular mesh. For a
query point inside a triangle with vertices v1, v2, v3 and scalar values
z1, z2, z3, compute barycentric coordinates lambda1, lambda2, lambda3 such
that each lambda is non-negative (within numerical tolerance) and their sum
is one. The interpolated value is

```
z(x) = lambda1*z1 + lambda2*z2 + lambda3*z3
```

The implementation accepts a caller-supplied list of vertex coordinates,
vertex values and triangle index triples. It does not construct the TIN.
Queries outside all supplied triangles return None. Points on shared edges
are evaluated using the first containing triangle in input order.

## Scope

This is a direct O(number of queries × number of triangles) teaching
implementation. It assumes a valid non-overlapping planar triangulation,
does not validate global mesh topology or fill holes, and does not extrapolate
outside the mesh. Delaunay generation, constrained triangulation, breaklines,
natural-neighbour interpolation and uncertainty estimates are separate
methods.
