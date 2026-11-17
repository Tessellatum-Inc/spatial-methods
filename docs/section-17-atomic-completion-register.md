# Section 17 atomic completion register

**Source:** *Spatial Analysis Algorithms: Complete Compendium*, Section 17, pages 35–37.  
**Intake:** [preserved pages 31–35 transcription](../source-inventory/pages-31-35.md) and [pages 36–40](../source-inventory/pages-36-40.md).  
**Section index:** [Section 17 catalogue record](../catalog/sections/17-geometry-scalability-design-siting.md).

> Source names and groupings require verification. This register expands each grouped source row into child records, but does not establish canonical identity, bibliographic support or implementation completeness.

## Status policy

Use the [verification protocol](../catalog/verification-protocol.md) and [completion standard](compendium-completion-standard.md). A teaching baseline or external library is evidence only for its documented scope. Standards, formats and software must not be mislabelled as algorithms.

| Status | Meaning |
|---|---|
| Open | No item-specific verification/implementation evidence recorded here. |
| Partial | A related, bounded implementation exists; remaining variants or validation are explicit. |
| Verify | Exact name, variant, version or primary source must be resolved. |
| Not applicable | A format, data structure, software or workflow is not a standalone algorithm. |

## Atomic source register

### Computational geometry II — page 35

| ID | Atomic item | Kind | Status | Required completion work |
|---|---|---|---|---|
| S17-CG-01 | Additively weighted Voronoi diagram | Voronoi variant | Open | Define site weights/distance function and admissible domains; test degeneracies and topology. |
| S17-CG-02 | Multiplicatively weighted Voronoi diagram | Voronoi variant | Open | Define weighted distance and Apollonius boundaries; distinguish from additive weighting. |
| S17-CG-03 | Apollonius diagram | Voronoi variant | Verify | Verify terminology and exact weighted-site model; derive/test cell boundaries. |
| S17-CG-04 | Order-k Voronoi diagram | Voronoi variant | Open | Define k-nearest-site regions and tie handling; compare with brute-force point classification. |
| S17-CG-05 | Farthest-point Voronoi diagram | Voronoi variant | Open | Define farthest-site cells and convex-hull restriction; test degeneracies. |
| S17-CG-06 | Line-segment Voronoi diagram | Voronoi variant | Open | Define segment distance and endpoint/interior cases; test topology and degeneracies. |
| S17-CG-07 | Regular triangulation | Weighted triangulation | Open | Define power distance/weights and lower-hull construction; verify predicates and degeneracies. |
| S17-CG-08 | Alpha complexes | Computational topology | Open | Define filtration parameter and relation to alpha shapes; test simplex inclusion and filtration nesting. |
| S17-CG-09 | 3D Delaunay refinement | Mesh generation | Open | Define quality criteria, insertion and termination; compare tetrahedral mesh quality. |
| S17-CG-10 | Tetrahedralization / TetGen-style meshing | Mesh-generation software/workflow | Verify | Identify TetGen version and supported PLC/quality options; document integration and licence. |
| S17-CG-11 | Seidel polygon triangulation | Polygon triangulation | Verify | Verify randomized incremental/trapezoidal decomposition variant; test complexity assumptions. |
| S17-CG-12 | Chazelle polygon triangulation | Polygon triangulation | Verify | Verify theoretical algorithm and practical scope; do not conflate with generic triangulation. |
| S17-CG-13 | Monotone polygon partition | Polygon decomposition | Partial | Existing sweep/stack baseline is bounded; resolve equal-y, horizontal, collinear and hole cases and complexity. |
| S17-CG-14 | Hertel–Mehlhorn convex decomposition | Approximate convex partition | Partial | Existing diagonal-removal baseline is bounded; verify approximation guarantee and required triangulation assumptions. |
| S17-CG-15 | Optimal convex partition | Polygon optimisation | Open | Define objective (number of pieces/diagonals), constraints and known complexity; identify exact method. |
| S17-CG-16 | Martinez–Rueda polygon clipping | Polygon Boolean algorithm | Partial | Existing staged baseline has limitations; verify original sweep event ordering, multi-shell grouping and robustness. |
| S17-CG-17 | 3D mesh Boolean operations | Mesh Boolean family | Partial | Existing BSP teaching kernel only supports closed convex planar polygon soups; general triangle mesh robustness/manifold repair remain open. |
| S17-CG-18 | Watchman route problem | Visibility/path-planning problem | Open | Define polygonal environment, visibility model and route objective; distinguish variants and approximation guarantees. |
| S17-CG-19 | Geometric hashing | Geometric matching method | Open | Identify target problem and hash invariants; test collision, invariance and retrieval quality. |
| S17-CG-20 | BBD-tree approximate nearest neighbour | Spatial data structure | Verify | Verify balanced box-decomposition definition and approximation bound; compare recall and query cost. |
| S17-CG-21 | k-means coresets | Approximation algorithm | Open | Define coreset objective and error guarantee; test weighted objective preservation. |
| S17-CG-22 | Laplacian mesh smoothing | Mesh processing | Partial | Existing uniform Laplacian baseline is tested; document shrinkage, boundary and cotangent variants. |
| S17-CG-23 | Taubin mesh smoothing | Mesh processing | Partial | Existing alternating-pass baseline is tested; verify lambda/mu conditions and spectral behaviour. |
| S17-CG-24 | Mesh remeshing | Mesh processing family | Partial | Existing local split/collapse/flip baseline is bounded; feature constraints, quality guarantees and convergence remain open. |
| S17-CG-25 | Mesh repair | Mesh processing family | Partial | Existing conservative triangle cleanup/orientation repair is limited; hole filling, self-intersections and manifold repair remain open. |
| S17-CG-26 | Ball-pivoting surface reconstruction | Point-cloud surface reconstruction | Open | Verify radius schedule and normal assumptions; test against known surfaces and sampling density. |
| S17-CG-27 | Half-edge data structure | Mesh topology structure | Partial | Existing indexed triangular half-edge implementation is tested; define invariants and mutation operations. |
| S17-CG-28 | Winged-edge data structure | Mesh topology structure | Partial | Existing static polygon topology is bounded; add mutation invariants and independent topology fixtures. |
| S17-CG-29 | Quad-edge data structure | Mesh topology structure | Partial | Existing Guibas–Stolfi primitives are bounded; verify operator algebra, orientation and subdivision invariants. |

