# Section 2 atomic completion register

**Source:** *Spatial Analysis Algorithms: Complete Compendium*, Section 2, pages 2–4.  
**Intake:** [preserved pages 1–5 transcription](../source-inventory/pages-01-05.md).  
**Section index:** [Section 2 catalogue record](../catalog/sections/02-spatial-statistics.md).

This register decomposes grouped labels into auditable child records. Use the [verification protocol](../catalog/verification-protocol.md) and [completion standard](compendium-completion-standard.md). Existing implementations are bounded to their stated estimators and assumptions.

| Status | Meaning |
|---|---|
| Open | No item-specific independent evidence recorded here. |
| Partial | A related bounded implementation exists; variants or validation remain open. |
| Verify | Exact method, model or test variant must be resolved. |
| Not applicable | A workflow or broad model family needs a different record kind. |

## Atomic source register

### Autocorrelation and local statistics — pages 2–3

| ID | Atomic item | Kind | Status | Required completion work |
|---|---|---|---|---|
| S02-AU-01 | Global Moran's I | Global spatial autocorrelation statistic | Partial | Define weights, centring, expectation/variance and permutation null; test known graphs. |
| S02-AU-02 | Geary's C | Global spatial autocorrelation statistic | Partial | Verify scaling and null moments; test sensitivity to weights and islands. |
| S02-AU-03 | Join-count statistics | Spatial association statistic | Partial | Split binary categories and join types; test expected counts and variance. |
| S02-AU-04 | Lee's L | Bivariate spatial association statistic | Verify | Verify exact statistic, assumptions and inference; compare with published examples. |
| S02-AU-05 | Bivariate Moran's I | Bivariate spatial autocorrelation | Partial | Define lagged variable orientation and standardisation; test permutation inference. |
| S02-AU-06 | Mantel test | Matrix association test | Verify | Verify permutation scheme and known limitations; document distance-matrix dependence. |
| S02-AU-07 | Partial Mantel test | Conditional matrix association test | Verify | Verify exact procedure and inferential limitations; do not overstate causal interpretation. |
| S02-AU-08 | Local Moran's I (LISA) | Local spatial statistic | Partial | Verify quadrant/cluster labels and conditional randomisation; address multiple testing. |
| S02-AU-09 | Getis–Ord Gi* | Local hotspot statistic | Partial | Define self-inclusion, weights and variance; test edge effects and local significance. |
| S02-AU-10 | Moran scatterplot | Diagnostic visualisation | Partial | Define standardisation and lag; distinguish descriptive quadrants from inferential clusters. |
| S02-AU-11 | Mean centre | Summary geometry | Partial | Define weights and CRS; test invariance and empty/zero-weight cases. |
| S02-AU-12 | Median centre | Spatial location estimator | Partial | Identify geometric median variant and convergence; test non-uniqueness. |
| S02-AU-13 | Standard distance | Dispersion metric | Partial | Define weighting and dimensionality; test units and coordinate assumptions. |
| S02-AU-14 | Standard deviational ellipse | Spatial dispersion metric | Partial | Define covariance/axis orientation and weighting; test circular/isotropic and axial cases. |
| S02-AU-15 | Permutation tests for spatial statistics | Inference procedure | Partial | Define null randomisation and exchangeability; compare exact enumeration on small samples. |
| S02-AU-16 | Monte Carlo tests | Simulation inference | Partial | Define null generator, p-value correction and Monte Carlo error. |
| S02-AU-17 | Bonferroni correction | Multiple testing correction | Partial | Verify family definition and adjusted alpha; test dependence-independent bound. |
| S02-AU-18 | False discovery rate (FDR) | Multiple testing correction | Partial | Separate BH/BY and dependence assumptions; test monotonicity and ties. |
| S02-AU-19 | Šidák correction | Multiple testing correction | Verify | Verify independence assumption and adjusted threshold. |
| S02-AU-20 | Dutilleul modified t-test | Spatial correlation-adjusted test | Verify | Verify effective sample size derivation and covariance assumptions. |
| S02-AU-21 | Spatial bootstrap | Resampling inference | Open | Define spatial blocks/units and target estimand; assess bias and coverage. |
| S02-AU-22 | Block bootstrap | Resampling inference | Partial | Define block shape/size and boundary handling; test dependence preservation. |
| S02-AU-23 | Moran eigenvector filtering | Spatial eigenvector method | Partial | Define weights/eigenvectors and selection; test residual autocorrelation and overfit. |
| S02-AU-24 | Spatial+ | Spatial confounding adjustment method | Verify | Verify exact method and assumptions; compare coefficient bias/variance. |
| S02-AU-25 | Restricted spatial regression | Spatial confounding method | Verify | Verify restricted basis and inferential consequences; compare with unrestricted models. |

