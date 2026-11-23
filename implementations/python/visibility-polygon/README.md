# Visibility polygons

A dependency-free reference implementation of the visibility polygon for a viewpoint strictly inside a simple polygon.

## Run

```bash
python -m pytest -q
```

## Algorithm

For every polygon vertex, the implementation casts three rays: toward the vertex and at small angular offsets on either side. Each ray is intersected with every polygon edge, retaining the nearest hit. Sorting the hits by ray angle gives the visible boundary.

With n polygon vertices, this straightforward implementation uses O(n) rays, O(n) edge tests per ray, and O(n log n) sorting: O(n² log n) time and O(n) output space. The method is intended as a transparent reference implementation; a rotational-sweep algorithm with an ordered active-edge structure is preferable for large polygons.

## Contract and limitations

- The input must be a simple polygon represented by its boundary vertices, with no holes.
- The viewpoint must be strictly inside the polygon (not on its boundary).
- Coordinates must be finite and in one planar Cartesian coordinate system.
- `angular_epsilon` controls the perturbation around vertex directions. The default is a small angular value; near-degenerate geometry and extreme coordinate scales may require a robust-predicate implementation.
- Floating-point ray casting is not a substitute for an exact visibility kernel. The function does not validate polygon simplicity or repair self-intersections.

## Verification

Tests cover a convex rectangle (full visibility), a concave L-shaped polygon (occlusion behind a reflex vertex), ring closure and starting-vertex invariance, finite output, and invalid inputs.

## References

- O'Rourke, J. (1987). Art Gallery Theorems and Algorithms. Oxford University Press.
- Ghosh, S. K. (2007). Visibility Algorithms in the Plane. Cambridge University Press.
