# Working examples

This directory contains runnable examples linked to the explanations in [the algorithm collection](../algorithms/).

An example should make one thing clear: is it demonstrating a library operation, or is it implementing a named method from first principles? State that distinction plainly.

Each implementation should state:
- the language and exact library versions;
- how to install dependencies and run it;
- expected output, including units and coordinate assumptions;
- tests and the edge cases they cover;
- coordinate reference system, units and precision policy where relevant;
- known limitations and what the example does not implement;
- a step-by-step walkthrough that explains the code, decisions and validation.

## Examples

### Photogrammetry and survey planning

- [Photogrammetric flight-design calculations](python/photogrammetric-flight-design/README.md): nadir GSD, image footprint and overlap-constrained line/exposure spacing.
- [OpenDroneMap processing and checkpoint QA](python/photogrammetry-odm/README.md): Docker-based ODM runner plus independent 3D checkpoint residual statistics, with standard-library tests.

### Compositional statistics

- [Compositional data geometry](python/compositional-data/README.md): closure, explicit multiplicative zero replacement, CLR and Aitchison distance.

### Moving objects

- [Moving-object prediction](python/moving-object-prediction/README.md): constant-velocity prediction, uncertainty-aware predictive range queries and dead-reckoning update policy with reference tests.


### Statistical surveillance

- [Syndromic surveillance](python/syndromic-surveillance/README.md): two-sided tabular CUSUM and explicit EARS-style C1/C2/C3 count-series detectors, with lagged baselines, validation and reference tests.


### Forecast verification

- [Low-dimensional spatial data assimilation](python/spatial-data-assimilation/README.md): periodic upwind-advection/diffusion state propagation, point-sensor interpolation, sequential linear-Gaussian forecast-analysis cycling, Joseph covariance updates and free forecasts, with independent tests and a [step-by-step walkthrough](python/spatial-data-assimilation/implementation-walkthrough.md).
- [Binary-event forecast verification](python/forecast-verification/README.md): contingency-table counts and scores, Brier score/skill, reliability bins and tied-rank ROC AUC, with tests and an [intern walkthrough](python/forecast-verification/implementation-walkthrough.md). A separate [Fractions Skill Score module](python/forecast-verification/spatial_fss.py) adds regular-grid neighbourhood verification, with a [scale lab](../notebooks/forecast-fractions-skill-score-lab.ipynb); CRPS, ensemble rank histograms, SAL and MODE remain open.

### Flow-based facility location

- [Flow-refueling location model](python/flow-refueling-location/README.md): exact subset solver for finite-range route feasibility, distinct from FCLM.

### Geometry and computational geometry

- [Curve construction](python/curves-smoothing/README.md): Chaikin corner cutting, Catmull–Rom interpolation and de Casteljau Bézier evaluation, with tests, an [intern walkthrough](python/curves-smoothing/implementation-walkthrough.md) and a [lab notebook](../notebooks/curves-smoothing-lab.ipynb). B-splines, NURBS, curve fitting and Kalman/RTS smoothing are separate open topics.

- [Line clipping](python/line-clipping/README.md): Cohen–Sutherland and Liang–Barsky rectangle clipping plus Cyrus–Beck convex-window clipping, with tests, an [intern walkthrough](python/line-clipping/implementation-walkthrough.md) and a [lab notebook](../notebooks/line-clipping-lab.ipynb).

- [Exact orientation predicate](python/exact-orientation/README.md): rational-arithmetic reference sign test for 2D orientation, including near-degenerate float regression tests and an [intern walkthrough](python/exact-orientation/implementation-walkthrough.md).\n- [Bowyer–Watson Delaunay triangulation](python/bowyer-watson/README.md): dependency-free incremental 2D cavity retriangulation with exact rational predicates, cocircular tie policy, seeded invariant tests and a walkthrough. This is an exact reference implementation, not adaptive expansion arithmetic; the [visual lab](../notebooks/exact-orientation-lab.ipynb) compares it with a naive determinant.

