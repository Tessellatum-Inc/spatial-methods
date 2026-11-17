# Section 14 atomic completion register

**Source:** *Spatial Analysis Algorithms: Complete Compendium*, Section 14, pages 28–30.  
**Intake:** [preserved pages 26–30 transcription](../source-inventory/pages-26-30.md).  
**Section index:** [Section 14 catalogue record](../catalog/sections/14-databases-graphics-morphology-hazards.md).

> The source groups algorithms, software, standards, models and workflows. The atomic rows below preserve that variety; they are not claims that every named item has been verified.

## Status policy

Apply the [verification protocol](../catalog/verification-protocol.md) and [completion standard](compendium-completion-standard.md). Verify exact variant/version before technical claims. An existing implementation covers only the named scope.

| Status | Meaning |
|---|---|
| Open | No item-specific verification or implementation evidence recorded. |
| Partial | Bounded related implementation exists; variants or validation remain. |
| Verify | Exact algorithm, software, standard or product must be identified. |
| Not applicable | Workflow, format, platform or visualisation pattern is not a standalone algorithm. |

## Atomic source register

### Spatial database and distributed systems — page 29

| ID | Atomic item | Kind | Status | Required completion work |
|---|---|---|---|---|
| S14-DB-01 | Linear R-tree split | Index algorithm | Open | Define seed selection and distribution; test overlap/area and query performance. |
| S14-DB-02 | Quadratic R-tree split | Index algorithm | Open | Verify quadratic waste heuristic and tie handling; compare with linear split. |
| S14-DB-03 | R*-tree split/reinsertion | Index algorithm | Partial | Existing mutable R*-tree is bounded; verify forced reinsertion/split heuristics and invariants. |
| S14-DB-04 | Nearest-X bulk loading | Index construction | Open | Identify exact ordering and packing method; compare tree quality and build cost. |
| S14-DB-05 | Hilbert packing | Index construction | Open | Define Hilbert key and packing; test locality and query performance. |
| S14-DB-06 | STR bulk loading | Index construction | Open | Verify sort-tile-recursive construction; test packing and query behaviour. |
| S14-DB-07 | OMT bulk loading | Index construction | Verify | Resolve exact acronym/algorithm; document partitioning and source. |
| S14-DB-08 | Buffer trees | External-memory data structure | Verify | Identify exact buffer-tree variant; state I/O model and operation bounds. |
| S14-DB-09 | LSM-based spatial indexes | Storage/index architecture | Open | Define spatial keying, compaction and tombstones; benchmark write/read amplification. |
| S14-DB-10 | GiST spatial indexes | Database index access method | Verify | Verify PostgreSQL/operator-class version and consistency semantics. |
| S14-DB-11 | SP-GiST spatial indexes | Database index access method | Verify | Verify partitioning strategy and supported operator classes/version. |
| S14-DB-12 | BRIN spatial indexes | Database block-range index | Verify | Identify spatial operator classes and selectivity assumptions; compare to GiST. |
| S14-DB-13 | Time-partitioned spatial tables | Database design pattern | Not applicable | Document partition key, pruning and temporal retention; not a standalone algorithm. |
| S14-DB-14 | Broadcast spatial joins | Distributed join strategy | Not applicable | Define broadcast-side constraints and data skew; document execution strategy. |
| S14-DB-15 | Quadtree partitioning for distributed joins | Spatial partitioning | Open | Define split/replication and boundary handling; test join completeness. |
| S14-DB-16 | KDB-tree partitioning for distributed joins | Spatial partitioning | Verify | Verify K-D-B tree partition semantics; test load balance and boundary replication. |
| S14-DB-17 | Skew handling in distributed spatial joins | Distributed query optimisation | Open | Define heavy-hitter detection and repartitioning; measure skew/replication. |
| S14-DB-18 | Z-order partitioning | Space-filling-curve partitioning | Open | Define quantisation/interleaving and partition boundaries; test locality and skew. |
| S14-DB-19 | DITA trajectory engine | Distributed trajectory system | Verify | Resolve exact system and paper; document query model and data layout. |
| S14-DB-20 | Simba trajectory engine | Distributed trajectory system | Verify | Identify exact Simba variant and version; distinguish system from its index/query algorithms. |
| S14-DB-21 | Continuous range queries | Stream query | Open | Define window/update semantics and output changes; test event-time ordering. |
| S14-DB-22 | Sliding-window geofencing | Stream spatial query | Open | Define geometry validity, window and event-time semantics; test late/out-of-order events. |
| S14-DB-23 | Incremental kNN maintenance | Dynamic spatial query | Open | Define insertion/deletion and exactness; compare with full recomputation. |

