# Section 10 atomic completion register

**Source:** *Spatial Analysis Algorithms: Complete Compendium*, Section 10, pages 21–23.  
**Intake:** [preserved pages 21–25 transcription](../source-inventory/pages-21-25.md).  
**Section index:** [Section 10 catalogue record](../catalog/sections/10-classical-statistical-computational-additions.md).

> Section 10 extends earlier foundational topics. This register splits grouped rows into named algorithms, estimators, metrics, workflows and datasets. Existing implementations are bounded to the exact variants documented in the catalogue; this register does not certify full source-entry completion.

## Status policy

Apply the [source-entry verification protocol](../catalog/verification-protocol.md) and [compendium completion standard](compendium-completion-standard.md). Preserve relationships to Sections 1–9 and do not duplicate foundational lessons unnecessarily.

| Status | Meaning |
|---|---|
| Open | No item-specific evidence recorded. |
| Partial | A bounded implementation or canonical record exists; variants/review remain. |
| Verify | Exact name, variant or reference must be resolved. |
| Not applicable | A workflow, data model or broad application is not one standalone algorithm. |

## Atomic source register

### Rasterisation and low-level geometry — page 21

| ID | Atomic item | Kind | Status | Required completion work |
|---|---|---|---|---|
| S10-RG-01 | Bresenham line rasterisation | Rasterisation algorithm | Partial | Existing package tested; verify octant symmetry, endpoint inclusion and integer tie rules. |
| S10-RG-02 | Digital Differential Analyzer (DDA) line rasterisation | Rasterisation algorithm | Partial | Existing package tested; verify rounding and endpoint conventions. |
| S10-RG-03 | Xiaolin Wu anti-aliased line | Rasterisation algorithm | Partial | Existing package tested; verify intensity coverage and endpoint handling. |
| S10-RG-04 | Scanline polygon fill | Rasterisation algorithm | Partial | Existing package tested; verify vertex inclusion, horizontal edges and fill rule. |
| S10-RG-05 | Supercover line rasterisation | Rasterisation algorithm | Partial | Existing package tested; verify all intersected cells and corner-touch convention. |
| S10-RG-06 | Cohen–Sutherland clipping | Line clipping algorithm | Partial | Existing package tested; verify outcode and degenerate cases. |
| S10-RG-07 | Liang–Barsky clipping | Line clipping algorithm | Partial | Existing package tested; verify parametric interval and parallel edges. |
| S10-RG-08 | Cyrus–Beck clipping | Line clipping algorithm | Partial | Existing package tested; verify convex-window half-plane assumptions. |
| S10-RG-09 | Nicholl–Lee–Nicholl clipping | Line clipping algorithm | Partial | Existing implementation restricted to rectangular windows; verify region cases and boundary handling. |
| S10-RG-10 | Reumann–Witkam simplification | Line simplification | Partial | Existing package tested; verify strip width and endpoint preservation. |
| S10-RG-11 | Lang simplification | Line simplification | Partial | Existing package tested; verify look-ahead distance and tolerance. |
| S10-RG-12 | Opheim simplification | Line simplification | Partial | Existing constrained moving-strip baseline tested; verify original variant and parameter contract. |
| S10-RG-13 | Zhao–Saalfeld simplification | Line simplification | Partial | Existing narrow-sleeve baseline tested; verify deviation and topology assumptions. |
| S10-RG-14 | Visvalingam–Whyatt simplification | Line simplification | Partial | Existing effective-area implementation tested; verify heap/update and threshold semantics. |
| S10-RG-15 | Chaikin corner cutting | Curve smoothing | Partial | Existing curve package tested; document endpoint and closed-ring behaviour. |
| S10-RG-16 | Catmull–Rom splines | Curve interpolation | Partial | Existing implementation tested; verify parameterisation and endpoint tangents. |
| S10-RG-17 | B-splines | Curve representation | Partial | Existing package tested; document degree, knot vector and boundary conditions. |
| S10-RG-18 | NURBS | Rational spline representation | Partial | Existing package tested; verify weights, knot conventions and projective invariance. |
| S10-RG-19 | Schneider recursive Bezier fitting | Curve fitting algorithm | Partial | Existing package tested; verify error metric, split selection and termination. |
| S10-RG-20 | Kalman filtering | State estimation | Partial | Existing linear-Gaussian filter is bounded; verify covariance and process/measurement conventions. |
| S10-RG-21 | Rauch–Tung–Striebel (RTS) smoothing | State smoothing | Partial | Existing curve package contains a linear-Gaussian smoother; add independent batch posterior oracle. |
| S10-RG-22 | MMP exact polyhedral geodesics | Mesh geodesic algorithm | Verify | Verify Mitchell–Mount–Papadimitriou method and exactness; benchmark polyhedral shortest paths. |
| S10-RG-23 | Chen–Han exact geodesics | Mesh geodesic algorithm | Verify | Verify exact algorithm/variant and window propagation; compare to MMP. |
| S10-RG-24 | Fast marching on triangle meshes | Numerical geodesic method | Open | Define Eikonal discretisation and obtuse-triangle handling; compare with exact geodesics. |
| S10-RG-25 | ISEA3H grid | Discrete global grid system | Verify | Verify projection/subdivision and cell addressing; document exact DGGS specification. |
| S10-RG-26 | rHEALPix grid | Discrete global grid system | Verify | Verify projection, hierarchy and indexing; test equal-area and polar behaviour. |
| S10-RG-27 | DGGRID software | DGGS software | Verify | Identify version and supported grid systems; document integration/licence. |
| S10-RG-28 | Hierarchical triangular mesh (HTM) | Spherical indexing structure | Verify | Verify cell hierarchy, IDs and boundary predicates; test spherical coverage. |
| S10-RG-29 | Hexagonal grid operations | Grid operations family | Open | Split adjacency, hierarchy, traversal and overlay operations; specify grid system and edge semantics. |