- [Polygon intersection with Python and Shapely](python/polygon-intersection/README.md): a library-backed overlay operation with nine tests and a [step-by-step walkthrough](python/polygon-intersection/implementation-walkthrough.md).
- [Point in polygon with Python](python/point-in-polygon/README.md): a transparent ray-crossing implementation with 12 tests and a [step-by-step walkthrough](python/point-in-polygon/implementation-walkthrough.md).
- [Segment intersection with Python](python/segment-intersection/README.md): exact integer orientation tests and rational intersection coordinates, with 11 tests and a [step-by-step walkthrough](python/segment-intersection/implementation-walkthrough.md).
- [Bentley–Ottmann with Python](python/bentley-ottmann/README.md): paired list-status and implicit-treap implementations, exact rational event coordinates, differential tests, an intern walkthrough and a reproducible benchmark.
- [Polygon validity with Shapely](python/polygon-validity/README.md): a read-only validity inspection and explicit make-valid workflow, with tests for invalid rings, holes, overlapping MultiPolygon components and repair outputs, plus a [step-by-step walkthrough](python/polygon-validity/implementation-walkthrough.md).

### Optimization and location science

- [Exact p-median](python/p-median/README.md): exhaustive small-instance facility-location solver with deterministic assignments, tests and an [intern walkthrough](python/p-median/implementation-walkthrough.md).
- [Capacitated p-median](python/capacitated-p-median/README.md): exact tiny-instance assignment solver with indivisible demand, scalar capacity constraints, tests and an [intern walkthrough](python/capacitated-p-median/implementation-walkthrough.md).
- [Deterministic backup coverage](python/backup-coverage/README.md): exact small-instance r-covering solver that requires multiple distinct selected facilities to reach demand.
- [MEXCLP expected coverage](python/mexclp/README.md): exact small-instance expected-coverage solver with equal, independent unit busy probabilities and possible co-location.
- [M/M/c queue metrics](python/mmc-queue/README.md): steady-state Erlang-C waiting and system metrics for one FCFS queue feeding identical parallel servers.
- [Two-step floating catchment area](python/two-step-fca/README.md): binary-catchment supply/demand accessibility measure with explicit impedance matrix semantics, tests and an [intern walkthrough](python/two-step-fca/implementation-walkthrough.md).
- [Discrete p-center](python/p-center/README.md): exact small-instance minimax facility-location solver.\n- [Exact p-dispersion](python/p-dispersion/README.md): exact small-instance max-min separation solver with deterministic tie handling, tests and an [intern walkthrough](python/p-dispersion/implementation-walkthrough.md).
- [Location set covering](python/set-covering/README.md): exact small-instance solver for minimum-cardinality coverage of every demand row.

### Geodesy and georeferencing
- [Geodetic, ECEF and local ENU](python/ecef-enu/README.md): convert between geodetic coordinates, Earth-centred Cartesian coordinates and a local tangent frame, with a published EPSG reference test.

- [Affine georeferencing](python/affine-georeferencing/README.md): least-squares six-parameter 2D transform from control points, rank checks, residual diagnostics, tests and an [intern walkthrough](python/affine-georeferencing/implementation-walkthrough.md).
- [Helmert seven-parameter transformation](python/helmert-7-parameter/README.md): NumPy Position Vector transformation in geocentric XYZ, validated against a published IOGP example, with inverse tests and an [intern walkthrough](python/helmert-7-parameter/implementation-walkthrough.md).

### Sequence models

- [Discrete HMM and Viterbi decoding](python/hmm-viterbi/README.md): log-space maximum-probability state-sequence decoding with validated probability tables, tests, an [intern walkthrough](python/hmm-viterbi/implementation-walkthrough.md) and a [lab notebook](../notebooks/hmm-viterbi-lab.ipynb).

### GeoAI and model validation

- [Masked patch selection and restoration](python/masked-autoencoding/README.md): NumPy-only MAE sequence masking mechanics, deterministic per-sample masks, inverse permutation, tests and an [intern walkthrough](python/masked-autoencoding/implementation-walkthrough.md). This is not a trained model.

- [Spatial block cross-validation](python/spatial-cross-validation/README.md): deterministic grid-block folds with optional distance buffering, explicit projected-coordinate assumptions, tests and an [intern walkthrough](python/spatial-cross-validation/implementation-walkthrough.md).

### Geostatistics and covariance

- [Inverse distance weighting](python/inverse-distance-weighting/README.md): dependency-free IDW prediction with tested exact-location and neighbourhood policies.

- [Stationary covariance functions](python/covariance-functions/README.md): five Euclidean covariance models, dense covariance matrices, eigenvalue diagnostics, tests and an [intern walkthrough](python/covariance-functions/implementation-walkthrough.md). The examples do not implement spherical or network covariance models.

