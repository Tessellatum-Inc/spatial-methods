# Spatial and space-time kernel intensity estimation

## Point-process intensity

For a spatial point process, intensity describes expected event count per unit area, not a probability density that must integrate to one. A fixed-bandwidth Gaussian kernel estimator sums a normalized bivariate kernel centred on each observed event. Optional nonnegative event weights allow multiplicity or exposure weights.

## Space-time extension

A separable space-time estimator multiplies the spatial kernel by a univariate temporal kernel. It estimates events per unit area per unit time. The spatial and temporal bandwidths control smoothing in their respective units; their scales are not interchangeable.

## Implemented baseline

The [NumPy implementation](../implementations/python/spatial-intensity/README.md) provides fixed-bandwidth planar Gaussian spatial intensity and product-kernel space-time intensity. Tests cover the kernel peak, event-count scaling, weights, separability and invalid inputs.

## Spatial cautions

The implementation uses an uncorrected isotropic kernel. Near the edge of an observation window, part of each kernel lies outside the domain and the estimate is biased downward unless an appropriate edge correction or observation-process model is used. Projected metric coordinates are required. For road networks, coastlines, irregular study regions, anisotropic processes, prospective hotspots or exposure-varying surveillance, a planar isotropic KDE is not automatically appropriate.

## Limitations

This is not a Voronoi/Delaunay intensity estimator, adaptive KDE, network KDE, edge-corrected estimator, prospective hotspot test or inferential scan statistic. Bandwidth selection and uncertainty estimation are left to the analyst.

## Sources

- Diggle, P. J. (1985). “A kernel method for smoothing point process data.” *Journal of the Royal Statistical Society: Series C (Applied Statistics)*, 34(2), 138–147.
- Baddeley, A., Rubak, E., & Turner, R. (2015). *Spatial Point Patterns: Methodology and Applications with R*. Chapman & Hall/CRC.

No source figures, code or datasets are reproduced.
