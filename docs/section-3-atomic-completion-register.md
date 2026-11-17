# Section 3 atomic completion register

**Source:** *Spatial Analysis Algorithms: Complete Compendium*, Section 3, pages 4–6.  
**Intake:** [preserved pages 1–5](../source-inventory/pages-01-05.md) and [pages 6–10](../source-inventory/pages-06-10.md).  
**Section index:** [Section 3 catalogue record](../catalog/sections/03-geostatistics.md).

This register separates source groupings into child records and records the work required to establish method identity, statistical assumptions, implementation fidelity and validation. Follow the [verification protocol](../catalog/verification-protocol.md) and [completion standard](compendium-completion-standard.md).

| Status | Meaning |
|---|---|
| Open | No item-specific independent evidence recorded here. |
| Partial | A bounded related implementation exists; variants or validation remain open. |
| Verify | Exact method, model or software identity must be resolved. |
| Not applicable | A workflow or broad family requires a different record kind. |

## Atomic source register

### Interpolation — page 4

| ID | Atomic item | Kind | Status | Required completion work |
|---|---|---|---|---|
| S03-IN-01 | Inverse Distance Weighting (IDW) | Deterministic interpolator | Partial | Define power, neighbourhood and exact-point handling; test affine/constant surfaces. |
| S03-IN-02 | Natural neighbour interpolation | Geometric interpolator | Partial | Verify Sibson/Laplace variants and hull extrapolation; test duplicates and boundaries. |
| S03-IN-03 | Spline interpolation | Interpolator family | Open | Split thin-plate, tension and regularised variants; define smoothness and boundary conditions. |
| S03-IN-04 | Thin-plate spline | Radial basis interpolator | Partial | Verify kernel, polynomial terms and smoothing; test conditioning and affine reproduction. |
| S03-IN-05 | Radial Basis Function (RBF) interpolation | Interpolator family | Partial | Define kernel, shape parameter and polynomial tail; test conditioning and extrapolation. |
| S03-IN-06 | Shepard interpolation | Local weighted interpolator | Verify | Verify original/local variants and smoothing; compare with IDW. |
| S03-IN-07 | Cressman analysis | Successive correction interpolator | Verify | Verify radius sequence and correction weights; test station distribution and conservation. |
| S03-IN-08 | Barnes analysis | Objective analysis interpolator | Verify | Verify Gaussian weighting and successive passes; test response to sampling density. |
| S03-IN-09 | Trend surface analysis | Global regression interpolator | Partial | Define polynomial order and coordinate scaling; test overfit and extrapolation. |
| S03-IN-10 | TIN interpolation | Piecewise planar interpolator | Partial | Define triangulation and breakline handling; test continuity and convex-hull limits. |
| S03-IN-11 | Whittaker smoother | Penalised smoother | Verify | Verify penalty order, lambda and boundary treatment; test missing observations. |
| S03-IN-12 | PRISM climate interpolation | Climate mapping system/model | Verify | Identify PRISM version and predictors; document elevation/climate effects and licence. |
| S03-IN-13 | Daymet | Gridded climate product/method | Verify | Identify product/version and interpolation lineage; document station data and uncertainty. |
| S03-IN-14 | ANUSPLIN | Spline climate interpolation software | Verify | Verify software version, spline formulation and covariates; document licence. |
| S03-IN-15 | DINEOF | Data-interpolating empirical orthogonal functions | Verify | Verify iterative EOF algorithm, rank selection and convergence; test missing-data patterns. |
| S03-IN-16 | HANTS | Harmonic analysis of time series | Verify | Verify frequency selection, outlier rejection and gap filling; test irregular sampling. |
| S03-IN-17 | Matrix completion | Missing-data reconstruction family | Open | Split convex/nonconvex and low-rank methods; define missingness and rank assumptions. |
| S03-IN-18 | Tensor completion | Multidimensional missing-data reconstruction | Open | Split CP/Tucker/tensor-train and regularisation; test recovery under structured missingness. |
| S03-IN-19 | Deep inpainting | Learned gap-filling family | Open | Identify architectures and training data; assess spatial/temporal leakage and uncertainty. |
| S03-IN-20 | STARFM | Spatiotemporal image fusion | Verify | Verify original algorithm and inputs; reproduce temporal transfer and error metrics. |
| S03-IN-21 | ESTARFM | Spatiotemporal image fusion | Verify | Verify enhanced method and assumptions; test heterogeneous landscapes. |
| S03-IN-22 | FSDAF | Flexible spatiotemporal data fusion | Verify | Verify exact formulation and source; test land-cover change and spatial heterogeneity. |

