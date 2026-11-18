# Section 18 atomic completion register

**Source:** *Spatial Analysis Algorithms: Complete Compendium*, Section 18, pages 37–39.  
**Intake:** [preserved pages 36–40 transcription](../source-inventory/pages-36-40.md).  
**Section index:** [Section 18 catalogue record](../catalog/sections/18-moving-objects-routing-transit-water.md).

> The source warns that many names are from memory. This register decomposes the grouped entries into child records; it does not independently authenticate each name, product, algorithm variant or software package. Preserve that distinction throughout implementation and publication.

## Status and evidence rules

Apply [the source-entry verification protocol](../catalog/verification-protocol.md) and [the compendium completion standard](compendium-completion-standard.md). A bounded implementation is evidence only for its stated variant. A product, platform or workflow is not automatically a standalone algorithm.

| Status | Meaning |
|---|---|
| Open | No item-specific verification or implementation evidence recorded here. |
| Partial | A related bounded implementation exists; substantial children or validation remain open. |
| Verify | Exact method, acronym, product, model or version must be resolved before technical claims. |
| Not applicable | A format, platform, workflow or application is not a standalone algorithm; document the appropriate record kind. |

## Atomic source register

### Moving-object databases and spatiotemporal indexes — page 37

| ID | Atomic item | Kind | Status | Required completion work |
|---|---|---|---|---|
| S18-MO-01 | HR-tree | Spatiotemporal index | Verify | Resolve exact paper/variant, node structure and temporal extent; benchmark update/query workloads. |
| S18-MO-02 | MV3R-tree | Spatiotemporal index | Verify | Verify acronym and original design; specify moving-object representation and query semantics. |
| S18-MO-03 | TPR-tree | Spatiotemporal index | Verify | Verify time-parameterised bounding regions and update rules; test future-time range queries. |
| S18-MO-04 | 3D R-tree | Spatiotemporal index | Open | Define embedding of time as third dimension and interval semantics; compare with temporal indexes. |
| S18-MO-05 | SETI | Spatiotemporal index | Verify | Resolve acronym and exact paper; document partitioning and workload assumptions. |
| S18-MO-06 | PIST | Spatiotemporal index | Verify | Resolve acronym and exact structure; avoid expanding acronym from memory. |
| S18-MO-07 | STR-tree | Spatial/trajectory index | Verify | Disambiguate STR packing from any trajectory-specific STR-tree; identify exact source. |
| S18-MO-08 | TB-tree | Trajectory index | Verify | Verify trajectory-oriented page organisation and split strategy; benchmark sequential and window queries. |
| S18-MO-09 | Grid-based trajectory indexes | Index family | Open | Split grid variants by cell assignment, time partition and update strategy; define query semantics. |
| S18-MO-10 | Future-location queries | Moving-object query | Partial | Existing constant-velocity prediction is a bounded baseline; add model uncertainty, time horizon and trusted comparison. |
| S18-MO-11 | Predictive range queries | Moving-object query | Partial | Existing uncertainty-disk rectangle query covers one model; extend to covariance/elliptical regions and continuous-time semantics. |
| S18-MO-12 | Dead-reckoning update policies | Update policy | Partial | Existing displacement-error policy is bounded; verify error threshold, update cost and uncertainty propagation. |
| S18-MO-13 | Uncertainty regions for moving objects | Uncertainty model | Partial | Distinguish disks, ellipses, probabilistic contours and reachable sets; test coverage calibration. |
| S18-MO-14 | Snapshot spatiotemporal data model | Data model | Not applicable | Document semantics, temporal granularity and query implications; no invented algorithm. |
| S18-MO-15 | Space-time composite data model | Data model | Not applicable | Define spatial/temporal object composition, identity and versioning. |
| S18-MO-16 | Event-based spatiotemporal model | Data model | Not applicable | Define event identity, ordering, validity time and transaction time. |
| S18-MO-17 | Object-oriented spatiotemporal model | Data model | Not applicable | Identify model lineage and object identity/lifecycle; compare to event and snapshot models. |
| S18-MO-18 | Temporal GIS versioning | Data management approach | Open | Distinguish valid-time, transaction-time and bitemporal versioning; document consistency and query semantics. |