### 3D graphics and geospatial rendering — page 29

| ID | Atomic item | Kind | Status | Required completion work |
|---|---|---|---|---|
| S14-GR-01 | Möller–Trumbore ray-triangle intersection | Geometry algorithm | Partial | Tested dependency-free reference, analytic edge/vertex/parallel/degenerate/culling/interval tests and implementation walkthrough: [lesson](../algorithms/geometry/ray-triangle-intersection.md), [package](../implementations/python/ray-triangle-intersection/README.md). Robust predicates and exact source-entry review remain open. |
| S14-GR-02 | BVH construction | Acceleration structure | Partial | Deterministic binary AABB BVH with explicit leaf policy and nearest-hit traversal: [package](../implementations/python/ray-triangle-intersection/README.md), including seeded brute-force differential tests. Production binned/spatial-split variants remain open. |
| S14-GR-03 | Surface area heuristic (SAH) | BVH cost heuristic | Partial | Exact-centroid split scan evaluates A(left)*N(left)+A(right)*N(right) and compares with leaf cost; implementation and seeded query tests are in the [BVH package](../implementations/python/ray-triangle-intersection/README.md). Binned SAH and measured cost calibration remain open. |
| S14-GR-04 | kd-tree ray traversal | Acceleration structure/traversal | Partial | Added a spatial median-split triangle kd-tree with straddler duplication, bounded depth, near-first cell traversal and per-query triangle de-duplication; seeded brute-force differential and split-plane tests: [implementation](../implementations/python/ray-triangle-intersection/README.md), [algorithm note](../algorithms/geometry/ray-triangle-intersection.md). SAH builder and production clipping remain open. |
| S14-GR-05 | Frustum culling | Visibility algorithm | Partial | Conservative AABB-versus-inward-plane test with boundary/tolerance tests: [implementation package](../implementations/python/ray-triangle-intersection/README.md). View-projection matrix extraction and clip-space convention adapters remain open. |
| S14-GR-06 | Occlusion culling | Visibility algorithm | Open | Split hardware/query and hierarchical-Z variants; test conservative visibility. |
| S14-GR-07 | Level-of-detail selection | Rendering method | Open | Define screen-space error and transition; test popping and view dependence. |
| S14-GR-08 | Shadow mapping | Rendering algorithm | Open | Define depth bias, filtering and light projection; evaluate acne/peter-panning. |
| S14-GR-09 | Shadow volumes | Rendering algorithm | Open | Define stencil volume construction and caps; test robust silhouettes. |
| S14-GR-10 | Photon mapping | Global illumination algorithm | Open | Define photon emission, density estimation and bias; compare with reference scenes. |
| S14-GR-11 | Radiosity | Global illumination method | Open | Define patch discretisation and energy exchange; test energy conservation. |
| S14-GR-12 | Sky-view factor | Urban/terrain radiation metric | Open | Define hemisphere sampling and obstruction; test analytic terrain/building cases. |
| S14-GR-13 | Sunlight-hours computation on 3D city models | Solar exposure workflow | Open | Define sun path, temporal sampling and occlusion; compare analytic building cases. |
| S14-GR-14 | IFC-to-CityGML conversion | BIM/GIS conversion workflow | Verify | Identify schema versions and mapping rules; test semantic/geometry round-trip. |
| S14-GR-15 | Scan-to-BIM | Reconstruction workflow | Not applicable | Document registration, segmentation and semantic modelling stages; do not call one algorithm. |
| S14-GR-16 | Point-cloud-to-BIM | Reconstruction workflow | Not applicable | Define object recognition and BIM authoring stages; validate geometry/semantics. |
| S14-GR-17 | BIM-GIS integration | Data integration workflow | Not applicable | Define coordinate, semantic and identity mapping; test interoperability. |
| S14-GR-18 | 3D utility network mapping | Infrastructure mapping workflow | Open | Define topology, connectivity and asset schema; validate against surveyed network. |