### Kriging and geostatistics — pages 4–5

| ID | Atomic item | Kind | Status | Required completion work |
|---|---|---|---|---|
| S03-KR-01 | Simple kriging | Geostatistical predictor | Partial | Define known mean and covariance; test unbiasedness/MSE under simulated Gaussian field. |
| S03-KR-02 | Ordinary kriging | Geostatistical predictor | Partial | Verify unknown constant mean constraint; test variogram/covariance and prediction variance. |
| S03-KR-03 | Universal kriging | Geostatistical predictor | Partial | Define drift basis and unbiasedness constraints; test polynomial drift recovery. |
| S03-KR-04 | Co-kriging | Multivariate geostatistical predictor | Partial | Define cross-covariance validity and collocated variants; test co-regionalisation. |
| S03-KR-05 | Regression kriging | Hybrid regression/geostatistical predictor | Partial | Separate trend and residual components; test cross-validation and uncertainty combination. |
| S03-KR-06 | External drift kriging | Geostatistical predictor | Verify | Verify drift constraint and covariate support; test collinearity and missing covariates. |
| S03-KR-07 | Indicator kriging | Categorical/probability geostatistics | Partial | Define thresholds and indicator variograms; test probability ordering/calibration. |
| S03-KR-08 | Disjunctive kriging | Nonlinear geostatistical predictor | Verify | Verify Hermite transform and Gaussian assumptions; test back-transform. |
| S03-KR-09 | Block kriging | Areal support predictor | Partial | Define block integration and discretisation; compare point/block predictions. |
| S03-KR-10 | Area-to-point kriging | Change-of-support predictor | Verify | Verify mass-preserving constraints and covariance; test aggregation consistency. |
| S03-KR-11 | Area-to-area kriging | Change-of-support predictor | Verify | Define support covariance and target areas; test conservation and overlap. |
| S03-KR-12 | Spatiotemporal kriging | Space-time predictor | Partial | Define space-time covariance and temporal support; test separable/nonseparable cases. |
| S03-KR-13 | Variogram modelling | Covariance model fitting | Partial | Define estimator, lag binning, anisotropy and model validity; test simulation. |
| S03-KR-14 | Geometric anisotropy | Covariance structure | Partial | Define rotation/scaling and range ratios; test directional variograms. |
| S03-KR-15 | Zonal anisotropy | Covariance structure | Verify | Verify model definition and continuity; distinguish from geometric anisotropy. |
| S03-KR-16 | Nonstationary covariance | Covariance model family | Open | Split process convolution, deformation and local kernels; establish positive definiteness. |
| S03-KR-17 | Spatial deformation | Nonstationary spatial model | Verify | Verify deformation map and identifiability; test distance distortion and prediction. |
| S03-KR-18 | Process convolution | Gaussian process construction | Verify | Define kernel convolution and latent noise; test covariance derivation. |
| S03-KR-19 | Multiscale kriging | Multiresolution predictor family | Open | Split basis/scale formulations; define covariance and support across scales. |
| S03-KR-20 | Vecchia approximation | Scalable GP approximation | Partial | Define neighbour ordering and conditional factorisation; test KL/prediction error. |
| S03-KR-21 | Nearest-neighbour Gaussian process (NNGP) | Scalable GP model | Partial | Verify directed acyclic graph and neighbour selection; test sparse precision and prediction. |
| S03-KR-22 | Covariance tapering | Sparse covariance approximation | Partial | Define compact taper and positive-definiteness; test bias/variance and sparsity. |
| S03-KR-23 | Fixed-rank kriging | Low-rank GP approximation | Partial | Define basis construction and residual covariance; test approximation and uncertainty. |
| S03-KR-24 | Predictive processes | Low-rank GP approximation | Verify | Verify knot process and variance correction; test oversmoothing. |
| S03-KR-25 | Lattice kriging | Areal/spatial basis model | Verify | Resolve exact lattice formulation and conditional structure; test boundary behaviour. |
| S03-KR-26 | Multi-resolution approximation (MRA) | Multiresolution GP approximation | Verify | Verify basis partition and recursive residual; test approximation convergence. |

### Geostatistical simulation and extremes — page 5

