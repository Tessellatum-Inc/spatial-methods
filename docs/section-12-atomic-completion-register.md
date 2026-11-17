# Section 12 atomic completion register

**Source:** *Spatial Analysis Algorithms: Complete Compendium*, Section 12, pages 24–26.  
**Intake:** [preserved pages 21–25 transcription](../source-inventory/pages-21-25.md) and [pages 26–30](../source-inventory/pages-26-30.md).  
**Section index:** [Section 12 catalogue record](../catalog/sections/12-signal-gnss-regional-science.md).

> The source frames these as methods borrowed from adjacent fields. Verify exact model, estimator, test, product and implementation variants. This register is a child-level traceability backlog; existing records cover only the explicitly described scope.

## Status policy

Apply the [source-entry verification protocol](../catalog/verification-protocol.md) and [compendium completion standard](compendium-completion-standard.md). Separate estimators, model families, data products, software and workflows. For geodesy and integrity monitoring, do not overstate operational certification.

| Status | Meaning |
|---|---|
| Open | No item-specific evidence recorded. |
| Partial | A bounded implementation exists; variants or review remain open. |
| Verify | Exact named method, acronym, model or product must be resolved. |
| Not applicable | Workflow, model family or platform is not one standalone algorithm. |

## Atomic source register

### Spatial smoothing and semiparametric models — page 25

| ID | Atomic item | Kind | Status | Required completion work |
|---|---|---|---|---|
| S12-SM-01 | Generalised additive model (GAM) with spatial smooth | Statistical model | Open | Define likelihood, link, basis and smoothing selection; test against trusted package. |
| S12-SM-02 | Generalised additive mixed model (GAMM) with spatial smooth | Statistical model | Open | Define random effects and spatial smooth interaction; document inference and identifiability. |
| S12-SM-03 | Thin-plate regression spline (TPRS) | Smoothing basis | Partial | Existing dense Wood-style low-rank basis is bounded; verify basis construction and compare with mgcv implementation. |
| S12-SM-04 | Duchon splines | Smoothing basis | Open | Verify order/dimension and penalty; test null space and boundary behaviour. |
| S12-SM-05 | Soap-film smoothers | Boundary-constrained smoother | Open | Define boundary mesh and PDE penalty; test complex polygonal domains. |
| S12-SM-06 | Bayesian P-splines | Bayesian smoothing model | Open | Define basis, difference prior and hyperpriors; test posterior uncertainty. |
| S12-SM-07 | Geographically weighted LASSO | Spatial regularised regression | Open | Define local kernel, bandwidth and penalty; test coefficient stability and spatial CV. |
| S12-SM-08 | Spatial LASSO | Spatial regularised regression | Open | Resolve exact spatial penalty/likelihood; distinguish spatial lag/error and spatially varying coefficients. |
| S12-SM-09 | Graph-fused LASSO | Graph-regularised regression | Partial | Existing ADMM implementation is bounded; verify objective, graph scaling, convergence and parameter selection. |
| S12-SM-10 | Regularised spatially varying coefficients | Spatial regression model | Open | Define coefficient field and regularisation; test identifiability and inference. |
| S12-SM-11 | Voronoi intensity estimator | Point-process intensity estimator | Partial | Existing bounded-window inverse-area baseline is tested; assess edge correction and adaptive bias. |
| S12-SM-12 | Delaunay intensity estimator | Point-process intensity estimator | Open | Identify estimator and triangle/vertex assignment; test boundary and sampling effects. |
| S12-SM-13 | Space-time kernel density estimation (STKDE) | Point-process estimator | Partial | Existing separable planar Gaussian estimator is bounded; add alternative kernels, edge correction and anisotropic time-space scales. |
| S12-SM-14 | Prospective hotspot mapping | Spatiotemporal surveillance | Open | Define prospective statistic and temporal window; test false-alarm calibration. |
| S12-SM-15 | Palm distributions | Point-process theory/statistic | Open | Define conditioning event and stationary assumptions; derive estimable examples. |
| S12-SM-16 | Nearest-neighbour distance distributions | Point-process summary statistic | Partial | Existing nearest-neighbour summaries are bounded; add edge correction and inhomogeneous cases. |
| S12-SM-17 | Inhomogeneous K-function | Point-process summary statistic | Partial | Existing supplied-intensity translation-corrected estimator is bounded; verify intensity estimation and simulation envelopes. |
| S12-SM-18 | Pair-correlation function | Point-process summary statistic | Partial | Existing numerical estimator is bounded; verify bandwidth, edge correction and relation to K. |

