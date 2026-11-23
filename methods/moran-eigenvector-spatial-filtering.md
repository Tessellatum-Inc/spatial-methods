# Moran eigenvector spatial filtering

Moran eigenvector spatial filtering represents spatially structured patterns with orthogonal synthetic covariates derived from a spatial weights matrix.

## Eigenvector basis

For a symmetric spatial weights matrix W, define the intercept-centering matrix

\[
H=I-\frac{11^T}{n},\qquad B=HWH.
\]

The eigenvectors of B are centered, mutually orthogonal spatial patterns. Positive eigenvalues correspond to positive spatial autocorrelation patterns under the associated Moran coefficient. A filter selects a subset of these eigenvectors.

## Regression form

A fixed filter augments ordinary least squares:

\[
y=\alpha 1+X\beta+E\gamma+\varepsilon,
\]

where E contains selected Moran eigenvectors. The spatial filter can absorb residual spatial pattern into synthetic regressors, potentially reducing residual spatial autocorrelation.

## Selection matters

The subset E is decisive. Published procedures use candidate thresholds and stepwise criteria such as model fit, significance or minimizing residual spatial autocorrelation. This implementation deliberately uses a caller-specified number of leading positive eigenvectors; it does not claim to reproduce the full semiparametric selection procedure.

## Scope

The implementation uses a symmetric nonnegative weights matrix and intercept-only centering HWH. It does not implement the general covariate projection M_X W M_X, automatic eigenvector selection, Spatial+, restricted spatial regression, GLM eigenvector filtering, SAR/CAR estimation or corrected inferential standard errors. Row-standardized asymmetric weights must not be passed without an explicitly justified symmetric transformation.

## References

- Griffith, D. A. (2003). *Spatial Autocorrelation and Spatial Filtering: Gaining Understanding through Theory and Scientific Visualization*. Springer. DOI [10.1007/978-3-540-24806-4](https://doi.org/10.1007/978-3-540-24806-4).
- Griffith, D. A. and Peres-Neto, P. R. (2006). “Spatial modeling in ecology: the flexibility of eigenfunction spatial analyses.” *Ecology*, 87(11), 2603–2613. DOI [10.1890/0012-9658(2006)87[2603:SMIETF]2.0.CO;2](https://doi.org/10.1890/0012-9658(2006)87%5B2603:SMIETF%5D2.0.CO;2).
- Tiefelsdorf, M. and Griffith, D. A. (2007). “Semiparametric Filtering of Spatial Autocorrelation: The Eigenvector Approach.” *Environment and Planning A*, 39(5), 1193–1221. DOI [10.1068/a37378](https://doi.org/10.1068/a37378).