### Routing speedups and richer route choice — page 37

| ID | Atomic item | Kind | Status | Required completion work |
|---|---|---|---|---|
| S18-RT-01 | Transit node routing | Shortest-path acceleration | Open | Define transit-node selection, access/egress regions and locality filter; compare exact distances to Dijkstra. |
| S18-RT-02 | Highway hierarchies | Shortest-path acceleration | Verify | Verify hierarchy construction and query algorithm; test exactness and road-network assumptions. |
| S18-RT-03 | Reach-based routing | Shortest-path acceleration | Verify | Define reach and pruning proof/conditions; test threshold sensitivity and exactness. |
| S18-RT-04 | Arc flags | Shortest-path acceleration | Verify | Define partitioning and flag preprocessing; test query correctness across partition boundaries. |
| S18-RT-05 | PHAST | Shortest-path acceleration | Verify | Verify one-to-all hierarchy sweep and directed-graph assumptions; benchmark against baseline. |
| S18-RT-06 | RPHAST | Shortest-path acceleration | Verify | Verify restricted PHAST target-set processing; test exactness and target selection. |
| S18-RT-07 | Customizable route planning (CRP) | Customizable shortest-path method | Verify | Identify exact CRP variant; separate metric-independent preprocessing from metric customization. |
| S18-RT-08 | Time-dependent contraction hierarchies | Time-dependent shortest-path acceleration | Open | Define FIFO/non-FIFO assumptions, piecewise travel-time functions and shortcut composition; compare exact oracle. |
| S18-RT-09 | Martins Pareto label-setting | Multiobjective shortest paths | Partial | Existing Pareto label-setting covers nonnegative additive vector costs; verify canonical algorithm and complexity conditions. |
| S18-RT-10 | Bi-objective shortest path | Multiobjective shortest paths | Partial | Distinguish specialised algorithm from general Pareto implementation; test exact frontier and degeneracy. |
| S18-RT-11 | Skyline routes | Route-query product | Partial | Define dominance, duplicate handling and output semantics; distinguish algorithm from user-facing route set. |
| S18-RT-12 | Eco-routing | Route objective/application | Open | Specify emissions/energy model, vehicle and speed assumptions; validate against measured or authoritative model. |
| S18-RT-13 | Scenic routing | Route objective/application | Open | Define scenic evidence, aggregation and trade-off; evaluate bias and reproducibility. |
| S18-RT-14 | Safe routing | Route objective/application | Open | Define safety outcome, exposure and time dependence; avoid treating proxies as guaranteed safety. |
| S18-RT-15 | Bicycle level of traffic stress (LTS) | Active-mobility metric | Open | Verify canonical scoring levels and road attributes; document jurisdiction-specific calibration. |
| S18-RT-16 | Bicycle level of service (BLOS) | Active-mobility metric | Verify | Identify exact BLOS model/version and inputs; distinguish from LTS. |
| S18-RT-17 | Wheelchair-accessible routing | Accessibility-aware routing | Open | Define slope, surface, kerb, crossing and barrier constraints; include missing-data and user-profile uncertainty. |
| S18-RT-18 | Walkability-weighted paths | Route impedance model | Open | Define walkability impedance and scale; validate against observed route choice and accessibility needs. |
| S18-RT-19 | Path-size logit | Route-choice model | Partial | Existing overlap correction is tested; verify full choice-set probability model and parameter estimation. |
| S18-RT-20 | C-logit | Route-choice model | Partial | Existing commonality-factor baseline is tested; verify canonical commonality function and calibration. |
| S18-RT-21 | Stochastic user equilibrium | Traffic assignment model | Open | Specify equilibrium concept, stochastic perception and solution method; test convergence and conservation. |
| S18-RT-22 | Route diversity metrics | Network/choice metric | Open | Define path overlap/diversity measure and choice-set dependence; compare alternatives on known networks. |