### Point pattern analysis — page 3

| ID | Atomic item | Kind | Status | Required completion work |
|---|---|---|---|---|
| S02-PP-01 | Quadrat analysis | Point pattern statistic | Partial | Define quadrat size/origin and edge correction; test CSR with exact simulation. |
| S02-PP-02 | Clark–Evans statistic | Nearest-neighbour point pattern statistic | Partial | Verify boundary correction and null expectation; test CSR and regular/clustered patterns. |
| S02-PP-03 | Nearest-neighbour index | Point pattern metric | Partial | Define ratio and window correction; distinguish from related Clark–Evans test. |
| S02-PP-04 | Ripley's K | Second-order point pattern statistic | Partial | Verify edge correction and intensity estimation; test CSR and inhomogeneous patterns. |
| S02-PP-05 | Ripley's L | Variance-stabilising transform | Partial | Define transformation and reference line; test envelope calibration. |
| S02-PP-06 | G function | Nearest-neighbour distribution | Partial | Define empirical estimator and censoring; compare with simulated point processes. |
| S02-PP-07 | F function | Empty-space distribution | Partial | Define random-location sampling and edge correction; test CSR. |
| S02-PP-08 | J function | Combined G/F statistic | Verify | Verify ratio definition and estimator; assess stability when 1-F approaches zero. |
| S02-PP-09 | Pair correlation function | Second-order point pattern statistic | Partial | Verify derivative/smoothing and edge correction; test known process patterns. |
| S02-PP-10 | Homogeneous Poisson process | Point process model | Partial | Define intensity and CSR assumptions; test simulation and likelihood. |
| S02-PP-11 | Cox process | Doubly stochastic point process family | Partial | Split log-Gaussian and other random intensity variants; test latent intensity. |
| S02-PP-12 | Neyman–Scott process | Cluster point process family | Verify | Identify parent-offspring specification and parameterisation; test simulated moments. |
| S02-PP-13 | Gibbs process | Interacting point process family | Verify | Specify energy/potential and normalising constant; distinguish Strauss and hard-core models. |
| S02-PP-14 | Strauss process | Gibbs point process | Verify | Verify interaction radius/parameter and stability constraints; test simulation. |
| S02-PP-15 | Log-Gaussian Cox process | Cox point process model | Partial | Define latent Gaussian field and quadrature/inference; test marginal moments. |
| S02-PP-16 | Marked point patterns | Point process data model | Partial | Implements two-type cross-pattern summaries: source-to-target nearest-neighbour CDF, translation-corrected cross-K, finite-difference cross pair correlation and seeded Monte Carlo cross-J. Tests include hand calculations, seeded repeatability and invalid/missing mark-group cases. General multitype mark correlation, mark randomisation, marked simulation and broader dependence models remain open: [package](../implementations/python/point-process/README.md). |
| S02-PP-17 | Besag–Newell cluster test | Spatial cluster test | Verify | Verify nearest-neighbour case-count definition and null; test irregular population. |
| S02-PP-18 | Tango cluster test | Spatial cluster test | Verify | Verify statistic/weighting and null calibration; test alternatives. |
| S02-PP-19 | SaTScan scan statistics | Spatial/space-time scan framework | Verify | Pin version and model (Poisson/Bernoulli/space-time); document window and multiple testing. |
| S02-PP-20 | Elliptic scan statistic | Cluster detection variant | Verify | Verify ellipse search and shape constraints; test power and false-positive rate. |
| S02-PP-21 | Flexible-shape scan (FleXScan) | Cluster detection algorithm/software | Verify | Verify graph-based flexible window and implementation; test irregular clusters. |
| S02-PP-22 | Adaptive-bandwidth KDE | Point intensity estimator | Partial | Define bandwidth adaptation and edge correction; compare integrated error. |
| S02-PP-23 | Variable-bandwidth KDE | Point intensity estimator | Partial | Define sample-point vs evaluation-point bandwidth; test bias/variance. |
| S02-PP-24 | Silverman bandwidth selection | Bandwidth selection rule | Verify | Identify exact rule and assumptions; distinguish univariate rule from spatial adaptation. |
| S02-PP-25 | Cross-validated bandwidth selection | Bandwidth optimisation | Partial | Define likelihood/least-squares CV and spatial blocking; test held-out log score. |
| S02-PP-26 | Network K-function | Network point pattern statistic | Verify | Verify network distance and edge correction; compare with simulation on known networks. |
| S02-PP-27 | Network KDE (NKDE) | Network intensity estimator | Partial | Define kernel along network distance and junction correction; test conservation. |
| S02-PP-28 | SANET methods | Network spatial analysis software/method family | Verify | Identify exact SANET version and individual methods; do not treat suite as one algorithm. |

