# Verification record — D-infinity flow routing

## Identity and bibliography

Tarboton, D. G. (1997). “A new method for the determination of flow
directions and upslope areas in grid digital elevation models.”
*Water Resources Research*, 33(2), 309–319.
https://doi.org/10.1029/96WR03137

The reference identifies the triangular-facet D-infinity method. This record
does not claim that every edge, tie, sink or flat convention in the teaching
implementation is identical to a particular GIS vendor's implementation.

## Technical claims and assumptions

The method fits a planar gradient to each triangular facet formed by the
centre cell and two adjacent neighbours. A downslope aspect inside a facet is
partitioned between its bounding directions by angular position; when the
aspect falls outside, a downhill facet edge is considered. The steepest
candidate is retained. Horizontal cell dimensions are explicit and may be
anisotropic. Elevation and horizontal distance units must be compatible.

## Implementation and reproduction

Implemented in `implementations/python/d8-flow/dinf_flow.py`:

- Eight triangular facets, with clockwise E, SE, S, SW, W, NW, N, NE channels.
- Angular two-neighbour partition for an in-facet downslope aspect.
- Steepest downhill edge handling outside a facet and beside incomplete
  facets, NoData and raster boundaries.
- Rectangular cell spacing, validity masks and explicit NoData values.
- Zero outflow for sinks, flats and invalid cells.
- Compatibility with the repository's topological weighted accumulation
  routine, without conflating D-infinity with power-law MFD.

The independent unit suite includes an analytic planar-gradient partition,
elevation-offset invariance, anisotropic cells, strict downhill and
unit-sum invariants, sink/flat/NoData cases, a one-row and singleton raster,
a seeded random DEM invariant check, invalid input checks and accumulation
conservation.

## Known gaps

- No depression filling, breaching or flat resolution.
- No geographic-coordinate/geodesic cell geometry.
- No explicit comparison against TauDEM, WhiteboxTools, GRASS GIS or another
  independent implementation.
- No benchmark or large-raster performance claim.
- No source-entry review or rights review is implied by this algorithm record.

## Rights

This record paraphrases the published method and cites its bibliographic
identity. It does not reproduce the paper's text, figures, datasets or code.