| ID | Atomic item | Kind | Status | Required completion work |
|---|---|---|---|---|
| S03-SI-01 | Sequential Gaussian simulation | Conditional geostatistical simulation | Partial | Define path, conditioning and variogram; test conditional moments and reproduction. |
| S03-SI-02 | Sequential indicator simulation | Conditional categorical simulation | Partial | Define indicator thresholds and conditional probabilities; test proportions and connectivity. |
| S03-SI-03 | SNESIM | Multiple-point geostatistics | Verify | Verify training-image search tree and pattern conditioning; test reproduction. |
| S03-SI-04 | Direct Sampling | Multiple-point geostatistics | Verify | Verify pattern distance and scan stopping; document computational trade-offs. |
| S03-SI-05 | Object-based geostatistical simulation | Simulation family | Open | Define object catalogue, placement and conditioning; test spatial statistics. |
| S03-SI-06 | p-field simulation | Conditional simulation method | Verify | Verify probability-field construction and conditioning; test marginal/variogram reproduction. |
| S03-EX-01 | Max-stable processes | Spatial extremes model family | Verify | Split Brown–Resnick/Smith/Schlather variants; define extremal dependence and inference. |
| S03-EX-02 | Brown–Resnick process | Max-stable process | Verify | Verify variogram parameterisation and spectral construction; test extremal coefficient. |
| S03-EX-03 | Spatial copulas | Dependence model family | Open | Split copula construction and tail dependence; test valid multivariate dependence. |
| S03-EX-04 | GEV fitting | Extreme-value distribution estimation | Partial | Define block maxima, parameter constraints and uncertainty; test coverage. |
| S03-EX-05 | Gumbel fitting | Extreme-value distribution estimation | Partial | Define Gumbel parameterisation and relation to GEV; test MLE and return levels. |

### Sampling design and digital soil mapping — page 5

| ID | Atomic item | Kind | Status | Required completion work |
|---|---|---|---|---|
| S03-SA-01 | Generalised Random Tessellation Stratified (GRTS) sampling | Spatially balanced sampling | Verify | Verify hierarchy/order and inclusion probabilities; test balance and design variance. |
| S03-SA-02 | Balanced Acceptance Sampling (BAS) | Spatially balanced sampling | Verify | Verify acceptance criterion and spatial balance; test inclusion probabilities. |
| S03-SA-03 | Conditioned Latin Hypercube Sampling (cLHS) | Sampling design | Partial | Define marginal/correlation matching and objective; test representativeness. |
| S03-SA-04 | Stratified spatial sampling | Sampling design family | Partial | Define strata, allocation and spatial balance; test variance estimation. |
| S03-SA-05 | Spatial thinning | Point pattern sampling | Partial | Define minimum separation and selection algorithm; test intensity and bias. |
| S03-SA-06 | SCORPAN digital soil mapping framework | Soil mapping framework | Verify | Verify factors and modelling protocol; distinguish framework from estimator. |
| S03-SA-07 | Pedotransfer functions | Soil property prediction family | Open | Identify target properties and predictor domains; validate independent soil profiles. |
| S03-SA-08 | Equal-area splines | Soil mapping interpolation | Verify | Verify spline basis and area-preserving constraints; test aggregation. |
| S03-SA-09 | SoilGrids-style model stacking | Soil mapping workflow | Verify | Identify SoilGrids version and model ensemble; document covariates, depth and licence. |

### Spatiotemporal statistics — page 5

