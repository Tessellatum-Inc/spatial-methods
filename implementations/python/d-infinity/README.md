# D-infinity raster flow routing

Dependency-free Tarboton-style D-infinity routing for rectangular-cell DEMs.
The implementation fits planes on the eight triangular facets formed by the
centre and adjacent neighbours, selects the steepest feasible downslope
direction, and divides flow between its two bracketing neighbours by angular
proportion. Each valid cell routes to zero, one or two strictly lower valid
neighbours.

The package also accumulates weighted contributions in topological order.
Default initial contribution is one per valid cell; custom non-negative
contributions are supported. Link validation checks downhill targets,
fraction sums and graph acyclicity.

Run pytest from this directory. Tests cover planar slopes, angular splitting,
NoData/sinks, weighted accumulation, conservation and random DEMs.

Scope: no depression filling, breaching, flat resolution, contour-length
correction, edge renormalisation, stream extraction or dynamic hydrology.
Use compatible horizontal and vertical units. This is a compact educational
implementation, not a reproduction of every D-infinity variant.
