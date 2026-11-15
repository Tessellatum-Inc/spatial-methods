# Spatial smoothing baselines

This directory contains NumPy implementations of a full-knot two-dimensional thin-plate smoothing spline and its low-rank thin-plate regression spline (TPRS) basis for a scalar response.

## Thin-plate spline

The model combines the radial basis kernel r² log(r) with an unpenalized affine plane. It solves the full-knot penalized system for a user-supplied nonnegative smoothing parameter. Zero penalty interpolates the supplied values (when the system is nonsingular); positive penalty trades fit against surface roughness.

Run tests from this directory with: python -m pytest -q

## Low-rank thin-plate regression spline

ThinPlateRegressionSpline2D(k, smoothing) constructs the reduced basis from the full-knot kernel: it removes the affine null space, eigendecomposes the projected kernel, retains the k largest positive eigen-directions and scales them so the transformed wiggliness penalty is the identity. The model has k + 3 coefficients (the affine null space plus k penalized radial terms). With k = n - 3, the fitted curve agrees with the full-knot smoother to numerical precision for the same penalty.

This is the transparent dense eigen-decomposition construction. It reduces the fitted coefficient count, but basis construction still forms and decomposes dense matrices; it is not the Lanczos/subsampled large-data implementation used by production GAM software.

## Scope and limitations

This is an exact-knot 2-D thin-plate smoothing spline teaching baseline, not a complete generalized additive model. It uses every training location as a knot and a dense linear solve, with cubic-order computational scaling and quadratic memory. It does not implement smoothing-parameter selection, generalized responses, multiple additive smooth terms, random effects/GAMM, Duchon splines, soap-film boundary conditions, Bayesian P-splines or uncertainty bands.

Coordinates must be projected into a suitable planar metric coordinate system. Longitude/latitude in degrees are not Euclidean distances, and the global radial kernel does not respect coastlines, holes or barriers. Use boundary-aware smoothers where domain geometry matters.