- [Isotropic spherical covariance](python/spherical-covariance/README.md): a finite non-negative Legendre-series model on the unit two-sphere, coordinate conversion, covariance matrices, tests and an [intern walkthrough](python/spherical-covariance/implementation-walkthrough.md). This is a scalar isotropic S2 model, not ellipsoidal geodesy or network covariance.

### Graph and network statistics

- [Graph-spectral covariance](python/graph-spectral-covariance/README.md): positive-semidefinite covariance construction from an undirected graph Laplacian, heat-kernel spectral variances, tests and an [intern walkthrough](python/graph-spectral-covariance/implementation-walkthrough.md). It is not a directed flow-network or shortest-path stationary model.

### Remote sensing

- [Marine heatwave detection lab](../notebooks/marine-heatwave-detection-lab.ipynb): a visual synthetic daily series, event intervals, event metrics and missing-observation experiment.

- [NDVI](python/spectral-indices/README.md): NumPy-based Normalised Difference Vegetation Index with explicit NoData and quality-mask handling, tests and an [intern walkthrough](python/spectral-indices/implementation-walkthrough.md).

### Raster analysis

- [Rasterisation algorithms](python/rasterization/README.md): DDA, all-octant Bresenham, Wu anti-aliasing, closed-cell supercover and centre-sampled scanline polygon fill, with tests, an [intern walkthrough](python/rasterization/implementation-walkthrough.md) and a [lab notebook](../notebooks/rasterization-lab.ipynb).

- [Horn slope and aspect](python/terrain-derivatives/README.md): a NumPy implementation of 3×3 Horn derivatives, local analytical hillshade and topographic wetness index, with explicit units, sun-angle conventions, specific-area and slope-floor contracts, aspect convention, NoData policy, tests and an [intern walkthrough](python/terrain-derivatives/implementation-walkthrough.md).
- [Raster least-cost distance](python/cost-distance/README.md): multi-source Dijkstra on a weighted 4/8-neighbour grid, with explicit edge-cost integration, corner policy, NoData barriers, tests and an [intern walkthrough](python/cost-distance/implementation-walkthrough.md).
- [Raster resampling](python/raster-resampling/README.md): same-extent nearest-neighbour and bilinear interpolation, explicit NoData policies, tests and an [intern walkthrough](python/raster-resampling/implementation-walkthrough.md).
- [Zonal raster statistics](python/zonal-statistics/README.md): NoData-aware summaries by aligned integer zone labels, with explicit population standard deviation and empty-zone semantics, tests and an [intern walkthrough](python/zonal-statistics/implementation-walkthrough.md).
- [Raster connected components](python/raster-components/README.md): breadth-first labeling with 4/8-connectivity, explicit validity barriers, deterministic labels, tests and an [intern walkthrough](python/raster-components/implementation-walkthrough.md).
- [InfoNCE contrastive loss](python/info-nce/README.md): symmetric NT-Xent for paired embedding batches, with normalized cosine similarity, temperature scaling, stable log-sum-exp, tests and an [intern walkthrough](python/info-nce/implementation-walkthrough.md).
- [CRS coordinate transformation](python/crs-transform/README.md): a pyproj wrapper with explicit x/y axis order, finite-coordinate checks, round-trip tests and an [intern walkthrough](python/crs-transform/implementation-walkthrough.md).

- [Euclidean distance transform](python/raster-distance/README.md): a SciPy-backed exact Euclidean distance wrapper with anisotropic cell spacing, tests and an [intern walkthrough](python/raster-distance/implementation-walkthrough.md).
- [Focal raster statistics](python/focal-statistics/README.md): NoData-aware square-window means using value and count integral images, with tests and an [intern walkthrough](python/focal-statistics/implementation-walkthrough.md).
- [Priority-Flood](python/priority-flood/README.md): heap-based eight-neighbour DEM depression filling with explicit NoData boundary policy, fill-depth output, tests and an [intern walkthrough](python/priority-flood/implementation-walkthrough.md).
- [D8 flow direction](python/d8-flow/README.md): a tested strict steepest-descent raster method with ESRI direction codes, rectangular cell spacing and an [intern walkthrough](python/d8-flow/implementation-walkthrough.md).
- [D8 flow accumulation](python/d8-flow-accumulation/README.md): a topological O(n) accumulation routine with weighted contributions, explicit NoData/domain-exit policy, cycle detection, tests and an [intern walkthrough](python/d8-flow-accumulation/implementation-walkthrough.md).
- [Single-outlet watershed delineation](python/watershed-delineation/README.md): reverse-graph traversal with cycle validation, explicit outlet and boundary semantics, tests and an [intern walkthrough](python/watershed-delineation/implementation-walkthrough.md).
- [Strahler and Shreve stream order](python/stream-order/README.md): topological channel-network ordering with connected-mask validation, cycle detection, tests and an [intern walkthrough](python/stream-order/implementation-walkthrough.md).

