# Source verification — power-law multiple-flow-direction routing

## Identity and bibliography
- Freeman, T. G. (1991). “Calculating catchment area with divergent flow based on a regular grid.” *Computers & Geosciences*, 17(3), 413–422. DOI 10.1016/0098-3004(91)90048-I.
- Holmgren, P. (1994). “Multiple flow direction algorithms for runoff modelling in grid based elevation models: an empirical evaluation.” *Hydrological Processes*, 8(4), 327–334. DOI 10.1002/hyp.3360080405.

## Technical claims
The implemented variant computes positive downhill slope gradients to all lower adjacent cells, raises each gradient to a user-supplied positive convergence exponent, and normalises the resulting weights. Flow accumulation is a weighted directed acyclic graph computation. The implementation uses a topological traversal and conserves the sum of initial contributions across terminal sinks when all cells are valid and all outgoing edges remain within the raster.

## Implementation/reproduction
Implemented: power-law MFD weights for eight neighbours; anisotropic row/column cell spacing; NoData and validity masks; zero-outflow sink representation; weighted initial contributions; validation of unit-sum fractions and strictly downhill edges; Kahn topological accumulation. Tests cover two-neighbour splitting, exponent response, anisotropic spacing, sink and NoData handling, weighted contributions, invalid graph inputs and random-DEM mass conservation.

Not implemented: D-infinity, Qin adaptive MFD, contour-length weighting, flat resolution, depression filling, sink breaching, dynamic flow depth, stream extraction or watershed delineation. This is a scoped Freeman/Holmgren-style power-law variant, not a claim to reproduce all options in SAGA or other hydrology software. Repository CI is required to establish passing status.

## Rights
Only published algorithmic concepts and bibliographic metadata are paraphrased; no source code or figures are reproduced.
