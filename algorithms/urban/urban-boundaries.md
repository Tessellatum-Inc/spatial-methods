# Urban boundaries and natural cities

## Building-centroid DBSCAN

Each building centroid is a point in a projected coordinate system. DBSCAN connects points within radius \(\varepsilon\) and retains only components with at least the minimum number of observations. Noise receives label -1. This delineates dense building clusters, not a legal city boundary.

## Density-grid components

Building counts are aggregated into axis-aligned cells. Cells meeting a declared minimum count are labelled using 4- or 8-neighbour connectivity; components below a minimum cell count are removed. This is a transparent connected-component baseline for rasterized urban density.

## Head/tail natural-city threshold

For positive cell densities, the head/tail procedure repeatedly computes the mean of the current tail and retains values above it while the head fraction remains below a caller-defined limit. Cells above the final threshold form natural-city candidates. The stopping rule and raster resolution are explicit modelling choices, not universal constants.

## Verification and limitations

Tests compare building DBSCAN with a two-cluster/noise fixture, grid counts with a direct histogram oracle, connected-component behaviour under 4/8 connectivity, and head/tail edge cases. These methods do not reproduce every City Clustering Algorithm variant, stochastic percolation, functional commuting regions or authoritative administrative delineations.

See the [implementation package](../../implementations/python/urban-boundaries/README.md).