### Time series and change detection — page 21

| ID | Atomic item | Kind | Status | Required completion work |
|---|---|---|---|---|
| S10-TS-01 | CUSUM change detection | Sequential detector | Partial | Existing detector tested; document reference mean, allowance and ARL calibration. |
| S10-TS-02 | PELT | Change-point optimisation | Partial | Existing mean-shift implementation tested; verify penalty/pruning and supported cost functions. |
| S10-TS-03 | Binary segmentation | Change-point algorithm | Partial | Existing implementation tested; document greedy split and multiple-change limitations. |
| S10-TS-04 | BEAST | Bayesian time-series decomposition/change detection | Verify | Identify exact BEAST software/version and model; document trend/seasonality priors. |
| S10-TS-05 | Bayesian online change-point detection (BOCPD) | Bayesian sequential detector | Partial | Existing conjugate-Gaussian baseline tested; verify hazard function and non-conjugate variants. |
| S10-TS-06 | STL decomposition | Time-series decomposition | Partial | Existing package tested; verify seasonal window/robust options and boundary behaviour. |
| S10-TS-07 | Prophet | Forecasting software/model | Verify | Identify version and component model; document holidays/changepoints and licence. |
| S10-TS-08 | Theil–Sen trend estimator | Robust trend estimator | Partial | Existing implementation tested; verify median-slope convention and confidence intervals. |
| S10-TS-09 | Pettitt change-point test | Nonparametric change test | Partial | Existing implementation tested; verify exact statistic and p-value approximation. |
| S10-TS-10 | ARIMA | Time-series forecasting model | Partial | Existing ARIMA/SARIMA package tested; document order selection, stationarity and diagnostics. |
| S10-TS-11 | Kalman filtering of EO series | State-space time-series workflow | Partial | Generic linear filter exists; define EO observation/missingness and seasonal state models. |
| S10-TS-12 | Hidden Markov model for map matching | Probabilistic sequence model | Partial | Existing HMM/Viterbi baseline is generic; define road-network transition/emission model and route truth. |
| S10-TS-13 | Viterbi decoding | Dynamic programming algorithm | Partial | Existing decoder tested; verify log-domain stability and tie handling. |
| S10-TS-14 | HMM for land-cover trajectories | Temporal classification model | Open | Define state taxonomy, transition constraints and observation likelihood; test temporal smoothing. |

### Forecast verification and nowcasting — page 21

