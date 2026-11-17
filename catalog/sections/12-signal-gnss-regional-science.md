# Section 12 — Additions: signal processing, GNSS, regional science, resilience

- **Original source section:** 12
- **Source pages:** 24–26
- **Source transcription:** [pages 21–25](../../source-inventory/pages-21-25.md) and [pages 26–30](../../source-inventory/pages-26-30.md)
- **Review state:** source entries extracted into this index; the source describes these as methods borrowed from adjacent fields
- **Current canonical records:** [GNSS integer least-squares search](../../methods/gnss-integer-ambiguity-resolution.md), [dual-frequency GNSS combinations](../../methods/gnss-dual-frequency-combinations.md), [point-pattern second-order statistics](../../methods/point-pattern-second-order-statistics.md), [nonnegative matrix factorization](../../methods/nonnegative-matrix-factorization.md), [network percolation and resilience](../../methods/network-percolation-resilience.md), [network edge failure and reliability](../../methods/network-edge-failure-and-reliability.md), [Motter–Lai cascading overload failures](../../methods/network-cascading-overload-failures.md), [regional distribution dynamics](../../methods/regional-distribution-dynamics.md), [regional beta-convergence](../../methods/regional-beta-convergence.md), [geometry-free cycle-slip screening](../../methods/gnss-geometry-free-cycle-slip-screening.md), [Melbourne–Wübbena cycle-slip screening](../../methods/gnss-melbourne-wubbena-cycle-slip-screening.md), and [CP/PARAFAC tensor decomposition](../../methods/cp-parafac-tensor-decomposition.md), [Tucker/HOSVD tensor decomposition](../../methods/tucker-hosvd-tensor-decomposition.md), [nonlinear and particle state estimation](../../methods/nonlinear-kalman-ekf-ukf.md), [spatial thin-plate smoothing](../../methods/spatial-thin-plate-smoothing-spline.md), [graph-fused spatial regression](../../methods/graph-fused-spatial-regression.md), [spatial/space-time kernel intensity](../../methods/spatial-and-spacetime-kernel-intensity.md), [bounded-window Voronoi point intensity](../../methods/voronoi-point-intensity.md), [Baarda-style geodetic data snooping](../../methods/baarda-data-snooping.md), [least-squares collocation](../../methods/least-squares-collocation.md), [ensemble transform Kalman filter](../../methods/ensemble-transform-kalman-filter.md), [Poisson pseudo-maximum likelihood gravity baseline](../../methods/poisson-pseudo-maximum-likelihood-gravity.md), [Harris-style market potential](../../methods/harris-market-potential.md), [third-order tensor t-SVD](../../methods/third-order-tensor-svd.md), [residual-based GNSS RAIM/FDE baseline](../../methods/gnss-residual-raim-fde.md), with implementations and learning notebooks linked from their respective method pages.

The source explicitly frames these as methods from adjacent fields that spatial analysts regularly borrow. Explain the original method first, then show what changes when it is applied to spatial data.

## Smoothing and semiparametric spatial models

| Source entry | Provisional kind | Source page | Verification status |
|---|---|---:|--- |
| GAM and GAMM with spatial smooths (thin plate, Duchon splines, soap film smoothers), Bayesian P-splines | Generalised additive models / spatial smoothing bases | 25 | [Spatial thin-plate smoothing lesson](../../methods/spatial-thin-plate-smoothing-spline.md), NumPy implementation, tests and notebook cover both a full-knot 2-D thin-plate smoothing spline and a Wood-style low-rank TPRS basis with an affine null space, eigenvalue truncation and identity transformed penalty; the TPRS basis constructor is dense and not mgcv's Lanczos/subsampled large-data implementation; GAM/GAMM, Duchon, soap-film and Bayesian P-splines remain open | Partial — related record exists; source-entry review pending
| Penalized spatial regression: geographically weighted LASSO, spatial LASSO, fused LASSO on graphs, spatially varying coefficients with regularization | Regularised regression methods / graph penalties | 25 | [Graph-fused spatial regression lesson](../../methods/graph-fused-spatial-regression.md) and ADMM implementation, tests and notebook cover location-specific coefficients with L1 sparsity and graph total-variation penalties; geographically weighted LASSO, spatial lag/error models and inferential spatially varying coefficient models remain open | Partial — related record exists; source-entry review pending
| Intensity estimation: Voronoi and Delaunay-based estimators, STKDE (space-time KDE), prospective hotspot mapping | Spatial intensity estimators / hotspot methods | 25 | [Spatial and space-time KDE lesson](../../methods/spatial-and-spacetime-kernel-intensity.md), NumPy implementation, tests and notebook cover fixed-bandwidth planar Gaussian spatial and separable space-time intensity; a separate [bounded-window Voronoi intensity baseline](../../methods/voronoi-point-intensity.md) now constructs clipped cells and inverse-area estimates; Delaunay-based estimators, boundary correction and prospective hotspot inference remain open | Partial — related record exists; source-entry review pending
| Palm distributions, nearest neighbor distance distributions, inhomogeneous K and pair correlation functions | Point-process summary statistics | 25 | [Point-pattern lesson](../../methods/point-pattern-second-order-statistics.md) and tested [Python package](../../implementations/python/point-process/README.md) cover nearest-neighbor distances, homogeneous and supplied-intensity inhomogeneous rectangular translation-corrected K, and numerical pair correlation; Palm distributions, automatic intensity modelling and simulation envelopes remain open | Partial — related record exists; source-entry review pending