### Matrix and tensor methods — page 25

| ID | Atomic item | Kind | Status | Required completion work |
|---|---|---|---|---|
| S12-MT-01 | Nonnegative matrix factorisation (NMF) | Matrix factorisation | Partial | Existing Euclidean multiplicative updates are tested; add KL divergence, regularisation and convergence criteria. |
| S12-MT-02 | Independent component analysis (ICA) | Matrix factorisation | Open | Identify FastICA/Infomax variants; test source recovery and scaling/permutation ambiguity. |
| S12-MT-03 | Maximum autocorrelation factors (MAF) | Spatial signal transform | Verify | Verify exact MAF formulation and covariance-lag assumptions; test known spatial fields. |
| S12-MT-04 | Dictionary learning | Sparse representation | Open | Define dictionary objective, sparsity and solver; test reconstruction and stability. |
| S12-MT-05 | Sparse coding | Optimisation method | Open | Specify L1/greedy objective and solver; test exact small cases. |
| S12-MT-06 | Compressive sensing | Sampling/reconstruction theory | Open | Define sensing matrix, sparsity and recovery conditions; test reconstruction guarantees. |
| S12-MT-07 | CP/PARAFAC decomposition | Tensor factorisation | Partial | Existing dense three-way CP-ALS is bounded; add initialisation, degeneracy diagnostics and missing-data support. |
| S12-MT-08 | Tucker decomposition | Tensor factorisation | Partial | Existing N-way HOOI/HOSVD is bounded; document core/rank selection and convergence. |
| S12-MT-09 | Tensor-train decomposition | Tensor factorisation | Partial | Existing TT-SVD baseline is bounded; verify rank truncation and ordering. |
| S12-MT-10 | Low-rank spatiotemporal tensor completion | Tensor completion | Partial | Existing data-consistent TT-SVD heuristic is not a general missing-data solver; add explicit objective and independent recovery tests. |
| S12-MT-11 | Third-order t-SVD | Tensor factorisation | Partial | Existing FFT-based tubal-rank truncation is bounded; verify t-product conventions and optimality claims. |
| S12-MT-12 | Extended Kalman filter (EKF) | State estimator | Partial | Existing additive-noise EKF with supplied Jacobians is bounded; add nonlinear observability and covariance consistency tests. |
| S12-MT-13 | Unscented Kalman filter (UKF) | State estimator | Partial | Existing scaled UKF is bounded; verify sigma-point parameter conventions and numerical stability. |
| S12-MT-14 | Ensemble square-root filters | Ensemble data assimilation | Open | Split ETKF/EnSRF/LETKF variants; verify deterministic transform and covariance properties. |
| S12-MT-15 | Rauch–Tung–Striebel (RTS) smoother | State smoothing | Open | Implement linear-Gaussian smoother and test against batch Gaussian posterior. |
| S12-MT-16 | Particle smoothing | Sequential Monte Carlo | Partial | Existing FFBSi-style smoother is bounded; add degeneracy/ancestor diagnostics and alternative smoothers. |
| S12-MT-17 | Ensemble transform Kalman filter (ETKF) | Ensemble data assimilation | Partial | Existing symmetric batch transform is bounded; verify ensemble convention, localisation and inflation. |

### GNSS and geodetic adjustment — page 25