| ID | Atomic item | Kind | Status | Required completion work |
|---|---|---|---|---|
| S03-ST-01 | STARMA | Space-time autoregressive moving-average model | Verify | Verify spatial weights/lag formulation and stationarity; test simulated process. |
| S03-ST-02 | Space-time ARIMA | Spatiotemporal time-series model | Open | Define temporal/spatial differencing and covariance; distinguish lattice variants. |
| S03-ST-03 | GTWR | Geographically and temporally weighted regression | Verify | Resolve overlap with Section 2 GTWR; define temporal kernel and bandwidth selection. |
| S03-ST-04 | Dynamic linear models | State-space model family | Partial | Define latent state, observation and evolution; test filtering/smoothing. |
| S03-ST-05 | State-space models | Time-series model family | Partial | Separate linear/nonlinear and Gaussian/non-Gaussian variants; define inference. |
| S03-ST-06 | Separable spatiotemporal GP kernels | Covariance family | Partial | Define product covariance and validity; test separability assumptions. |
| S03-ST-07 | Nonseparable spatiotemporal GP kernels | Covariance family | Open | Verify Gneiting and other valid classes; test space-time interaction. |
| S03-ST-08 | Spatiotemporal INLA | Bayesian inference workflow | Verify | Identify latent model and mesh construction; document approximation and posterior diagnostics. |
| S03-ST-09 | Functional data analysis | Statistical model family | Open | Define functional domain, basis and covariance; specify spatial dependence separately. |
| S03-ST-10 | Space-time scan statistics | Cluster detection | Partial | Define scanning window and null; test multiple testing and temporal aggregation. |
| S03-ST-11 | Knox test | Space-time interaction test | Verify | Verify spatial/temporal distance thresholds and null randomisation. |
| S03-ST-12 | Space-time K function | Point process statistic | Verify | Verify estimator and edge correction; test separable/clustered processes. |
| S03-ST-13 | Space-time cube | Visual analytics representation | Not applicable | Define aggregation/time binning and interaction; do not treat as inferential algorithm. |
| S03-ST-14 | Emerging hot spot analysis | Space-time cluster classification workflow | Verify | Identify exact Mann-Kendall/Getis-Ord sequence and category rules; test temporal edge cases. |
| S03-ST-15 | Spatial survival models | Survival model family | Open | Define spatial frailty/dependence and censoring; test proportional hazards assumptions. |
| S03-ST-16 | Spatial frailty models | Survival/random-effects model | Verify | Define frailty distribution and spatial structure; test identifiability. |
| S03-ST-17 | Hawkes process | Self-exciting point process | Partial | Define triggering kernel and background intensity; test branching ratio/stability. |
| S03-ST-18 | Log-Gaussian Cox process (LGCP) | Spatiotemporal point process | Partial | Resolve static/space-time variants and latent field inference; test moments. |
| S03-ST-19 | Epidemic-Type Aftershock Sequence (ETAS) | Self-exciting event model | Verify | Verify productivity/temporal-spatial kernels and magnitude mark; test simulation. |
| S03-ST-20 | Mann–Kendall trend test | Nonparametric trend test | Partial | Define tie/seasonal variants and serial correlation correction; test null size. |
| S03-ST-21 | Sen's slope | Robust trend estimator | Partial | Define median pairwise slope and missing/tie handling; test trend recovery. |
| S03-ST-22 | Harmonic regression | Periodic regression | Partial | Define frequencies, trend and uncertainty; test irregular sampling. |
| S03-ST-23 | BFAST | Time-series break detection | Verify | Verify decomposition and breakpoint procedure; test seasonal/trend changes. |
| S03-ST-24 | LandTrendr | Spectral time-series segmentation | Verify | Verify algorithm/version and temporal segmentation; document sensor harmonisation. |
| S03-ST-25 | CCDC | Continuous Change Detection and Classification | Verify | Verify model update and change rules; test temporal gaps and false alarms. |

### Data assimilation and inverse methods — page 5

| ID | Atomic item | Kind | Status | Required completion work |
|---|---|---|---|---|
| S03-DA-01 | Optimal interpolation | Data assimilation method | Partial | Define background/observation covariance and gain; test linear Gaussian oracle. |
| S03-DA-02 | 3D-Var | Variational assimilation | Verify | Verify cost function and background covariance; test gradient and minimiser. |
| S03-DA-03 | 4D-Var | Variational assimilation | Verify | Define time window, tangent-linear/adjoint and strong/weak constraint; test twin experiment. |
| S03-DA-04 | Ensemble Kalman filter | Sequential assimilation | Partial | Define ensemble transform/stochastic update; test spread and filter consistency. |
| S03-DA-05 | Local Ensemble Transform Kalman Filter (LETKF) | Local ensemble assimilation | Verify | Verify local analysis and inflation/localisation; test rank-deficient ensembles. |
| S03-DA-06 | Particle filters | Sequential Bayesian inference family | Partial | Split bootstrap/auxiliary/resample-move; test degeneracy and effective sample size. |
| S03-DA-07 | Variational inversion | Inverse problem framework | Partial | Define objective, regularisation and adjoint; test synthetic parameter recovery. |
| S03-DA-08 | Bayesian inversion | Bayesian inverse problem | Partial | Define prior, likelihood and posterior approximation; test identifiability/coverage. |
| S03-DA-09 | Adjoint methods | Gradient computation | Verify | Verify adjoint derivation and discrete consistency; compare with finite differences. |
| S03-DA-10 | Emulators and surrogate models | Approximation workflow | Partial | Define training design and uncertainty; validate against held-out simulator runs. |
| S03-DA-11 | PROSAIL inversion | Radiative transfer inversion | Verify | Verify PROSPECT+SAIL versions and parameter priors; test LUT/optimisation inversion. |
| S03-DA-12 | Look-up-table inversion | Retrieval method | Partial | Define parameter grid, interpolation and ambiguity; quantify discretisation error. |