### Public transport planning — page 37

| ID | Atomic item | Kind | Status | Required completion work |
|---|---|---|---|---|
| S18-PT-01 | Transit line planning | Transit optimisation | Open | Define line set, frequency, fleet and demand constraints; distinguish strategic and operational formulations. |
| S18-PT-02 | Transit network design problem | Network optimisation | Open | Specify decision variables, objective, demand assignment and budget; test benchmark instances. |
| S18-PT-03 | Stop spacing | Transit planning method | Open | Define access/egress, dwell, operating speed and demand assumptions; assess equity and local context. |
| S18-PT-04 | Stop consolidation | Transit planning method | Open | Define candidate removal, catchment and service impacts; test before/after accessibility. |
| S18-PT-05 | Bus-stop siting by set covering | Facility location / set cover | Open | Define demand points, coverage threshold and candidate sites; compare greedy and exact solutions. |
| S18-PT-06 | Timetable-based accessibility | Accessibility metric | Open | Define timetable, transfer, waiting and destination opportunities; test service-day and time-window semantics. |
| S18-PT-07 | Frequency-based accessibility | Accessibility metric | Open | State frequency and random-arrival assumptions; distinguish expected wait and transfer penalties. |
| S18-PT-08 | Transfer optimisation | Transit optimisation | Open | Define transfer edges, minimum interchange time and reliability; test feasible itineraries. |
| S18-PT-09 | Headway analysis | Service metric | Partial | Existing observed-departure and expected-wait metrics are bounded; add irregularity/reliability and schedule adherence. |
| S18-PT-10 | GTFS-Realtime processing | Data standard/workflow | Verify | Verify current GTFS-RT spec and version; implement feed validation, timestamps, entity relationships and stale-data checks. |
| S18-PT-11 | Transit equity analysis | Equity assessment | Open | Define population groups, opportunity metric and normative criteria; report distribution and uncertainty separately. |
| S18-PT-12 | RAPTOR timetable routing | Transit routing algorithm | Partial | Existing reference baseline is tested; verify round semantics, footpaths, transfer constraints and benchmark comparisons. |
| S18-PT-13 | Connection Scan Algorithm (CSA) | Transit routing algorithm | Partial | Existing earliest-arrival baseline is tested; verify connection ordering, transfer and footpath handling. |

### UAV and survey flight planning — page 38

| ID | Atomic item | Kind | Status | Required completion work |
|---|---|---|---|---|
| S18-UAV-01 | Ground sample distance (GSD) design | Photogrammetric calculation | Partial | Existing nadir GSD calculation is bounded; document sensor geometry, terrain and oblique-camera effects. |
| S18-UAV-02 | Forward overlap design | Survey planning calculation | Partial | Existing spacing baseline is tested; verify exposure interval, terrain and motion constraints. |
| S18-UAV-03 | Side overlap design | Survey planning calculation | Partial | Existing spacing baseline is tested; verify strip geometry, terrain and cross-track variation. |
| S18-UAV-04 | Corridor mapping flight design | Mission planning | Open | Define corridor buffer, turn geometry, overlap and legal/operational constraints. |
| S18-UAV-05 | Terrain-following flight | Mission planning/control | Open | Define DEM uncertainty, clearance, vertical dynamics and safety envelope; simulation required. |
| S18-UAV-06 | Camera-footprint coverage path planning | Coverage path planning | Open | Define footprint geometry, overlap, no-fly regions and coverage objective; test completeness. |
| S18-UAV-07 | Multi-UAV swarm coverage | Multi-agent planning | Open | Define task allocation, collision avoidance, communication loss and synchronisation; simulation and robustness tests. |
| S18-UAV-08 | Battery-aware routing | Resource-constrained routing | Open | Define battery model, payload, wind and reserve policy; test feasibility and energy prediction error. |