### Geostatistics and interpolation

- [IDW and ordinary kriging](python/geostatistics/README.md): transparent IDW and a dense ordinary-kriging solver using a specified exponential variogram, with tests and an [intern walkthrough](python/geostatistics/implementation-walkthrough.md).

### Spatial clustering

- [DBSCAN](python/dbscan/README.md): a transparent O(n²) planar density-clustering baseline with deterministic border-point handling, tests and an [intern walkthrough](python/dbscan/implementation-walkthrough.md).

### Point-pattern analysis

- [Ripley's K and L](python/ripley-k/README.md): uncorrected planar pair-count summaries with explicit edge-effect limits, tests and an [intern walkthrough](python/ripley-k/implementation-walkthrough.md).
- [Clark–Evans nearest-neighbour index](python/clark-evans/README.md): chunked planar nearest-neighbour distances and a descriptive CSR ratio, with explicit edge-effect limits, tests and an [intern walkthrough](python/clark-evans/implementation-walkthrough.md).

- [Planar Gaussian KDE](python/point-pattern-kde/README.md): fixed-bandwidth intensity estimation with explicit units, bounds and edge-effect caveats, tests and an [intern walkthrough](python/point-pattern-kde/implementation-walkthrough.md).

### Decision support

- [TOPSIS](python/topsis/README.md): vector-normalised multi-criteria ranking with benefit/cost direction, ideal and anti-ideal distances, tests and an [intern walkthrough](python/topsis/implementation-walkthrough.md).
- [Ordered Weighted Averaging](python/owa/README.md): standard OWA and GIS weighted OWA with per-cell sorting, ORness, strict NoData semantics, tests and an [intern walkthrough](python/owa/implementation-walkthrough.md).
- [Boolean and fuzzy overlay](python/fuzzy-overlay/README.md): logical AND/OR and fuzzy min, product, max, probabilistic-sum and gamma operators, with strict NoData semantics, tests and an [intern walkthrough](python/fuzzy-overlay/implementation-walkthrough.md).
- [AHP priority weights](python/ahp-weights/README.md): principal-eigenvector priorities from a validated reciprocal comparison matrix, with consistency diagnostics, tests and an [intern walkthrough](python/ahp-weights/implementation-walkthrough.md).
- [Weighted linear combination](python/weighted-overlay/README.md): combine aligned, standardised raster criteria with relative weights and an explicit eligibility mask; includes strict NoData handling, tests, an [intern walkthrough](python/weighted-overlay/implementation-walkthrough.md) and an [interactive suitability lab](../notebooks/weighted-linear-combination-lab.ipynb).

### Spatial statistics

- [Global Moran's I in Python](python/global-morans-i/README.md): a dependency-free dense-matrix calculation, row-standardisation helper and 13 tests. It computes the statistic only; use a spatial statistics library for inference. Follow the [Global Moran's I walkthrough](python/global-morans-i/implementation-walkthrough.md).
- [Global Geary's C in Python](python/geary-c/README.md): a dependency-free dense-matrix calculation and 16 tests. It computes the statistic only; use a spatial statistics library for inference. Follow the [Geary's C walkthrough](python/geary-c/implementation-walkthrough.md).
- [Spatial econometrics](python/spatial-econometrics/README.md): classic OLS-based LM-lag/LM-error diagnostics, spatial lag 2SLS, concentrated Gaussian SAR/SEM maximum likelihood, spatial Durbin 2SLS, and exact dense-matrix SAR/SDM direct, indirect and total impact decomposition, with tests and an [implementation walkthrough](python/spatial-econometrics/implementation-walkthrough.md). These are scoped dense-matrix teaching estimators, not a full spatial econometrics estimation suite.

### Indexing and query processing

- [STR-packed R-tree in Python](python/str-packed-rtree/README.md): an immutable 2D bounding-box index using STR packing, checked against brute force across 300 entries and 60 query windows, with a [step-by-step walkthrough](python/str-packed-rtree/implementation-walkthrough.md).
- [Indexed spatial join with Shapely](python/spatial-join/README.md): filter-and-refine join using STRtree, with tests for predicate direction, boundaries, holes and brute-force equivalence, plus a [step-by-step walkthrough](python/spatial-join/implementation-walkthrough.md).
- [2D k-d tree in Python](python/kd-tree/README.md): a static median-built tree for exact planar Euclidean nearest-neighbour search, with brute-force differential tests and a [step-by-step walkthrough](python/kd-tree/implementation-walkthrough.md).
- [Point-region quadtree in Python](python/quadtree/README.md): a bucket PR quadtree for inclusive rectangular window queries, with explicit midpoint, root-boundary and stopping rules, brute-force differential tests and a [step-by-step walkthrough](python/quadtree/implementation-walkthrough.md).
- [Sutherland–Hodgman polygon clipping](python/polygon-clipping/README.md): a dependency-free convex-polygon intersection implementation, with explicit input limits, edge-case tests and a [step-by-step walkthrough](python/polygon-clipping/implementation-walkthrough.md).
- [Polygon overlay operations with Shapely](python/polygon-overlay/README.md): validated intersection, union, difference and symmetric difference, with topology and precision tests, an [intern walkthrough](python/polygon-overlay/implementation-walkthrough.md) and a [visual notebook](../notebooks/polygon-overlay-lab.ipynb).
- [Graham scan convex hull](python/convex-hull/README.md): a dependency-free convex hull implementation with duplicate, collinear and degenerate-input tests, an [intern walkthrough](python/convex-hull/implementation-walkthrough.md) and a [visual notebook](../notebooks/convex-hull-lab.ipynb).
- [Voronoi and Delaunay with SciPy](python/voronoi-delaunay/README.md): a validated Qhull-backed workflow with equidistance and empty-circumcircle tests, an [intern walkthrough](python/voronoi-delaunay/implementation-walkthrough.md) and a [visual notebook](../notebooks/voronoi-delaunay-lab.ipynb).
- [Coverage-aware polygon simplification](python/coverage-simplification/README.md): a Shapely/GEOS wrapper with input/output coverage validation and edge-matched fixtures.
- [Fixed-grid precision operations](python/precision-grid/README.md): explicit coordinate precision reduction and GEOS fixed-grid overlay, with tests that distinguish these operations from full snap rounding.
- [Clipper2 native offsetting in C#](clipper2-csharp/README.md): an integer-path implementation using the Clipper2 NuGet package, with an executable CI smoke test.
- [Shortest-path baselines](python/shortest-paths/README.md): Dijkstra, A*, bidirectional Dijkstra, directed ALT landmarks, Yen's k-shortest loopless paths, Bellman–Ford and Floyd–Warshall with tests.
- [Road-routing baselines](python/road-routing/README.md): edge-based turn restrictions, turn penalties and FIFO time-dependent earliest-arrival search.
- [Nonseparable space-time covariance](python/nonseparable-space-time-covariance/README.md): a Gneiting-class Euclidean space-time covariance implementation with tests, intern walkthrough and notebook.

## Automated checks

The [Python examples workflow](../.github/workflows/python-tests.yml) is configured to run the test suites for all eighty-three Python example packages and the Clipper2 C# smoke test, and execute all seventy-four learning notebooks on relevant pushes and pull requests, using Python 3.13. The Local Moran notebook uses PySAL's maintained implementation rather than presenting a new from-scratch implementation. The Bentley–Ottmann job also adds the sibling segment-intersection package to `PYTHONPATH`.

A successful automated run means the tests in the repository passed in that environment. It does not prove correctness for every possible geometry or make a restricted teaching implementation production-ready. Always read the input contract and limitations before adapting an example.

## How the examples fit together

The canonical lesson explains the problem and method. The implementation shows one concrete way to put it into practice. Tests make expected behaviour explicit. The walkthrough explains how the code is built and why. A notebook is added when changing values or inspecting intermediate results makes the idea easier to learn.

These are connected teaching materials, not interchangeable copies of the same explanation.

### Point patterns and disease mapping

- [Planar point-pattern summaries and circular Poisson scan](python/point-process/README.md): nearest-neighbour distances, homogeneous and inhomogeneous Ripley's K, finite-difference pair correlation, conditional-CSR quadrat testing and a centroid-based population-offset Poisson scan with conditional multinomial calibration.

### Multi-criteria routing

- [Pareto shortest paths](python/shortest-paths/README.md): nondominated source-to-target paths for finite graphs with nonnegative additive cost vectors, alongside the single-criterion shortest-path baselines.

### Computational geometry metrics

- [Hausdorff, discrete Fréchet and smallest enclosing circle](python/geometry-metrics/README.md): directed/symmetric sampled-point Hausdorff, order-sensitive discrete Fréchet and randomized Welzl minimum enclosing circle, rotating-calipers convex diameter, and polygon Polylabel pole-of-inaccessibility search, with tests and walkthrough.
- [Hausdorff, discrete Fréchet, smallest enclosing circle, convex diameter and Polylabel](python/geometry-metrics/README.md): directed/symmetric sampled-point Hausdorff, order-sensitive discrete Fréchet, randomized Welzl minimum circle, rotating-calipers convex diameter, polygon pole of inaccessibility and minimum-area oriented rectangle, with tests and walkthrough.


### Solar geometry

- [Solar geometry](python/solar-geometry/README.md): UTC-normalized solar position and top-of-atmosphere irradiance, with timezone and coordinate validation.


### Coastal optical retrieval

- [Stumpf bathymetry and OC4v4 chlorophyll](python/coastal-optical-retrieval/README.md): calibrated empirical satellite-derived depth and SeaWiFS-specific chlorophyll-a reference methods.


### DEM quality

- [DEM void filling](python/dem-void-fill/README.md): iterative IDW gap filling with explicit masks, neighbourhood controls and map-unit pixel dimensions.


### Image fusion

- [Brovey pan-sharpening](python/brovey-pansharpening/README.md): pure-Python component substitution with spectral-ratio preservation and explicit masking.


### Hydrologic routing

- [Muskingum channel routing](python/muskingum-routing/README.md): linear storage routing for equally spaced inflow hydrographs, with stability and storage tests.


### Open-channel hydraulics

- [Manning open-channel flow](python/manning-open-channel/README.md): trapezoidal/rectangular discharge and bracketed normal-depth inversion.


### Image segmentation

- [SLIC superpixels](python/slic-superpixels/README.md): feature-space/spatial clustering with local assignment and explicit connectivity limitations.


### Trend analysis

- [Mann-Kendall and Sen trend methods](python/mann-kendall-sen/README.md): tie-corrected monotonic trend testing and median pairwise slope with optional time coordinates.


### Small-area estimation

- [Fay-Herriot area-level model](python/fay-herriot/README.md): REML estimation of between-area variance, GLS fixed effects, empirical BLUP predictions and a qualified plug-in MSE approximation, with tests and an [implementation walkthrough](python/fay-herriot/implementation-walkthrough.md).


### Statistical downscaling

- [Quantile mapping and delta change](python/statistical-downscaling/README.md): empirical univariate quantile mapping and additive/multiplicative mean-change adjustment, with tests and an [implementation walkthrough](python/statistical-downscaling/implementation-walkthrough.md).


### Spatial microsimulation

- [Iterative proportional fitting](python/spatial-microsimulation/README.md): row/column raking with structural-zero preservation, convergence diagnostics, tests and an [implementation walkthrough](python/spatial-microsimulation/implementation-walkthrough.md).


### Time-series analysis

- [HANTS harmonic time-series fitting](python/hants-time-series/README.md): Fourier fitting with iterative low/high residual rejection and missing-value reconstruction, with tests and an [implementation walkthrough](python/hants-time-series/implementation-walkthrough.md).


### Matrix completion

- [Soft-Impute matrix completion](python/matrix-completion/README.md): dense low-rank SVD thresholding with observed-cell clamping, rank control, tests and an [implementation walkthrough](python/matrix-completion/implementation-walkthrough.md).


### Cloud and shadow quality masks

- [Landsat QA_PIXEL, Sentinel-2 SCL and cloud-probability masks](python/qa-cloud-masks/README.md): deterministic quality-layer interpretation with configurable clear-class handling, tests and an [implementation walkthrough](python/qa-cloud-masks/implementation-walkthrough.md).


### Districting and territory design

- [Polygon compactness metrics](python/districting-compactness/README.md): Polsby–Popper, Reock and Schwartzberg scores with a deterministic minimum enclosing circle, tests and an [implementation walkthrough](python/districting-compactness/implementation-walkthrough.md).


### Partitioning clustering

- [PAM k-medoids and CLARA](python/k-medoids/README.md): deterministic BUILD/SWAP medoid search and sample-based CLARA with full-data scoring, independent tests and an [implementation walkthrough](python/k-medoids/implementation-walkthrough.md).


### Remote sensing

- [Lee local-statistics speckle filter](python/lee-speckle-filter/README.md): a NumPy-only adaptive local-mean estimator with explicit noise variance, NaN handling, tests and scope limitations.


### Geodesy and location encoding
- [Open Location Code (Plus Codes)](python/open-location-code/README.md): full-code encoding and decoding with cell bounds, parameter validation and a known-coordinate fixture; short-code recovery is intentionally excluded.

### Remote sensing and fractional cover
- [Fractional-cover regression tree](python/fractional-cover/README.md): deterministic CART regression for field-labelled fractions, with independent tests and explicit spatial-validation limitations.

### Photogrammetry
- [Brown-Conrady lens model](python/brown-conrady/README.md): normalized-coordinate radial/tangential distortion and checked Newton inversion; calibration estimation remains out of scope.

- [Progressive morphological ground filter](python/progressive-morphological-filter/README.md): rasterised point-cloud ground classification with progressive window and threshold schedule.

- [RANSAC plane fitting](python/ransac-plane-fitting/README.md): robust single-plane point-cloud fitting with deterministic seeds and inlier diagnostics.

- [CHM watershed crowns](python/chm-watershed-crowns/README.md): deterministic local-maximum seeding and marker-controlled canopy watershed.

- [Marching cubes](python/marching-cubes/README.md): scikit-image Lewiner integration with explicit voxel spacing and origin.

- [Thermal hotspot screening](python/thermal-hotspot-detection/README.md): robust local-context anomaly screening with NaN-aware median/MAD diagnostics.

- [Point-cloud voxelization](python/point-cloud-voxelization/README.md): sparse voxel keys, point mappings, counts, centroids and coordinate extrema.

- [Vecchia GP approximation](python/vecchia-approximation/README.md): nearest-predecessor conditional likelihood with a squared-exponential covariance baseline.

- [Knox space-time test](python/knox-test/README.md): reproducible permutation inference for close-in-space/close-in-time event pairs.


### Domain modeling

- [Spatial cellular automata and Schelling simulation](python/spatial-simulation/README.md): synchronous binary B/S rules, seeded Schelling relocation, site percolation, stochastic forest-fire dynamics, spatial preferential attachment, Watts–Strogatz small-world graphs a discrete-time network SIR model and a first-order categorical Markov land-change baseline, with independent tests and a [walkthrough](python/spatial-simulation/implementation-walkthrough.md).

- [Matrix factorizations: LU, QR, Cholesky and SVD](python/matrix-factorizations/README.md): reproducible NumPy/SciPy examples comparing pivoted LU, QR least squares, Cholesky covariance whitening and SVD/PCA, with tests. An [integrated synthetic spatial case](python/matrix-factorizations/integrated-case.md) connects affine control, terrain-plane estimation, correlated-error GLS and SVD diagnostics. A companion [learner exercise with worked solution](python/matrix-factorizations/integrated-case-exercise.md) turns it into a staged practical assessment.

### 3D geometry

- [Möller–Trumbore ray/triangle intersection](python/ray-triangle-intersection/README.md): dependency-free reference implementation, independent edge/degeneracy/culling tests and a walkthrough.


### Design-based map accuracy

- [Area-adjusted map accuracy](python/area-adjusted-accuracy/README.md): mapped-class-stratified simple-random-sample estimators for area-proportion error matrices, overall/user's/producer's accuracy, reference-class area and approximate uncertainty. Not a general unequal-probability or spatial sampling engine.


### Hydrographic surveying and sounding geometry

- [Layered-water-column acoustic ray tracing](python/hydrographic-ray-tracing/README.md): a bounded two-dimensional Snell-law forward model through piecewise-constant sound-speed layers.
- [Hydrographic sounding geometry and local Jacobian](python/hydrographic-sounding-geometry/README.md): navigation-frame sounding-point transform and an explicitly conventioned small-attitude-error Jacobian; not a full vessel or sonar model.
- [Covariance propagation](python/uncertainty-propagation/README.md): generic first-order joint-covariance propagation and independent-uniform Monte Carlo/Sobol baselines.
