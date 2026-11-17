# D-infinity flow routing

- **Kind:** algorithm
- **Domain:** raster hydrology and terrain analysis
- **Status:** implemented as a teaching facet-routing method; independent GIS comparison pending
- **Version:** 0.1

## Why D-infinity?

D8 forces all flow from a cell into one of eight neighbours. Power-law MFD
splits flow among every lower neighbour using a chosen exponent. D-infinity
instead estimates a continuous downslope direction from triangular facets
around the cell and partitions flow between the two adjacent grid directions
that bound that aspect.

## Facet gradient

Let the centre elevation be (z_0), and let two adjacent neighbour centres
have local coordinates (v_1=(x_1,y_1)), (v_2=(x_2,y_2)) and elevations
(z_1,z_2). The planar facet gradient (g=(g_x,g_y)) solves

```text
gx*x1 + gy*y1 = z1-z0
gx*x2 + gy*y2 = z2-z0
```

The downslope vector is (-g). If its aspect lies within the angular sector
between the two neighbour rays, the implementation splits flow by angular
position. If the aspect is outside the facet, the steeper downhill facet edge
is considered. The best candidate is selected across the eight facets.

## Raster and NoData conventions

Direction channels are ordered E, SE, S, SW, W, NW, N, NE. Cell dimensions
are supplied as (row spacing, column spacing), so the local geometry accounts
for rectangular cells. A cell with no lower valid neighbour has zero outgoing
weights. Invalid cells also have zero weights. At incomplete facets near
NoData or raster edges, available downhill neighbour edges provide a fallback.

The resulting array has shape (rows, columns, 8). It is compatible with the
existing topological `mfd_flow_accumulation` routine because positive
fractions point strictly downhill and each active cell's weights sum to one.
This compatibility is an interface choice; D-infinity and power-law MFD are
different routing models.

## Limitations

The teaching implementation does not fill depressions, resolve flats, use
multiple-flow partitioning beyond the selected facet, or reproduce every
GIS vendor's edge and tie conventions. It uses floating-point facet
gradients and a deterministic clockwise candidate order. Elevation and
horizontal distance units must be compatible, and geographic longitude/
latitude grids should be projected or handled geodesically. The current
tests use analytic planar surfaces, edge/NoData cases, randomized DEM
invariants and accumulation conservation; comparison with an independent
GIS implementation remains outstanding.

## Runnable implementation

- [Python code and tests](../../implementations/python/d8-flow/dinf_flow.py)
- [Package README](../../implementations/python/d8-flow/README.md)
- [Verification record](../../catalog/verification/d-infinity-flow-routing.md)
- [D8/MFD lesson](d8-flow-direction.md)

## References

- Tarboton, D. G. (1997). A new method for the determination of flow
  directions and upslope areas in grid digital elevation models.
  *Water Resources Research*, 33(2), 309–319.
  https://doi.org/10.1029/96WR03137
