# Spatial econometrics teaching implementations

This package contains small, dense-matrix reference implementations:

1. **Classic and Bera–Yoon robust spatial LM diagnostics** for lag and error dependence.
2. **SAR/SDM direct, indirect and total impact decomposition**, plus both analytic delta-method and parametric Monte Carlo uncertainty propagation from a supplied joint parameter covariance.
3. **Spatial lag 2SLS** using exogenous covariates and spatial lags as instruments for endogenous Wy.
4. **Spatial Durbin 2SLS** with higher-order spatial lags as excluded instruments.
5. **SLX OLS and SDEM concentrated Gaussian ML** for spatially lagged covariates, with and without spatially correlated errors.
6. **Gaussian proper-CAR regression ML** with an eigenvalue-derived positive-definite parameter interval.
7. **Constrained ICAR Gaussian fields** with component-wise sum-to-zero spectral simulation and normalized log-density evaluation on the constrained subspace.
8. **Concentrated Gaussian maximum likelihood** for SAR, SEM and SDM, plus joint two-parameter SARAR/SAC likelihood estimation.
9. **Spatial HAC covariance for OLS** using a compact-support positive-definite Wendland kernel.
10. **Two-step heteroskedasticity-robust spatial-lag GMM** with 2SLS initial weighting, an updated moment covariance, robust standard errors and an overidentification statistic.
11. **Kelejian–Prucha spatial-error generalized moments and feasible GLS** using the three innovation moment conditions.
12. **Spatial-lag first-stage instrument diagnostics** with partial R-squared, classical partial F and an HC1 robust Wald F.
13. **Anderson–Rubin inference** for a caller-supplied candidate spatial-lag coefficient, with classical F and HC1 robust Wald chi-square tests.
14. **Heteroskedastic spatial-error GM moments** for a supplied consistent disturbance predictor, using the two zero-diagonal quadratic restrictions of Kelejian–Prucha (2010).
15. **Three-step heteroskedastic SARAR generalized spatial 2SLS**: initial spatial 2SLS, KP disturbance GM, and Cochrane–Orcutt transformed 2SLS.
16. **Conley-style spatial HAC covariance for spatial-lag 2SLS**, using projected IV regressors and a compact-support Wendland kernel.
17. **Kelejian–Prucha joint asymptotic covariance for heteroskedastic SARAR GTSLS**, including generated first-stage residual uncertainty and covariance between the final IV estimator and disturbance GM moments.

## Run

~~~bash
python -m pip install numpy pytest
python -m pytest -q
~~~

18. **Global Moran's I permutation inference** with a seeded conditional randomization distribution, plus-one Monte Carlo p-values and explicit one-/two-sided alternatives.
19. **Local Moran's I conditional permutation inference** with HH/LL/HL/LH classifications and Benjamini–Hochberg false-discovery-rate adjustment.
20. **Koenker studentized Breusch–Pagan and White tests** for heteroskedasticity after OLS spatial-regression baselines.
21. **Ramsey RESET** partial-F specification test using powers of fitted values to detect generic functional-form misspecification.
22. **SAR/SEM/SDM profile-likelihood intervals** for the spatial lag or error parameter by inversion of the one-degree-of-freedom likelihood-ratio test.\n23. **Spatial-lag Anderson–Rubin confidence-set inversion** over a declared rho grid, retaining empty, disconnected and grid-limited sets.

## Scope and limits

- Anderson–Rubin confidence sets are finite-grid approximations: segment endpoints are grid values, edge-touching segments may continue beyond the search range, and disconnected components are retained. The caller supplies the critical value for the chosen classical F or robust Wald chi-square statistic.\n- Profile-likelihood intervals are conditional on the supplied weights and the conservative nonsingularity interval; an endpoint can be truncated at that interval's boundary. The default LR cutoff is 3.84146 (95% under chi-square(1)).

