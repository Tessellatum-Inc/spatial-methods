# Marching cubes

Marching cubes extracts a triangular isosurface from a three-dimensional
scalar field. Each grid cell is classified by whether its corner values lie
above or below a chosen level; edge intersections are interpolated and
combined into triangles according to a case table. Ambiguous configurations
require consistent disambiguation to avoid cracks and topology defects.

## Reference implementation

The repository wrapper delegates the extraction algorithm to scikit-image's
Lewiner method, which addresses ambiguous cases. See
[the implementation](../../implementations/python/marching-cubes/README.md).
The wrapper makes axis spacing and origin explicit and validates the scalar
volume before calling the library.

## Scope and cautions

This is a maintained-library integration, not a from-scratch lookup-table
implementation. It returns a triangle mesh; it does not guarantee that the
mesh is watertight for arbitrary masks, repair topology, simplify geometry or
perform Poisson reconstruction. Preserve coordinate-system and axis-order
metadata when exporting the result.