### Scalable computation for spatial statistics — page 35

| ID | Atomic item | Kind | Status | Required completion work |
|---|---|---|---|---|
| S17-SC-01 | Chebyshev log-determinant approximation | Numerical approximation | Open | Define spectral interval and polynomial degree; test against exact small-matrix determinants. |
| S17-SC-02 | Monte Carlo trace estimators | Numerical approximation | Open | Define probe distribution and variance; test unbiasedness/convergence against exact trace. |
| S17-SC-03 | Lanczos log-determinant approximation | Krylov method | Open | Specify quadrature and reorthogonalisation; test positive-definite matrices and error bounds. |
| S17-SC-04 | Pace–Barry log-determinant approximation | Spatial econometrics method | Verify | Identify exact algorithm and model context; compare with sparse Cholesky on benchmark matrices. |
| S17-SC-05 | Sparse Cholesky factorisation | Sparse numerical linear algebra | Open | Define ordering/fill behaviour and positive-definite assumptions; test residual and determinant identities. |
| S17-SC-06 | Gaussian Markov random field sampling | Spatial stochastic simulation | Partial | Existing proper-CAR Gibbs and constrained ICAR baselines cover limited models; add exact small-graph comparisons and broader precision structures. |
| S17-SC-07 | Conjugate-gradient solvers | Iterative numerical solver | Open | Define SPD requirements, preconditioning and stopping tolerance; test residual/error and failure cases. |
| S17-SC-08 | Kronecker-structured covariance | Covariance structure/operator | Open | Define separability and factor ordering; test operator identities and solves against dense matrices. |
| S17-SC-09 | Circulant embedding with FFT | Gaussian field simulation | Open | Define embedding validity and positive definiteness; compare empirical covariance with target. |
| S17-SC-10 | Inducing-point sparse Gaussian processes | GP approximation | Open | Define inducing objective and placement; test predictive mean/variance against exact GP. |
| S17-SC-11 | Stochastic variational GP (SVGP) | GP approximation/inference | Verify | Identify canonical formulation and variational objective; document minibatch and likelihood assumptions. |
| S17-SC-12 | Nyström approximation | Kernel approximation | Open | Define landmark selection and rank; test spectral and predictive approximation errors. |
| S17-SC-13 | KISS-GP / structured kernel interpolation | GP approximation | Verify | Verify method and interpolation grid assumptions; test covariance approximation and scaling. |
| S17-SC-14 | Random Fourier features | Kernel approximation | Open | Define spectral sampling and feature scaling; test kernel approximation error across seeds. |
| S17-SC-15 | Hierarchical matrices | Structured matrix approximation | Open | Define admissibility, block tree and error control; test storage and solve accuracy. |
| S17-SC-16 | Fast multipole methods | Fast summation algorithm | Open | Identify kernel and expansion order; test error versus direct summation. |
| S17-SC-17 | Matheron variogram estimator | Empirical variogram | Partial | Existing estimator is implemented; verify binning, pair weighting and edge conventions. |
| S17-SC-18 | Cressie–Hawkins robust variogram estimator | Robust empirical variogram | Partial | Existing estimator is implemented; verify finite-sample correction and assumptions. |
| S17-SC-19 | Genton robust variogram estimator | Robust empirical variogram | Partial | Existing Qn-based baseline is implemented; verify exact estimator definition and scaling. |
| S17-SC-20 | Restricted maximum likelihood (REML) variogram fitting | Model estimation | Partial | Existing dense constant-mean REML is bounded; extend covariance structures, uncertainty and sparse scaling. |
| S17-SC-21 | Composite-likelihood variogram fitting | Model estimation | Open | Define pair/block likelihood and weighting; test consistency and standard errors. |
| S17-SC-22 | Cross-validation-based variogram fitting | Model selection | Open | Define spatial folds, scoring and dependence-aware validation; avoid random-fold leakage. |