### Surface water, altimetry and river remote sensing — page 38

| ID | Atomic item | Kind | Status | Required completion work |
|---|---|---|---|---|
| S18-WA-01 | OCOG altimetry retracker | Radar altimetry retracking | Verify | Verify acronym/formulation and waveform assumptions; test against reference waveforms. |
| S18-WA-02 | Threshold retracker | Radar altimetry retracking | Open | Define threshold fraction and waveform conditioning; quantify sensitivity and bias. |
| S18-WA-03 | Brown-model retracker | Radar altimetry retracking | Verify | Verify Brown ocean waveform model and parameterisation; distinguish ocean from inland-water adaptation. |
| S18-WA-04 | Coastal altimetry processing | Altimetry workflow | Open | Define land contamination, waveform retracking and geophysical corrections; document mission-specific choices. |
| S18-WA-05 | SWOT KaRIn processing | Mission/product processing | Verify | Identify product level/version and official processing; distinguish mission pipeline from individual algorithm. |
| S18-WA-06 | RivWidth-style river-width extraction | River remote-sensing method | Verify | Identify exact method/version and centreline/edge rules; validate against independent reference widths. |
| S18-WA-07 | BAM discharge estimation | River discharge method | Verify | Resolve BAM expansion and exact model; document calibration and hydrological assumptions. |
| S18-WA-08 | MetroMan discharge estimation | River discharge method | Verify | Verify original method and inputs; compare against gauged discharge. |
| S18-WA-09 | Rating-curve discharge estimation | Hydrological estimator | Open | Define stage-discharge relation, hysteresis and extrapolation; quantify prediction intervals. |
| S18-WA-10 | Lake/reservoir water-level estimation | Water-level retrieval | Open | Define sensor, datum, retracking and temporal sampling; validate against gauges. |
| S18-WA-11 | Lake/reservoir storage estimation | Storage-volume model | Open | Define area-elevation/volume-elevation relation and bathymetry; quantify uncertainty. |
| S18-WA-12 | JRC Global Surface Water expert-system classification | Product/classification workflow | Verify | Identify product/version and classifier lineage; distinguish official product from a generic classifier. |
| S18-WA-13 | Floodplain mapping | Flood mapping workflow | Open | Define water extent, terrain/hydraulic inputs and event timing; assess cloud/vegetation limitations. |
| S18-WA-14 | Water occurrence mapping | Temporal water metric | Open | Define observation denominator, masking and sensor harmonisation; test missing observations. |
| S18-WA-15 | Water seasonality mapping | Temporal water metric | Open | Define seasonal period and recurrence rule; distinguish seasonality from occurrence. |

### Snow, ice and permafrost — page 38