### Clustering and regionalisation — page 3

| ID | Atomic item | Kind | Status | Required completion work |
|---|---|---|---|---|
| S02-CL-01 | DBSCAN | Density clustering | Partial | Define metric, eps and min_samples; test border assignment and variable density. |
| S02-CL-02 | HDBSCAN | Hierarchical density clustering | Partial | Verify mutual reachability and stability selection; test noise/cluster hierarchy. |
| S02-CL-03 | OPTICS | Density ordering algorithm | Verify | Verify reachability ordering and extraction; compare with DBSCAN/HDBSCAN. |
| S02-CL-04 | DENCLUE | Density-based clustering | Verify | Verify influence function and hill-climbing; test parameter sensitivity. |
| S02-CL-05 | Density peaks clustering | Density clustering | Verify | Verify local density/distance criterion and cluster assignment; test ties. |
| S02-CL-06 | ST-DBSCAN | Spatiotemporal density clustering | Verify | Define spatial/temporal thresholds and feature threshold; test temporal ordering. |
| S02-CL-07 | T-DBSCAN | Trajectory/temporal DBSCAN variant | Verify | Resolve exact acronym and paper; distinguish from ST-DBSCAN. |
| S02-CL-08 | k-means | Partition clustering | Partial | Define objective, initialisation and empty-cluster handling; test local minima. |
| S02-CL-09 | k-medoids | Partition clustering | Partial | Define dissimilarity and medoid update; compare with exhaustive small cases. |
| S02-CL-10 | CLARA | Large-data k-medoids approximation | Verify | Verify sampling/repetition and candidate evaluation; quantify approximation. |
| S02-CL-11 | CLARANS | Randomised k-medoids search | Verify | Verify neighbour sampling and stopping; test reproducibility. |
| S02-CL-12 | Constrained k-means | Constrained clustering | Partial | Define must/cannot-link or capacity constraints; test feasibility and objective. |
| S02-CL-13 | Equal-size k-means | Balanced clustering | Verify | Verify assignment optimisation and balance tolerance; test infeasible constraints. |
| S02-CL-14 | BIRCH | Hierarchical clustering/index | Verify | Verify CF-tree structure, threshold and leaf clustering; test streaming order. |
| S02-CL-15 | STING | Grid-based clustering | Verify | Verify hierarchical grid statistics and pruning; test resolution effects. |
| S02-CL-16 | CLIQUE | Subspace clustering | Verify | Verify dense-unit generation and Apriori property; test high-dimensional data. |
| S02-CL-17 | Ward hierarchical clustering | Hierarchical clustering | Partial | Define linkage objective and distance constraints; test reducibility. |
| S02-CL-18 | Mean shift | Mode-seeking clustering | Partial | Define kernel/bandwidth and convergence; test boundary and scale sensitivity. |
| S02-CL-19 | Affinity propagation | Message-passing clustering | Verify | Verify responsibility/availability updates and damping; test preference sensitivity. |
| S02-CL-20 | Spectral clustering | Graph clustering | Partial | Define affinity, Laplacian and discretisation; test disconnected graphs. |
| S02-CL-21 | Gaussian mixture models | Probabilistic clustering | Partial | Define covariance families, EM and regularisation; test label switching. |
| S02-CL-22 | Fuzzy c-means | Fuzzy clustering | Partial | Define fuzzifier and membership constraints; test zero-distance cases. |
| S02-CL-23 | Self-organising maps | Neural clustering | Verify | Verify topology, neighbourhood schedule and convergence; test map stability. |
| S02-CL-24 | Growing neural gas | Incremental neural clustering | Verify | Verify insertion/removal rules and stopping; test stream order. |
| S02-CL-25 | Consensus clustering | Ensemble clustering | Open | Define base clusterings and co-association; test label permutation and instability. |
| S02-CL-26 | Co-clustering | Biclustering | Open | Split spectral/iterative variants and objective; test row/column recovery. |
| S02-CL-27 | SKATER | Spatially constrained regionalisation | Verify | Verify spanning-tree pruning and heterogeneity objective; test contiguity. |
| S02-CL-28 | REDCAP | Spatially constrained regionalisation | Verify | Verify agglomeration/partition variants and constraints. |
| S02-CL-29 | AZP | Automatic zoning procedure | Verify | Verify local search, objective and initialisation; test contiguity and stability. |
| S02-CL-30 | Max-p regionalisation | Spatial regionalisation | Verify | Verify threshold constraint and objective; test feasibility and optimality gap. |
| S02-CL-31 | Spatial LDA | Spatial topic/model family | Verify | Resolve exact spatial LDA formulation; document spatial prior and inference. |
| S02-CL-32 | OAC-style geodemographic classification | Classification workflow | Verify | Identify official OAC edition and methodology; distinguish reproduction from adaptation. |
| S02-CL-33 | Principal component analysis | Dimension reduction | Partial | Define centring/scaling and missingness; test eigenvector sign and reconstruction. |
| S02-CL-34 | Factor analysis | Latent-variable model | Partial | Define identification/rotation and covariance structure; test recovery and uncertainty. |

