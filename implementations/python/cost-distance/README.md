# Raster least-cost distance

This implementation runs multi-source Dijkstra on a regular raster grid. Each valid cell stores a non-negative cost per horizontal distance unit. All non-finite cells (NaN and positive/negative infinity) are barriers.

For adjacent cells u and v, the edge cost is the mean endpoint cost multiplied by the physical step length:

$$w(u,v)=\frac{c(u)+c(v)}{2}\,\ell(u,v)$$

The source cells start at accumulated cost zero. Their cell cost is not charged.

## Install and test

~~~bash
python -m pip install -r requirements.txt
python -m pytest -q
~~~

## Contract

- 4- or 8-neighbour connectivity.
- Rectangular cell spacing is supported; diagonal step length uses the Euclidean hypotenuse.
- Diagonal movement can be prevented from squeezing between two blocked orthogonal neighbours.
- Multiple sources are supported; each cell receives the minimum accumulated cost from any source.
- NoData is a barrier. Valid but unreachable cells remain positive infinity.
- Cost values must be finite and non-negative on valid cells.
- This is a raster graph approximation, not a continuous fast-marching/Eikonal solver.
- The cost surface must have a defensible interpretation and units. The result is accumulated cost, not necessarily physical distance or travel time.

See the [canonical lesson](../../../algorithms/raster/cost-distance.md) and [intern walkthrough](implementation-walkthrough.md).


## Directional terrain travel-time models

The companion `terrain_travel.py` module adds Tobler's hiking function, Naismith's rule and Langmuir's descent correction, plus a directional multi-source Dijkstra accumulator over an elevation grid. Output units are seconds. Unlike the symmetric cost-surface routine above, each directed edge uses the elevation change from the current cell to the next cell. Non-finite elevation cells are barriers. The Langmuir correction is applied per raster edge and is therefore resolution-sensitive.


## Least-cost corridors

The `least_cost_corridor` function runs the same multi-source Dijkstra solver from the source and destination. A cell belongs to the corridor when its source-to-cell plus cell-to-destination accumulated cost is no greater than the optimum source-to-destination cost plus a caller-specified additive tolerance. The output includes both distance surfaces, their through-cost sum, the optimum and a Boolean corridor mask. The method inherits the package's raster connectivity, endpoint-averaged edge costs, cell spacing, NoData and corner-cutting rules. It is a graph-based corridor, not a probabilistic uncertainty surface or a continuous geometric buffer.
