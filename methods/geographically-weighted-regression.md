# Geographically weighted regression

Geographically weighted regression (GWR) fits a separate weighted least-squares model at each target location. Nearby observations receive larger weights than distant observations, allowing coefficients to vary over space.

For target location i, design row x_j, response y_j and spatial distance d_ij, the local estimate is

    beta_hat(i) = (X' W(i) X)^(-1) X' W(i) y

when the weighted design is full rank. The implementation solves the weighted least-squares system with NumPy least squares rather than explicitly forming the inverse.

## Kernel and bandwidth

The reference package supports:

- Bisquare: w(u) = (1-u²)² for 0 ≤ u < 1 and zero otherwise.
- Gaussian: w(u) = exp(-u²/2).

Here u=d/h and h is either a fixed positive distance or an adaptive neighbour distance. Optional observation weights multiply the spatial kernel weights. The model matrix is supplied by the caller; include an intercept column explicitly.

## Diagnostics and interpretation

The implementation returns local coefficients, fitted values, residuals, effective local sample sizes and weighted-design condition numbers. Effective sample size is (sum w)²/sum(w²). A local rank deficiency or condition number above the declared limit raises an error rather than silently returning unstable coefficients.

Use projected planar coordinates in a common linear unit. Coefficient surfaces are descriptive local estimates; local standard errors, multiple-testing correction and bandwidth-selection uncertainty are not supplied.

## Scope

The tested implementation is a dense, small-data baseline. It does not implement MGWR, GTWR, geographically weighted PCA or summary statistics, general spatially varying-coefficient models, or GeoDetector. It does not automatically select bandwidths, perform inferential significance mapping, or handle geographic/ellipsoidal distance.
