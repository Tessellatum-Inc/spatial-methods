# D-infinity flow routing

D-infinity (D∞) estimates a continuous downslope direction from triangular
facets formed by adjacent raster neighbours. A planar gradient is fitted from
the centre-cell elevation and two neighbour elevations. The negative gradient
defines the flow angle; flow is assigned to the two bounding neighbour
directions according to its angular position. When the direction lies outside
the facet, the steepest descending facet edge is used.

The tested implementation in implementations/python/advanced-flow-routing
provides rectangular cell spacing, NoData handling, receiver proportions and
topological flow accumulation. Angles are radians counter-clockwise from east
in a Cartesian east/north frame.

D∞ does not itself resolve depressions or flats. The implementation routes
only to strictly lower neighbours; use a documented depression-filling,
breaching and flat-resolution method before interpreting a full catchment
network. Validate against an independent GIS engine before operational use.
