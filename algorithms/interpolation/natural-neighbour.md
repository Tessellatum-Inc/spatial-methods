# Sibson natural-neighbour interpolation

Natural-neighbour interpolation estimates a value at a query location from the sample sites whose Voronoi cells are adjacent to the query's inserted Voronoi cell. Sibson's construction assigns each site a weight equal to the area it loses when the query is inserted, divided by the area of the new query cell.

For query q and site i, let A_i(q) be the area of the intersection between the query's new Voronoi cell and site i's old Voronoi cell. Then

\[
\hat z(q)=\sum_i w_i(q)z_i,\qquad
w_i(q)=\frac{A_i(q)}{\sum_j A_j(q)}.
\]

The weights are nonnegative and sum to one. The method is locally supported, reproduces constants and affine planes in exact arithmetic, and does not require a variogram model. It is not ordinary kriging: there is no fitted covariance model or kriging variance.

## Reference implementation

The [Python implementation](../../implementations/python/natural-neighbour/README.md) computes the query Voronoi cell by clipping an initial rectangle against perpendicular-bisector half-planes. It then clips that cell against each old site's Voronoi half-planes to measure stolen areas. This direct construction costs O(m n²) for m queries and n sites.

## Assumptions and limits

- Use projected Cartesian coordinates with meaningful Euclidean distances; do not feed longitude/latitude degrees.
- Sites must be distinct and span two dimensions.
- Queries must lie strictly inside the convex hull. Outside-hull extrapolation and boundary cases are rejected rather than silently assigned unstable weights.
- The implementation uses floating-point polygon clipping. Near-coincident sites, extremely large coordinate magnitudes and near-degenerate Voronoi cells need scaling or robust predicates.
- It is a reference implementation, not a replacement for optimised Delaunay-based Sibson implementations in large workloads.