| ID | Atomic item | Kind | Status | Required completion work |
|---|---|---|---|---|
| S10-FV-01 | Fractions Skill Score (FSS) | Spatial forecast metric | Partial | Existing regular-grid square-neighbourhood implementation tested; verify threshold/scale conventions. |
| S10-FV-02 | Neighbourhood verification | Forecast verification framework | Partial | Existing FSS covers one method; add neighbourhood ensembles and scale sensitivity. |
| S10-FV-03 | SAL structure score | Object-based forecast metric | Partial | Existing bounded SAL baseline; verify object identification and reference parity. |
| S10-FV-04 | SAL amplitude score | Object-based forecast metric | Partial | Existing bounded SAL baseline; verify domain aggregation and normalisation. |
| S10-FV-05 | SAL location score | Object-based forecast metric | Partial | Existing bounded SAL baseline; verify centroid/volume displacement terms. |
| S10-FV-06 | MODE object-based verification | Forecast verification method | Partial | Existing MODE-inspired extraction/matching baseline; verify reference implementation and matching. |
| S10-FV-07 | Equitable Threat Score (ETS) | Categorical forecast metric | Partial | Existing metrics package tested; verify random-hit correction and contingency table. |
| S10-FV-08 | Probability of Detection (POD) | Categorical forecast metric | Partial | Existing metrics package tested; document zero-denominator handling. |
| S10-FV-09 | False Alarm Ratio (FAR) | Categorical forecast metric | Partial | Existing metrics package tested; distinguish from false-alarm rate. |
| S10-FV-10 | Critical Success Index (CSI) | Categorical forecast metric | Partial | Existing metrics package tested; verify contingency convention. |
| S10-FV-11 | Brier Skill Score | Probabilistic forecast metric | Partial | Existing implementation tested; document reference forecast and decomposition. |
| S10-FV-12 | ROC curve and AUC | Probabilistic classification metric | Partial | Existing tied-rank AUC tested; add threshold convention and confidence intervals. |
| S10-FV-13 | CRPS decomposition | Probabilistic forecast metric | Partial | Existing finite-threshold reliability/resolution/uncertainty decomposition is bounded; verify reference identity and truncation error. |
| S10-FV-14 | Rank histograms | Ensemble calibration diagnostic | Partial | Existing expected-rank histogram tested; verify tie randomisation and sample uncertainty. |
| S10-FV-15 | Lucas–Kanade optical flow | Motion estimation | Partial | Existing package tested; verify sparse/dense variants and brightness-constancy assumptions. |
| S10-FV-16 | Farnebäck optical flow | Dense motion estimation | Partial | Existing OpenCV-backed implementation tested; record version and parameter settings. |
| S10-FV-17 | DIS optical flow | Dense motion estimation | Partial | Existing OpenCV-backed implementation tested; record preset/version and limits. |
| S10-FV-18 | Variational optical flow (TV-L1) | Dense motion estimation | Partial | Existing scikit-image TV-L1 baseline tested; verify regularisation and boundary conditions. |

### Spatial cross-validation and sampling — pages 21–22

| ID | Atomic item | Kind | Status | Required completion work |
|---|---|---|---|---|
| S10-CV-01 | Nearest-neighbour distance matching (NNDM) | Spatial CV design | Partial | Existing projected-Euclidean greedy LOO baseline tested; verify reference algorithm and geographic-distance variants. |
| S10-CV-02 | k-nearest-neighbour distance matching (kNNDM) | Spatial CV design | Partial | Existing KMeans/Euclidean k-fold candidate tested; verify exact reference equivalence and spatial metric. |
| S10-CV-03 | Buffered leave-one-out | Spatial CV design | Partial | Existing splitter tested; define buffer distance and fold feasibility. |
| S10-CV-04 | Cluster-based spatial k-fold | Spatial CV design | Partial | Existing deterministic cluster splitter tested; assess cluster size and spatial separation. |
| S10-CV-05 | blockCV | R package/software | Verify | Identify package/version and exact split methods; distinguish software from design principles. |
| S10-CV-06 | Spatial-temporal leave-out | Spatiotemporal validation design | Partial | Existing strict location/time pair-fold baseline tested; verify reference semantics and buffers. |
| S10-CV-07 | Bayesian optimisation on spatial fields | Adaptive design | Partial | Existing GP-UCB selection is bounded; add posterior utility optimisation and calibration. |
| S10-CV-08 | Multi-armed bandits for survey design | Adaptive sampling | Partial | Existing UCB1 baseline is bounded; spatially correlated rewards and regret remain open. |
| S10-CV-09 | Adaptive cluster sampling | Survey design | Partial | Existing adaptive expansion baseline tested; verify inclusion probabilities and design-based variance. |
| S10-CV-10 | Active learning for map validation | Active learning workflow | Partial | Existing uncertainty/cost selection is bounded; complete annotation/retraining loop and independent validation. |
| S10-CV-11 | Maximum Mean Discrepancy (MMD) | Two-sample statistic | Partial | Existing unbiased MMD and block permutation baselines tested; verify kernel selection and spatial exchangeability assumptions. |
| S10-CV-12 | Energy distance | Two-sample statistic | Partial | Existing statistic tested; verify finite-sample convention and block permutation validity. |
| S10-CV-13 | Domain divergence metrics | Distribution-shift metric family | Partial | Existing MMD/energy and NN applicability envelope are bounded; add calibrated domain classifier/KMM methods. |