## Matrix and tensor methods for spatial data

| Source entry | Provisional kind | Source page | Verification status |
|---|---|---:|--- |
| NMF, ICA, MAF (maximum autocorrelation factors), dictionary learning, sparse coding, compressive sensing | Matrix factorisation / representation and signal-processing methods | 25 | [NMF lesson](../../methods/nonnegative-matrix-factorization.md) and tested [Python implementation](../../implementations/python/matrix-factorization/README.md) cover Euclidean multiplicative updates; ICA, MAF, dictionary learning, sparse coding and compressive sensing remain open | Partial — related record exists; source-entry review pending
| Tensor decomposition: CP, Tucker, tensor train; low-rank spatiotemporal completion | Tensor factorisation / completion methods | 25 | [CP/PARAFAC lesson](../../methods/cp-parafac-tensor-decomposition.md) and dense three-way CP-ALS implementation, tests and notebook cover fully observed unconstrained tensors; [Tucker/HOSVD lesson](../../methods/tucker-hosvd-tensor-decomposition.md), dense N-way implementation, tests and notebook cover truncated HOSVD and HOOI refinement; tensor train and a data-consistent TT-SVD completion heuristic are implemented; a separate FFT-based third-order t-SVD with tubal-rank truncation is now implemented; specialized missing-data optimization methods remain open | Partial — related record exists; source-entry review pending
| Kalman variants: EKF, UKF, ensemble square-root filters, RTS smoothing, particle smoothing | State estimation and smoothing algorithms | 25 | [EKF/UKF and bootstrap particle filter lesson](../../methods/nonlinear-kalman-ekf-ukf.md), NumPy implementations, tests and lab notebooks cover additive-noise EKF with supplied Jacobians, scaled UKF and bootstrap particle filtering with ESS/systematic resampling and an offline FFBSi smoother that samples full trajectories from stored filtering particles using the transition density; [ETKF batch analysis](../../methods/ensemble-transform-kalman-filter.md) is now implemented with a deterministic symmetric ensemble-space transform, tests and notebook; other ensemble square-root variants, localization/inflation, nonlinear RTS and additional particle-smoothing methods remain open | Partial — related record exists; source-entry review pending

## GNSS and geodetic adjustment

