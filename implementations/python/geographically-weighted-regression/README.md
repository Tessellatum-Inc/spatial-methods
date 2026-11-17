# Geographically weighted regression (GWR)

A NumPy-only, small-data reference implementation of local weighted least squares. At each observation location it fits the supplied design matrix with spatial weights from either a fixed-distance or adaptive-neighbourhood kernel.

## Supported

- Bisquare compact-support and Gaussian kernels.
- Fixed positive-distance bandwidths and adaptive integer neighbour counts.
- Optional nonnegative observation weights.
- Location-specific coefficients, fitted values and residuals.
- Effective local sample size and weighted-design condition-number diagnostics.
- Explicit rejection of locally rank-deficient or ill-conditioned systems.

The caller supplies the model matrix, including any intercept column. Coordinates are treated as planar Euclidean coordinates in consistent linear units. Adaptive bandwidth uses the distance to the (k+1)th sorted observation, then expands it by one floating-point step so compact support does not discard the boundary neighbour.

## Run

    python -m pytest -q

## Deliberate limits

This is a transparent dense reference, not a scalable spatial index. It does not choose bandwidths by cross-validation, estimate local standard errors or multiple-testing corrections, support polygonal/ellipsoidal distance, fit MGWR or GTWR, or implement geographically weighted PCA/summary statistics. It is not a general spatially varying-coefficient model or GeoDetector.