- Global Moran's I permutation inference treats values as exchangeable over fixed locations under its randomization null. The two-sided test measures absolute deviation from -1/(n-1); it is global, not a local cluster detector. Weights are used as supplied and are not automatically symmetrised or row-standardised.
- Local Moran inference conditions on each focal value and permutes the remaining observations over the other locations. By default, Benjamini–Hochberg adjustment is applied across non-islands; arbitrary spatial dependence can affect its guarantees.
- Koenker BP and White diagnostics test constant conditional variance in an OLS baseline. They are not tests of spatial dependence and do not establish which heteroskedastic spatial model should be fitted. Islands receive NaN p-values and no cluster classification.
- The LM diagnostics calculate classic and Bera–Yoon robust score statistics from an OLS baseline. They do not implement finite-sample corrections, joint tests or model selection. Robust scores are unavailable when their adjustment denominator is not identified.
- All routines use the supplied weights exactly as given. Neighbour construction, row standardisation, islands, alignment and substantive interpretation are modelling decisions for the analyst.
- SLX fits OLS to [X, WX]. SDEM applies the concentrated SEM likelihood to the independent columns of [X, WX]. Neither includes Wy. Redundant WX columns (notably a row-standardised intercept) are dropped and reported with zero spatial-covariate coefficients.
- The spatial lag 2SLS and SDM 2SLS estimators use spatial lags as excluded instruments for Wy; exogeneity and relevance are assumptions, not automatically tested. They do not report second-stage standard errors; the companion first-stage diagnostics report instrument relevance summaries.
- Spatial-lag GMM uses [X, WX, ..., W^qX] as instruments, starts with the 2SLS weighting matrix, then updates it using a heteroskedasticity-robust estimate of the instrument-moment covariance. It reports a robust sandwich covariance and J statistic, but no J-test p-value. It does not accommodate spatially autocorrelated structural errors.
- Anderson–Rubin inference tests a supplied candidate rho by regressing y - rho0 Wy on [X, WX, ..., W^qX] and testing joint exclusion of the added instruments. The classical F relies on iid homoskedastic Gaussian errors; HC1 Wald chi-square is asymptotic under independent observations and is not spatial-HAC robust. Instrument validity remains essential. Confidence-set inversion, which can yield unbounded or disjoint sets, is not implemented.
- Spatial-error GMM implements the homoskedastic-innovation Kelejian–Prucha (1999) three-moment estimator for lambda, followed by feasible GLS. Its reported GLS covariance relies on the iid innovation variance model.
- The heteroskedastic spatial-error GM routine implements the two zero-diagonal quadratic moment restrictions of Kelejian and Prucha (2010), taking a consistent disturbance predictor as input.
- The three-step SARAR GTSLS routine uses first-stage spatial 2SLS residuals for the heteroskedastic KP GM estimate, then applies the Cochrane–Orcutt transformation and a second 2SLS fit. It reports both a conditional HC1 covariance and the Kelejian–Prucha (2010) plug-in joint asymptotic covariance for `[beta..., rho, lambda]`, including generated-residual and cross-moment terms. The joint result uses identity weighting for the GM moments and is restricted to the common-weights case `M=W`; it is not finite-sample exact or spatial HAC. The standalone GM routine remains available for other consistent residual predictors.
- The SAR/SEM/SDM ML estimators use conservative norm-bounded parameter intervals and dense log-determinants. SDM drops spatially lagged covariate columns linearly dependent on the included design. SARAR/SAC profiles both spatial parameters over a conservative rectangle using a coarse grid and alternating one-dimensional refinements.
- The impact matrix is \(S_r=(I-\rho W)^{-1}(\beta_r I+\gamma_r W)\). Direct impact is the mean diagonal, total impact is the mean row sum, and indirect impact is total minus direct. Impact uncertainty propagates a supplied joint covariance for [rho, beta..., gamma...] through Monte Carlo; it does not estimate that covariance.
- Proper CAR uses a symmetric non-negative adjacency matrix, no isolated nodes, and the precision τ(D - αA). It is a proper Gaussian CAR regression, not ICAR, BYM/BYM2 or Leroux CAR.
- ICAR simulation uses the singular graph-Laplacian precision τ(D - A), detects connected components, and samples on the component-wise sum-to-zero subspace. It is a field simulator, not a fitted Bayesian regression model.
- Spatial HAC estimates OLS coefficient covariance from distance-weighted residual cross-products using projected planar coordinates and a declared bandwidth. It does not correct endogeneity or spatially lagged outcomes.
- Spatial-lag 2SLS HAC uses the same compact-support kernel but forms its sandwich from projected instruments/regressors, allowing heteroskedasticity and residual cross-correlation within the declared bandwidth. It does not cure weak or invalid instruments; coordinate units and bandwidth remain analyst decisions.
- Dense matrices are intended for small teaching cases. These implementations do not provide a complete production inference workflow; use sparse numerical methods and maintained spatial-econometric software for larger or consequential analyses.