### Mathematical morphology and image structure — page 29

| ID | Atomic item | Kind | Status | Required completion work |
|---|---|---|---|---|
| S14-MM-01 | Binary erosion | Morphological operation | Partial | Existing binary implementation tested; verify structuring-element origin and border semantics. |
| S14-MM-02 | Binary dilation | Morphological operation | Partial | Existing binary implementation tested; verify border and footprint conventions. |
| S14-MM-03 | Opening | Morphological operation | Partial | Existing implementation tested; verify erosion/dilation composition and idempotence. |
| S14-MM-04 | Closing | Morphological operation | Partial | Existing implementation tested; verify dilation/erosion composition and idempotence. |
| S14-MM-05 | Hit-or-miss transform | Morphological operation | Partial | Existing implementation tested; verify foreground/background structuring elements. |
| S14-MM-06 | Geodesic reconstruction | Morphological operation | Partial | Existing implementation tested; verify marker/mask ordering and convergence. |
| S14-MM-07 | Granulometry | Morphological scale analysis | Partial | Added binary opening granulometry for a homothetic centred-square structuring-element family; reports foreground area by scale and the area-difference pattern spectrum, with monotonicity/conservation tests: [binary morphology package](../implementations/python/binary-morphology/README.md). Grayscale granulometry and alternative structuring-element families remain open. |
| S14-MM-08 | Max-tree | Component-tree structure | Open | Define upper-level-set tree and canonical representation; test attribute filtering. |
| S14-MM-09 | Min-tree | Component-tree structure | Open | Define lower-level-set dual and tree construction; test reconstruction. |
| S14-MM-10 | Alpha-tree | Component-tree structure | Verify | Resolve exact alpha-tree definition and relation to connectivity hierarchy. |
| S14-MM-11 | Attribute filters | Connected filtering | Open | Define attribute and pruning rule; test increasing/decreasing attributes. |
| S14-MM-12 | Area opening | Connected morphological filter | Partial | Existing grayscale area opening is tested; verify connectivity and threshold semantics. |
| S14-MM-13 | Shape opening | Connected morphological filter | Open | Define shape attribute and pruning; test rotation/scale dependence. |
| S14-MM-14 | Zhang–Suen thinning | Skeletonisation algorithm | Partial | Existing implementation tested; verify simultaneous sub-iteration deletion and topology preservation. |
| S14-MM-15 | Moore-neighbour contour tracing | Contour tracing | Open | Define stop criterion and connectivity; test holes, diagonal contacts and border loops. |
| S14-MM-16 | Suzuki border following | Contour extraction | Open | Verify hierarchy/label conventions; test nested holes and connected components. |
| S14-MM-17 | Two-pass connected components | Labelling algorithm | Partial | Existing union-find implementation tested; verify 4/8-connectivity and label equivalence. |
| S14-MM-18 | GrabCut | Interactive segmentation | Open | Verify graph-cut energy and GMM updates; test seed constraints and convergence. |
| S14-MM-19 | Random walker segmentation | Interactive segmentation | Partial | Existing sparse Dirichlet solver is bounded to small 2D grids; add multiscale/large-grid solver and calibrated tests. |
| S14-MM-20 | Seeded region growing | Segmentation algorithm | Open | Define seed, similarity and conflict policy; test order dependence. |
| S14-MM-21 | Morphological spatial pattern analysis (MSPA) | Landscape pattern method | Open | Verify foreground/connectivity/edge/core classes and width parameter; test synthetic habitat patterns. |

