# Bowyer–Watson incremental Delaunay triangulation

A dependency-free, readable planar Delaunay reference implementation. Unlike the adjacent Voronoi/Delaunay package, this code performs incremental cavity reconstruction itself; it does not call SciPy or Qhull.

## Run

```bash
python -m pip install -r requirements.txt
python -m pytest -q
```

## Algorithm

1. Add a large super-triangle enclosing the sites.
2. Insert sites one at a time.
3. Find current triangles whose circumcircles contain the inserted site, including values numerically tied within a scale-relative tolerance.
4. Count the edges of those triangles; edges appearing once form the cavity boundary.
5. Remove the cavity triangles and connect each boundary edge to the inserted site.
6. Remove all triangles incident to a super-triangle vertex.

The implementation orients every triangle counter-clockwise. Its incircle determinant is positive for a strictly interior point when the triangle is counter-clockwise. The tolerance is computed from point-relative coordinate differences, so a simple translation of the dataset does not change the tolerance scale.

## Scope and limitations

This is a teaching baseline, not a robust production triangulator. It scans all current triangles for each insertion, giving quadratic time and linear working storage for ordinary planar inputs. It uses floating-point predicates with a scale-relative tolerance and resolves cocircular choices deterministically by insertion order. Near-collinear and near-cocircular configurations can remain ambiguous. It does not implement exact arithmetic, constrained edges, weighted sites, or a spatial point-location structure. Use a robust geometry library for safety-critical or large-scale work.

## Independent checks

Tests check orientation, triangle/edge counts, inclusion of an interior site, an independently computed empty-circumcircle condition, a planar Euler-count fixture, invalid input handling, translation invariance and small-coordinate-scale behaviour.

## Related material

- [Voronoi/Delaunay concepts](../../../algorithms/geometry/voronoi-delaunay.md)
- [Qhull-backed reference wrapper](../voronoi-delaunay/README.md)