### Regression and spatial econometrics — pages 3–4

| ID | Atomic item | Kind | Status | Required completion work |
|---|---|---|---|---|
| S02-RE-01 | Spatial autoregressive (SAR) lag model | Spatial regression model | Partial | Define weights, likelihood and impact measures; test stability and endogeneity. |
| S02-RE-02 | Conditional autoregressive (CAR) model | Spatial regression model | Partial | Specify proper/improper CAR and graph conditions; test precision positive-definiteness. |
| S02-RE-03 | Spatial lag model | Spatial regression model | Partial | Clarify naming overlap with SAR; document reduced form and impacts. |
| S02-RE-04 | Spatial error model | Spatial regression model | Partial | Define error process and identification; test residual dependence. |
| S02-RE-05 | SLX model | Spatially lagged covariate regression | Partial | Define covariate lags and impacts; test weights sensitivity. |
| S02-RE-06 | SDEM model | Spatial Durbin error model | Verify | Verify exact specification and parameter constraints; compare nested models. |
| S02-RE-07 | SAC/SARAR model | Spatial regression model | Partial | Joint concentrated Gaussian ML for SARAR/SAC, with both spatial-lag ρ and spatial-error λ processes, is implemented using a coarse two-parameter grid and alternating one-dimensional refinements. Seeded synthetic recovery tests check both parameters and β, plus search-control validation. The conservative parameter rectangle, dense likelihood, Gaussian iid innovations, local refinement and lack of standard errors/robust inference remain open limitations. |
| S02-RE-08 | Spatial Durbin model | Spatial regression model | Partial | Define lagged outcome/covariates and direct/indirect impacts; test interpretation. |
| S02-RE-09 | Manski model | Spatial regression model | Verify | Verify general nesting of lagged y, x and error; document identification. |
| S02-RE-10 | GWR | Local regression model | Partial | Define kernel/bandwidth and local collinearity; test spatial CV. |
| S02-RE-11 | MGWR | Multiscale local regression | Verify | Verify variable-specific bandwidth selection; test inference and collinearity. |
| S02-RE-12 | GTWR | Spatiotemporal local regression | Verify | Verify temporal/spatial kernel and bandwidth; test temporal leakage. |
| S02-RE-13 | Geographically weighted principal components | Local dimension reduction | Verify | Identify exact formulation and local covariance; test bandwidth effects. |
| S02-RE-14 | Geographically weighted summary statistics | Local descriptive statistics | Open | Define local moments and weighting; test edge and sparse-neighbour cases. |
| S02-RE-15 | Spatially varying coefficient models | Regression model family | Partial | Separate frequentist/Bayesian formulations; define smoothness and identifiability. |
| S02-RE-16 | GeoDetector | Spatial stratified heterogeneity method | Verify | Verify factor/ecological detector statistics and discretisation sensitivity. |
| S02-RE-17 | LM-lag diagnostic | Spatial regression diagnostic | Partial | Verify score test and assumptions; test under null/alternative. |
| S02-RE-18 | LM-error diagnostic | Spatial regression diagnostic | Partial | Verify score test and assumptions; test under null/alternative. |
| S02-RE-19 | Robust LM-lag | Spatial regression diagnostic | Partial | Bera–Yoon robust score adjustment for the competing spatial-error alternative is implemented with asymptotic chi-square(1) inference; hand-computed score/denominator tests and a degenerate-identification case are covered. Source-variant verification and broader null/alternative size and power studies remain open. |
| S02-RE-20 | Robust LM-error | Spatial regression diagnostic | Partial | Bera–Yoon robust score adjustment for the competing spatial-lag alternative is implemented with asymptotic chi-square(1) inference; hand-computed score/denominator tests and a degenerate-identification case are covered. Source-variant verification and broader null/alternative size and power studies remain open. |
| S02-RE-21 | Wald test | Model comparison/inference | Partial | Define parameter restrictions and covariance estimator; test finite-sample behaviour. |
| S02-RE-22 | Likelihood-ratio test | Model comparison/inference | Partial | Define nested likelihood conditions and boundary cases. |
| S02-RE-23 | Moran's I on regression residuals | Residual diagnostic | Partial | Define weights and residual standardisation; test size under fitted spatial models. |
| S02-RE-24 | Chow test | Structural break test | Verify | Identify exact spatial/regime variant and known-break assumptions. |
| S02-RE-25 | Spatial regime tests | Spatial heterogeneity diagnostics | Open | Split regime definitions and test statistics; document multiple testing. |
| S02-RE-26 | Breusch–Pagan test | Heteroskedasticity diagnostic | Partial | The auxiliary-regression LM implementation includes the Koenker studentized BP form, uses nR² and rank-based degrees of freedom, and is checked against an independently constructed auxiliary OLS regression and known chi-square tails. The original Gaussian score-test variant and broader finite-sample calibration remain open. |
| S02-RE-27 | Koenker test | Heteroskedasticity diagnostic | Partial | Koenker's studentized Breusch–Pagan nR² test is implemented after OLS, with rank-based chi-square degrees of freedom, independent auxiliary-regression comparison, known-tail checks and invalid/rank-deficient input tests. Spatially dependent error calibration and broader finite-sample size/power studies remain open. |
| S02-RE-28 | GWR significance tests | Local model inference | Verify | Identify exact test and multiple-testing treatment; test bandwidth uncertainty. |
| S02-RE-29 | Spatial GMM | Estimation framework | Partial | Two bounded estimators are implemented: heteroskedasticity-robust two-step spatial-lag IV-GMM with a robust sandwich and overidentification statistic, and homoskedastic-innovation Kelejian–Prucha spatial-error GM followed by feasible GLS. Synthetic SAR recovery, exact-identification, zero-error and invalid/underidentified cases are tested. SARAR GTSLS and heteroskedastic error-GM extensions also exist as separate packages; weak-instrument, spatial-dependence, finite-sample and broader model-family validation remain open. |
| S02-RE-30 | Spatial HAC standard errors | Covariance estimator | Partial | OLS spatial-HAC and spatial-lag 2SLS spatial-HAC covariance baselines use a compact-support Wendland C2 kernel over projected planar coordinates and an explicit bandwidth; tests cover the HC0 no-neighbour limit, hand-reconstructed IV sandwich, symmetry/PSD and invalid inputs. Kernel/bandwidth sensitivity, empirical size and coverage, alternative kernels and scalable sparse implementations remain open. |
| S02-RE-31 | Spatial panel models | Panel econometric family | Open | Split fixed/random effects and lag/error structures; define time/spatial weights. |
| S02-RE-32 | Dynamic spatial panel models | Dynamic panel family | Open | Define temporal and spatial lags, instruments and bias correction. |
| S02-RE-33 | Spatial probit | Limited dependent-variable model | Verify | Verify latent-variable spatial dependence and likelihood approximation. |
| S02-RE-34 | Spatial Heckman model | Selection model | Verify | Define selection/outcome equations and spatial dependence; test identification. |
| S02-RE-35 | Spatial quantile regression | Quantile model | Open | Define spatial dependence and quantile estimand; test crossing and inference. |
| S02-RE-36 | Spatial stochastic frontier | Frontier model | Verify | Verify inefficiency distribution and spatial dependence; test frontier recovery. |
| S02-RE-37 | Spatial SUR | Seemingly unrelated regression | Verify | Define cross-equation and spatial error covariance; test efficiency. |
| S02-RE-38 | Hedonic regression | Applied regression model | Partial | Define spatial dependence, functional form and market boundary; test robustness. |
| S02-RE-39 | Endogenous spatial weights | Model specification/inference | Open | Define weight generation and identification; test sensitivity/endogeneity. |
| S02-RE-40 | Bayesian model averaging over weights | Bayesian model uncertainty | Open | Define candidate weight matrices and posterior model probabilities; test calibration. |
| S02-RE-41 | BYM model | Bayesian disease mapping model | Partial | Separate BYM/BYM2 scaling and priors; test identifiability and structured/unstructured variance. |
| S02-RE-42 | INLA/SPDE | Bayesian latent Gaussian inference | Verify | Distinguish INLA inference from SPDE construction; verify mesh and Matérn mapping. |
| S02-RE-43 | Hierarchical CAR models | Bayesian spatial model family | Partial | Define graph priors and constraints; test propriety and scaling. |
| S02-RE-44 | Spatial Dirichlet process | Bayesian nonparametric model | Open | Define spatial dependence and mixture prior; test posterior clustering. |
| S02-RE-45 | Gaussian process mixtures | Bayesian mixture model | Open | Define component covariance and mixing process; test label identifiability. |