Follow the [implementation walkthrough](implementation-walkthrough.md) to trace formulas, validation and tests.

Canonical explanations: [heteroskedasticity diagnostics](../../../algorithms/statistics/heteroskedasticity-diagnostics.md); [local Moran's I permutation inference](../../../algorithms/statistics/local-morans-i-permutation.md); [global Moran's I permutation inference](../../../algorithms/statistics/global-morans-i-permutation.md); [joint heteroskedastic SARAR inference](../../../algorithms/statistics/heteroskedastic-sarar-joint-inference.md); [heteroskedastic SARAR GTSLS](../../../algorithms/statistics/heteroskedastic-sarar-gtsls.md); [spatial 2SLS HAC covariance](../../../algorithms/statistics/spatial-2sls-hac.md); [heteroskedastic spatial-error GM](../../../algorithms/statistics/heteroskedastic-spatial-error-gm.md); [spatial-lag Anderson–Rubin inference](../../../algorithms/statistics/spatial-lag-anderson-rubin.md); [spatial-lag instrument diagnostics](../../../algorithms/statistics/spatial-lag-instrument-diagnostics.md); [Kelejian–Prucha spatial-error GMM](../../../algorithms/statistics/kelejian-prucha-spatial-error-gmm.md); [spatial LM diagnostics](../../../algorithms/statistics/spatial-lm-diagnostics.md); [spatial impacts](../../../algorithms/statistics/spatial-impacts.md); [impact uncertainty](../../../algorithms/statistics/spatial-impact-uncertainty.md); [spatial lag 2SLS](../../../algorithms/statistics/spatial-lag-2sls.md); [spatial lag GMM](../../../algorithms/statistics/spatial-lag-gmm.md); [concentrated SAR/SEM maximum likelihood](../../../algorithms/statistics/spatial-maximum-likelihood.md); [spatial Durbin 2SLS](../../../algorithms/statistics/spatial-durbin-2sls.md); [spatial Durbin maximum likelihood](../../../algorithms/statistics/spatial-durbin-mle.md); [SARAR/SAC maximum likelihood](../../../algorithms/statistics/spatial-sarar-mle.md); [SLX/SDEM](../../../algorithms/statistics/slx-and-sdem.md); [Gaussian proper CAR](../../../algorithms/statistics/proper-car-gaussian-regression.md); [constrained ICAR Gaussian fields](../../../algorithms/statistics/icar-gaussian-fields.md); [spatial HAC covariance](../../../algorithms/statistics/spatial-hac-covariance.md).

24. **Analytic delta-method impact uncertainty** with exact first derivatives of the SAR/SDM impact matrix and joint covariance propagation.

25. **Spatial Durbin common-factor likelihood-ratio test** comparing unrestricted SDM maximum likelihood with the nested SEM restriction on identified spatially lagged covariates.
