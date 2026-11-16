# OD flow clustering, line KDE and hotspots

Install and test:

```bash
python -m pip install -r requirements.txt
python -m pytest -q
```

- `functional_regions_from_flows`: reciprocal OD-flow weighted Louvain communities, optionally restricted to zone-neighbour edges. This is not Intramax, CURDS or Leiden.
- `cluster_od_flows`: DBSCAN in a four-dimensional feature space formed by separately scaled origin and destination coordinates. The distance scale is a modelling choice; it is not network distance.
- `line_flow_kde`: weighted Gaussian kernel density integrated along each straight OD segment using Gauss–Legendre quadrature. Grid coordinates and bandwidth share a projected coordinate unit. Chunking limits temporary memory.
- `flow_density_hotspots`: grid-local maxima above a chosen quantile threshold. This is descriptive extraction, not a statistical significance test.

The package does not implement network-constrained flow communities, network shortest-path KDE, adaptive bandwidths, edge correction, spatially varying uncertainty or inferential hotspot significance. Straight-line segments may cross barriers and should not be mistaken for actual routes.
