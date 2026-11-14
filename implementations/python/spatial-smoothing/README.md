# Spatial smoothing baselines

This directory contains a NumPy implementation of a two-dimensional thin-plate smoothing spline for a scalar response.

## Thin-plate spline

The model combines the radial basis kernel r² log(r) with an unpenalized affine plane. It solves the full-knot penalized system for a user-supplied nonnegative smoothing parameter. Zero penalty interpolates the supplied values (when the system is nonsingular); positive penalty trades fit against surface roughness.

Run tests from this directory with: python -m pytest -q

## Scope and limitations

This is an exact-knot 2-D thin-plate smoothing spline teaching baseline, not a complete generalized additive model. It uses every training location as a knot and a dense linear solve, with cubic-order computational scaling and quadratic memory. It does not implement low-rank thin-plate regression splines, smoothing-parameter selection, generalized responses, multiple additive smooth terms, random effects/GAMM, Duchon splines, soap-film boundary conditions, Bayesian P-splines or uncertainty bands.

Coordinates must be projected into a suitable planar metric coordinate system. Longitude/latitude in degrees are not Euclidean distances, and the global radial kernel does not respect coastlines, holes or barriers. Use boundary-aware smoothers where domain geometry matters.