### Accessibility and public-health catchments — page 29

| ID | Atomic item | Kind | Status | Required completion work |
|---|---|---|---|---|
| S14-AC-01 | E2SFCA | Accessibility metric | Partial | Existing 2SFCA/E2SFCA baseline is bounded; verify demand/supply weights and distance zones. |
| S14-AC-02 | 3SFCA | Accessibility metric | Open | Verify exact three-step variant and provider competition; test benchmark cases. |
| S14-AC-03 | M2SFCA | Accessibility metric | Verify | Resolve exact M2SFCA variant and weighting; do not expand acronym by guess. |
| S14-AC-04 | G2SFCA | Accessibility metric | Verify | Resolve exact Gaussian variant and parameterisation; test distance decay. |
| S14-AC-05 | KD2SFCA | Accessibility metric | Verify | Resolve kernel-density variant and bandwidth; test limiting cases. |
| S14-AC-06 | Gaussian travel-time decay | Accessibility kernel | Partial | Existing kernel tested; document scale/decay parameter and normalisation. |
| S14-AC-07 | Power travel-time decay | Accessibility kernel | Partial | Existing regularised power kernel tested; verify exponent and zero-distance handling. |
| S14-AC-08 | Kernel-density travel-time decay | Accessibility kernel | Partial | Existing Epanechnikov compact-support kernel tested; distinguish from KDE accessibility estimator. |
| S14-AC-09 | Multimodal accessibility | Accessibility model | Open | Define mode transfer, waiting, fares and service time; test network integration. |
| S14-AC-10 | Spatial mismatch indices | Equity/accessibility metric | Open | Define jobs/population opportunity and scale; test denominator and interpretation. |
| S14-AC-11 | Leroux CAR disease mapping | Bayesian spatial model | Verify | Verify Leroux precision parameterisation and priors; test independent/CAR limits. |
| S14-AC-12 | Knorr–Held space-time interaction model | Bayesian disease mapping | Verify | Identify interaction type and model version; test space/time components. |
| S14-AC-13 | Age standardisation | Epidemiological rate method | Open | Define direct/indirect method and standard population; test rates and uncertainty. |
| S14-AC-14 | Poisson-gamma disease mapping | Bayesian hierarchical model | Open | Define conjugate prior and risk estimand; test posterior moments. |
| S14-AC-15 | Cuzick–Edwards test | Spatial clustering test | Verify | Verify nearest-neighbour statistic and null simulation; test case-control design. |
| S14-AC-16 | Whittemore test | Spatial clustering test | Verify | Verify exact statistic and sampling assumptions; test published examples. |
| S14-AC-17 | Spatial scan with covariates | Cluster detection | Partial | Existing Poisson scan is unadjusted baseline; specify covariate model and null calibration. |

### Mass movement and volcanic/coastal hazards — pages 29–30