### Fast density and sketching — page 35

| ID | Atomic item | Kind | Status | Required completion work |
|---|---|---|---|---|
| S17-FD-01 | Binned KDE with FFT convolution | Fast density estimator | Partial | Existing weighted Gaussian grid KDE is tested; document binning/convolution approximation and boundary correction. |
| S17-FD-02 | Dual-tree KDE | Fast density estimator | Open | Define tree bounds and approximation tolerance; compare with direct KDE. |
| S17-FD-03 | Random Fourier feature KDE | Approximate density estimator | Open | Define feature approximation and bandwidth; test integrated error and seed stability. |
| S17-FD-04 | Quantized DBSCAN | Density clustering | Open | Identify quantisation variant and error bounds; compare cluster stability with exact DBSCAN. |
| S17-FD-05 | Grid-based DBSCAN | Density clustering | Open | Define cell-neighbourhood pruning and exactness conditions; test border/noise assignment. |
| S17-FD-06 | HyperLogLog | Cardinality sketch | Partial | Existing bounded implementation is tested; verify estimator corrections, precision/error and merge semantics. |
| S17-FD-07 | Count-Min sketch | Frequency sketch | Partial | Existing implementation is tested; verify width/depth error bounds and update/query semantics. |
| S17-FD-08 | Bloom filter | Probabilistic membership structure | Partial | Existing implementation is tested; verify false-positive rate, hash independence assumptions and merge semantics. |
| S17-FD-09 | Reservoir sampling / Algorithm R | Streaming sample | Partial | Existing implementation is tested; verify uniformity and deterministic seeded behaviour. |

### Optimal sampling and experimental design — pages 35–36

