# Alpha shapes: a scale-dependent envelope of point data

A convex hull encloses every site but fills every concavity. An alpha shape offers a scale-dependent alternative: it retains local Delaunay simplices according to their circumradius, allowing the resulting envelope to follow the point distribution more closely.

## Parameter convention

This repository uses a length-valued threshold \(R_{max}\): retain a Delaunay triangle when its circumradius \(R_T\) satisfies

$$
R_T \leq R_{max}.
$$

Some software uses the reciprocal convention \(\alpha=1/R_{max}\), and some definitions use a squared radius. Always check the parameter convention before comparing outputs.

For a triangle with side lengths a, b, c and area A, the circumradius is

$$
R_T=\frac{abc}{4A}.
$$

The Delaunay triangulation supplies the candidate triangles. Once the retained triangles are selected, an edge belongs to the boundary of their union when it is incident to exactly one retained triangle. Edges shared by two retained triangles are interior edges and are removed.

## Algorithm implemented here

1. Validate unique, finite, non-collinear planar sites.
2. Construct a Delaunay triangulation using SciPy/Qhull.
3. Compute each triangle's circumradius.
4. Retain triangles whose radius does not exceed the chosen threshold.
5. Count undirected edge incidences and return the singly incident edges, directed with retained triangle interiors on their left.

This is a **triangle-union boundary** implementation. It does not return isolated edges or vertices that may belong to the full alpha complex without being incident to a retained triangle. It also delegates Delaunay construction to Qhull rather than implementing a triangulation algorithm from scratch.

## How the scale changes the shape

A small radius threshold retains few or no triangles. Increasing the threshold admits larger circumcircles and joins more of the point set. At sufficiently large thresholds, all Delaunay triangles are retained and the triangle union fills the convex hull.

The parameter is therefore a modelling choice, not a universal default. It should reflect the spatial scale of meaningful gaps or clusters in the data.

## GIS applications and cautions

Alpha shapes can describe point-cloud footprints, clustered observations, settlement extents, habitat patches and survey coverage. They can also fragment or change topology abruptly as the threshold changes. A threshold chosen in longitude/latitude degrees has no consistent ground-distance meaning; use a suitable projected coordinate system.

Delaunay triangulations can be ambiguous for cocircular points, and floating-point circumradius comparisons near the threshold may change inclusion. The implementation is a transparent numerical baseline, not an exact-predicate alpha-complex kernel.

## Verification

Tests check a right-triangle circumradius threshold, the removal of a shared square diagonal, boundary edge incidence, invalid inputs and a seeded point cloud compared with an independent circumradius calculation over the Delaunay triangles.

## References

- Edelsbrunner, H., Kirkpatrick, D. and Seidel, R. (1983). [On the shape of a set of points in the plane](https://doi.org/10.1109/TC.1983.1676304). IEEE Transactions on Information Theory, 29(4), 551–559.
- Edelsbrunner, H. and Mücke, E. P. (1994). [Three-dimensional alpha shapes](https://doi.org/10.1109/34.4007). ACM Transactions on Graphics, 13(1), 43–72.
- [SciPy Delaunay documentation](https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.Delaunay.html).

**Evidence state:** the geometric construction is based on the alpha-shape literature. This repository implements the 2D boundary of the retained Delaunay triangle union with a maximum-circumradius parameter; it does not claim a complete alpha-complex representation or an independent Delaunay implementation.