### Uncertainty, accuracy and sensitivity — page 5

| ID | Atomic item | Kind | Status | Required completion work |
|---|---|---|---|---|
| S03-UN-01 | Positional RMSE | Accuracy metric | Partial | Define reference/control sample and coordinate frame; report bias and confidence intervals. |
| S03-UN-02 | Error propagation | Uncertainty method | Partial | Define linear/nonlinear propagation and covariance; compare Monte Carlo. |
| S03-UN-03 | Monte Carlo uncertainty analysis | Simulation method | Partial | Define sampling distribution, convergence and Monte Carlo error. |
| S03-UN-04 | Latin hypercube sampling | Space-filling sampling | Partial | Verify stratification and dependence handling; test discrepancy. |
| S03-UN-05 | Sobol sensitivity indices | Global sensitivity analysis | Verify | Verify first/total/higher-order estimators and sample design; test analytic functions. |
| S03-UN-06 | Polynomial chaos expansion | Uncertainty propagation | Verify | Define polynomial basis/distribution and truncation; test convergence. |
| S03-UN-07 | Confusion matrix | Classification evaluation | Partial | Define class ordering and weighting; test absent classes and multiclass. |
| S03-UN-08 | Cohen's kappa | Classification agreement metric | Partial | Define chance agreement and prevalence caveats; test imbalanced data. |
| S03-UN-09 | Area-adjusted accuracy (Olofsson) | Map accuracy estimator | Verify | Verify stratified area estimator and confidence interval; test unequal sampling. |
| S03-UN-10 | Fuzzy kappa | Fuzzy classification agreement | Verify | Verify similarity kernel and reference; test spatial tolerance. |
| S03-UN-11 | Figure of Merit | Change detection metric | Verify | Verify change/no-change confusion definition; test class imbalance. |
| S03-UN-12 | Quantity disagreement | Map comparison metric | Verify | Verify Pontius decomposition and normalisation; test known contingency tables. |
| S03-UN-13 | Allocation disagreement | Map comparison metric | Verify | Verify decomposition and relation to quantity disagreement. |
| S03-UN-14 | MCMC | Bayesian sampling family | Partial | Split kernels and diagnostics; verify convergence, mixing and reproducibility. |
| S03-UN-15 | Metropolis algorithm | MCMC transition kernel | Partial | Verify acceptance ratio and irreducibility; test known posterior. |
| S03-UN-16 | Hamiltonian Monte Carlo (HMC) | Gradient-based MCMC | Partial | Define mass matrix, step size and energy diagnostics; test Gaussian target. |
| S03-UN-17 | NUTS | Adaptive HMC algorithm | Verify | Verify tree-building and stopping criterion; test divergences and effective sample size. |
| S03-UN-18 | Variational inference | Approximate Bayesian inference | Partial | Define variational family/objective; assess posterior underdispersion. |
| S03-UN-19 | Approximate Bayesian computation (ABC) | Likelihood-free inference | Verify | Define summary statistics, distance and tolerance; test posterior calibration. |
| S03-UN-20 | Bayesian model averaging | Bayesian model uncertainty | Partial | Define candidate set/prior and predictive combination; test calibration. |
| S03-UN-21 | Ensemble spread | Predictive uncertainty summary | Partial | Distinguish spread from calibrated uncertainty; test coverage. |
| S03-UN-22 | Interval-valued maps | Uncertainty representation | Open | Define interval construction and interpretation; test spatial dependence. |
| S03-UN-23 | Possibilistic maps | Uncertainty representation | Open | Define possibility distribution and calibration; distinguish from probability. |
| S03-UN-24 | Conformal prediction | Distribution-free predictive inference | Partial | Define exchangeability and score; test marginal coverage under spatial dependence. |
| S03-UN-25 | Locally adaptive conformal prediction | Adaptive conformal method | Verify | Verify local score/scale estimation; test conditional coverage. |
| S03-UN-26 | Quantile regression forests | Conditional quantile model | Verify | Verify forest variant and quantile estimator; test calibration and extrapolation. |
| S03-UN-27 | Area of applicability | Model transfer diagnostic | Verify | Identify exact method and distance metric; test geographic transfer and threshold. |
| S03-UN-28 | Dissimilarity index | Extrapolation diagnostic | Verify | Verify feature-space distance and scaling; test sensitivity to covariate support. |
| S03-UN-29 | Fuzzy sets | Imprecise reasoning framework | Not applicable | Define membership functions and operators; link concrete algorithms separately. |
| S03-UN-30 | Rough sets | Imprecise reasoning framework | Not applicable | Define approximation spaces and indiscernibility; distinguish model from workflow. |
| S03-UN-31 | Dempster–Shafer theory | Evidence combination framework | Verify | Verify mass functions, combination and conflict handling; test edge cases. |
| S03-UN-32 | Bayesian belief networks | Probabilistic graphical model | Partial | Define DAG, conditional probability tables and inference; test exact small networks. |
| S03-UN-33 | Possibility theory | Uncertainty framework | Not applicable | Define possibility/necessity measures; distinguish from probability and fuzzy membership. |

