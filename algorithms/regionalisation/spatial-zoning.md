# Spatially constrained zoning and scale effects

The reference method begins with one zone per spatial unit. At each step it merges an adjacent pair with minimum Ward increase

\[
\Delta SSE_{ab}=\frac{n_an_b}{n_a+n_b}
\left\|\bar{x}_a-\bar{x}_b\right\|^2.
\]

Only adjacency-graph neighbours are eligible, so each merged region remains contiguous when the starting units and graph are valid. The merge sequence can be stopped at a declared number of zones. The scale-effect utility reports within-zone sum of squares across multiple zone counts.

## Interpretation and limitations

This is a spatially constrained Ward agglomeration baseline. It is not AMOEBA, and a within-zone variance curve alone does not resolve the modifiable areal unit problem. Attribute scaling, spatial weights, contiguity, zone-count selection and boundary conditions materially affect results.

## Verification

Tests cover a line graph with two obvious clusters, direct within-zone SSE, monotonic scale curves, disconnected graphs and invalid inputs.

See the [implementation package](../../implementations/python/spatial-zoning/README.md).