| ID | Atomic item | Kind | Status | Required completion work |
|---|---|---|---|---|
| S14-HZ-01 | CRSP rockfall simulation | Rockfall model/software | Verify | Identify exact CRSP system/version and physics; validate against field trajectories. |
| S14-HZ-02 | Rockyfor3D | Rockfall simulation software | Verify | Verify version, terrain inputs and calibration; document licence. |
| S14-HZ-03 | RAMMS debris-flow runout | Hazard simulation software | Verify | Identify RAMMS module/version and rheology; validate against documented events. |
| S14-HZ-04 | r.avaflow | Mass-flow simulation software | Verify | Verify version and governing equations; document terrain and material parameters. |
| S14-HZ-05 | Energy cone model | Empirical runout model | Open | Define angle/starting-zone assumptions; test against observed runout. |
| S14-HZ-06 | Energy line model | Empirical runout model | Open | Verify line/angle convention and calibration domain; compare with energy cone. |
| S14-HZ-07 | TITAN2D pyroclastic-flow model | Numerical hazard model | Verify | Identify exact version and depth-averaged equations; document calibration. |
| S14-HZ-08 | LaharZ | Lahar inundation model | Verify | Verify model version, volume assumptions and validation; distinguish empirical from dynamic models. |
| S14-HZ-09 | MAGFLOW lava-flow model | Numerical hazard model | Verify | Identify version and cellular automaton physics; test against benchmark flows. |
| S14-HZ-10 | Probabilistic lava path models | Hazard model family | Open | Define source uncertainty, topography and flow rules; test ensemble calibration. |
| S14-HZ-11 | Tsunami inundation/runup coupling | Coastal hazard workflow | Open | Define offshore propagation, nearshore coupling and bathymetry; validate against benchmark events. |
| S14-HZ-12 | Coastal landslide hazard | Hazard assessment workflow | Open | Define slope stability, triggering, runout and exposure; document uncertainty. |

### Precision agriculture and forest inventory — page 30

| ID | Atomic item | Kind | Status | Required completion work |
|---|---|---|---|---|
| S14-AG-01 | Fuzzy c-means management zones | Clustering method | Open | Define features, fuzzifier and spatial constraints; test initialization and stability. |
| S14-AG-02 | MZA management-zone analysis | Management-zone workflow | Verify | Resolve exact MZA method/software; document indicators and validation. |
| S14-AG-03 | Variable-rate prescriptions | Decision-support workflow | Not applicable | Define agronomic response, constraints and machinery interface; require field validation. |
| S14-AG-04 | Yield-monitor data cleaning | Data-quality workflow | Open | Define calibration, lag, outlier and spatial alignment corrections; compare field records. |
| S14-AG-05 | Spatially varying coefficient on-farm experiments | Statistical design/model | Open | Define treatment assignment, spatial covariance and estimand; test design-based inference. |
| S14-AG-06 | UAV plant counting | Object detection workflow | Open | Define plant unit and overlap handling; validate counts by field plot. |
| S14-AG-07 | Weed mapping | Remote-sensing classification | Open | Define weed species/patch labels and phenology; evaluate false negatives. |
| S14-AG-08 | Crop-row detection | Geometric extraction | Open | Define row geometry and spacing; test curved/partial rows. |
| S14-AG-09 | Stand-emergence mapping | Crop monitoring | Open | Define emergence timing and detection unit; validate field observations. |
| S14-AG-10 | Canopy-cover estimation | Vegetation metric | Open | Define pixel/area estimator and shadow treatment; validate with field measurements. |
| S14-AG-11 | LiDAR area-based forest inventory | Forest estimation method | Open | Define plot/area model and calibration; report design-based uncertainty. |
| S14-AG-12 | Individual-tree inventory | Tree detection/estimation workflow | Open | Define segmentation, matching and attributes; evaluate omission/commission. |
| S14-AG-13 | kNN forest attribute imputation | Statistical imputation | Open | Define distance/features and donor pool; test bias and uncertainty. |
| S14-AG-14 | Gradient nearest neighbour imputation | Forest inventory method | Verify | Verify canonical GNN method and model; test spatial transfer. |
| S14-AG-15 | Stand delineation | Forest segmentation | Open | Define stand criteria and boundaries; validate against inventory polygons. |
| S14-AG-16 | Forest volume models | Allometric/statistical model | Open | Define species, DBH/height and model domain; validate regionally. |
| S14-AG-17 | Basal-area estimation | Forest inventory metric | Open | Define plot expansion and sampling design; test unit conversion. |
| S14-AG-18 | Small-area estimation for inventory | Survey/model-based estimation | Open | Define direct/synthetic estimator and auxiliary data; report uncertainty and shrinkage. |

### Cartographic mathematics — page 30