### Small-area and survey estimation — pages 5–6

| ID | Atomic item | Kind | Status | Required completion work |
|---|---|---|---|---|
| S03-SA-10 | Fay–Herriot area-level model | Small-area estimation model | Verify | Verify sampling variance and linking model; test benchmark domain estimates. |
| S03-SA-11 | Unit-level small-area models | Small-area model family | Open | Split nested error and alternatives; define sampling design and population prediction. |
| S03-SA-12 | Horvitz–Thompson estimator | Design-based estimator | Partial | Define inclusion probabilities and variance; test unbiasedness under unequal sampling. |
| S03-SA-13 | Model-assisted estimation | Survey estimation framework | Open | Define design consistency and auxiliary model; test design-based variance. |
| S03-SA-14 | Multilevel regression and poststratification (MRP) | Small-area estimation workflow | Partial | Define multilevel model, poststratification cells and population counts; test calibration. |
| S03-SA-15 | Spatial microsimulation by iterative proportional fitting (IPF) | Synthetic population generation | Partial | Define marginal constraints and seed matrix; test convergence and exact margins. |
| S03-SA-16 | Spatial microsimulation by simulated annealing | Synthetic population generation | Verify | Verify objective, proposals and cooling schedule; test constraint satisfaction. |
| S03-SA-17 | Areal interpolation | Change-of-support method | Partial | Split area-weighted/dasymetric/pycnophylactic methods; test conservation. |
| S03-SA-18 | Dasymetric mapping | Population/attribute disaggregation | Partial | Define ancillary masks/weights and conservation; validate at independent fine scale. |
| S03-SA-19 | WorldPop-style random forest population surfaces | Population mapping workflow | Verify | Identify product version, model and covariates; document uncertainty, training data and licence. |
| S03-SA-20 | Quantile mapping | Statistical downscaling/bias correction | Partial | Define empirical/parametric and trend-preserving variants; test distribution tails. |
| S03-SA-21 | Bias Correction and Spatial Disaggregation (BCSD) | Climate downscaling workflow | Verify | Verify exact method/version and sequence; test spatial coherence and trend preservation. |
| S03-SA-22 | Delta-change method | Climate downscaling method | Partial | Define additive/multiplicative delta and baseline; test climate-change signal. |
| S03-SA-23 | Analog methods | Statistical downscaling family | Open | Define analogue distance and selection; validate extremes and spatial coherence. |

## Completion gates

1. For all geostatistical predictors, define support, mean/trend, covariance/variogram validity, neighbourhood, uncertainty and back-transformation.
2. For simulations and approximations, validate moments, covariance, conditioning and uncertainty against exact/small or analytical cases.
3. For spatiotemporal methods, state temporal sampling, missingness, stationarity and leakage controls.
4. For data assimilation/inversion, specify forward model, observation operator, prior/background covariance, solver and identifiability.
5. For accuracy and uncertainty, distinguish predictive uncertainty, measurement error, model error and sampling uncertainty.
6. For small-area/survey estimates, preserve inclusion probabilities, population support, design consistency and privacy.
7. Update canonical records and coverage only after independent evidence and tests are recorded.

**Current conclusion:** Section 3 is decomposed into atomic review items. It remains open; the register is not a claim that every method, model or workflow has been verified or reproduced.