| ID | Atomic item | Kind | Status | Required completion work |
|---|---|---|---|---|
| S18-IC-01 | MODSCAG-style fractional snow cover | Snow retrieval | Verify | Identify exact algorithm/product and sensor; test fractional cover against field/reference data. |
| S18-IC-02 | Passive-microwave snow water equivalent (SWE) | Snow retrieval | Open | Define frequency, emissivity and vegetation/deep-snow corrections; validate by region/season. |
| S18-IC-03 | LiDAR snow-depth estimation | Snow measurement | Open | Define snow-on/off differencing, co-registration and vertical datum; quantify uncertainty. |
| S18-IC-04 | Structure-from-motion snow-depth estimation | Photogrammetric measurement | Open | Define image acquisition, surface matching and georeferencing; validate against independent depth samples. |
| S18-IC-05 | SAR wet-snow detection | Radar classification | Open | Define backscatter/coherence change and incidence effects; validate by snow condition. |
| S18-IC-06 | Snow-albedo models | Radiative model family | Open | Identify model family and impurity/grain-size inputs; test energy-balance sensitivity. |
| S18-IC-07 | Debris-covered glacier mapping | Glacier remote sensing | Open | Define debris/ice classification and training evidence; validate against field or high-resolution reference. |
| S18-IC-08 | GlabTop ice-thickness inversion | Glacier inversion model | Verify | Verify model/version and stress-balance assumptions; compare with measured thickness. |
| S18-IC-09 | OGGM glacier modelling | Modelling framework | Verify | Identify OGGM version and component model; document calibration and mass-balance inputs. |
| S18-IC-10 | Huss–Farinotti ice-thickness inversion | Glacier inversion method | Verify | Verify exact formulation and input assumptions; test benchmark glaciers. |
| S18-IC-11 | Glacier outline delineation | Image interpretation/classification | Open | Define spectral/terrain rules and debris handling; validate inter-operator and temporal consistency. |
| S18-IC-12 | GRACE mascon mass-change estimation | Satellite gravimetry product/method | Verify | Identify product/version and leakage/scaling corrections; distinguish mascon solution from downstream basin estimate. |
| S18-IC-13 | Input-output ice-sheet mass balance | Mass-balance method | Open | Define input/output components, time interval and uncertainty; test mass conservation. |
| S18-IC-14 | Stefan equation permafrost/frost-depth model | Thermal conduction model | Verify | Verify boundary/initial conditions and latent heat assumptions; compare analytical cases. |
| S18-IC-15 | TTOP permafrost model | Permafrost model | Verify | Identify exact TTOP formulation and climate/terrain factors; validate against ground temperature. |
| S18-IC-16 | Active-layer thickness mapping | Permafrost metric/workflow | Open | Define thaw-depth observations, spatial model and season; validate against field measurements. |
| S18-IC-17 | InSAR thaw-subsidence monitoring | Deformation workflow | Open | Define coherence, reference, seasonal signal and attribution; validate with in-situ observations. |

### Vegetation radiative transfer and fluorescence — page 38

| ID | Atomic item | Kind | Status | Required completion work |
|---|---|---|---|---|
| S18-VEG-01 | DART 3D radiative transfer model | Software/model | Verify | Identify version, licence and supported scene physics; document integration rather than cloning. |
| S18-VEG-02 | SCOPE model | Canopy radiative/energy model | Verify | Identify version and coupled processes; document input/output and calibration. |
| S18-VEG-03 | Leaf chlorophyll retrieval | Biophysical retrieval | Open | Define spectral model, target and inversion; validate with laboratory/field measurements. |
| S18-VEG-04 | Hemispherical-photo LAI estimation | Canopy metric | Open | Define gap fraction and clumping corrections; test image threshold sensitivity. |
| S18-VEG-05 | Gap-fraction models | Canopy radiative model | Open | Specify angular distribution and canopy assumptions; test synthetic canopy geometries. |
| S18-VEG-06 | FLD sun-induced fluorescence retrieval | Fluorescence retrieval | Verify | Verify Fraunhofer Line Discrimination variant and spectral requirements; test atmospheric/spectral artefacts. |
| S18-VEG-07 | SFM sun-induced fluorescence retrieval | Fluorescence retrieval | Verify | Verify Spectral Fitting Method formulation; compare with synthetic spectra and FLD. |
| S18-VEG-08 | Farquhar–von Caemmerer–Berry (FvCB) photosynthesis model | Physiological model | Verify | Verify parameterisation and limiting assumptions; test assimilation response curves. |
| S18-VEG-09 | LiDAR canopy-structure retrieval | 3D remote-sensing workflow | Open | Define point-cloud metrics and crown/height inference; validate against field plots. |

### Emission estimation and atmospheric inversion — pages 38–39

