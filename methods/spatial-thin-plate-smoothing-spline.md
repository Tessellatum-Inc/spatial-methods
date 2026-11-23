# Spatial thin-plate smoothing spline

## Purpose

A thin-plate smoothing spline estimates a smooth scalar surface from noisy observations at planar locations. In two dimensions its radial basis kernel is proportional to r² log(r), with an affine polynomial null space. The smoothness penalty corresponds to integrated squared curvature (second derivatives) over the plane.

## Implemented system

For observed coordinates s(i) and responses y(i), the implementation uses each observed location as a radial basis centre and combines the radial component with an unpenalized affine plane. It solves the constrained block system

\[
\begin{bmatrix}K+\lambda I & P\\P^T&0\end{bmatrix}
\begin{bmatrix}a\\b\end{bmatrix}
=
\begin{bmatrix}y\\0\end{bmatrix},
\]

where K contains the thin-plate radial kernel, P spans {1, x, y}, and lambda is a user-supplied nonnegative smoothing parameter. The fitted surface at new locations is the radial expansion plus the affine term. The affine null-space component is not penalized.

## Implemented baseline

The package provides two distinct estimators. ThinPlateSpline2D uses every observation as a radial centre and solves the full-knot system. ThinPlateRegressionSpline2D(k, smoothing) constructs a reduced-rank basis from the full-knot problem. Let P span the affine null space and let Q2 have orthonormal columns spanning its orthogonal complement. With E_ij = ||s_i-s_j||^2 log ||s_i-s_j||, form A = Q2^T E Q2, then eigendecompose A = U Lambda U^T. Retain the k largest positive eigenvalues and set R = Q2 U_k Lambda_k^(-1/2). The radial basis is B = E R, and the transformed wiggliness penalty is theta^T theta. Fit y approximately B theta + P beta with penalty lambda ||theta||^2. This is the Wood-style optimal rank truncation of the full thin-plate basis, not arbitrary knot placement.

The [NumPy implementation](../implementations/python/spatial-smoothing/README.md) provides fit, predict and fit_predict for both estimators on projected 2-D coordinates. For k = n - 3, the reduced model reproduces the full-knot solution to numerical precision. Tests cover this equivalence, zero-penalty interpolation, preservation of the affine null space, reduced basis dimensions, prediction at new points and invalid inputs.

## Spatial interpretation and limitations

This method can represent a spatially varying trend, for example a smooth field of elevation residuals, environmental measurements or local demand. It is globally supported and does not automatically account for coastlines, barriers, holes, disconnected domains, anisotropy or spatially varying measurement uncertainty. Geographic coordinates need a suitable projection or geodesic-aware basis.

This is not a complete GAM/GAMM. It does not implement smoothing-parameter selection, generalized likelihoods, multiple additive smooths, random effects, Duchon splines, soap-film smoothers or Bayesian P-splines. The TPRS basis is rank-reduced for fitting, but this transparent implementation still forms and eigendecomposes dense n-by-n matrices; it does not implement mgcv's Lanczos iteration, large-data subsampling, automatic basis-dimension checks or smoothing selection. Both methods are intended as small teaching examples.

## Sources

- Wood, S. N. (2003). “Thin plate regression splines.” *Journal of the Royal Statistical Society: Series B*, 65(1), 95–114. DOI: 10.1111/1467-9868.00374.
- [mgcv thin-plate regression spline construction notes](https://stat.ethz.ch/R-manual/R-devel/library/mgcv/help/tprs.html) — describes the optimal truncation of the full thin-plate basis and its unchanged penalty.

No source figures, code or datasets are reproduced.


## Related non-RBF spatial spline

A separate [tensor-product B-spline P-surface](../algorithms/interpolation/tensor-product-p-spline-surface.md) uses local tensor-product basis functions and discrete directional coefficient penalties. It is a different model family from the radial thin-plate spline described above.