| ID | Atomic item | Kind | Status | Required completion work |
|---|---|---|---|---|
| S17-OD-01 | Maximin space-filling design | Experimental design | Partial | Existing multi-start normalized maximin LHS is bounded; define metric, scaling and optimisation quality. |
| S17-OD-02 | Coffee-house design | Experimental design | Verify | Resolve exact named design; source gives no reproducible definition, so do not guess. |
| S17-OD-03 | k-means spatial coverage design | Spatial sampling design | Partial | Existing deterministic coverage baseline is tested; document initialisation and representativeness. |
| S17-OD-04 | Latin hypercube sampling | Experimental design | Partial | Existing LHS and centred LHS are tested; add discrepancy/stratification diagnostics and multidimensional constraints. |
| S17-OD-05 | Kriging-variance minimisation | Model-based design | Partial | Existing greedy trace-reduction selector is bounded; verify criterion and observation-noise assumptions. |
| S17-OD-06 | Bayesian optimal design | Bayesian experimental design | Open | Define utility/posterior target and design constraints; test expected utility on conjugate models. |
| S17-OD-07 | Sequential design | Adaptive experimental design | Partial | Existing adaptive sampling primitives are bounded; define sequential update, stopping and budget policy. |
| S17-OD-08 | Adaptive design | Adaptive experimental design | Partial | Distinguish adaptive from sequential variants; define response-dependent candidate selection and uncertainty. |
| S17-OD-09 | Mutual-information sensor selection | Information-theoretic design | Partial | Existing GP log-determinant greedy selector is bounded; verify submodularity/noise assumptions and approximation guarantee. |
| S17-OD-10 | Submodular greedy selection | Approximation algorithm | Partial | State monotonicity/submodularity conditions and cardinality constraints; test guarantee applicability. |
| S17-OD-11 | Adaptive sampling with AUVs | Robotic sensing workflow | Open | Define vehicle dynamics, observation model, communication and safety constraints; simulate informative missions. |
| S17-OD-12 | Adaptive sampling with drones | Robotic sensing workflow | Open | Define flight endurance, coverage, safety and sensor constraints; compare routes with unconstrained site selection. |
| S17-OD-13 | Informative path planning | Robotic path planning | Open | Define path-dependent utility, travel cost and online observations; test on synthetic fields. |

### 3D formats and level-of-detail — page 36

| ID | Atomic item | Kind | Status | Required completion work |
|---|---|---|---|---|
| S17-3D-01 | LAZ point-cloud compression | Data format | Verify | Identify LASzip/LAZ specification and licence; validate lossless round-trip and metadata. |
| S17-3D-02 | COPC | Cloud Optimized Point Cloud format | Verify | Verify specification/version and hierarchy metadata; test range requests and interoperability. |
| S17-3D-03 | Entwine EPT | Point-cloud data format/index | Verify | Identify EPT version and hierarchy schema; test query interoperability. |
| S17-3D-04 | Potree octrees | Point-cloud LOD/index | Verify | Identify Potree format/version; document hierarchy, attributes and rendering semantics. |
| S17-3D-05 | OGC 3D Tiles | Geospatial streaming standard | Verify | Verify current normative version and tile/content formats; test conformance and metadata. |
| S17-3D-06 | Screen-space-error refinement | LOD selection method | Open | Define SSE calculation, geometric error and view parameters; test refinement stability. |
| S17-3D-07 | I3S | 3D geospatial scene format | Verify | Identify current OGC specification/version; document node pages, geometry and attributes. |
| S17-3D-08 | Quantized-mesh terrain | Terrain tile format | Verify | Verify encoding, quantisation and skirt semantics; test decode/mesh continuity. |
| S17-3D-09 | CityGML LoD0 | City model representation | Verify | Identify CityGML version and LoD semantics; distinguish specification from reconstruction method. |
| S17-3D-10 | CityGML LoD1 | City model representation | Verify | Verify LoD1 geometry and semantic requirements against standard version. |
| S17-3D-11 | CityGML LoD2 | City model representation | Verify | Verify roof geometry and semantic requirements against standard version. |
| S17-3D-12 | CityGML LoD3 | City model representation | Verify | Verify detailed architectural representation and version-specific semantics. |
| S17-3D-13 | OGC Simple Features | Geometry data model/standard | Verify | Verify standard version, geometry model and CRS semantics; test conformance. |
| S17-3D-14 | Arc-node topology | Topological data model | Open | Define arc/node incidence and planar graph assumptions; compare to feature-based topology. |
| S17-3D-15 | TIN model | Terrain data model | Open | Define triangulated irregular network and interpolation semantics; test breaklines and constraints. |
| S17-3D-16 | TopoJSON | Topological encoding | Verify | Verify specification/version and transform/arc semantics; test shared-arc round-trip. |
| S17-3D-17 | GeoSPARQL | Geospatial RDF vocabulary/standard | Verify | Identify current OGC version and entailment functions; test conformance and CRS. |

