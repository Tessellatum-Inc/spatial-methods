# Triangulated irregular network (TIN) interpolation

A dependency-free 2D barycentric interpolation baseline over a caller-
supplied triangular mesh. Each triangle carries values at its three vertices;
a query inside that triangle receives the barycentric weighted sum. Queries
outside every supplied triangle return `None`.

## Use

```python
from tin_interpolation import tin_interpolate

vertices = [(0, 0), (2, 0), (2, 2), (0, 2)]
values = [5, 9, 3, -1]
triangles = [(0, 1, 2), (0, 2, 3)]
predictions = tin_interpolate(vertices, values, triangles, [(0.5, 0.25)])
```

The mesh is an input: this package does not generate a Delaunay triangulation.
The caller is responsible for supplying a valid, non-overlapping planar
triangulation. A point on a shared edge is evaluated using the first
containing triangle in input order. Mesh holes remain unsupported.

## Tests and limits

Run `python -m pytest -q`. Tests include affine-plane reproduction, vertex
and shared-edge cases, outside-mesh behaviour, holes, malformed faces,
degenerate triangles and invalid inputs. The reference implementation scans
every triangle for each query (O(mq), where m is triangle count and q is
query count); it does not build a spatial index, enforce mesh topology,
perform extrapolation, or return uncertainty.