| ID | Atomic item | Kind | Status | Required completion work |
|---|---|---|---|---|
| S12-GN-01 | LAMBDA ambiguity resolution | GNSS integer estimation | Partial | Existing reduction/search baseline is bounded; verify decorrelation, integer search and reference cases. |
| S12-GN-02 | GNSS cycle-slip detection | GNSS signal processing | Partial | Existing geometry-free and MW screens are bounded; verify thresholds, sampling and slip combinations. |
| S12-GN-03 | Ionosphere-free combination | GNSS linear combination | Partial | Existing dual-frequency combination is tested; verify frequencies, noise amplification and sign convention. |
| S12-GN-04 | Geometry-free combination | GNSS linear combination | Partial | Existing combination is tested; document ionospheric and hardware-bias sensitivity. |
| S12-GN-05 | Wide-lane combination | GNSS linear combination | Partial | Existing combination is tested; verify wavelength and noise properties. |
| S12-GN-06 | Precise point positioning ambiguity resolution (PPP-AR) | GNSS positioning workflow | Open | Define bias products, ambiguity fixing and datum; validate against independent reference solutions. |
| S12-GN-07 | GNSS multipath mitigation | Signal/error mitigation | Open | Split antenna, sidereal filtering and signal-domain methods; test environment dependence. |
| S12-GN-08 | Receiver autonomous integrity monitoring (RAIM) | Integrity monitoring | Partial | Existing snapshot chi-square baseline is bounded; certified protection levels and integrity risk remain open. |
| S12-GN-09 | GNSS fault detection and exclusion (FDE) | Integrity monitoring | Partial | Existing single-measurement leave-one-out candidates are bounded; multi-fault and certified availability remain open. |
| S12-GN-10 | Baarda data snooping | Geodetic outlier detection | Partial | Existing known-variance global/local tests are bounded; verify iterative and correlated-observation variants. |
| S12-GN-11 | Least-squares collocation | Geodetic estimation | Partial | Existing finite-dimensional fixed-trend baseline is bounded; full physical geodesy covariance and prediction remain open. |
| S12-GN-12 | GNSS time transfer | Timing estimation | Open | Define clock observable, common-view/all-in-view method and time scale; test reference clocks. |
| S12-GN-13 | GNSS clock modelling | Stochastic process model | Open | Define clock bias/drift/noise components; test Allan variance and residuals. |
| S12-GN-14 | Loosely coupled INS/GNSS integration | Sensor fusion architecture | Open | Define state/measurement interface and update rates; test outage recovery. |
| S12-GN-15 | Tightly coupled INS/GNSS integration | Sensor fusion architecture | Open | Define raw observation integration and dynamics; test satellite visibility degradation. |

### Sensor calibration and image quality — page 25

| ID | Atomic item | Kind | Status | Required completion work |
|---|---|---|---|---|
| S12-CA-01 | Vicarious radiometric calibration | Calibration method | Open | Define reference targets/atmosphere and uncertainty; compare to sensor calibration records. |
| S12-CA-02 | Cross-sensor radiometric calibration | Calibration method | Open | Define spectral response, spatial/temporal matching and transfer model; quantify uncertainty. |
| S12-CA-03 | Modulation transfer function (MTF) estimation | Image quality measurement | Open | Identify edge/point target method and sampling; test frequency response. |
| S12-CA-04 | General Image Quality Equation (GIQE) | Image quality model | Verify | Identify exact GIQE version and input definitions; verify applicable sensor class. |
| S12-CA-05 | NIIRS image quality scoring | Image interpretation scale | Verify | Identify version and rating protocol; do not infer a numeric score from imagery without validated method. |
| S12-CA-06 | Perceptual hashing for EO imagery | Image fingerprinting | Open | Define hash and invariance; test near-duplicate detection under geospatial transformations. |
| S12-CA-07 | Content-based EO image retrieval | Image retrieval workflow | Open | Define features/index and geographic metadata; evaluate retrieval relevance. |
| S12-CA-08 | Near-duplicate tile detection | Image deduplication | Open | Define overlap/scale/season tolerance; test shifted and partially overlapping tiles. |
| S12-CA-09 | Lossy imagery compression | Compression method family | Open | Split codecs and quality metrics; test downstream task impact. |
| S12-CA-10 | Learned/neural image codecs | Learned compression | Open | Identify model/checkpoint and licence; measure rate-distortion and task fidelity. |
| S12-CA-11 | Downstream task rate-distortion evaluation | Evaluation protocol | Open | Define task metric and bitrate; compare codec distortion with task loss. |