| ID | Atomic item | Kind | Status | Required completion work |
|---|---|---|---|---|
| S14-CM-01 | Robinson projection | Map projection | Verify | Verify official formula/implementation and intended compromise; test world control points. |
| S14-CM-02 | Winkel Tripel projection | Map projection | Verify | Verify parameter and implementation; test poles/seams and distortion. |
| S14-CM-03 | Equal Earth projection | Map projection | Verify | Verify normative formula and equal-area property; test control points. |
| S14-CM-04 | Natural Earth projection | Map projection | Verify | Verify exact Natural Earth variant and implementation; avoid naming ambiguity. |
| S14-CM-05 | Goode homolosine | Interrupted equal-area projection | Verify | Verify lobe layout and interruption rules; test area and seam behaviour. |
| S14-CM-06 | Dymaxion projection | Polyhedral projection | Verify | Identify exact orientation/unfolding; document discontinuities and face mapping. |
| S14-CM-07 | Azimuthal equidistant projection | Projection family | Verify | Define centre and ellipsoid/sphere; test radial distance property. |
| S14-CM-08 | Conic equidistant projection | Projection family | Verify | Define standard parallels and ellipsoid; test meridional distance property. |
| S14-CM-09 | Tissot indicatrix | Distortion diagnostic | Partial | Existing local principal/area/angular scale diagnostics are tested; verify ellipsoidal and seam-aware behaviour. |
| S14-CM-10 | Areal distortion indices | Projection metric | Open | Define local/global aggregation and weighting; test equal-area zero distortion. |
| S14-CM-11 | Angular distortion indices | Projection metric | Open | Define maximum angular deformation and sampling; test conformal limit. |
| S14-CM-12 | Projection selection algorithms | Decision/optimisation method | Open | Define objective, region and distortion weights; document subjective constraints. |
| S14-CM-13 | Rubber-sheet contiguous cartograms | Cartogram algorithm | Open | Define topology/area constraints and deformation; test adjacency and area error. |
| S14-CM-14 | Diffusion cartograms | Cartogram algorithm | Open | Verify diffusion formulation and mass conservation; test boundary conditions. |
| S14-CM-15 | Tile-grid maps via Hungarian assignment | Map layout optimisation | Open | Define tile candidates and assignment cost; test adjacency and geographic distortion. |
| S14-CM-16 | Voronoi treemaps | Hierarchical visualisation algorithm | Verify | Verify weighted cell construction and hierarchy; test area accuracy and stability. |
| S14-CM-17 | Hexagon maps | Cartographic layout method | Open | Define assignment and adjacency preservation; distinguish grid map from hexbin aggregation. |
| S14-CM-18 | CIELAB colour interpolation | Colour-space method | Open | Define white point, gamut and interpolation path; test perceptual smoothness. |
| S14-CM-19 | CIECAM colour interpolation | Colour appearance model | Verify | Identify CIECAM02/16 variant and viewing conditions; test gamut mapping. |
| S14-CM-20 | ColorBrewer rules | Cartographic design guidance | Verify | Verify palette metadata/licence and intended data types; not an algorithm. |
| S14-CM-21 | Viridis-style perceptual uniformity | Palette design property | Not applicable | Document perceptual criteria and colour-map provenance; do not claim a generic algorithm. |
| S14-CM-22 | Colour-blind-safe palette generation | Palette design workflow | Open | Define colour-vision simulation and contrast criteria; test accessibility. |

### Geovisualisation and interaction — page 30

