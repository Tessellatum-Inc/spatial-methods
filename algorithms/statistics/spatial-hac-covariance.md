# Spatial HAC covariance for OLS

## Purpose

Spatial heteroskedasticity-and-autocorrelation consistent (HAC) covariance estimators adjust OLS uncertainty when regression disturbances may be heteroskedastic and correlated across nearby locations. They change the estimated covariance of the OLS coefficients; they do not change the OLS point estimates or remove spatial endogeneity.

## Estimator

For response y, design matrix X and OLS residuals e, define the score row z_i=x_i e_i. Let d_ij be the planar distance between observations i and j, and let h be a positive distance bandwidth. The implementation uses the compact-support Wendland C2 radial kernel

\[
k(d_{ij}/h)=
\begin{cases}
(1-r)^4(4r+1), & r=d_{ij}/h<1,\\
0, & r\geq 1.
\end{cases}
\]

The spatial HAC sandwich is

\[
\widehat V(\hat\beta)=
(X'X)^{-1}
\left[\sum_i\sum_j k(d_{ij}/h)e_ie_jx_ix_j'\right]
(X'X)^{-1}.
\]

An optional finite-sample multiplier n/(n-k) is applied by default, where k is the number of design columns. Standard errors are square roots of the covariance diagonal.

## Implementation

The function spatial_hac_ols in implementations/python/spatial-econometrics/spatial_hac.py fits OLS and returns coefficients, residuals, the full covariance matrix, standard errors and the number of nonzero off-diagonal pairs. It uses the Wendland C2 kernel, which is compactly supported and positive definite for the two-dimensional Euclidean coordinate domain.

## Assumptions and interpretation

- Coordinates must be projected planar coordinates in a common linear unit. The bandwidth uses that same unit. Longitude/latitude degrees are not a suitable direct distance metric.
- The bandwidth is a modelling choice. A very small bandwidth approaches a heteroskedasticity-robust HC0 sandwich (before the optional correction); a larger bandwidth includes more cross-location residual products.
- This is an OLS covariance estimator. It does not estimate SAR/SEM parameters, correct for endogenous regressors, or make a misspecified conditional mean valid.
- The kernel is isotropic in Euclidean distance. Anisotropic, network-constrained, space-time, panel and data-driven bandwidth variants are not implemented.
- Dense pairwise distances and the N-by-N kernel matrix require O(N²) memory and work. Use sparse neighbourhood truncation or specialised software for large datasets.

## Validation

The tests compare the zero-overlap limit with the HC0 sandwich, check symmetry and positive semidefiniteness for a nearby-correlated synthetic example, and reject invalid coordinates, designs and bandwidths.