### Competitive location and matching — page 36

| ID | Atomic item | Kind | Status | Required completion work |
|---|---|---|---|---|
| S17-CL-01 | Huff competitive facility location | Probabilistic choice/location model | Partial | Existing attractiveness/impedance probabilities are tested; verify market-share calibration and competitor assumptions. |
| S17-CL-02 | Stackelberg location formulation | Game-theoretic location model | Open | Define leader/follower sequence, objective and equilibrium; test small exact instances. |
| S17-CL-03 | Nash location formulation | Game-theoretic location model | Open | Define players, strategy space and equilibrium concept; distinguish pure/mixed equilibria. |
| S17-CL-04 | Voronoi games | Competitive spatial game | Open | Define game rules, strategy space and payoff; identify exact literature variant. |
| S17-CL-05 | Gale–Shapley deferred acceptance | Matching algorithm | Partial | Existing resident-proposing many-to-one baseline is tested; add institution-proposing and two-sided stability. |
| S17-CL-06 | Auction algorithms | Assignment optimisation | Open | Identify auction algorithm variant and assignment objective; test optimality/gap and epsilon scaling. |
| S17-CL-07 | School choice | Allocation mechanism | Partial | Existing capacity/preference baseline is bounded; identify priorities, tie-breaking and strategy-proofness assumptions. |
| S17-CL-08 | Spatial assignment with preferences | Allocation model | Open | Define spatial cost/preferences and constraints; test stability/efficiency trade-offs. |

### EV charging and refuelling siting — page 36

| ID | Atomic item | Kind | Status | Required completion work |
|---|---|---|---|---|
| S17-EV-01 | Flow-capturing location model (FCLM) | Facility location optimisation | Partial | Existing exact/greedy baselines are tested; document flow assumptions and scale limitations. |
| S17-EV-02 | Flow-refuelling location model (FRLM) | Facility location optimisation | Partial | Existing exact small-instance range-feasibility solver is tested; add scalable heuristics and richer detour/range assumptions. |
| S17-EV-03 | Trajectory-based charging demand estimation | Demand estimation | Open | Define trajectory sample, charging inference and expansion weights; address privacy and selection bias. |
| S17-EV-04 | Charging coverage with queues | Queueing/location model | Open | Define arrival process, service rates, queue discipline and reliability target; validate queue approximation. |
| S17-EV-05 | Grid-capacity-aware charging siting | Energy/location optimisation | Open | Define feeder capacity, load profiles and upgrade costs; test network constraints. |
| S17-EV-06 | Hydrogen station siting | Facility location optimisation | Open | Define demand, supply logistics, safety and capacity; distinguish from EV charging model. |
| S17-EV-07 | Vehicle-to-grid (V2G) scheduling | Energy scheduling | Open | Define battery degradation, grid price, user availability and power constraints; test feasible schedules. |

### Surveillance and anomaly detection — page 36