| ID | Atomic item | Kind | Status | Required completion work |
|---|---|---|---|---|
| S14-GV-01 | Wood–Dykes OD map layout | Visualisation layout method | Verify | Identify exact layout paper/algorithm; evaluate crossings and flow overlap. |
| S14-GV-02 | Sankey flow layout | Visualisation algorithm | Open | Define node ordering, flow conservation and crossing minimisation. |
| S14-GV-03 | Space-time cube | Visualisation technique | Not applicable | Define axes, projection and interaction; document analytical use/limitations. |
| S14-GV-04 | Small multiples | Visualisation technique | Not applicable | Define shared scales, alignment and comparison; document design choices. |
| S14-GV-05 | Brushing and linking | Interactive visual analytics technique | Not applicable | Document linked selections, state and scalability; not a standalone algorithm. |
| S14-GV-06 | Bivariate uncertainty palettes | Uncertainty visualisation | Open | Define two-variable encoding and perceptual testing; avoid misleading colour interactions. |
| S14-GV-07 | Value-suppressing palettes | Uncertainty visualisation | Verify | Resolve exact technique and interpretation; test value/uncertainty encoding. |
| S14-GV-08 | Ensemble maps | Uncertainty visualisation | Not applicable | Document ensemble summary/visual encoding and uncertainty semantics. |
| S14-GV-09 | Hypothetical outcome plots | Uncertainty visualisation | Verify | Identify original HOP method and sampling semantics; test faithful posterior display. |
| S14-GV-10 | Animation and temporal generalisation | Temporal visualisation | Not applicable | Define temporal aggregation and change semantics; evaluate perceptual continuity. |
| S14-GV-11 | Data-driven scrollytelling | Narrative workflow | Not applicable | Document evidence, interaction and accessibility; not an algorithm. |
| S14-GV-12 | Level-of-detail streaming | Visualisation/system method | Open | Define refinement/error metric and streaming constraints; test temporal and spatial consistency. |

### Linguistic, political and social geography — page 30

| ID | Atomic item | Kind | Status | Required completion work |
|---|---|---|---|---|
| S14-LS-01 | Dialect mapping | Linguistic geography workflow | Open | Define sampling, dialect labels and uncertainty; protect participant identity. |
| S14-LS-02 | Isogloss detection | Linguistic boundary method | Open | Define feature-specific boundaries and smoothing; test sampling sensitivity. |
| S14-LS-03 | Spatial lexical variation analysis | Spatial text/statistical analysis | Open | Define corpus, spatial support and lexical model; assess language and sampling bias. |
| S14-LS-04 | King's ecological inference (EI) | Ecological inference model | Verify | Verify exact EI model/version and assumptions; test identification limits. |
| S14-LS-05 | Goodman's regression | Ecological inference model | Verify | Verify original regression formulation and ecological bias; compare with EI alternatives. |
| S14-LS-06 | Spatial voting models | Political/econometric model family | Open | Split by utility/spatial interaction model; define voter/precinct unit and inference. |
| S14-LS-07 | Efficiency gap | Partisan bias metric | Verify | Verify formula and legal/interpretive limitations; test synthetic district plans. |
| S14-LS-08 | Mean–median difference | Partisan bias metric | Open | Define vote-share convention and statewide aggregation; test sensitivity. |
| S14-LS-09 | Declination | Partisan bias metric | Verify | Verify geometric definition and applicability; test boundary cases. |
| S14-LS-10 | Ensemble redistricting simulation | Redistricting analysis | Open | Define constraints, sampling process and ensemble representativeness; document legal context. |
| S14-LS-11 | Packing diagnostics | Redistricting diagnostic | Open | Define voter/party concentration and benchmark; distinguish descriptive from causal claims. |
| S14-LS-12 | Cracking diagnostics | Redistricting diagnostic | Open | Define fragmentation measure and benchmark; test alternative district plans. |

## Completion gates

1. Verify algorithms against original papers and standards; software against current maintainers and release documentation.
2. State data model, index invariants, geometric/numerical assumptions and exact database/software version.
3. Test geometry and graphics with degeneracies, boundary conditions and independent geometric oracles.
4. Test morphology with connectivity, border, topology and idempotence properties.
5. For health, political, linguistic and social geography, document sampling, privacy, inference limits and potential harms.
6. Review licences and provenance for standards, software, palettes, datasets and imagery.
7. Reconcile section index, implementation index, tests, notebooks, coverage matrix and dashboard only when evidence changes.

**Current conclusion:** Section 14 is decomposed into atomic review items. It remains open; no claim is made that the named software systems, hazard models or political methods have been independently verified.
