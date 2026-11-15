# Multiple-flow-direction (MFD) routing on a raster DEM

Stable ID: SA-RASTER-MFD-FLOW-ROUTING · Draft 0.1 · Source compendium section 4

## Why multiple flow directions?

D8 assigns all flow from a cell to one steepest downslope neighbour. On hillslopes this can create artificial concentration along grid-aligned paths. Multiple-flow-direction (MFD) methods allow a cell's contribution to diverge among several lower neighbours. This lesson implements a transparent power-law MFD variant in the Freeman/Holmgren family.

## Power-law flow fractions

For a cell i and each strictly lower valid neighbour j, calculate the positive slope gradient

\[
s_{ij}=\frac{z_i-z_j}{d_{ij}},
\qquad
d_{ij}=\sqrt{(\Delta r\,s_r)^2+(\Delta c\,s_c)^2}.
\]

The unnormalised weight is \(s_{ij}^{p}\), where p is the convergence exponent. Normalise over all lower neighbours:

\[
w_{ij}=\frac{s_{ij}^{p}}{\sum_{k\in L(i)}s_{ik}^{p}}.
\]

The weights sum to one for a cell with at least one lower neighbour. A cell with no strictly lower neighbour is a sink and has zero outgoing weights. Larger p concentrates flow toward steeper neighbours; smaller p spreads it more evenly. The implementation uses p=1.1 by default but exposes it as a parameter.

The eight flow-weight channels are ordered E, SE, S, SW, W, NW, N, NE. Row spacing and column spacing are separate, and elevations must use compatible vertical units.

## Flow accumulation

Given an initial contribution \(c_i\), accumulation satisfies

\[
A_i=c_i+\sum_{j\rightarrow i}A_jw_{ji}.
\]

All edges are strictly downhill, so the flow graph is a directed acyclic graph. The implementation validates that every positive weight points to a valid lower neighbour, computes indegrees, then uses Kahn's topological traversal to process upstream cells before downstream cells. Runtime is O(N) for a fixed eight-neighbour grid. The default initial contribution is one unit per valid cell; pass a raster of cell areas to accumulate physical area.

## Boundaries and limitations

- Non-finite elevations, an explicit validity mask and a NoData sentinel define invalid cells.
- Invalid cells have zero outgoing weights and NaN accumulation.
- No flat resolution, depression filling, sink breaching, contour-length correction or edge renormalisation is performed.
- The implementation is a power-law MFD variant, not D-infinity, Qin's adaptive MFD, or a full reproduction of every Freeman/SAGA option.
- MFD's divergent routing can produce more dispersed flow than D8; the exponent changes this convergence/dispersion trade-off.
- It does not calculate stream networks, watershed labels, sediment transport or dynamic surface-water depth.

## References

- Freeman, T. G. (1991). “Calculating catchment area with divergent flow based on a regular grid.” *Computers & Geosciences*, 17(3), 413–422. https://doi.org/10.1016/0098-3004(91)90048-I.
- Holmgren, P. (1994). “Multiple flow direction algorithms for runoff modelling in grid based elevation models: an empirical evaluation.” *Hydrological Processes*, 8(4), 327–334. https://doi.org/10.1002/hyp.3360080405.
- SAGA GIS documentation describes the Freeman MFD convergence factor and distinguishes it from D8 and D-infinity: https://saga-gis.sourceforge.io/saga_tool_doc/9.11.2/ta_hydrology_1.html.

## Interactive lab

Work through the [MFD flow-routing notebook](../../notebooks/mfd-flow-routing-lab.ipynb) to inspect flow fractions, compare convergence exponents, and verify sink-level conservation.

## Exercises

1. On a two-neighbour slope, calculate the fractions for p=1 and p=2.
2. Explain how rectangular cell dimensions change slope weights.
3. Verify that the sum of sink accumulations equals the total initial contribution.
4. Compare D8 and MFD on a synthetic cone. What changes as p increases?
5. Why should flats and depressions be conditioned before interpreting a drainage network?
