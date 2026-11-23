# Implementation verification — 2D radial-basis interpolation

## Implemented contract

The package fits a global planar interpolant with an affine polynomial tail
and three selectable kernels: thin-plate, cubic and Gaussian. It supports
non-negative diagonal smoothing, centered/scaled coordinates and prediction
at multiple query locations.

The augmented system is solved directly with NumPy. Duplicate sites,
collinear point sets, malformed/non-finite values, invalid controls and
singular systems are rejected. This is a dense reference solver, not a
scalable local method.

## Independent checks in the package

- Affine fields are reproduced for all three kernels at interior and
  extrapolation queries.
- Zero-smoothing predictions reproduce training observations.
- Positive smoothing changes predictions for a deliberately perturbed
  observation set.
- Translation and uniform coordinate scaling preserve affine predictions.
- Empty queries and invalid controls/data are covered.

The PRESS oracle independently refits the model with each observation held out, providing a separate computational check of the hat-diagonal shortcut. These are algebraic and synthetic checks, not a comparison against an
independent RBF library or a geospatial field dataset. Such comparisons and
source-entry verification remain outstanding.

## Source and rights boundary

The implementation is an original, compact numerical reference based on
standard RBF interpolation formulations. The bibliography lists two
monographs for further study; no source code, figures or text are copied.
This record does not clear redistribution rights for the source compendium.
