# Section 3 — Geostatistics, interpolation, uncertainty, spatiotemporal models

- **Original source section:** 3
- **Source pages:** 4–6 (the small-area and survey estimation subsection continues onto page 6)
- **Source transcription:** [pages 1–5](../../source-inventory/pages-01-05.md) and [pages 6–10](../../source-inventory/pages-06-10.md)
- **Review state:** source entries extracted into this index; not every entry independently verified
- **Current canonical records:** [Space-filling sampling designs](../../algorithms/statistics/space-filling-sampling.md); [Classification accuracy assessment](../../algorithms/statistics/accuracy-assessment.md); [Positional accuracy and uncertainty propagation](../../algorithms/statistics/uncertainty-propagation.md); [Network Ripley's K](../../algorithms/statistics/network-ripley-k.md), an adjacent extension with a tested shortest-path estimator for finite linear networks; [Inverse distance weighting](../../algorithms/interpolation/inverse-distance-weighting.md); [Empirical semivariogram](../../methods/empirical-semivariogram.md); [Vecchia GP approximation](../../algorithms/geostatistics/vecchia-approximation.md); [Knox space-time interaction test](../../algorithms/geostatistics/knox-space-time-test.md); [Spatial interpolation: IDW and ordinary kriging](../../algorithms/geostatistics/interpolation.md); [simple, ordinary and universal kriging](../../algorithms/geostatistics/kriging-variants.md); [sequential Gaussian simulation](../../algorithms/geostatistics/sequential-gaussian-simulation.md); [random Fourier feature GP approximation](../../algorithms/geostatistics/random-fourier-features-gp.md); [stochastic EnKF](../../methods/stochastic-ensemble-kalman-filter.md); [ETKF](../../methods/ensemble-transform-kalman-filter.md) (tested implementations, walkthroughs and an interactive notebook are available; variogram fitting and the wider kriging family remain open)

This section combines surface estimation, stochastic spatial models, simulation, time-dependent analysis, data assimilation, uncertainty measures and small-area estimation. Some entries are model families, some are computational procedures and some are evaluation measures.

## Interpolation

| Source entry | Provisional kind | Source page | Verification status |
|---|---|---:|--- |
| Deterministic: [IDW / original Shepard](../../algorithms/interpolation/inverse-distance-weighting.md), [modified local-quadratic Shepard](../../algorithms/interpolation/modified-shepard.md), [RBF interpolation](../../algorithms/interpolation/radial-basis-function-interpolation.md), [polynomial trend surface](../../algorithms/interpolation/polynomial-trend-surface.md), [TIN barycentric interpolation](../../algorithms/interpolation/tin-interpolation.md), [Sibson natural neighbour](../../algorithms/interpolation/natural-neighbour.md), [Cressman and Barnes objective analysis](../../methods/geophysical-gridding.md), [Whittaker smoother](../../algorithms/interpolation/whittaker-smoother.md) | Interpolation methods / surface models | 4 | Partial — tested planar IDW (original Shepard), local-quadratic modified Shepard variant, thin-plate/cubic/Gaussian RBF interpolation, polynomial trend surfaces, caller-triangulation TIN barycentric interpolation, Sibson stolen-area interpolation, Cressman/Barnes iterative objective analysis and Whittaker-Eilers sequence smoothing are represented. B-spline/NURBS curve evaluation, Schneider cubic Bézier fitting and Kalman/RTS smoothing have separate tested implementations; non-RBF spatial spline-surface interpolation variants and item-level source-entry verification remain open |
| Climate and gap filling: PRISM, Daymet, ANUSPLIN, DINEOF, HANTS, matrix and tensor completion, deep inpainting, spatiotemporal fusion (STARFM, ESTARFM, FSDAF) | Climate products / interpolation and gap-filling methods / fusion workflows | 4 | Partial — tested HANTS-style harmonic fitting with iterative residual rejection and Soft-Impute low-rank matrix completion; PRISM, Daymet, ANUSPLIN, DINEOF, tensor completion, deep inpainting and STARFM/ESTARFM/FSDAF remain open |

## Kriging and geostatistics

| Source entry | Provisional kind | Source page | Verification status |
|---|---|---:|--- |
| Kriging: [ordinary kriging](../../algorithms/geostatistics/interpolation.md), simple, universal, co-kriging, regression kriging, external drift, indicator, disjunctive, block, area-to-point, area-to-area, spatiotemporal | Geostatistical estimators / kriging variants | 4 | Partial — tested dense simple, ordinary and planar universal kriging now complement the PyKrige ordinary-kriging workflow; co-kriging, regression/external drift, indicator/disjunctive, block, area-to-point/area-to-area and spatiotemporal variants remain open |
| [Empirical semivariogram](../../methods/empirical-semivariogram.md), theoretical variogram fitting, anisotropy, nonstationary covariance, spatial deformation, process convolution, multiscale kriging | Covariance and variogram modelling methods / geostatistical approaches | 4 | Partial — Matheron, Cressie-Hawkins, Dowd and Genton (Q_n) empirical estimators and bounded spherical/exponential/Gaussian weighted least-squares and dense constant-mean REML fitting are tested; automatic anisotropy estimation, uncertainty, broader covariance structures and source-entry review remain open |
| Large-data Gaussian processes: Vecchia, NNGP, covariance tapering, fixed rank kriging, predictive processes, lattice kriging, multi-resolution approximation | Gaussian-process approximations / scalable spatial models | 4 | Partial — a tested nearest-predecessor Vecchia Gaussian likelihood approximation with exact all-neighbour comparison and a Gaussian-kernel Bayesian random Fourier feature predictor are implemented; NNGP prediction, tapering, fixed-rank, lattice and multi-resolution methods remain open |
| Simulation: sequential Gaussian, indicator simulation, multiple-point statistics (SNESIM, direct sampling), object-based, p-field | Spatial simulation methods | 5 | Partial — a tested small-grid sequential Gaussian simulator now samples from simple-kriging conditional distributions with seeded random ordering; indicator simulation, SNESIM/direct sampling, object-based and p-field methods remain open |
| Extremes and dependence: max-stable processes (Brown-Resnick), spatial copulas, GEV and Gumbel fits | Extreme-value and dependence models | 5 | Not checked — intake only |
| Sampling design: spatially balanced (GRTS, BAS), cLHS, stratified, spatial thinning | Sampling designs / sampling procedures | 5 | Partial — tested Latin hypercube/centered LHS, multi-start maximin LHS and seeded greedy minimum-distance spatial thinning; GRTS, BAS, cLHS-specific balancing, design weights/inclusion probabilities and source-entry review remain open |
| Digital soil mapping: SCORPAN, pedotransfer functions, equal-area splines, SoilGrids-style stacking | Domain modelling frameworks / estimation methods / product-style workflow | 5 | Not checked — intake only |

## Spatiotemporal statistics

| Source entry | Provisional kind | Source page | Verification status |
|---|---|---:|--- |
| STARMA, space-time ARIMA, GTWR, dynamic linear and state-space models | Spatiotemporal model families | 5 | Not checked — intake only |
| Spatiotemporal GP (separable and non-separable kernels), spatiotemporal INLA, functional data analysis | Spatiotemporal Gaussian processes / inference framework / statistical methods | 5 | Not checked — intake only |
| Space-time scan statistics, Knox test, space-time K function, space-time cube, emerging hot spot analysis | Spatiotemporal tests / summary methods / analysis workflow | 5 | Partial — a tested Knox close-in-space/close-in-time pair statistic with temporal-label permutation inference is implemented; space-time K, scan statistics, cube and emerging-hotspot workflows remain open |
| Spatial survival and frailty models | Survival model families | 5 | Not checked — intake only |
| Spatiotemporal point processes: Hawkes, LGCP, ETAS | Point-process model families | 5 | Not checked — intake only |
| Trend and change: Mann-Kendall, Sen's slope, harmonic regression, BFAST, LandTrendr, CCDC | Trend tests / regression / change-detection methods | 5 | Partial — tested tie-corrected Mann-Kendall/tau-b, Sen slope, seasonal Mann-Kendall/seasonal Sen and least-squares harmonic regression; serial-correlation correction, BFAST, LandTrendr and CCDC remain open |

## Data assimilation and inverse methods

| Source entry | Provisional kind | Source page | Verification status |
|---|---|---:|--- |
| Optimal interpolation, 3D-Var, 4D-Var, ensemble Kalman filter, LETKF, particle filters | Data assimilation algorithms | 5 | Partial — tested stochastic perturbed-observation EnKF and deterministic ETKF analysis, plus EKF/UKF and particle filter/smoother baselines; optimal interpolation, 3D/4D-Var, LETKF, forecast cycling and full model-coupled assimilation remain open |
| Variational and Bayesian inversion, adjoint methods, emulators and surrogate models | Inverse methods / optimisation / approximation models | 5 | Not checked — intake only |
| Radiative transfer inversion (PROSAIL, look-up tables) | Physical retrieval / inversion workflow | 5 | Not checked — intake only |

## Uncertainty, accuracy and sensitivity

| Source entry | Provisional kind | Source page | Verification status |
|---|---|---:|--- |
| Positional accuracy (RMSE), error propagation, Monte Carlo, Latin hypercube, Sobol sensitivity, polynomial chaos | Accuracy measures / uncertainty propagation / sensitivity methods | 5 | Partial — tested coordinate bias/axis and pooled RMSE, seeded Monte Carlo propagation for independent uniform inputs, and Saltelli first-/total-order Sobol estimates; correlated/arbitrary distributions, confidence intervals, polynomial chaos and source-entry review remain open |
| Classification accuracy: confusion matrix, kappa, area-adjusted accuracy (Olofsson), fuzzy kappa, Figure of Merit, quantity and allocation disagreement | Accuracy assessment measures and procedures | 5 | Partial — tested reference-row/prediction-column confusion matrix, overall/producer/user accuracy, Cohen's kappa, quantity/allocation disagreement and binary change Figure of Merit; area-adjusted accuracy, fuzzy kappa, design-based uncertainty and source-entry review remain open |
| Bayesian: MCMC (Metropolis, HMC, NUTS), variational inference, approximate Bayesian computation, Bayesian model averaging | Bayesian inference algorithms / approximation methods | 5 | Not checked — intake only |
| Probabilistic and fuzzy maps: ensemble spread, interval-valued, possibilistic, conformal prediction (including locally adaptive), quantile regression forests, area of applicability, dissimilarity index | Uncertainty representations / prediction methods / applicability diagnostics | 5 | Not checked — intake only |
| Reasoning under imprecision: fuzzy and rough sets, Dempster-Shafer, Bayesian belief networks, possibility theory | Uncertainty and evidence frameworks | 5 | Not checked — intake only |

## Small-area and survey estimation

| Source entry | Provisional kind | Source page | Verification status |
|---|---|---:|--- |
| Fay-Herriot, unit-level small-area models, Horvitz-Thompson, model-assisted estimation, MRP | Small-area estimators / survey estimators / multilevel modelling | 6 | Partial — tested Fay-Herriot area-level REML/EBLUP and Horvitz-Thompson total/mean with pairwise design-variance estimator; unit-level models, model-assisted estimation and MRP remain open |
| Spatial microsimulation (IPF, simulated annealing), areal interpolation, dasymetric mapping, WorldPop-style random forest population surfaces | Spatial microsimulation / areal estimation / mapping workflows | 6 | Partial — tested 2D iterative proportional fitting with structural-zero preservation and convergence diagnostics; simulated annealing, areal interpolation, dasymetric mapping and random-forest surfaces remain open |
| Statistical downscaling: quantile mapping, BCSD, delta change, analog methods | Downscaling methods | 6 | Partial — tested univariate empirical quantile mapping and additive/multiplicative delta-change baselines; BCSD, analog and multivariate methods remain open |

## First audited lesson

The [empirical semivariogram lesson](../../methods/empirical-semivariogram.md) explains the pairwise estimator and binning contract. The [interpolation lesson](../../algorithms/geostatistics/interpolation.md) compares deterministic inverse distance weighting with ordinary kriging. A tested teaching implementation covers IDW and a dense ordinary-kriging solver using a specified zero-nugget isotropic exponential variogram. It does not fit variogram parameters or cover the wider kriging family.

## Decisions for the next pass

1. Separate deterministic interpolation from stochastic geostatistical prediction.
2. Verify the assumptions behind variograms, stationarity, covariance models and kriging variants.
3. Explain prediction uncertainty separately from prediction error and validation accuracy.
4. Distinguish space-time models from methods that merely display or aggregate data in a time cube.
5. Treat named products and workflows (such as PRISM, Daymet and SoilGrids-style stacking) differently from algorithms.
6. Use reproducible synthetic surfaces and known sampling designs to demonstrate uncertainty and interpolation behaviour.

## Bibliographic check on the geostatistics foundation

Matheron (1963), “Principles of geostatistics,” *Economic Geology*, 58(8), 1246–1266, [10.2113/gsecongeo.58.8.1246](https://doi.org/10.2113/gsecongeo.58.8.1246), was checked against the publisher and DOI records and is now cited in the interpolation lesson. This confirms the selected foundational citation only; it does not verify the full kriging family or all Section 3 source entries.


The trend/change source entry now also links to seasonal Mann-Kendall and seasonal Sen slope reference methods. Seasonal comparisons are restricted to matching season labels; score and tie-corrected variance are aggregated across seasons, and the slope is the median of within-season pair slopes. The implementation is dependency-free and covered by tests. It does not correct serial correlation within seasons, dependence between seasons, missingness mechanisms or multiple testing, and its p-value remains a normal approximation. The grouped source row remains partial; harmonic regression, BFAST, LandTrendr and CCDC remain open.


The trend/change source entry now also links to a least-squares harmonic regression baseline with configurable period, number of Fourier harmonics and optional linear trend. It returns coefficients, fitted values, residuals, RMSE and R², with rank and sample-size checks. The implementation does not provide autocorrelation-robust inference, automatic period selection, BFAST, LandTrendr or CCDC; the grouped source row remains partial.