| ID | Atomic item | Kind | Status | Required completion work |
|---|---|---|---|---|
| S18-EM-01 | XCO2 retrieval | Atmospheric retrieval | Open | Identify sensor/product algorithm and version; document spectroscopy, averaging kernels and uncertainty. |
| S18-EM-02 | OCO-2 carbon-flux inversion | Atmospheric inverse modelling | Verify | Identify inversion framework/product version; document transport, priors and observation operator. |
| S18-EM-03 | GOSAT carbon-flux inversion | Atmospheric inverse modelling | Verify | Identify inversion/product and version; distinguish satellite retrieval from flux inversion. |
| S18-EM-04 | Methane emission inversion | Atmospheric inverse modelling | Open | Define observations, transport model, prior and regularisation; test synthetic plume/flux recovery. |
| S18-EM-05 | NOx emission estimation by divergence methods | Emissions estimation | Open | Define wind field, column density and divergence operator; assess boundary and transport assumptions. |
| S18-EM-06 | TROPOMI oversampling | Satellite aggregation method | Verify | Verify oversampling kernel, weighting and product version; test sampling/coverage bias. |
| S18-EM-07 | Wind-rotation method | Plume/emissions method | Verify | Resolve exact method and assumptions; test wind alignment and plume geometry. |
| S18-EM-08 | EMG point-source plume fitting | Plume fitting | Verify | Define exponentially modified Gaussian variant and fit constraints; test synthetic plume recovery. |
| S18-EM-09 | Plume-based flux quantification | Emissions estimator | Open | Define enhancement integration, wind and plume mask; quantify uncertainty and failure cases. |
| S18-EM-10 | Log-law wind profile | Wind profile model | Open | State surface-layer assumptions, roughness and stability corrections; test units and height domain. |
| S18-EM-11 | Power-law wind profile | Wind profile model | Open | Define exponent calibration and height reference; compare to log-law and measured profiles. |
| S18-EM-12 | Weibull wind-speed fit | Distribution model | Open | Define parameter estimation and goodness-of-fit; test censored/zero/seasonal samples. |
| S18-EM-13 | WindNinja mass-consistent wind model | Software/model | Verify | Identify version and solver; document terrain/forcing and limits; no unsupported reproduction claim. |
| S18-EM-14 | CFD wind downscaling | Numerical modelling workflow | Open | Define governing equations, boundary conditions and mesh; validate against observations and convergence. |

### Structural geology and directional statistics — pages 38–39

| ID | Atomic item | Kind | Status | Required completion work |
|---|---|---|---|---|
| S18-GE-01 | Circular mean and resultant length | Circular statistic | Partial | Existing summaries are tested; verify weighting and undefined-resultant handling. |
| S18-GE-02 | Rayleigh test | Circular uniformity test | Partial | Existing baseline is tested; verify sample-size correction and power/assumption limits. |
| S18-GE-03 | von Mises distribution | Circular probability model | Partial | Existing density baseline is tested; verify normalisation and concentration parameter estimation. |
| S18-GE-04 | Kuiper test | Circular uniformity test | Partial | Existing baseline is tested; verify finite-sample calibration and tie handling. |
| S18-GE-05 | Watson U-squared test | Circular uniformity test | Partial | Existing baseline is tested; verify correction and critical-value convention. |
| S18-GE-06 | Rose diagram analysis | Circular visual summary | Partial | Existing weighted histogram is tested; define bin origin, width, normalisation and area convention. |
| S18-GE-07 | Fisher spherical distribution | Spherical probability model | Open | Verify directional distribution on sphere, concentration and normalisation; test rotational invariance. |
| S18-GE-08 | Kent spherical distribution | Spherical probability model | Open | Verify ovalness parameterisation and admissible parameter domain; test limiting Fisher case. |
| S18-GE-09 | Bingham spherical distribution | Axial probability model | Open | Verify antipodal symmetry and parameter identifiability; test normalisation and axial data. |
| S18-GE-10 | Stereonet analysis | Structural-geology workflow | Open | Define projection (equal-area/equal-angle), orientation convention and statistical overlays. |
| S18-GE-11 | Plane fitting to point clouds | Geometric fitting | Partial | Existing RANSAC plane fit is bounded; add orientation/uncertainty and robust residual validation. |
| S18-GE-12 | Discontinuity-set extraction | Point-cloud structural analysis | Open | Define normal clustering, scale and outlier handling; validate against interpreted scanlines. |
| S18-GE-13 | Fracture-network analysis | Network analysis | Open | Define fracture traces/nodes and censoring; report sampling and scale effects. |
| S18-GE-14 | Discrete fracture network (DFN) generation | Stochastic geological modelling | Open | Define distributions, conditioning and truncation; test statistics against target field data. |
| S18-GE-15 | Kinematic slope-stability analysis | Geomechanical analysis | Open | Define discontinuity geometry, slope orientation and failure modes; require engineering validation. |
| S18-GE-16 | Geological cross-section construction | Geological modelling workflow | Open | Define horizons, faults, constraints and uncertainty; document interpretation. |
| S18-GE-17 | Fault-network modelling | Geological network model | Open | Define topology, geometry and structural hierarchy; validate against mapped data. |
| S18-GE-18 | RBF implicit geological modelling | Implicit surface modelling | Open | Specify basis, regularisation, constraints and extrapolation; test known surfaces. |
| S18-GE-19 | Potential-field implicit geological modelling | Implicit geological modelling | Open | Define field function, constraints and geological assumptions; test synthetic stratigraphy. |