### Geophysical gridding and potential fields — page 22

| ID | Atomic item | Kind | Status | Required completion work |
|---|---|---|---|---|
| S10-GP-01 | Minimum-curvature gridding | Gridding method | Partial | Existing fixed-perimeter discrete biharmonic solver is bounded; verify Briggs scattered-data formulation. |
| S10-GP-02 | Nearest-neighbour gridding | Interpolation method | Partial | Existing package tested; document tie and extrapolation semantics. |
| S10-GP-03 | Delaunay triangulation gridding | Interpolation method | Partial | Existing linear triangulation interpolation tested; test hull boundaries and degeneracy. |
| S10-GP-04 | Ordinary kriging comparison baseline | Geostatistical interpolation | Partial | Existing fixed-covariance ordinary kriging tested; fitted variogram and fair benchmark remain open. |
| S10-GP-05 | Analytic signal amplitude | Potential-field attribute | Partial | Existing spectral derivative package tested; verify 2D/3D formulation and noise sensitivity. |
| S10-GP-06 | Tilt derivative | Potential-field attribute | Partial | Existing implementation tested; verify sign and zero-crossing interpretation. |
| S10-GP-07 | Euler deconvolution | Potential-field source estimation | Partial | Existing bounded implementation; verify structural index, windowing and source geometry. |
| S10-GP-08 | Werner deconvolution | Potential-field source estimation | Partial | Existing single-thin-dike baseline is bounded; verify full variants and model assumptions. |
| S10-GP-09 | Matched filtering | Potential-field spectral method | Partial | Existing supplied-model bandpass decomposition is bounded; verify source-spectrum fitting. |
| S10-GP-10 | Upward continuation | Potential-field transform | Partial | Existing spectral implementation tested; verify grid padding and height units. |
| S10-GP-11 | Downward continuation | Potential-field transform | Partial | Existing regularised implementation tested; quantify instability and regularisation. |
| S10-GP-12 | Vertical derivatives | Potential-field attribute | Partial | Existing spectral derivatives tested; verify sign/frequency conventions. |
| S10-GP-13 | Horizontal derivatives | Potential-field attribute | Partial | Existing spectral derivatives tested; verify axis and units. |
| S10-GP-14 | Airborne electromagnetic inversion | Geophysical inversion workflow | Open | Identify forward model, instrument and inversion regularisation; validate synthetic responses. |
| S10-GP-15 | Magnetotelluric inversion | Geophysical inversion workflow | Open | Define 1D/2D/3D formulation, impedance convention and regularisation; benchmark synthetic Earth models. |
| S10-GP-16 | Seismic attribute analysis | Seismic interpretation workflow | Open | Split attributes (coherence, curvature, amplitude etc.); define data conditioning and interpretation. |
| S10-GP-17 | Receiver-function analysis | Seismic analysis method | Open | Define deconvolution, phase picking and velocity model; test synthetic layered models. |

### Urban microclimate and energy — page 22

