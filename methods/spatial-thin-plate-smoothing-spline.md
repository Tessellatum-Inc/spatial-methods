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

The [NumPy implementation](../implementations/python/spatial-smoothing/README.md) provides fit, predict and fit_predict for a single scalar response on two-dimensional projected coordinates. Tests cover zero-penalty interpolation, exact recovery of an affine plane under positive smoothing, prediction at new points and invalid inputs.

## Spatial interpretation and limitations

This method can represent a spatially varying trend, for example a smooth field of elevation residuals, environmental measurements or local demand. It is globally supported and does not automatically account for coastlines, barriers, holes, disconnected domains, anisotropy or spatially varying measurement uncertainty. Geographic coordinates need a suitable projection or geodesic-aware basis.

This is not a complete GAM/GAMM. It does not implement low-rank thin-plate regression splines, smoothing-parameter selection, generalized likelihoods, multiple additive smooths, random effects, Duchon splines, soap-film smoothers or Bayesian P-splines. The full-knot solve is dense and intended for small teaching examples.

## Sources

- Wood, S. N. (2003). “Thin plate regression splines.” *Journal of the Royal Statistical Society: Series B*, 65(1), 95–114. DOI: 10.1111/1467-9868.00374.
- Duchon spline foundations are described in Duchon (1977); see the documented thin-plate/Duchon relationship in the R mgcv smooth-constructor reference.

No source figures, code or datasets are reproduced.
