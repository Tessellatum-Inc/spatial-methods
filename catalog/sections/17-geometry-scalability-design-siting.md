# Section 17 — Additions: geometry II, scalable computation, design, siting, implementations

- **Original source section:** 17
- **Source pages:** 35–37
- **Source transcription:** [pages 31–35](../../source-inventory/pages-31-35.md) and [pages 36–40](../../source-inventory/pages-36-40.md)
- **Review state:** source entries extracted into this index; not every entry independently verified
- **Current canonical records:** [Stable matching](../../algorithms/networks/stable-matching.md) with resident-proposing deferred acceptance (partial coverage of the matching/allocation family); [Huff competitive facility choice](../../algorithms/spatial-interaction/huff-competitive-location.md), a probabilistic attractiveness/impedance market-share model; [FFT-grid KDE](../../algorithms/statistics/fft-grid-kde.md), a tested binned Gaussian KDE with FFT convolution; mesh smoothing, indexed half-edge topology, conservative triangle-mesh cleanup, local isotropic-style remeshing, winged-edge and quad-edge (partial coverage of the source mesh-processing family), plus tested HyperLogLog, Count-Min, Bloom-filter and reservoir-sampling sketches; space-filling LHS/maximin and k-means coverage, plus exact/greedy FCLM, are now implemented; ball pivoting remains outstanding

This section extends computational geometry and adds scalable statistics, fast density methods, sampling design, 3D data formats, competitive location, charging infrastructure, surveillance and a representative implementation map.

## Computational geometry II

| Source entry | Provisional kind | Source page | Verification status |
|---|---|---:|--- |
| Voronoi variants: weighted (additively and multiplicatively weighted, Apollonius), order-k, farthest-point, line-segment Voronoi | Voronoi diagram variants | 35 | Not checked — intake only |
| Triangulation variants: regular triangulation, alpha complexes, 3D Delaunay refinement and tetrahedralization (TetGen-style) | Triangulation and mesh-generation methods | 35 | Partially implemented: polygon-boundary constrained Delaunay triangulation uses exact-predicate Lawson flips over an ear-clipping seed; a separate entry point now enforces non-crossing interior diagonals between existing normalized vertices by splitting the polygon into pieces; no holes, arbitrary segment recovery, Steiner points or quality refinement; regular triangulation, alpha complexes and 3D Delaunay refinement/tetrahedralization remain outstanding |
| Polygon decomposition: Seidel and Chazelle triangulation, monotone partition, Hertel-Mehlhorn, optimal convex partition | Polygon triangulation and decomposition algorithms | 35 | Partially implemented: exact-predicate y-monotone partition sweep handles start/end/split/merge/regular vertices and feeds a stack triangulator; current list-based sweep status is O(n^2), requires distinct vertex y-values, rejects consecutive collinear event triples, and has no holes/horizontal-event handling; a single-pass Hertel-Mehlhorn-style diagonal-removal routine now follows ear clipping, but the seed remains O(n^3) and the specialized linear-time post-process / approximation guarantee are not yet certified; Seidel/Chazelle and optimal convex partition remain outstanding |
| Boolean operations: Martinez-Rueda polygon clipping, 3D mesh Booleans; watchman route problem | Polygon and mesh Boolean operations / visibility path problem | 35 | Partially implemented: Greiner–Hormann intersection for simple rings and GEOS-backed overlay exist; a separate Weiler–Atherton simple-ring intersection baseline now handles concave/disconnected outputs with explicit touch/collinear limitations; a staged Martinez–Rueda baseline now discovers/splits cross-source intersections, classifies fragments for intersection/union/difference/XOR and stitches closed oriented rings (including disconnected components and containment-difference hole rings); an augmented y-interval treap sweep-status broad phase now prunes y-disjoint pairs (dense cases remain quadratic), full neighbour-ordered sweep scheduling, multiple independent shells per input and explicit Polygon/MultiPolygon shell-hole grouping remain outstanding; 3D BSP CSG union/intersection/difference now have a teaching implementation for closed convex planar polygon soups, with floating tolerance and no robust manifold repair; generalized triangle-mesh Booleans remain outstanding |
| Approximate geometry: geometric hashing, BBD-trees for approximate nearest neighbor, coresets for k-means | Geometric hashing / spatial index / approximation methods | 35 | Not checked — intake only |
| Mesh processing: Laplacian and Taubin smoothing, remeshing, mesh repair, ball pivoting, half-edge, winged-edge and quad-edge data structures | Mesh-processing algorithms / mesh data structures | 35 | Partially implemented: uniform Laplacian and Taubin smoothing, indexed triangular half-edge topology, conservative triangle cleanup/orientation repair, local split-collapse-flip remeshing with tangential relaxation, static winged-edge polygon topology and Guibas–Stolfi quad-edge primitives have code and authored tests; hole filling, ball pivoting, feature-aware remeshing and production geometric predicates remain outstanding |