### Smoothing and outlier detection — page 4

| ID | Atomic item | Kind | Status | Required completion work |
|---|---|---|---|---|
| S02-SM-01 | Empirical Bayes rate smoothing | Small-area rate estimator | Partial | Define prior/moment estimation and zero-population handling; compare with direct rates. |
| S02-SM-02 | Head-banging | Spatial smoothing method | Verify | Verify algorithm and convergence; compare with median/local smoothers. |
| S02-SM-03 | Median polish | Robust additive decomposition | Partial | Define row/column effects and missingness; test convergence and residuals. |
| S02-SM-04 | Gaussian filter | Image/spatial filter | Partial | Define kernel support and boundary mode; test variance and units. |
| S02-SM-05 | Laplacian filter | Spatial differential filter | Partial | Define discrete stencil and boundary conditions; test grid spacing. |
| S02-SM-06 | Median filter | Nonlinear spatial filter | Partial | Define neighbourhood and edge policy; test impulse/noise fixtures. |
| S02-SM-07 | Bilateral filter | Edge-preserving filter | Partial | Define spatial/range kernels and units; test edge preservation. |
| S02-SM-08 | Non-local means | Patch-based denoising | Verify | Verify patch search/weighting and complexity; test textured images. |
| S02-SM-09 | Anisotropic diffusion | PDE-based smoothing | Verify | Verify Perona–Malik or alternative model, time step and stability. |
| S02-SM-10 | Total-variation denoising | Variational denoising | Partial | Define isotropic/anisotropic TV and solver; test staircasing and convergence. |
| S02-SM-11 | Guided filter | Edge-preserving filter | Verify | Verify local linear model and radius/epsilon units; test halo behaviour. |
| S02-SM-12 | Z-value spatial outlier test | Spatial outlier statistic | Open | Define local/global reference and variance; test contaminated distributions. |
| S02-SM-13 | Scatterplot outlier approach | Spatial outlier diagnostic | Verify | Resolve exact Moran scatterplot quadrant/outlier method and thresholds. |
| S02-SM-14 | Variogram cloud | Geostatistical diagnostic | Partial | Define pair sampling and distance; test anisotropy and outlier detection. |
| S02-SM-15 | Isolation forest | Anomaly detection | Partial | Define feature representation and contamination; validate spatially blocked. |
| S02-SM-16 | Spatial Local Outlier Factor | Local anomaly detection | Partial | Define neighbourhood and reachability density; test spatial metric. |
| S02-SM-17 | Geographically weighted outlier detection | Local anomaly method family | Open | Define local model/residual and bandwidth; assess masking and multiple tests. |

