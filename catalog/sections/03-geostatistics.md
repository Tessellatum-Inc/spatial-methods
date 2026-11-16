# Section 3 — Geostatistics, interpolation, uncertainty, spatiotemporal models

- **Original source section:** 3
- **Source pages:** 4–6 (the small-area and survey estimation subsection continues onto page 6)
- **Source transcription:** [pages 1–5](../../source-inventory/pages-01-05.md) and [pages 6–10](../../source-inventory/pages-06-10.md)
- **Review state:** source entries extracted into this index; not every entry independently verified
- **Current canonical records:** [Network Ripley's K](../../algorithms/statistics/network-ripley-k.md), an adjacent extension with a tested shortest-path estimator for finite linear networks; [Inverse distance weighting](../../algorithms/interpolation/inverse-distance-weighting.md); [Empirical semivariogram](../../methods/empirical-semivariogram.md); [Spatial interpolation: IDW and ordinary kriging](../../algorithms/geostatistics/interpolation.md) (tested implementations, walkthroughs and an interactive notebook are available; variogram fitting and the wider kriging family remain open)

This section combines surface estimation, stochastic spatial models, simulation, time-dependent analysis, data assimilation, uncertainty measures and small-area estimation. Some entries are model families, some are computational procedures and some are evaluation measures.

## Interpolation

| Source entry | Provisional kind | Source page | Verification status |
|---|---|---:|--- |
| Deterministic: [IDW](../../algorithms/interpolation/inverse-distance-weighting.md), [Sibson natural neighbour](../../algorithms/interpolation/natural-neighbour.md), spline, thin plate spline, RBF, Shepard, [Cressman objective analysis](../../methods/geophysical-gridding.md#6-cressman-successive-correction-objective-analysis), [Barnes objective analysis](../../methods/geophysical-gridding.md#7-barnes-gaussian-successive-correction-analysis), [polynomial trend surface](../../methods/geophysical-gridding.md#8-polynomial-trend-surface-analysis), TIN, Whittaker smoother | Interpolation methods / surface models | 4 | Partial — tested Sibson stolen-area reference implementation now added; Cressman and Barnes have tested iterative objective-analysis baselines; Shepard and source-entry review remain pending; a tested Whittaker-Eilers finite-difference smoother now covers the ordered-sequence smoothing component |
| Climate and gap filling: PRISM, Daymet, ANUSPLIN, DINEOF, HANTS, matrix and tensor completion, deep inpainting, spatiotemporal fusion (STARFM, ESTARFM, FSDAF) | Climate products / interpolation and gap-filling methods / fusion workflows | 4 | Not checked — intake only |

## Kriging and geostatistics

| Source entry | Provisional kind | Source page | Verification status |
|---|---|---:|--- |
| Kriging: [ordinary kriging](../../algorithms/geostatistics/interpolation.md), simple, universal, co-kriging, regression kriging, external drift, indicator, disjunctive, block, area-to-point, area-to-area, spatiotemporal | Geostatistical estimators / kriging variants | 4 | Partial — tested ordinary and universal kriging baselines use explicit spherical/exponential/Gaussian variogram parameters and polynomial drift; simple, co-kriging, regression/external-drift, indicator, disjunctive, block, area-to-point/area-to-area and spatiotemporal variants remain open |
| [Empirical semivariogram](../../methods/empirical-semivariogram.md), theoretical variogram fitting, anisotropy, nonstationary covariance, spatial deformation, process convolution, multiscale kriging | Covariance and variogram modelling methods / geostatistical approaches | 4 | Partial — related record exists; source-entry review pending |
| Large-data Gaussian processes: Vecchia, NNGP, covariance tapering, fixed rank kriging, predictive processes, lattice kriging, multi-resolution approximation | Gaussian-process approximations / scalable spatial models | 4 | Not checked — intake only |
| Simulation: sequential Gaussian, indicator simulation, multiple-point statistics (SNESIM, direct sampling), object-based, p-field | Spatial simulation methods | 5 | Not checked — intake only |
| Extremes and dependence: max-stable processes (Brown-Resnick), spatial copulas, GEV and Gumbel fits | Extreme-value and dependence models | 5 | Not checked — intake only |
| Sampling design: spatially balanced (GRTS, BAS), cLHS, stratified, spatial thinning | Sampling designs / sampling procedures | 5 | Not checked — intake only |
| Digital soil mapping: SCORPAN, pedotransfer functions, equal-area splines, SoilGrids-style stacking | Domain modelling frameworks / estimation methods / product-style workflow | 5 | Not checked — intake only |

## Spatiotemporal statistics

| Source entry | Provisional kind | Source page | Verification status |
|---|---|---:|--- |
| STARMA, space-time ARIMA, GTWR, dynamic linear and state-space models | Spatiotemporal model families | 5 | Not checked — intake only |
| Spatiotemporal GP (separable and non-separable kernels), spatiotemporal INLA, functional data analysis | Spatiotemporal Gaussian processes / inference framework / statistical methods | 5 | Not checked — intake only |
| Space-time scan statistics, Knox test, space-time K function, space-time cube, emerging hot spot analysis | Spatiotemporal tests / summary methods / analysis workflow | 5 | Partial — a permutation-based Knox test for excess space-time close pairs is implemented and tested; space-time scan statistics, space-time K, cube analytics and emerging-hotspot workflows remain open |
| Spatial survival and frailty models | Survival model families | 5 | Not checked — intake only |
| Spatiotemporal point processes: Hawkes, LGCP, ETAS | Point-process model families | 5 | Partial — a tested univariate exponential Hawkes process simulator and point-process log-likelihood are implemented; spatial Hawkes/LGCP, ETAS earthquake triggering and marked multivariate processes remain open |
| Trend and change: Mann-Kendall, Sen's slope, harmonic regression, BFAST, LandTrendr, CCDC | Trend tests / regression / change-detection methods | 5 | Partial — tested Mann–Kendall and seasonal Mann–Kendall significance tests plus Theil–Sen slope estimation are implemented; harmonic regression, BFAST, LandTrendr and CCDC remain open |

## Data assimilation and inverse methods

| Source entry | Provisional kind | Source page | Verification status |
|---|---|---:|--- |
| Optimal interpolation, 3D-Var, 4D-Var, ensemble Kalman filter, LETKF, particle filters | Data assimilation algorithms | 5 | Not checked — intake only |
| Variational and Bayesian inversion, adjoint methods, emulators and surrogate models | Inverse methods / optimisation / approximation models | 5 | Not checked — intake only |
| Radiative transfer inversion (PROSAIL, look-up tables) | Physical retrieval / inversion workflow | 5 | Not checked — intake only |

## Uncertainty, accuracy and sensitivity

| Source entry | Provisional kind | Source page | Verification status |
|---|---|---:|--- |
| Positional accuracy (RMSE), error propagation, Monte Carlo, Latin hypercube, Sobol sensitivity, polynomial chaos | Accuracy measures / uncertainty propagation / sensitivity methods | 5 | Partial — tested Monte Carlo propagation for independent bounded inputs and Saltelli first-/total-order Sobol indices are implemented; correlated inputs, Latin hypercube, polynomial chaos and spatially structured error propagation remain open |
| Classification accuracy: confusion matrix, kappa, area-adjusted accuracy (Olofsson), fuzzy kappa, Figure of Merit, quantity and allocation disagreement | Accuracy assessment measures and procedures | 5 | Not checked — intake only |
| Bayesian: MCMC (Metropolis, HMC, NUTS), variational inference, approximate Bayesian computation, Bayesian model averaging | Bayesian inference algorithms / approximation methods | 5 | Not checked — intake only |
| Probabilistic and fuzzy maps: ensemble spread, interval-valued, possibilistic, conformal prediction (including locally adaptive), quantile regression forests, area of applicability, dissimilarity index | Uncertainty representations / prediction methods / applicability diagnostics | 5 | Not checked — intake only |
| Reasoning under imprecision: fuzzy and rough sets, Dempster-Shafer, Bayesian belief networks, possibility theory | Uncertainty and evidence frameworks | 5 | Not checked — intake only |

## Small-area and survey estimation

| Source entry | Provisional kind | Source page | Verification status |
|---|---|---:|--- |
| Fay-Herriot, unit-level small-area models, Horvitz-Thompson, model-assisted estimation, MRP | Small-area estimators / survey estimators / multilevel modelling | 6 | Partial — a tested area-level Fay–Herriot empirical-Bayes estimator with REML random-effect variance estimation is implemented; unit-level models, Horvitz–Thompson, model-assisted estimation and MRP remain open |
| Spatial microsimulation (IPF, simulated annealing), areal interpolation, dasymetric mapping, WorldPop-style random forest population surfaces | Spatial microsimulation / areal estimation / mapping workflows | 6 | Not checked — intake only |
| Statistical downscaling: quantile mapping, BCSD, delta change, analog methods | Downscaling methods | 6 | Not checked — intake only |

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


### Universal kriging implementation update

A dense universal-kriging solver now supports constant, linear and quadratic polynomial drift with caller-specified spherical, exponential or Gaussian variogram parameters. It returns predictions and conditional kriging variance and rejects rank-deficient drift designs. The implementation is a small-data reference solver; it does not fit variograms, select neighbourhoods, or implement co-kriging, regression/external drift, indicator, disjunctive, block, area-to-point or spatiotemporal kriging.


### Monte Carlo uncertainty propagation and Sobol sensitivity

A tested reference package propagates independent bounded uniform input uncertainty through a user-supplied numerical model, reporting output moments and quantiles. It also estimates first-order and total-order Sobol sensitivity indices with the Saltelli pick-freeze design. Dependent input distributions, arbitrary probability transforms, correlated spatial errors, Latin-hypercube designs and polynomial-chaos surrogates remain open.


### Knox space-time interaction test

The Knox test counts event pairs that are simultaneously within a declared spatial distance and temporal interval. Its reference permutation test holds event locations fixed and randomly permutes event times, testing for excess close pairs under temporal-label exchangeability. It is a pairwise interaction test, not a space-time scan statistic or a full space-time point-process model.


### Fay–Herriot area-level small-area estimation

An area-level Gaussian Fay–Herriot model now estimates regression coefficients by generalized least squares and the between-area random-effect variance by restricted maximum likelihood. It returns empirical-Bayes area estimates and conditional random-effect variances. This does not implement unit-level models, survey-weighted Horvitz–Thompson estimators, model-assisted estimation or multilevel regression and poststratification (MRP).


### Exponential Hawkes self-exciting process

A univariate temporal Hawkes process with exponential triggering kernel now has Ogata-thinning simulation and an exact conditional log-likelihood for observed event times over a finite window. The baseline assumes a stationary subcritical process with branching ratio below one. Spatial Hawkes processes, log-Gaussian Cox processes, ETAS earthquake models and marked/multivariate variants remain open.


### Mann–Kendall and Theil–Sen trend analysis

The existing Theil–Sen package now includes tie-corrected Mann–Kendall and seasonal Mann–Kendall tests alongside the median pairwise slope estimator. The rank test uses a normal approximation and assumes no unmodelled serial dependence; neither method alone diagnoses seasonality, structural breaks or causal drivers.
