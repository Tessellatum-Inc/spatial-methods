# Alpha shapes: a scale-dependent envelope of point data

A convex hull fills every concavity. An alpha shape offers a scale-dependent alternative: it retains local Delaunay triangles according to their circumradius, allowing the resulting envelope to follow the point distribution more closely.

## Parameter convention

This repository uses a length-valued threshold R: retain a Delaunay triangle when its circumradius r satisfies r <= R. Some software uses the reciprocal convention alpha = 1/R, and some definitions use a squared radius. Check the parameter convention before comparing outputs.

For a triangle with side lengths a, b, c and area A, its circumradius is abc/(4A).

## Implemented construction

1. Validate and deduplicate finite planar sites.
2. Construct a Delaunay triangulation using SciPy/Qhull.
3. Compute each triangle's circumradius.
4. Retain triangles whose radius does not exceed the selected threshold.
5. Extract edges incident to exactly one retained triangle and trace oriented boundary rings.

This is the boundary of the retained triangle union. It does not represent isolated edges or vertices in the full alpha complex. Delaunay construction is delegated to Qhull; it is not independently implemented here.

## Scale and interpretation

A small threshold retains few or no triangles. Increasing it admits larger circumcircles and joins more of the point set. At sufficiently large thresholds, all Delaunay triangles are retained and the union fills the convex hull.

The threshold is a modelling choice, not a universal default. It should reflect the scale of meaningful gaps or clusters. Alpha shapes can describe point-cloud footprints, clustered observations, settlement extents, habitat patches and survey coverage. Topology may change abruptly as the threshold changes.

## Limitations

The 2D implementation returns unclosed boundary rings: outer rings are counter-clockwise and holes clockwise. The 3D companion returns vertices and outward-oriented triangular boundary faces. It removes duplicate sites. Inputs with fewer than three unique sites or collinear sites return no polygon rings. Non-manifold or open boundaries raise ValueError rather than silently producing malformed output.

The implementation uses floating-point circumradius comparisons and inherits Qhull's handling of cocircular and near-degenerate sites. It is a transparent 2D teaching baseline, not an exact-predicate production geometry kernel. A 3D companion filters Delaunay tetrahedra by circumradius and returns the oriented boundary of their union. Weighted alpha shapes and the complete lower-dimensional alpha complex remain outside scope. Use a suitable projected CRS when the threshold represents physical distance.

## Verification

The test suite checks 2D square circumradius and concave U-shaped fixtures, plus 3D tetrahedron circumradius thresholds, outward face orientation, cube surface area, lower-dimensional inputs, invalid values and translation/scaling invariance. The U-shaped test demonstrates a concave envelope before a larger threshold fills the convex hull.

## Implementation

See the [Python alpha-shape package](../../implementations/python/alpha-shapes/README.md) for the implementation, dependencies and runnable tests.

## References

- Edelsbrunner, H., Kirkpatrick, D. and Seidel, R. (1983). [On the shape of a set of points in the plane](https://doi.org/10.1109/TC.1983.1676304). IEEE Transactions on Information Theory, 29(4), 551–559.
- Edelsbrunner, H. and Mücke, E. P. (1994). [Three-dimensional alpha shapes](https://doi.org/10.1109/34.4007). ACM Transactions on Graphics, 13(1), 43–72.
- [SciPy Delaunay documentation](https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.Delaunay.html).

**Evidence state:** the repository implements the 2D boundary of the retained Delaunay triangle union with a maximum-circumradius parameter. It does not claim a complete alpha-complex representation or an independent Delaunay implementation.