### Data-quality statistics for spatial data — page 39

| ID | Atomic item | Kind | Status | Required completion work |
|---|---|---|---|---|
| S18-DQ-01 | Spatial multiple imputation | Missing-data inference | Open | Define spatial dependence, missingness mechanism and uncertainty pooling; validate on masked synthetic fields. |
| S18-DQ-02 | Multiple imputation by chained equations (MICE) | Multiple imputation framework | Verify | Verify implementation/version and conditional models; document compatibility and spatial dependence limitations. |
| S18-DQ-03 | k-nearest-neighbour imputation | Imputation algorithm | Open | Define distance, feature scaling and spatial/time constraints; test missingness and leakage. |
| S18-DQ-04 | missForest | Imputation software/method | Verify | Identify package/version and algorithm; document mixed-type handling and out-of-bag error. |
| S18-DQ-05 | Gaussian-process imputation | Spatial statistical model | Open | Define kernel, observation noise and predictive uncertainty; test calibration and scalability. |
| S18-DQ-06 | Berrocal-style downscaler fusion | Spatial downscaling model | Verify | Identify exact model/paper and variant; document change-of-support and covariate assumptions. |
| S18-DQ-07 | Spatial misalignment model | Spatial data integration model | Open | Define latent process and observation supports; test known displacement and aggregation effects. |
| S18-DQ-08 | Change-of-support modelling | Spatial statistical framework | Open | Define areal/point support transformations and covariance integration; compare exact and approximate cases. |
| S18-DQ-09 | Berkson measurement error | Measurement-error model | Open | Define latent/observed relationship and error assumptions; compare bias/variance to classical error. |
| S18-DQ-10 | Classical measurement error | Measurement-error model | Open | Define error distribution and identification; test attenuation and spatially structured error. |
| S18-DQ-11 | Ecological-fallacy diagnostics | Inference diagnostic | Open | Define aggregation sensitivity and inferential target; demonstrate limits without claiming a universal test. |
| S18-DQ-12 | Diggle-style preferential sampling | Spatial sampling model | Verify | Identify exact preferential-sampling formulation; define joint point-process/response model and identifiability. |
| S18-DQ-13 | Informative sampling | Sampling model | Open | Define inclusion process and target estimand; compare design- and model-based correction. |
| S18-DQ-14 | Spatial selection-bias correction | Bias correction | Open | Define selection mechanism, positivity and target population; test sensitivity to unobserved selection. |
| S18-DQ-15 | Aitchison geometry | Compositional geometry | Partial | Existing closure/CLR/Aitchison distance baselines are tested; add full geometric properties and zero-aware treatment. |
| S18-DQ-16 | Log-ratio transforms | Compositional transformation | Partial | Existing CLR is bounded; add ILR/ALR, basis conventions and inverse transforms. |
| S18-DQ-17 | Compositional kriging | Geostatistical model | Open | Define simplex-valued process and variogram/covariance in log-ratio space; test closure and uncertainty. |
| S18-DQ-18 | Gaussian graphical models | Graphical statistical model | Open | Define precision estimation and sparsity; validate graph recovery on known Gaussian fields. |
| S18-DQ-19 | Spatial Bayesian networks | Probabilistic graphical model | Open | Define directed acyclic structure, spatial dependence and inference; distinguish from undirected GMRF. |
| S18-DQ-20 | Causal discovery on spatial data | Research family | Open | Split by assumptions and method family; address spatial confounding, interference and temporal ordering. |