| ID | Atomic item | Kind | Status | Required completion work |
|---|---|---|---|---|
| S17-SU-01 | CUSUM surveillance | Sequential detection | Partial | Existing two-sided tabular CUSUM is tested; verify reference/allowance design and ARL calibration. |
| S17-SU-02 | EARS C1 detector | Syndromic surveillance | Partial | Existing explicit C1 baseline is tested; verify baseline window and alert threshold. |
| S17-SU-03 | EARS C2 detector | Syndromic surveillance | Partial | Existing explicit C2 baseline is tested; verify moving-window and variance assumptions. |
| S17-SU-04 | EARS C3 detector | Syndromic surveillance | Partial | Existing explicit C3 baseline is tested; verify smoothing and signal accumulation. |
| S17-SU-05 | Farrington outbreak detector | Statistical surveillance | Open | Verify original/Farrington Flexible variant, overdispersion and trend/seasonality; benchmark on reference data. |
| S17-SU-06 | Spatial syndromic surveillance | Spatial event detection | Open | Define spatial units, baseline and multiplicity; test outbreak localisation and false alarms. |
| S17-SU-07 | Space-time syndromic surveillance | Space-time event detection | Open | Define scan window, temporal baseline and multiple testing; test synthetic outbreaks. |
| S17-SU-08 | Sensor-network event detection | Event detection workflow | Open | Define sensor model, event labels and network topology; quantify detection delay and false positives. |
| S17-SU-09 | Graph-based anomaly detection | Graph anomaly detection | Open | Define node/edge anomaly and graph dynamics; compare with known anomalous subgraphs. |
| S17-SU-10 | Spatial scan on counts with covariates | Spatial scan statistic | Partial | Existing Poisson scan baseline is bounded; add covariate adjustment and validate null calibration. |
| S17-SU-11 | RX anomaly detector | Multivariate anomaly score | Partial | Existing global Gaussian-background raster score is tested; local RX, covariance conditioning and masking remain separate. |

### Infrastructure and land-use mapping from imagery — page 36

| ID | Atomic item | Kind | Status | Required completion work |
|---|---|---|---|---|
| S17-IM-01 | Solar-farm detection | Remote-sensing application | Open | Define imagery, object/area labels and temporal persistence; validate regionally. |
| S17-IM-02 | Wind-turbine detection | Remote-sensing application | Open | Define turbine object and shadows; evaluate positional accuracy and temporal changes. |
| S17-IM-03 | Hydropower infrastructure detection | Remote-sensing application | Open | Define dam/reservoir/powerhouse classes and reference labels; validate completeness. |
| S17-IM-04 | Mine detection | Remote-sensing application | Open | Define mine/ancillary classes and change detection; address environmental and legal context. |
| S17-IM-05 | Illegal-mining mapping | Monitoring application | Open | Define legal reference and evidence standard; protect communities and avoid unsupported accusations. |
| S17-IM-06 | Aquaculture-pond mapping | Land/water classification | Open | Define pond object and seasonality; validate against independent imagery/records. |
| S17-IM-07 | Greenhouse mapping | Land-use classification | Open | Define spectral/structural signatures and region; evaluate confusion with roofs/plastic surfaces. |
| S17-IM-08 | Rice-paddy mapping using SAR phenology | Crop mapping workflow | Open | Define SAR time series, phenology features and crop calendar; test regional transfer. |
| S17-IM-09 | Oil-palm mapping | Crop mapping workflow | Open | Define plantation/individual palm unit and age structure; validate against licensed reference. |
| S17-IM-10 | Tree-crop mapping | Crop mapping family | Open | Split crop species and spatial scale; define labels and phenological evidence. |
| S17-IM-11 | Shade-coffee mapping | Agroforestry classification | Open | Define canopy/shade evidence and field labels; validate seasonal and regional transfer. |
| S17-IM-12 | Agroforestry mapping | Land-use classification | Open | Define system classes and tree/crop mixture; document spatial resolution and ambiguity. |
| S17-IM-13 | Building-age estimation | Building attribute inference | Open | Define age target, renovation and imagery dates; validate against dated records. |
| S17-IM-14 | Roof-material classification | Building attribute inference | Open | Define material taxonomy and sensor resolution; assess regional domain shift. |
| S17-IM-15 | Building-height estimation from imagery/shadows | 3D attribute estimation | Open | Define stereo/shadow geometry and sun angle; validate against surveyed heights. |

