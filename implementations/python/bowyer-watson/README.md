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
3. Find all current triangles whose circumcircles strictly contain the new site.
4. Count the edges of those triangles; edges appearing once form the cavity boundary.
5. Remove the cavity triangles and connect each boundary edge to the inserted site.
6. Remove all triangles incident to a super-triangle vertex.

The implementation orients every triangle counter-clockwise. Its incircle determinant is positive for an interior point when the triangle is counter-clockwise.

## Scope and limitations

This is a teaching baseline, not a robust production triangulator. It scans all current triangles for each insertion, uses floating-point predicates with a scale-based tolerance, and resolves exact cocircular ties by insertion order. Near-collinear and near-cocircular configurations can be ambiguous. It does not implement exact arithmetic, constrained edges, weighted sites, or a spatial point-location structure. Use a robust geometry library for safety-critical or large-scale work.

## Independent checks

Tests check orientation, triangle/edge counts, inclusion of an interior site, an independently computed empty-circumcircle condition, a planar Euler-count fixture and invalid input handling.

## Related material

- [Voronoi/Delaunay concepts](../../../algorithms/geometry/voronoi-delaunay.md)
- [Qhull-backed reference wrapper](../voronoi-delaunay/README.md)