### SAR and polarimetric deep learning — page 25

| ID | Atomic item | Kind | Status | Required completion work |
|---|---|---|---|---|
| S12-SAR-01 | Deep SAR despeckling | Denoising model family | Open | Split architectures and noise assumptions; preserve radiometry and texture. |
| S12-SAR-02 | SAR ship detection | Object detection workflow | Open | Define sensor, polarisation, target labels and clutter; spatially independent evaluation. |
| S12-SAR-03 | SAR automatic target recognition (ATR) | Classification workflow | Open | Define target taxonomy, aspect angle and acquisition; assess domain shift. |
| S12-SAR-04 | Polarimetric feature learning | Representation learning | Open | Define polarimetric decomposition/input encoding; test physical consistency. |
| S12-SAR-05 | SAR–optical cross-modal matching | Multimodal matching | Open | Define modality-specific descriptors and geometric model; test seasonal/terrain conditions. |
| S12-SAR-06 | SAR image registration | Registration workflow | Open | Define sensor geometry and transform model; validate control-point residuals. |
| S12-SAR-07 | Interferogram denoising networks | InSAR denoising | Open | Define phase representation and noise model; test phase preservation and coherence. |

### Quantitative spatial economics and regional science — page 26

| ID | Atomic item | Kind | Status | Required completion work |
|---|---|---|---|---|
| S12-EC-01 | Garin–Lowry model | Regional economic model | Verify | Verify exact model formulation and equilibrium assumptions; test benchmark input-output case. |
| S12-EC-02 | Lowry model | Urban land-use/economic model | Verify | Identify original variant and residential/employment allocation; document calibration. |
| S12-EC-03 | Input-output regional model | Economic accounting model | Open | Define intersectoral table, import/export treatment and regionalisation; test accounting identities. |
| S12-EC-04 | Spatial computable general equilibrium (SCGE) model | Economic equilibrium model | Open | Define agents, markets, transport costs and closure; document calibration and solution. |
| S12-EC-05 | Rosen–Roback quantitative spatial equilibrium | Spatial equilibrium framework | Verify | Identify exact formulation and amenity/productivity channels; distinguish model family from one solver. |
| S12-EC-06 | PPML gravity trade estimation | Count regression | Partial | Existing cross-sectional PPML baseline is bounded; add fixed effects, clustered inference and trade-flow diagnostics. |
| S12-EC-07 | Market access | Spatial economic metric | Partial | Existing Harris-style potential index is bounded; verify model-specific market access and endogenous trade costs. |
| S12-EC-08 | Spatial price equilibrium | Economic equilibrium model | Open | Define supply/demand, transport costs and market-clearing; test equilibrium existence and solution. |
| S12-EC-09 | Regional convergence analysis | Econometric analysis | Partial | Existing beta/sigma convergence baselines are descriptive/cross-sectional; add panel/spatial inference. |
| S12-EC-10 | Spatial Markov chains | Spatial transition model | Partial | Existing pooled-quantile and spatially conditioned transition matrices are bounded; test state/weight sensitivity. |
| S12-EC-11 | LISA transitions | Local spatial dynamics | Partial | Existing quadrant transition summaries are descriptive; inferential transition testing remains open. |
| S12-EC-12 | Spatial income-distribution dynamics | Regional distribution analysis | Partial | Existing distribution dynamics baselines are bounded; add distributional uncertainty and panel identification. |