### Inequality, entropy and scale — page 4

| ID | Atomic item | Kind | Status | Required completion work |
|---|---|---|---|---|
| S02-IE-01 | Spatial Gini coefficient | Inequality metric | Partial | Define population/area weighting and spatial decomposition; test invariance. |
| S02-IE-02 | Theil index | Inequality metric | Partial | Define within/between decomposition and zero handling; test additivity. |
| S02-IE-03 | Spatial entropy | Entropy metric family | Open | Define probability support and spatial weights; distinguish Shannon and spatial dependence forms. |
| S02-IE-04 | Dissimilarity segregation index | Segregation metric | Partial | Define groups and spatial units; test bounds and decomposition. |
| S02-IE-05 | Isolation segregation index | Segregation metric | Partial | Define exposure and group proportions; test population composition. |
| S02-IE-06 | Fractal dimension | Scale/complexity metric | Partial | Identify estimator and scale range; test finite-size bias. |
| S02-IE-07 | Lacunarity | Spatial texture metric | Partial | Define gliding-box method and scale; test binary/weighted patterns. |
| S02-IE-08 | Hurst exponent | Long-range dependence metric | Partial | Define estimator and stationarity assumptions; test synthetic fractional processes. |
| S02-IE-09 | Multifractal analysis | Scaling analysis family | Open | Split partition-function and wavelet methods; define finite-sample limits. |
| S02-IE-10 | Scale-space theory | Multiscale analysis framework | Not applicable | Define scale parameter and representation; link specific filters/feature detectors separately. |
| S02-IE-11 | MAUP analysis | Spatial scale diagnostic | Partial | Define zoning perturbations and statistic; quantify scale and zoning effects separately. |
| S02-IE-12 | 2D periodogram | Spatial spectral analysis | Partial | Define grid/window/periodic assumptions; test known spatial frequencies. |
| S02-IE-13 | Empirical orthogonal functions (EOF) | Spatial dimension reduction | Partial | Define covariance/correlation EOF and centring; test missing data and sign. |
| S02-IE-14 | Singular Spectrum Analysis (SSA) | Time-series decomposition | Verify | Define embedding window and reconstruction; distinguish univariate SSA from spatial extensions. |
| S02-IE-15 | Multichannel SSA (MSSA) | Multivariate time-series decomposition | Verify | Define channel embedding and grouping; test coupled synthetic oscillations. |
| S02-IE-16 | Canonical correlation analysis | Multivariate association | Partial | Define regularisation and rank constraints; test canonical variates. |
| S02-IE-17 | Maximum covariance analysis | Coupled-field analysis | Verify | Verify SVD covariance formulation and preprocessing; test coupled fields. |
| S02-IE-18 | Cross-spectral coherence | Frequency-domain association | Verify | Define cross-spectrum, smoothing and confidence intervals; test known signals. |
| S02-IE-19 | Wavelet coherence | Time-frequency association | Verify | Verify wavelet/edge cone and significance; test phase interpretation. |
| S02-IE-20 | Hilbert–Huang transform | Adaptive signal decomposition | Verify | Verify EMD/HHT variants and mode mixing; test nonlinear nonstationary signals. |