### Representative implementation map — pages 36–37

These are software/platform entries, not algorithms. Their completion requires a dated, source-backed software record rather than an invented from-scratch implementation.

| ID | Software/system | Kind | Status | Required completion work |
|---|---|---|---|---|
| S17-LIB-01 | GEOS | Geometry library | Verify | Verify supported operations, version and licence; identify repository integrations. |
| S17-LIB-02 | JTS | Geometry library | Verify | Verify current version, topology model and licence. |
| S17-LIB-03 | Shapely | Python geometry library | Verify | Verify version, GEOS dependency and API semantics. |
| S17-LIB-04 | S2 | Spherical geometry/indexing library | Verify | Identify official implementation/version and cell semantics. |
| S17-LIB-05 | H3 | Hierarchical spatial index | Verify | Verify version, cell hierarchy and pentagon semantics. |
| S17-LIB-06 | libspatialindex | Spatial indexing library | Verify | Verify index types, maintenance and licence. |
| S17-LIB-07 | PROJ | Projection/CRS library | Verify | Verify version, database and operation-grid licensing. |
| S17-LIB-08 | GDAL | Geospatial IO/processing library | Verify | Verify version, drivers and licence/dependency implications. |
| S17-LIB-09 | Rasterio | Python raster IO library | Verify | Verify version and GDAL compatibility. |
| S17-LIB-10 | Fiona | Python vector IO library | Verify | Verify current maintenance/version and driver support. |
| S17-LIB-11 | GeoPandas | Python geospatial dataframe library | Verify | Verify version and spatial-index backend semantics. |
| S17-LIB-12 | xarray | N-dimensional labelled array library | Verify | Verify version and data-model interoperability. |
| S17-LIB-13 | rioxarray | Raster/xarray integration | Verify | Verify version, CRS metadata and IO semantics. |
| S17-LIB-14 | PySAL | Spatial analysis ecosystem | Verify | Map subpackages to specific methods and versions; avoid treating ecosystem as one algorithm. |
| S17-LIB-15 | spdep | R spatial dependence package | Verify | Verify package/version and method-specific references. |
| S17-LIB-16 | spatialreg | R spatial regression package | Verify | Verify package/version and model coverage. |
| S17-LIB-17 | mgcv | R statistical modelling package | Verify | Verify package/version and spatial smooth capabilities. |
| S17-LIB-18 | INLA | Bayesian inference software | Verify | Verify project/version and supported latent models. |
| S17-LIB-19 | gstat | Geostatistics package | Verify | Verify package/version and estimator/kriging coverage. |
| S17-LIB-20 | scikit-gstat | Python variogram package | Verify | Verify version and estimator/model semantics. |
| S17-LIB-21 | OSMnx | Network analysis package | Verify | Verify version, data source and network construction semantics. |
| S17-LIB-22 | NetworkX | Graph algorithms library | Verify | Verify version and algorithm complexity/semantics. |
| S17-LIB-23 | igraph | Graph analysis library | Verify | Verify version, language binding and algorithm availability. |
| S17-LIB-24 | pgRouting | Database routing extension | Verify | Verify version, SQL API and PostgreSQL/PostGIS compatibility. |
| S17-LIB-25 | OSRM | Routing engine | Verify | Verify version, profile and preprocessing assumptions. |
| S17-LIB-26 | Valhalla | Routing engine | Verify | Verify version, costing model and data build. |
| S17-LIB-27 | GraphHopper | Routing engine | Verify | Verify version, licence and profile/custom model semantics. |
| S17-LIB-28 | OpenTripPlanner | Multimodal transit routing | Verify | Verify version, GTFS/OSM inputs and routing semantics. |
| S17-LIB-29 | R5 | Transit routing engine | Verify | Verify version, accessibility outputs and feed assumptions. |
| S17-LIB-30 | momepy | Urban morphology package | Verify | Verify version and metric definitions. |
| S17-LIB-31 | scikit-mobility | Mobility analysis package | Verify | Verify version, trajectory schema and privacy assumptions. |
| S17-LIB-32 | MovingPandas | Trajectory analysis package | Verify | Verify version and trajectory/time semantics. |
| S17-LIB-33 | Traja | Trajectory analysis package | Verify | Verify maintenance/version and method coverage. |
| S17-LIB-34 | SNAP | EO processing platform | Verify | Identify ESA SNAP version and module/plugin support. |
| S17-LIB-35 | Orfeo Toolbox | Remote-sensing toolkit | Verify | Verify version, algorithms and licence. |
| S17-LIB-36 | eo-learn | EO workflow library | Verify | Verify project maintenance/version and data dependencies. |
| S17-LIB-37 | TorchGeo | Geospatial ML library | Verify | Verify version, dataset licences and model APIs. |
| S17-LIB-38 | TerraTorch | Geospatial foundation-model toolkit | Verify | Verify exact project, version and model-weight licences. |
| S17-LIB-39 | Raster Vision | EO ML framework | Verify | Verify version and supported training/inference pipeline. |
| S17-LIB-40 | Google Earth Engine | Cloud geospatial platform | Verify | Verify current terms, API and dataset licensing; document cloud dependency. |
| S17-LIB-41 | openEO | EO processing API/platform | Verify | Verify API version and backend-specific behaviour. |
| S17-LIB-42 | WhiteboxTools | Terrain/hydrology software | Verify | Verify version, tool definitions and licence. |
| S17-LIB-43 | GRASS GIS | GIS platform | Verify | Verify version and module references. |
| S17-LIB-44 | SAGA GIS | GIS platform | Verify | Verify version, module availability and licence. |
| S17-LIB-45 | TauDEM | Terrain/hydrology toolkit | Verify | Verify version and flow-routing assumptions. |
| S17-LIB-46 | pysheds | Python hydrology library | Verify | Verify version and algorithm semantics. |
| S17-LIB-47 | Apache Sedona | Distributed spatial analytics | Verify | Verify version, SQL functions and Spark compatibility. |
| S17-LIB-48 | GeoMesa | Distributed geospatial datastore | Verify | Verify version, backend and query semantics. |
| S17-LIB-49 | cuSpatial | GPU spatial analytics library | Verify | Verify version, supported operations and GPU requirements. |
| S17-LIB-50 | Dask-GeoPandas | Distributed geospatial dataframe library | Verify | Verify version and partition/spatial shuffle behaviour. |
| S17-LIB-51 | DuckDB spatial | Spatial database extension | Verify | Verify DuckDB/extension version and function semantics. |