## Scalable computation for spatial statistics

| Source entry | Provisional kind | Source page | Verification status |
|---|---|---:|--- |
| Log-determinant approximation: Chebyshev, Monte Carlo trace estimators, Lanczos, Pace-Barry, sparse Cholesky | Numerical approximation / sparse matrix methods | 35 | Not checked — intake only |
| Gaussian Markov random field sampling, conjugate gradient solvers, Kronecker-structured covariances, circulant embedding with FFT on regular grids | Spatial stochastic simulation / numerical solvers / covariance structures | 35 | Not checked — intake only |
| Sparse GP methods: inducing points, SVGP, Nystrom, structured kernel interpolation (KISS-GP), random Fourier features, hierarchical matrices, fast multipole | Scalable Gaussian-process approximations | 35 | Not checked — intake only |
| Variogram estimation: Matheron, Cressie-Hawkins and Genton robust estimators, REML, composite likelihood, cross-validation-based fitting | Variogram estimators / model-fitting methods | 35 | Partially implemented: Matheron, Cressie-Hawkins, Dowd and Genton Q_n empirical estimators, directional bins, spherical/exponential/Gaussian/Matérn covariance models, bounded weighted nonlinear least-squares fitting, dense constant-mean REML, fixed geometric anisotropy and bounded joint anisotropy estimation are tested; composite likelihood, cross-validation-based fitting, nested structures, Matérn smoothness estimation, prediction uncertainty and source-entry verification remain open |

## Fast density and sketching

| Source entry | Provisional kind | Source page | Verification status |
|---|---|---:|--- |
| Fast KDE: binned KDE with FFT, dual-tree KDE, random Fourier feature KDE, quantized and grid-based DBSCAN | Scalable density estimation / clustering | 35 | Partially implemented: weighted binned Gaussian KDE with FFT convolution and optional boundary correction is tested; dual-tree/RFF KDE and grid DBSCAN remain open |
| Streaming sketches for grids and tiles: HyperLogLog for distinct counts, count-min sketch, Bloom filters for tile existence, reservoir sampling for spatial streams | Streaming summaries / probabilistic data structures / sampling | 35 | Implemented as four tested bounded-memory reference structures; spatial partitioning, distributed merge/workload evaluation and exact-record integration remain open |

## Optimal sampling and experimental design

| Source entry | Provisional kind | Source page | Verification status |
|---|---|---:|--- |
| Space-filling designs: maximin, coffee-house, spatial coverage design (k-means based), Latin hypercube | Spatial sampling and experimental design | 35 | Partially implemented: Latin hypercube, centered LHS, multi-start normalized maximin LHS and deterministic k-means coverage have code and tests; coffee-house design remains unresolved because the source gives no reproducible definition |
| Model-based design: kriging variance minimization, Bayesian optimal design, sequential and adaptive designs, mutual information sensor selection (submodular greedy) | Model-based and adaptive experimental design | 36 | Partially implemented: tested Gaussian-process mutual-information (log-determinant) and greedy kriging-variance (trace-reduction) sensor selectors support target/candidate covariance and independent observation noise; Bayesian optimal design and broader adaptive path planning remain open |
| Robotic sampling: adaptive sampling with AUVs and drones, informative path planning | Mobile sensing / robotic path planning | 36 | Not checked — intake only |

## 3D formats and level-of-detail

| Source entry | Provisional kind | Source page | Verification status |
|---|---|---:|--- |
| Point cloud storage: LAZ compression, COPC, Entwine EPT, Potree octrees | Point-cloud formats / storage and indexing systems | 36 | Not checked — intake only |
| City and terrain streaming: OGC 3D Tiles with screen-space-error refinement, I3S, quantized-mesh terrain, CityGML levels of detail (LoD0 to LoD3) | 3D geospatial formats / streaming and LOD methods | 36 | Not checked — intake only |
| Data models: Simple Features, arc-node topology, TIN model, TopoJSON, GeoSPARQL | Data models / standards and encodings | 36 | Not checked — intake only |

## Competitive location and matching