## Completion gates

1. For every statistic, record estimand, null, spatial weights, edge correction, standardisation, inference and multiple-testing policy.
2. For point processes, validate with simulations under both null and alternatives; preserve observation window and intensity estimation.
3. For clustering, test stability, spatial constraints, metric assumptions and scale; compare with nonspatial baselines.
4. For econometric models, document identification, endogeneity, impacts, priors and covariance assumptions; do not confuse software support with verification.
5. For local methods, account for bandwidth selection, multiple testing, boundary effects and spatial leakage.
6. Reconcile canonical lessons, implementations, independent tests, notebooks and coverage records after evidence changes.

**Current conclusion:** Section 2 is decomposed into atomic review items. It remains open; no grouped family is declared fully verified by this register.


## Implementation reconciliation — two-type marked point-pattern summaries

The Partial status for S02-PP-16 reflects a bounded two-mark cross-pattern implementation and its hand-calculation/seeded tests. It does not establish a general marked point-process model or close mark-dependence and randomisation methods.


## Implementation reconciliation — robust spatial LM diagnostics

The Partial status for S02-RE-19 and S02-RE-20 reflects the tested Bera–Yoon robust LM-lag and LM-error score adjustments in `implementations/python/spatial-econometrics/diagnostics.py`. The implementation uses the supplied weights unchanged, reports asymptotic chi-square(1) p-values, and returns unavailable results when the nuisance-adjustment denominator is unidentified. The tests compare both statistics with hand-computed formulae and cover the degenerate case. The canonical lesson cites Anselin, Bera, Florax and Yoon (1996). This is a dense-matrix teaching baseline; broader finite-sample calibration, empirical size/power studies, alternative robust score formulations and independent source review remain open.


