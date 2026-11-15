# Spatial distribution summaries

Dependency-free weighted planar implementations of mean center, geometric median center, standard distance and the covariance-based standard deviational ellipse.

## Quick start

~~~python
from spatial_centers import (
    mean_center, median_center, standard_distance, standard_deviational_ellipse,
)

points = [(0, 0), (2, 0), (0, 2), (1, 1)]
weights = [1, 3, 1, 2]
print(mean_center(points, weights))
print(median_center(points, weights))
print(standard_distance(points, weights))
print(standard_deviational_ellipse(points, weights))
~~~

## Definitions and conventions

- **Mean center:** weighted arithmetic mean of x and y coordinates.
- **Median center:** weighted geometric median, the point minimizing the sum of weighted Euclidean distances. It is computed by modified Weiszfeld iteration, including a coincident-point optimality check.
- **Standard distance:** weighted root-mean-square radial distance from the weighted mean center.
- **Standard deviational ellipse:** eigen-decomposition of the weighted population coordinate covariance matrix. The returned semiaxes are the square roots of its eigenvalues, and orientation is counterclockwise from the positive x-axis.

The ellipse's default scale is 1. For a bivariate normal distribution, multiply both semiaxes by sqrt(2) to obtain the joint 68-percent probability ellipse. This is different from treating a one-dimensional 1-SD interval as a 68-percent two-dimensional region.

## Assumptions and limitations

Coordinates must be projected planar coordinates in a consistent linear unit. Weights must be finite and nonnegative with a positive total. The package accepts point coordinates only; it does not compute centroids from line/polygon geometries, group by case fields, create output geometries, handle geographic/ellipsoidal distances, compute central features, or implement 3D centers/ellipsoids. The median solver is iterative and reports non-convergence rather than returning an unverified result.