### Network resilience and infrastructure risk — page 26

| ID | Atomic item | Kind | Status | Required completion work |
|---|---|---|---|---|
| S12-NR-01 | Critical-node detection | Network vulnerability analysis | Partial | Existing removal/giant-component baselines are bounded; define demand-weighted criticality and alternate metrics. |
| S12-NR-02 | Critical-edge detection | Network vulnerability analysis | Partial | Existing edge attack/failure curves are bounded; add flow/capacity impact and spatial exposure. |
| S12-NR-03 | Road-network percolation | Network resilience method | Partial | Existing topology-only percolation is bounded; add spatially weighted network and demand connectivity. |
| S12-NR-04 | Cascading failure models | Network dynamics | Partial | Existing Motter–Lai topology/load cascade is bounded; add capacity calibration and alternative cascade rules. |
| S12-NR-05 | Interdependent infrastructure models | Network-of-networks model | Open | Define dependency links and failure propagation; test synthetic coupled systems. |
| S12-NR-06 | Vulnerability curves | Risk metric | Open | Define hazard intensity, damage/loss and asset class; validate calibration domain. |
| S12-NR-07 | Fragility curves | Probabilistic damage model | Open | Define limit states and intensity measure; test monotonicity and uncertainty. |
| S12-NR-08 | HAZUS-style loss estimation | Loss-estimation workflow | Verify | Identify HAZUS version/module and input data; document official methodology and licence. |
| S12-NR-09 | Monte Carlo network reliability | Reliability estimator | Partial | Existing IID edge-survival direct Monte Carlo is bounded; add correlated failures and variance reduction. |
| S12-NR-10 | Minimal cut sets | Reliability analysis | Partial | Existing exhaustive small-graph inclusion-minimal cuts are bounded; add scalable enumeration and validation. |
| S12-NR-11 | Post-disaster restoration scheduling | Scheduling optimisation | Open | Define crew, precedence, access and resource constraints; test scenario robustness. |

### Computational geometry for districting and partitioning — page 26

| ID | Atomic item | Kind | Status | Required completion work |
|---|---|---|---|---|
| S12-DI-01 | Power diagrams | Weighted geometric partition | Open | Define power distance and weights; test cell construction and degeneracies. |
| S12-DI-02 | Centroidal Voronoi tessellation (CVT) | Geometric optimisation | Partial | Existing discrete Lloyd finite-sample baseline is bounded; exact polygonal CVT remains open. |
| S12-DI-03 | Lloyd's algorithm | Iterative centroidal tessellation | Partial | Verify convergence/energy descent and empty-cell handling; compare deterministic starts. |
| S12-DI-04 | Capacity-constrained Voronoi | Balanced geometric partition | Open | Define cell mass/capacity and optimal transport solver; test constraint satisfaction. |
| S12-DI-05 | Semi-discrete optimal transport | Optimal transport method | Open | Define source measure, discrete target and cost; test dual/primal consistency. |
| S12-DI-06 | Compactness-constrained balanced partitioning | Districting optimisation | Open | Define compactness metric, contiguity and population constraints; test benchmark plans. |
| S12-DI-07 | Equal-population graph partitioning | Graph partitioning | Open | Define population weights, contiguity and objective; assess compactness/efficiency trade-off. |

### Climate analysis and attribution — page 26

