# Bowyer–Watson Delaunay triangulation

A dependency-free incremental 2D Delaunay teaching implementation. It uses exact rational orientation and in-circle determinants (coordinates are converted from their decimal string representation to `Fraction`) and removes a large enclosing super-triangle before returning the finite triangulation.

```python
from bowyer_watson import delaunay_triangulate
triangles = delaunay_triangulate([(0, 0), (4, 0), (3, 3), (0, 2)])
```

## Contract and limits

- Input is at least three distinct finite planar points; all-collinear inputs are rejected.
- The implementation uses Euclidean planar geometry, not longitude/latitude geodesics.
- Output triangles are counter-clockwise tuples of exact rational coordinate pairs.
- Cocircular ties use a strict in-circle test: a zero determinant does not remove an existing triangle. This makes the result deterministic for a fixed input order, but does not promise a unique diagonal.
- The super-triangle is an implementation device (currently scaled to 128 times the input bounding-box span) and is removed from output. A previous CI regression showed that a smaller enclosure could leave a missing finite face even when all sites appeared in returned triangles. The seeded regression now checks Euler's planar triangle-count relation and that every input site appears in the finite output. A fixed multiplier cannot guarantee safety for arbitrarily near-collinear input; such cases remain outside the verified envelope.
- The straightforward cavity rebuild is intended for learning and small/medium inputs. It does not implement a production point-location structure, robust mesh data structure, constrained segments, holes, or refinement.

## Run

```bash
python -m pytest -q
```