| ID | Atomic item | Kind | Status | Required completion work |
|---|---|---|---|---|
| S10-UM-01 | SOLWEIG | Urban radiation software | Verify | Verify version, model physics and licence; distinguish platform from MRT output. |
| S10-UM-02 | UMEP | Urban climate software/toolbox | Verify | Verify version, modules and licence; document data requirements. |
| S10-UM-03 | ENVI-met | Urban microclimate software | Verify | Verify current version, physics and licence; document reproducibility. |
| S10-UM-04 | Mean radiant temperature (MRT) | Thermal comfort metric | Partial | Existing globe-based ISO 7726 estimate is bounded; add radiative-flux/view-factor formulation. |
| S10-UM-05 | UTCI | Thermal comfort index | Open | Verify official polynomial/model and input domain; test reference examples. |
| S10-UM-06 | Physiological Equivalent Temperature (PET) | Thermal comfort index | Open | Verify model and physiological inputs; compare reference cases. |
| S10-UM-07 | RANS street-canyon modelling | CFD method | Open | Define turbulence closure and boundary conditions; validate against wind-tunnel/field data. |
| S10-UM-08 | LES street-canyon modelling | CFD method | Open | Define subgrid model and resolution; quantify convergence and computational cost. |
| S10-UM-09 | Lattice Boltzmann street-canyon modelling | CFD method | Open | Define collision/streaming scheme and boundary treatment; compare with Navier–Stokes reference. |
| S10-UM-10 | Pedestrian wind comfort | Urban wind assessment | Open | Verify comfort/safety criteria and averaging; document jurisdiction-specific thresholds. |
| S10-UM-11 | SWMM | Stormwater modelling software | Verify | Identify version and modules; document licence and calibration. |
| S10-UM-12 | 1D–2D coupled urban flood models | Hydrodynamic modelling workflow | Open | Define coupling, exchange and boundary conditions; validate benchmark flood events. |
| S10-UM-13 | Low-impact development siting | Spatial optimisation workflow | Open | Define hydrology, land suitability, cost and equity constraints; test scenarios. |
| S10-UM-14 | Archetype-based building energy simulation | Building energy model | Open | Define archetypes, schedules and envelope; calibrate against metered data. |
| S10-UM-15 | CityBES | Building energy software/platform | Verify | Identify version and model pipeline; document data and licence. |
| S10-UM-16 | Shading computation | 3D solar geometry method | Open | Define sun path, geometry and temporal integration; test analytic cases. |
| S10-UM-17 | View-factor computation | Radiative geometry method | Open | Define surfaces, visibility and reciprocity; test closed-form geometries. |

### Environmental monitoring and MRV — page 22

| ID | Atomic item | Kind | Status | Required completion work |
|---|---|---|---|---|
| S10-MRV-01 | GLAD deforestation alerts | Monitoring system | Verify | Identify current product/version, alert logic and licence; distinguish alert product from method. |
| S10-MRV-02 | RADD forest disturbance alerts | Monitoring system | Verify | Identify exact release and radar methodology; document detection delay and uncertainty. |
| S10-MRV-03 | SAR–optical forest-loss fusion | Change-detection workflow | Open | Define sensor harmonisation, cloud gaps and fusion; test event detection. |
| S10-MRV-04 | Forest carbon-stock mapping | Carbon estimation workflow | Open | Define allometry, biomass, carbon fraction and uncertainty; validate against plots. |
| S10-MRV-05 | REDD+ monitoring, reporting and verification | MRV framework/workflow | Not applicable | Document applicable standard, reference level and uncertainty; not a single algorithm. |
| S10-MRV-06 | Soil-carbon mapping | Spatial estimation workflow | Open | Define depth, lab measurements and covariates; validate spatially. |
| S10-MRV-07 | Additionality analysis | Carbon project evaluation | Open | Define counterfactual baseline and leakage; document causal assumptions. |
| S10-MRV-08 | Leakage analysis | Carbon accounting method | Open | Define spatial displacement boundary and monitoring; test sensitivity. |
| S10-MRV-09 | Matched-filter methane plume detection | Remote-sensing detector | Partial | Existing synthetic matched-filter baseline is bounded; validate against sensor-specific radiance/noise. |
| S10-MRV-10 | Deep plume segmentation | ML segmentation workflow | Open | Identify architecture/checkpoint and plume labels; test domain shift and false negatives. |
| S10-MRV-11 | Integrated Mass Enhancement (IME) | Emissions metric | Partial | Existing arithmetic baseline tested; verify plume mask, background and uncertainty treatment. |
| S10-MRV-12 | Cross-sectional flux | Emissions estimator | Partial | Existing bounded calculation tested; verify wind profile and cross-section placement. |
| S10-MRV-13 | Gaussian plume inversion | Atmospheric inverse model | Partial | Existing fixed-geometry column-plume inversion bounded; test transport assumptions and identifiability. |
| S10-MRV-14 | Vessel behaviour classification | Maritime analytics | Open | Define behaviour classes, AIS gaps and label provenance; address class imbalance. |
| S10-MRV-15 | AIS gap detection | Maritime data quality | Partial | Existing reporting-gap and implied-speed screening tested; distinguish outages from suspicious behaviour. |
| S10-MRV-16 | Fishing-effort mapping from SAR/AIS | Maritime remote-sensing workflow | Open | Define vessel matching, fishing inference and effort unit; validate against independent data. |
| S10-MRV-17 | Chlorophyll indices | Water-quality metric family | Open | Split sensor-specific formulas and bands; validate against in-situ chlorophyll. |
| S10-MRV-18 | Turbidity indices | Water-quality metric family | Open | Define band/model and water type; validate against field measurements. |
| S10-MRV-19 | Cyanobacteria indices | Water-quality metric family | Open | Identify sensor-specific index and bloom conditions; assess false alarms. |

