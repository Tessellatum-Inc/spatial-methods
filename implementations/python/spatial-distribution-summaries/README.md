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

The ellipse's default scale is 1. For a bivariate normal distribution, multiply both semiaxes by approximately 1.515 to obtain the joint 68.3-percent probability ellipse. This is different from treating a one-dimensional 1-SD interval as a 68-percent two-dimensional region.

## Assumptions and limitations

Coordinates must be projected planar coordinates in a consistent linear unit. Weights must be finite and nonnegative with a positive total. The package accepts point coordinates only; it does not compute centroids from line/polygon geometries, group by case fields, create output geometries, handle geographic/ellipsoidal distances, compute central features, or implement 3D centers/ellipsoids. The median solver is iterative and reports non-convergence rather than returning an unverified result.


## Circular and directional statistics

The companion `directional_statistics.py` module adds circular mean direction and mean resultant length, the Rayleigh test for unimodal concentration, Kuiper and Watson U-squared rotation-invariant tests against circular uniformity, the von Mises probability density, and weighted rose-histogram counts. Angles are radians counterclockwise from +x. These methods are not interchangeable: Rayleigh is primarily sensitive to unimodal concentration, while Kuiper can detect broader departures from uniformity. The Kuiper and Watson p-values are asymptotic approximations; small samples, ties and strongly discrete bearings need careful interpretation. The von Mises evaluator uses direct Bessel normalization and rejects concentrations that overflow that calculation.

See the [circular and directional statistics lesson](../../../algorithms/statistics/circular-directional-statistics.md) and `test_directional_statistics.py`.
