# Alpha shapes: parameterized concave envelopes

This package builds a planar alpha complex from a SciPy Delaunay triangulation and extracts its polygon boundary. A triangle is retained when its circumradius is no greater than alpha. Alpha is therefore a radius in coordinate units, not the reciprocal convention used by some libraries.

## Run

    python -m pip install -r requirements.txt
    python -m pytest -q

## API

    from alpha_shapes import alpha_shape
    points = [(0,0),(4,0),(4,4),(3,4),(3,1),(1,1),(1,4),(0,4)]
    rings = alpha_shape(points, alpha=2.0)

The result is a list of unclosed boundary rings. Outer rings are counter-clockwise and holes are clockwise. Duplicate coordinates are removed. Fewer than three unique points and collinear sites return no polygon rings.

## Method and complexity

1. Construct a Delaunay triangulation.
2. Compute each triangle circumradius from its side lengths and area.
3. Retain triangles whose circumradius is at most alpha.
4. Extract edges incident to exactly one retained triangle.
5. Trace oriented boundary edges into rings.

Delaunay construction is typically O(n log n); filtering and boundary extraction are O(n) after triangulation. Memory is O(n) for a planar triangulation.

## Scope and limitations

This is a teaching implementation for finite planar point sets. SciPy/Qhull supplies the triangulation; near-degenerate inputs inherit its floating-point limitations. Non-manifold or open boundaries are rejected rather than silently returned as malformed rings. Weighted and 3D alpha shapes, arbitrary polygonization and production robust predicates are outside scope. Use a projected CRS when alpha represents physical distance.

## Verification

Tests cover exact square circumradius thresholds, a concave U-shaped fixture with hand-computed areas, lower-dimensional inputs, duplicates, invalid values, orientation, and translation/scaling invariance.

## References

- Edelsbrunner, H., Kirkpatrick, D., & Seidel, R. (1983). On the shape of a set of points in the plane. IEEE Transactions on Information Theory, 29(4), 551–559.
- Edelsbrunner, H. (1992). Weighted alpha shapes. Technical Report, Department of Computer Science, University of Illinois.
- SciPy spatial Delaunay documentation: https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.Delaunay.html