### Population and social data — pages 22–23

| ID | Atomic item | Kind | Status | Required completion work |
|---|---|---|---|---|
| S10-PS-01 | Top-down dasymetric population mapping | Population disaggregation | Partial | Existing conservative weighted allocation tested; document ancillary weights and source-total conservation. |
| S10-PS-02 | Bottom-up microcensus population estimation | Population estimation | Open | Define sampling frame, expansion weights and uncertainty; validate coverage. |
| S10-PS-03 | Building-based population disaggregation | Population allocation | Partial | Existing residential floor-area × occupancy baseline tested; validate occupancy and building completeness. |
| S10-PS-04 | Settlement-level population estimation | Population estimation | Open | Define settlement boundaries, sample and expansion model; report uncertainty. |
| S10-PS-05 | Synthetic spatial microdata | Privacy-preserving data synthesis | Partial | Existing IPF/raking donor resampling is bounded; it does not generate novel attribute combinations or geographies. |
| S10-PS-06 | Spatial k-anonymity for census | Spatial privacy method | Partial | Existing adaptive quadtree generalisation is bounded; assess composition and linkage attacks. |
| S10-PS-07 | Differential privacy for aggregates | Privacy mechanism | Partial | Existing user-level Laplace and basic accountant are bounded; verify adjacency, composition and privacy budget. |
| S10-PS-08 | Reardon–Firebaugh multigroup segregation indices | Segregation metric | Partial | Existing multigroup entropy implementation tested; verify decompositions and weighting. |
| S10-PS-09 | Spatial exposure indices | Segregation metric family | Partial | Existing areal exposure metric bounded; add spatially weighted/interaction variants. |
| S10-PS-10 | Shannon diversity | Diversity metric | Partial | Existing population diversity metric tested; define normalisation and zero handling. |
| S10-PS-11 | Simpson diversity | Diversity metric | Partial | Existing population diversity metric tested; distinguish concentration and diversity forms. |

## Completion gates

1. Verify each named algorithm, test, metric, software product and data collection against primary/official sources.
2. Preserve exact numerical conventions, thresholds, coordinate systems, temporal support and boundary conditions.
3. For forecast metrics, define event threshold, neighbourhood, reference forecast and uncertainty; do not conflate related scores.
4. For geophysical inversions, document forward model, regularisation, identifiability and physical validity.
5. For microclimate and hazard workflows, document calibration, model domain and operational limitations.
6. For population, maritime and carbon data, require privacy, licensing and provenance review.
7. Test implementations against analytic cases, independent libraries, synthetic truth and domain-specific reference datasets.
8. Reconcile cross-links to Sections 1–9 rather than duplicate canonical lessons; update coverage/dashboard only after evidence review.

**Current conclusion:** Section 10 is decomposed into atomic review items. It remains open; existing packages cover bounded variants and do not close every source family.