| Source entry | Provisional kind | Source page | Verification status |
|---|---|---:|--- |
| Competitive facility location: Huff-based, Stackelberg and Nash formulations, Voronoi games | Competitive location models / game-theoretic formulations | 36 | Partially implemented: Huff attractiveness/impedance probabilities and demand aggregation are tested; Stackelberg/Nash competition and Voronoi games remain open |
| Stable matching (Gale-Shapley), auction algorithms, school choice and spatial assignment with preferences | Matching and assignment algorithms / allocation problems | 36 | Partially implemented: resident-proposing many-to-one deferred acceptance with incomplete strict preferences, capacities and a blocking-pair audit is tested; ties, couples, auctions and other preference-allocation models remain open |

## EV charging and refueling siting

| Source entry | Provisional kind | Source page | Verification status |
|---|---|---:|--- |
| Flow-capturing location model (FCLM), flow-refueling location model (FRLM), charging demand estimation from trajectories | Flow-based facility location / demand estimation | 36 | Partially implemented: exact and greedy FCLM plus an exact small-instance [FRLM range-feasibility solver](../../implementations/python/flow-refueling-location/README.md) are tested against deterministic and seeded randomized subset oracles; see the [FRLM source-verification record](../verification/flow-refueling-location.md). Trajectory-derived charging demand and scalable FRLM heuristics remain outstanding |
| Charging coverage with queuing, grid-capacity-aware siting, hydrogen station siting, V2G scheduling | Infrastructure siting / queueing and energy scheduling | 36 | Not checked — intake only |

## Surveillance and anomaly detection

| Source entry | Provisional kind | Source page | Verification status |
|---|---|---:|--- |
| Syndromic surveillance: CUSUM, EARS, Farrington, spatial and space-time variants | Surveillance and outbreak detection methods | 36 | Partially implemented: two-sided tabular CUSUM and an explicitly specified EARS-style C1/C2/C3 count-series detector have tests; Farrington, seasonality/covariates, spatial and space-time variants remain outstanding |
| Event detection from sensor networks, graph-based anomaly detection, spatial scan on counts with covariates | Event and anomaly detection methods | 36 | Not checked — intake only |

## Infrastructure and land-use mapping from imagery

| Source entry | Provisional kind | Source page | Verification status |
|---|---|---:|--- |
| Solar farm and wind turbine detection, hydropower and mine detection, illegal mining mapping | Infrastructure and land-use detection workflows | 36 | Not checked — intake only |
| Aquaculture ponds, greenhouses, rice paddies (SAR phenology), oil palm and tree crop mapping, shade coffee and agroforestry mapping | Agricultural and land-use mapping workflows | 36 | Not checked — intake only |
| Building age, roof material and building height estimation from imagery and shadows | Building attribute estimation methods | 36 | Not checked — intake only |

## Implementation map (representative libraries)

The source lists software families, not algorithms. Treat this as an orientation list, then verify current project status, supported formats, licences and maintenance before recommending a tool.

| Area | Source-listed implementations | Source page |
|---|---|---:|
| Geometry and indexing | GEOS, JTS, Shapely, S2, H3, libspatialindex | 36 |
| Projections and IO | PROJ, GDAL, Rasterio, Fiona, GeoPandas, xarray, rioxarray | 36 |
| Spatial statistics | PySAL, spdep, spatialreg, mgcv, INLA, gstat, scikit-gstat | 36–37 |
| Networks and routing | OSMnx, NetworkX, igraph, pgRouting, OSRM, Valhalla, GraphHopper, OpenTripPlanner, R5, momepy | 37 |
| Mobility | scikit-mobility, MovingPandas, Traja | 37 |
| Remote sensing and EO ML | SNAP, Orfeo Toolbox, eo-learn, TorchGeo, Terratorch, Raster Vision, Google Earth Engine, openEO | 37 |
| Terrain and hydrology | WhiteboxTools, GRASS, SAGA, TauDEM, pysheds | 37 |
| Big data | Apache Sedona, GeoMesa, cuSpatial, Dask-GeoPandas, DuckDB spatial | 37 |

## Decisions for the next pass

1. Distinguish mathematical algorithms from data structures, standards, formats and libraries.
2. Verify complexity and numerical assumptions for scalable methods before making performance claims.
3. For adaptive sampling, define the objective, observation cost and stopping condition.
4. For siting, record demand, network, capacity and equity constraints.
5. Treat the implementation map as a dated software landscape, not a permanent endorsement list.


### Streaming-sketch implementation update

The new package supplies HyperLogLog cardinality estimation, Count-Min frequency estimation, Bloom membership screening and Algorithm R reservoir sampling. These are generic streaming summaries suitable for tile/feature keys; they do not preserve geometries or source records.


### Fast KDE implementation update

The FFT-grid KDE package adds weighted point binning, truncated Gaussian convolution, density scaling and optional discrete boundary correction. It is an approximate regular-grid estimator; dual-tree KDE, adaptive bandwidths and distributed implementations remain open.