| ID | Atomic item | Kind | Status | Required completion work |
|---|---|---|---|---|
| S12-CL-01 | Teleconnection indices | Climate index family | Open | Split named indices, variables and baselines; document sign and standardisation. |
| S12-CL-02 | Climate regime detection | Time-series/regime model | Open | Define state model and regime persistence; validate across periods. |
| S12-CL-03 | Pattern scaling | Climate downscaling/attribution method | Open | Define pattern field, global temperature predictor and residual; test scenario transfer. |
| S12-CL-04 | CMIP ensemble weighting | Ensemble weighting method | Open | Define skill/independence weighting and dependence correction; test robustness. |
| S12-CL-05 | Extreme-event attribution | Climate attribution workflow | Open | Define factual/counterfactual worlds and event metric; document causal assumptions. |
| S12-CL-06 | Detection and attribution | Climate inference framework | Open | Define forced/internal variability fingerprints and uncertainty; reproduce benchmark. |
| S12-CL-07 | Return-level estimation with covariates | Extreme-value model | Open | Define GEV/GPD covariate structure and nonstationarity; test uncertainty and extrapolation. |
| S12-CL-08 | MBCn multivariate bias correction | Bias-correction algorithm | Verify | Verify exact MBCn variant and transformations; test marginal and dependence restoration. |
| S12-CL-09 | Schaake shuffle | Multivariate downscaling/reordering | Verify | Verify rank-reordering method and historical analogue selection; test spatial dependence. |
| S12-CL-10 | Ensemble copula coupling (ECC) | Ensemble post-processing | Verify | Verify ECC variant and rank structure; test multivariate calibration. |
| S12-CL-11 | Spatial-coherence-preserving downscaling | Downscaling workflow | Open | Define target covariance/dependence and conservation; test spatial and temporal consistency. |
| S12-CL-12 | Empirical quantile mapping | Bias correction | Partial | Existing univariate implementation is bounded; document trend preservation and tail handling. |
| S12-CL-13 | Delta-change correction | Bias correction | Partial | Existing baseline is bounded; define additive/multiplicative choice and seasonal application. |

### Terrain traversability and off-road mobility — page 26

| ID | Atomic item | Kind | Status | Required completion work |
|---|---|---|---|---|
| S12-TR-01 | LiDAR-based terrain traversability estimation | Terrain classification | Open | Define terrain classes, point-cloud features and vehicle profile; validate with field traverses. |
| S12-TR-02 | Imagery-based terrain traversability estimation | Terrain classification | Open | Define visual features, illumination and surface labels; validate independently. |
| S12-TR-03 | Rover path planning | Robotics path planning | Open | Define robot kinematics, obstacle and risk costs; test feasible paths in simulation. |
| S12-TR-04 | Slope cost maps | Terrain cost surface | Open | Define slope derivation, resolution and vehicle thresholds; test DEM noise sensitivity. |
| S12-TR-05 | Roughness cost maps | Terrain cost surface | Open | Define roughness metric and scale; calibrate against vehicle traversability. |
| S12-TR-06 | Soil–vehicle interaction models | Physical mobility model | Open | Define soil constitutive model and vehicle contact; validate against measured traction/sinkage. |
| S12-TR-07 | Swarm coverage planning | Multi-robot planning | Open | Define agents, communication, collision and coverage; test robustness. |
| S12-TR-08 | Multi-robot coverage planning | Multi-agent optimisation | Open | Define assignment, path and coordination; compare centralised/distributed methods. |

## Completion gates

1. Verify original papers and exact software versions; record citations for each material claim.
2. State mathematical objective, estimand, assumptions, units, CRS, uncertainty and failure conditions.
3. For GNSS integrity, distinguish research baselines from certified protection levels and operational integrity claims.
4. For economic and climate models, document identification, scenario assumptions, temporal support and uncertainty.
5. Test numerical methods against analytic/synthetic cases, trusted implementations and domain-specific benchmarks.
6. Protect sensitive mobility, geodetic and infrastructure data; review licences for datasets, software and model weights.
7. Reconcile lessons, implementation packages, independent tests, notebooks, coverage matrix and dashboard after evidence changes.

**Current conclusion:** Section 12 is decomposed into atomic review items. It remains open; this register does not claim that all model variants, GNSS integrity procedures or domain workflows are implemented or certified.