## Implementation reconciliation — spatial GMM and spatial HAC

S02-RE-29 is Partial because `implementations/python/spatial-econometrics/` contains a two-step heteroskedasticity-robust spatial-lag IV-GMM estimator using `[X, WX, …, W^qX]`, and a separate homoskedastic-innovation Kelejian–Prucha spatial-error generalized-moments estimator followed by feasible GLS. The package also includes heteroskedastic SARAR GTSLS and a Kelejian–Prucha joint asymptotic covariance extension. Synthetic recovery and identification/invalid-input tests provide bounded implementation evidence, not proof of instrument validity or a complete spatial-GMM family.

S02-RE-30 is Partial because OLS and spatial-lag 2SLS spatial-HAC covariance routines use a documented compact-support Wendland C2 kernel and declared projected-coordinate bandwidth. Tests include the no-cross-location HC0 limit and an independently reconstructed 2SLS sandwich. Finite-sample size/coverage studies, bandwidth selection and sensitivity, alternative kernel families, space-time/network dependence and scalable sparse computation remain open.


## Implementation reconciliation — Koenker studentized heteroskedasticity test

S02-RE-27 is Partial because `implementations/python/spatial-econometrics/heteroskedasticity_diagnostics.py` implements the Koenker studentized Breusch–Pagan auxiliary regression and reports its nR² statistic with rank-based asymptotic chi-square inference. The same routine also implements White's general auxiliary-regression test, but that is a separate method and is not used to overstate the Koenker entry. Tests compare statistics with independently constructed auxiliary regressions, exercise redundant White terms and invalid designs, and check chi-square survival probabilities at known critical values. The methods diagnose non-constant conditional variance after OLS; they do not test spatial dependence. Finite-sample size/power and calibration under spatially correlated errors remain open.


## Implementation reconciliation — SDEM and SARAR/SAC likelihoods

S02-RE-06 is Partial because `implementations/python/spatial-econometrics/slx_sdem.py` implements concentrated Gaussian maximum likelihood for the SDEM specification with spatially lagged covariates and spatially correlated errors. The lesson distinguishes SDEM from SAR/SDM, and tests recover the spatial-error parameter and covariate effects on seeded synthetic data, including the redundant spatial lag of a constant. S02-RE-07 is Partial because `maximum_likelihood.py` implements the joint SARAR/SAC likelihood with separate response-lag and disturbance-lag parameters. A two-dimensional coarse search followed by alternating golden-section refinement is tested against synthetic parameter recovery and invalid search controls. Both are dense teaching baselines; conservative parameter bounds, Gaussian innovation assumptions, no robust covariance/standard errors and no production-scale sparse likelihood remain unresolved.
