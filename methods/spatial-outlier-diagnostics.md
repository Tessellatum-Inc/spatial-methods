# Spatial outlier diagnostics

Spatial outlier analysis is a collection of exploratory diagnostics, not one universal test. A large global Z score, an unusual neighbour relationship, an extreme pairwise semivariance and a geographically local residual answer different questions.

## Implemented reference methods

The NumPy package [spatial-outliers](../implementations/python/spatial-outliers/README.md) provides five bounded baselines:

1. **Global Z scores:** population-standardised column values. These ignore spatial arrangement and assume the supplied numeric scale is meaningful.
2. **Spatial scatterplot data:** centred values paired with the row-standardised spatial lag from a supplied weights matrix. Quadrants can expose high-high, low-low and spatial outlier patterns; this helper does not compute Moran inference.
3. **Variogram cloud:** every unique pair contributes Euclidean separation and half the squared value difference. Large semivariances at short distances can reveal local discontinuities, but pair dependence means points are not independent observations.
4. **Local outlier factor:** the standard reachability-density ratio using brute-force Euclidean k-nearest neighbours. LOF above one indicates lower local density relative to neighbours; it is not a p-value.
5. **Distance-weighted local scores:** a Gaussian-kernel local mean and standardised deviation, with self-weight removed and an explicit radius.

## Coordinate and inferential cautions

Distance-based methods require projected coordinates with a suitable linear unit. Geographic longitude/latitude must not be passed as if degrees were metres. Choice of neighbourhood, radius, features and scaling can change rankings. Variogram-cloud pairs are dependent, and scanning many local scores creates multiplicity. Calibrated tests require an explicit null model and a resampling design that respects the sampling process and spatial dependence.

## Open scope

Isolation forest, robust multivariate scaling, formal variogram-cloud outlier tests, adaptive neighbourhood selection, geographically weighted regression residual diagnostics, edge correction, permutation calibration, multiplicity adjustment and scalable spatial indexes remain open. The implementations are deliberately labelled exploratory baselines rather than complete substitutes for those methods.

See the [verification record](../catalog/verification/spatial-outliers.md).
