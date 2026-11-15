# D-infinity flow direction and accumulation

Stable ID: SA-RASTER-D-INFINITY · Draft 0.1 · Source compendium section 4

## From eight directions to a continuous direction

D8 sends all flow to one of eight neighbours. Power-law multiple-flow
direction sends flow to every lower neighbour. D-infinity (D∞), introduced by
Tarboton, estimates a continuous downslope angle and distributes flow to the
one or two adjacent raster directions that bracket it.

## Triangular facet calculation

For each of the eight facets formed by the centre cell and two adjacent
neighbours, fit a plane. Let the neighbour displacement vectors be v1 and v2
and their elevation differences from the centre be dz1 and dz2. Solve

\[
\nabla z\cdot v_1=dz_1,\qquad \nabla z\cdot v_2=dz_2.
\]

The steepest descent vector is \(-\nabla z\). If its direction lies within the
facet's angular sector, it is a candidate. If it falls outside, the feasible
facet-edge slopes are considered. The steepest feasible candidate over the
facets determines the direction.

## Angular flow partition

The selected continuous direction is bracketed by adjacent neighbour
directions. Flow is divided between them in proportion to angular distance.
A direction aligned with one neighbour sends all flow there; a sink has no
outgoing links. Each valid cell therefore has zero, one or two links, and
non-empty fractions sum to one.

The implementation accounts for separate horizontal and vertical cell sizes.
Every link is strictly downhill, so the resulting graph is acyclic. Weighted
accumulation uses a topological traversal:

\[
A_j=c_j+\sum_{i\to j}w_{ij}A_i.
\]

## Implementation and limits

The [Python package](../../implementations/python/d-infinity/README.md)
implements facet routing and accumulation. Tests include analytic planar
slopes, a half-angle split, sink and NoData behaviour, random DEM downhill
checks and total mass conservation.

This does not fill depressions, resolve flats, breach sinks, extract streams
or model dynamic water. DEM conditioning and consistent horizontal/vertical
units remain essential. Edge cells have fewer available facets and use
available lower-neighbour edge slopes as fallback.

## Reference

Tarboton, D. G. (1997). A new method for the determination of flow directions
and upslope areas in grid digital elevation models. Water Resources Research,
33(2), 309–319. https://doi.org/10.1029/96WR03137.
