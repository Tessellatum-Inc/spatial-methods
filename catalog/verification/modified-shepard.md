# Implementation verification — local quadratic modified Shepard

## Source identity

The method family is described by Franke and Nielson (1980) and Renka
(1988). The NAG Library's `nag_2d_shep_interp (e01sgc)` documentation
confirms that each local quadratic is constrained to interpolate its centre
node and that compact, node-specific radial weights restrict influence.
Shepard's original 1968 inverse-distance interpolation is a distinct global
weighted-mean baseline and is already represented by the IDW package.

## Implemented variant

This package uses local weighted least-squares quadratic fits with the
centre observation fixed as the intercept, nearest-neighbour fit radii,
Franke–Nielson-style compact blend weights, and rank-based linear/constant
fallbacks. It is intentionally labelled a variant rather than a reproduction
of QSHEP2D or NAG's exact implementation.

## Independent checks and limits

Tests recover a known quadratic surface, preserve exact node values, cover
unsupported regions, exercise a linear fallback and reject malformed or
degenerate data. Neighbour search is brute force. External comparison against
QSHEP2D/NAG, broader Franke test functions and performance validation remain
open.

Bibliographic identity was checked against the ACM record for Shepard (1968),
the Wiley record for Franke and Nielson (1980), and NAG's method documentation.
The algorithm description is paraphrased; no source code, figures or
documentation text is reproduced. Source-compendium redistribution rights
remain unresolved.