### Spatial humanities — page 39

| ID | Atomic item | Kind | Status | Required completion work |
|---|---|---|---|---|
| S18-HU-01 | Georeferencing historical texts | Digital humanities workflow | Open | Define gazetteer, uncertainty and temporal place identity; validate with historical reference cases. |
| S18-HU-02 | Spatial narrative extraction | NLP/spatial information extraction | Open | Define entities, relations and narrative scope; evaluate against annotated texts. |
| S18-HU-03 | Literary GIS | Research/application field | Not applicable | Document scope, data ethics and interpretive methods; do not invent a single algorithm. |
| S18-HU-04 | Deep mapping | Research/methodological framework | Not applicable | Define layers, provenance and interpretive plurality; document as framework. |
| S18-HU-05 | Place-based corpus analysis | Text/spatial analysis workflow | Open | Define corpus, place disambiguation and spatial aggregation; evaluate extraction quality and bias. |

## Completion gates

1. Verify each named index, algorithm, statistical model and product against original papers, official specifications or maintained project documentation; record exact title, authors/organisation, version and stable link.
2. Split product pipelines (SWOT, JRC GSW, OCO-2/GOSAT), modelling frameworks (OGGM, DART, SCOPE, WindNinja) and methodological families from the algorithms they contain.
3. State spatial/temporal support, CRS, units, sensor band/frequency, model assumptions, calibration domain and uncertainty for every applicable record.
4. Implement only methods with a stable technical contract. Keep proprietary, large-system or high-cost methods as documented integrations where appropriate.
5. Test against analytic fixtures, synthetic truth, published reference outputs, field measurements or independent maintained implementations. Include boundary, degenerate and adversarial cases.
6. Provide canonical explanations and reproducible learning labs where they materially improve understanding; notebooks do not replace tests.
7. Review privacy for moving trajectories, UAV missions and sensitive infrastructure; review licences for data, software and imagery.
8. Reconcile the 22 section indexes, source dashboard, coverage matrix and roadmap only after the evidence has changed.

## Execution priorities

1. Complete exact identity and primary-source verification for specialised indexes, routing accelerators, altimetry retrackers, glacier models and atmospheric retrieval systems.
2. Build independent analytic baselines for water-level/discharge, permafrost, directional distributions, measurement error and compositional methods where the contracts are clear.
3. Treat mission products and software platforms as versioned reproducible integrations rather than clones.
4. Add cross-cutting validation for time-dependent routes, uncertainty-aware moving-object queries, transit feeds and remote-sensing data lineage.
5. Keep Section 18 open until every child has an evidence-backed disposition and all applicable tests, lessons, examples and rights reviews are complete.

**Current conclusion:** Section 18 is decomposed into atomic review items. It remains open; this register is traceability infrastructure, not verification or completion.