| Source entry | Provisional kind | Source page | Verification status |
|---|---|---:|--- |
| Ambiguity resolution (LAMBDA), cycle slip detection, ionosphere-free and geometry-free combinations, PPP-AR | GNSS ambiguity and signal-processing methods | 25 | [GNSS ILS lesson](../../methods/gnss-integer-ambiguity-resolution.md) and [dual-frequency combination lesson](../../methods/gnss-dual-frequency-combinations.md), with tested [Python baselines](../../implementations/python/gnss-ambiguity/README.md), cover small-dimensional ILS and geometry-free/ionosphere-free/wide-lane combinations; [LAMBDA reduction and integer least-squares search](../../methods/gnss-lambda-integer-ambiguity-resolution.md) are now implemented alongside the original sphere-enumeration baseline; float ambiguity estimation, integer slip repair and PPP-AR remain open; separate geometry-free quadratic-prediction and Melbourne–Wübbena running-threshold screens are documented in [the GF lesson](../../methods/gnss-geometry-free-cycle-slip-screening.md) and [the MW lesson](../../methods/gnss-melbourne-wubbena-cycle-slip-screening.md) | Partial — related record exists; source-entry review pending
| Multipath mitigation, RAIM and fault detection, Baarda data snooping, least squares collocation | GNSS error mitigation / integrity monitoring / geodetic estimation | 25 | [Baarda-style data snooping](../../methods/baarda-data-snooping.md) covers known-variance global and local residual tests; [Pope's tau test](../../methods/pope-tau-test.md) adds internally studentized residual screening with an explicit Bonferroni family-wise threshold; [least-squares collocation](../../methods/least-squares-collocation.md) covers a finite-dimensional fixed-trend baseline; [residual-based RAIM/FDE](../../methods/gnss-residual-raim-fde.md) covers a known-covariance linear snapshot chi-square test and single-measurement leave-one-out candidates. Certified protection levels, integrity-risk/availability calculations, multi-fault RAIM, physical multipath mitigation, iterative/robust data snooping and full physical-geodesy collocation remain open | Partial — scoped implementations exist; source-entry review pending |
| Time transfer, clock modeling, kinematic positioning with INS integration (loosely and tightly coupled) | Timing and positioning models / sensor-fusion architectures | 25 | Not checked — intake only |

## Sensor calibration and image quality

| Source entry | Provisional kind | Source page | Verification status |
|---|---|---:|--- |
| Vicarious and cross-sensor radiometric calibration, MTF estimation, GIQE and NIIRS image quality scoring | Calibration methods / image-quality measures | 25 | Not checked — intake only |
| Perceptual hashing and content-based image retrieval for EO archives, near-duplicate tile detection | Image retrieval / deduplication methods | 25 | Not checked — intake only |
| Lossy and learned compression for imagery (neural codecs), rate-distortion evaluation for downstream tasks | Compression methods / rate-distortion evaluation | 25 | Not checked — intake only |

## SAR and polarimetric deep learning

| Source entry | Provisional kind | Source page | Verification status |
|---|---|---:|--- |
| Deep despeckling, SAR ship detection, SAR target recognition (ATR), polarimetric feature learning | Deep learning methods for radar imagery | 25 | Not checked — intake only |
| Cross-modal SAR-optical matching, SAR image registration, interferogram denoising networks | Multimodal matching / registration / denoising models | 25 | Not checked — intake only |

## Quantitative spatial economics and regional science

| Source entry | Provisional kind | Source page | Verification status |
|---|---|---:|--- |
| Garin-Lowry and Lowry models, input-output and spatial CGE models, quantitative spatial equilibrium (Rosen-Roback style) | Regional economic models / spatial equilibrium frameworks | 26 | Not checked — intake only |
| Gravity trade models (PPML estimation), market access, spatial price equilibrium | Trade and interaction models / estimation methods | 26 | [PPML gravity lesson](../../methods/poisson-pseudo-maximum-likelihood-gravity.md), cross-sectional NumPy implementation with zero-outcome support, known offset, HC0 covariance, tests and synthetic lab; separate [Harris-style market-potential index](../../methods/harris-market-potential.md) computes destination-mass-weighted generalized-cost accessibility with explicit self-potential handling; fixed effects, clustered inference, structural equilibrium and estimated market-access models remain open | Partial — related record exists; source-entry review pending
| Regional convergence analysis, spatial Markov chains, LISA transitions, spatial dynamics of income distributions | Regional convergence and spatial transition analysis | 26 | [Regional distribution dynamics lesson](../../methods/regional-distribution-dynamics.md), [NumPy implementations](../../implementations/python/regional-dynamics/README.md), tests and lab notebooks cover pooled-quantile Markov transitions, spatial Markov conditioning, descriptive LISA quadrant transitions and sigma-dispersion; a separate [absolute/conditional beta-convergence baseline](../../methods/regional-beta-convergence.md) now adds cross-sectional OLS and HC1 standard errors; spatial error/lag models, panel econometrics, inferential LISA and causal analysis remain open | Partial — related record exists; source-entry review pending

## Network resilience and infrastructure risk

| Source entry | Provisional kind | Source page | Verification status |
|---|---|---:|--- |
| Critical node and edge detection, percolation on road networks, cascading failure models | Network vulnerability and resilience analysis | 26 | [Network percolation lesson](../../methods/network-percolation-resilience.md) and tested [Python baselines](../../implementations/python/network-resilience/README.md) cover largest-component analysis, random/degree-targeted node removal, random/static-betweenness edge attacks, edge-failure curves and a topology-only Motter–Lai overload cascade; spatially weighted loads, flow-constrained failures and interdependent-network cascades remain open | Partial — related record exists; source-entry review pending
| Interdependent infrastructure modeling, vulnerability and fragility curves, HAZUS-style loss estimation | Infrastructure risk models / loss estimation | 26 | Not checked — intake only |
| Reliability analysis for networks (Monte Carlo, minimal cut sets), post-disaster restoration scheduling | Reliability analysis / optimisation and scheduling | 26 | [Network edge-failure and reliability lesson](../../methods/network-edge-failure-and-reliability.md), tested Python baselines and notebook cover direct Monte Carlo all-terminal/k-terminal reliability under IID edge survival and exhaustive inclusion-minimal cut sets on small graphs; exact reliability solvers and restoration scheduling remain open | Partial — related record exists; source-entry review pending

## Computational geometry for districting and partitioning

| Source entry | Provisional kind | Source page | Verification status |
|---|---|---:|--- |
| Power diagrams, centroidal Voronoi tessellation (Lloyd's algorithm), capacity-constrained Voronoi, semi-discrete optimal transport | Geometric partitioning / tessellation / optimal transport methods | 26 | [Discrete Lloyd CVT lesson](../../methods/discrete-centroidal-voronoi-lloyd.md), [NumPy implementation](../../implementations/python/voronoi-lloyd/README.md), tests and notebook cover weighted Lloyd updates over finite point samples; exact polygonal CVTs, power diagrams, capacity constraints and semi-discrete optimal transport remain open | Partial — related record exists; source-entry review pending
| Balanced partitioning with compactness constraints, graph partitioning for equal-population districts | Constrained spatial and graph partitioning | 26 | Not checked — intake only |

## Climate analysis and attribution

| Source entry | Provisional kind | Source page | Verification status |
|---|---|---:|--- |
| Teleconnection indices, regime detection, pattern scaling, ensemble weighting of CMIP models | Climate indices / regime and ensemble analysis | 26 | Not checked — intake only |
| Extreme event attribution, detection and attribution, return level estimation with covariates | Climate attribution / extreme-value analysis | 26 | Not checked — intake only |
| Multivariate bias correction (MBCn), spatial coherence-preserving downscaling (Schaake shuffle, ECC) | Bias correction / spatial downscaling methods | 26 | [Statistical downscaling baselines](../../implementations/python/statistical-downscaling/README.md) provide tested empirical quantile mapping and delta-change correction | Partial — univariate quantile mapping and delta change are implemented; MBCn, Schaake shuffle, ECC and spatial dependence-preserving downscaling remain open |

## Terrain traversability and off-road mobility

| Source entry | Provisional kind | Source page | Verification status |
|---|---|---:|--- |
| Traversability estimation from LiDAR and imagery, rover path planning, slope and roughness cost maps | Terrain classification / robotics path planning / cost-surface methods | 26 | Not checked — intake only |
| Soil-vehicle interaction models, swarm and multi-robot coverage planning | Physical interaction models / multi-agent planning | 26 | Not checked — intake only |

## Decisions for the next pass

1. Identify which methods are borrowed from signal processing, statistics, geodesy, economics or network science.
2. Preserve the original domain assumptions when adapting a method to spatial data.
3. Verify abbreviations and named procedures before assigning stable records.
4. Keep resilience, regional economics and geodetic adjustment distinct despite their shared mathematical tools.
5. Connect these methods to the relevant foundations in sections 1–9.


## Atomic completion tracking

The grouped source entries above have been decomposed into individually auditable child IDs in the [Section 12 atomic completion register](../../docs/section-12-atomic-completion-register.md). The register preserves the original domain assumptions and distinguishes estimators, model families, workflows and integrity systems. It is a traceability backlog, not a verification or completion claim.