## Completion gates

1. Verify each algorithm and software name against original papers, normative standards or current maintainer documentation; record version and stable reference.
2. Preserve exact problem definitions, variants, approximation guarantees, input domains and degeneracy handling.
3. For scalable statistics, include error, convergence, memory and workload evidence rather than generic speed claims.
4. For formats/standards, use conformance and interoperability tests; do not claim an algorithm implementation.
5. For software entries, document dependency, licence, maintenance, version and exact repository integration where applicable.
6. Tests must include independent oracles, property/invariant checks, numerical tolerances and adversarial cases appropriate to the method.
7. Reconcile canonical lessons, implementations, verification records, notebooks, coverage matrix and dashboard after evidence changes.
8. Review rights for software, datasets, models, images and documentation.

## Execution priorities

1. Finish high-risk geometry variants with exact predicates and independent topology/mesh oracles.
2. Verify scalable statistical methods against primary sources and compare approximate outputs to dense/exact baselines.
3. Complete the still-open density, adaptive design and spatial sampling variants.
4. Create a dated, maintained software landscape with official references and licence/maintenance checks.
5. Keep Section 17 open until all children have evidence-backed dispositions and applicable learning/release gates pass.

**Current conclusion:** Section 17 is decomposed into atomic review items. It remains open; the register does not claim that the 51 software entries or the algorithm families have been independently verified.
