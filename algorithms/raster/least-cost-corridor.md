# Least-cost corridors on raster cost surfaces

A least-cost path is not always the only useful output. A corridor identifies cells that lie on, or close in accumulated cost to, an optimal source-to-destination route.

Let (D_s(x)) be accumulated cost from source (s) to cell (x), and (D_t(x)) cost from (x) to destination (t). With non-negative symmetric edge costs, the optimal path cost is (D_s(t)). For an additive tolerance \(\delta\), the corridor is

\[
C_\delta=\{x:D_s(x)+D_t(x)\leq D_s(t)+\delta\}.
\]

The implementation computes the two distance surfaces with the existing raster Dijkstra solver and returns the intermediate surfaces and Boolean corridor mask. At zero tolerance, only cells that participate in an optimal route are retained; positive tolerance expands the set to near-optimal alternatives.

## Assumptions and limits

- The graph is the package's 4- or 8-neighbour raster graph.
- Edge cost is the arithmetic mean of endpoint cost densities times physical step length.
- Costs are non-negative and symmetric; directional travel-time models require a directed reverse-cost solver instead.
- Non-finite cells are barriers; diagonal corner cutting follows the selected solver option.
- The additive tolerance uses the same units as accumulated cost.
- The result is not a probability of route use, confidence interval, continuous buffer or ecological least-cost corridor model with multiple resistance assumptions.

## Verification

The test suite checks a unique shortest path, monotonic corridor expansion, NoData barriers, unreachable destinations and an independent exhaustive simple-path oracle on a small grid.

See [the cost-distance implementation](../../implementations/python/cost-distance/README.md).
