# Spatial econometrics implementation walkthrough

This package deliberately separates three tasks that are often conflated: diagnosing a non-spatial OLS model, estimating a spatial-lag model by instruments, and interpreting a fitted spatial model through impacts.

## 1. Classic LM diagnostics

Open \`diagnostics.py\`.

1. \`_inputs\` checks that \(y\), \(X\) and \(W\) align; the design has full column rank; values are finite; and weights are non-negative with a zero diagonal.
2. \`np.linalg.lstsq\` estimates the null OLS coefficients without explicitly inverting \(X'X\).
3. The residual variance is \(e'e/n\), matching the maximum-likelihood variance estimate used in the score-statistic expressions.
4. The trace term \(T=\operatorname{tr}(W'W+W^2)\) is calculated once.
5. LM-error uses \(e'We\); LM-lag uses \(e'Wy\) and the projected \(WX\hat\beta\) term in its denominator.
6. The one-degree-of-freedom chi-square upper-tail probability is evaluated with the closed-form survival function.

These are classic score tests. They are not the robust LM variants and they do not estimate either spatial model.

## 2. Spatial lag 2SLS

Open \`spatial_2sls.py\`.

1. The structural regressors are \(Q=[Wy,X]\). The first column, \(Wy\), is endogenous in a spatial lag model.
2. The instrument builder starts with \(X\) and appends \(WX,W^2X,\ldots,W^qX\).
3. Linearly dependent columns are removed in stable order. This matters for a constant column under row-standardised weights.
4. The instrument-space projection is applied to both \(Q\) and \(y\).
5. Least squares on the projected system returns the spatial coefficient \(\rho\) and the regression coefficients \(\beta\).
6. The implementation checks that the projected regressors are identified, but it cannot prove that the chosen instruments are exogenous or sufficiently relevant.

The method is intentionally narrow: no spatially autocorrelated error term, standard errors, weak-instrument diagnostics or heteroskedasticity-robust GMM.

## 3. SAR/SDM impacts

Open \`impacts.py\`.

1. For each covariate, construct the right-hand side \(\beta_rI+\gamma_rW\).
2. Solve \((I-\rho W)S_r=\beta_rI+\gamma_rW\) using a linear solver. Do not explicitly form a matrix inverse.
3. Average the diagonal for the direct impact.
4. Average all matrix elements (equivalently the mean row sum) for the total impact.
5. Calculate the indirect impact as total minus direct.

The coefficients are assumed to come from a separately fitted model. The `spatial_impact_uncertainty` companion accepts a joint covariance ordered as `[rho, beta..., gamma...]` and propagates it through parametric Monte Carlo draws. It reports rejected ill-conditioned draws; it does not estimate the covariance or validate its sampling assumptions.

## 4. Concentrated maximum likelihood

Open `maximum_likelihood.py`.

1. SAR profiles the Gaussian likelihood over the spatial-lag parameter, including the Jacobian term `log|I-rho W|`.
2. SEM transforms both the response and design by `I-lambda W`.
3. SDM transforms the response by `I-rho W` and regresses on the augmented `[X, WX]` design, dropping redundant spatial-lag columns in stable order.
4. SARAR/SAC applies both filters, `A_lambda A_rho`, to the response and `A_lambda` to the design. Its likelihood includes both log-determinants. A two-dimensional coarse grid is refined by alternating local golden-section searches around the best grid cell.
5. All estimators use a conservative norm-bounded interval and dense matrix operations. They are teaching baselines, not scalable production likelihoods; they do not provide coefficient covariance or robust inference.

## 5. Gaussian proper-CAR regression

Open `proper_car.py`.

1. The model uses precision \(Q=\tau(D-\alpha A)\), with a symmetric adjacency matrix and positive node degrees.
2. The implementation forms the symmetric normalised adjacency \(B=D^{-1/2}AD^{-1/2}\). Its extreme eigenvalues determine the interval in which \(I-\alpha B\), and therefore the precision matrix, is positive definite.
3. For each candidate \(\alpha\), generalised least squares solves \(X^TQ_0X\hat\beta=X^TQ_0y\), where \(Q_0=D-\alpha A\).
4. The residual quadratic form profiles out \(\tau\): \(\hat\tau=n/R(\alpha)\).
5. The concentrated likelihood includes \(\tfrac12\log|Q_0|\) and the profiled residual term. A grid scan followed by local golden-section refinement selects \(\alpha\).
6. The result reports the conditional mean \(X\hat\beta\), residuals, dependence parameter and precision scale and node-specific conditional variances. This is a proper Gaussian CAR model, not a singular ICAR/BYM model.

The dense eigendecomposition and log determinant limit this teaching estimator to small graphs. The graph must be symmetric and contain no isolated nodes; the routine does not repair the graph or choose its weights.


## 6. Constrained intrinsic-CAR field simulation

Open icar.py.

1. Validate an undirected, non-negative graph and require positive degree for every node.
2. Find connected components by graph traversal. Each component contributes one null direction to its graph Laplacian.
3. Form the component Laplacian D - A and eigendecompose it.
4. Exclude the constant-vector null eigenvector. Scale independent standard-normal coefficients by the inverse square roots of the positive eigenvalues and by 1/sqrt(tau).
5. Map the coefficients back to node space. The resulting field has a separate sum-to-zero constraint on each component.
6. Report the component labels and log pseudo-determinant, not a fictitious ordinary determinant.

The conditional variance 1/(tau * degree_i) is not the marginal variance. This routine simulates a constrained field; it does not fit a regression, estimate tau or perform posterior inference. Dense eigendecomposition limits it to small teaching graphs.


## 7. Spatial HAC covariance for OLS

Open spatial_hac.py.

1. Fit OLS and retain residuals e.
2. Calculate pairwise Euclidean distances from projected planar coordinates.
3. Apply the compact-support Wendland C2 kernel at the caller's bandwidth.
4. Form the meat matrix from all weighted score cross-products (x_i e_i)(x_j e_j)'.
5. Sandwich the meat between (X'X)^(-1), symmetrise numerical round-off and extract standard errors.
6. Apply n/(n-k) when the finite-sample correction is enabled.

The bandwidth and coordinate units must agree. The kernel controls which spatial residual pairs contribute; this does not solve omitted-variable bias, spatial endogeneity or model misspecification.

## 8. Two-step heteroskedasticity-robust spatial-lag GMM

Open spatial_gmm.py.

1. Construct the structural regressors R = [Wy, X] and the instrument matrix Z = [X, WX, ..., W^q X].
2. Remove dependent instrument columns in stable order, then check the sample-size and rank conditions for identification and a nonsingular moment covariance.
3. Estimate the first-step GMM model using (Z'Z/N)^(-1), which yields the conventional 2SLS weighting choice.
4. Calculate first-step residuals and estimate S = N^(-1) sum(z_i z_i' u_i^2).
5. Use S^(-1) as the second-step efficient weighting matrix and re-estimate the structural coefficients.
6. Recalculate the residual moment covariance for the heteroskedasticity-robust sandwich standard errors. Report the overidentification statistic and degrees of freedom when instruments exceed structural regressors.

The instruments must be exogenous and relevant; rank checks do not establish either condition. This estimator handles heteroskedasticity in the IV moments but does not model spatially autocorrelated structural errors. It is not the full Kelejian–Prucha spatial-error GMM procedure.

## 9. Tests and verification

\`test_spatial_econometrics.py\` checks the LM formulas against independently assembled matrix expressions, rejects invalid inputs, checks SAR/SDM impact identities, tests parametric impact uncertainty, and generates synthetic SAR, SDM, SARAR and heteroskedastic SAR-GMM processes for estimator recovery tests.

Run:

~~~bash
python -m pip install -r requirements.txt
python -m pytest -q
~~~

The CI workflow includes this package and executes the companion notebook. A successful local or CI test run should be recorded separately from static inspection.


## 9. Kelejian–Prucha spatial-error generalized moments

Open `spatial_error_gmm.py`.

1. Fit OLS to obtain residuals as a consistent first-step predictor of the latent spatial error.
2. For each candidate lambda, filter the OLS residuals with (I-\lambda W), then spatially lag the filtered residuals.
3. Match the three innovation moments: innovation variance, the variance of its spatial lag (scaled by \(\mathrm{tr}(W'W)/N\)), and the zero cross-moment between the spatially lagged innovation and the innovation.
4. Profile the innovation variance analytically for each lambda, scan a bounded grid, and refine the best interior interval with golden-section minimisation.
5. Apply feasible GLS by filtering both y and X with (I-\hat\lambda W). The reported covariance is the model-based iid-innovation GLS covariance.
6. This is the homoskedastic Kelejian–Prucha (1999) GM estimator. The heteroskedastic extension requires different moment weighting and asymptotic covariance treatment; it is not claimed here.

The implementation follows the three population moments and nonlinear least-squares construction in Kelejian and Prucha (1999). Dense matrices and a bounded scalar search keep it inspectable, not scalable.


## 10. Spatial-lag first-stage instrument diagnostics

Open `instrument_diagnostics.py`.

1. Construct the endogenous first-stage outcome \(Wy\) and the candidate instrument set \([X,WX,\ldots,W^qX]\).
2. Drop redundant columns in stable order. This matters for row-standardised weights, where lagged intercepts often reproduce the intercept.
3. Estimate the restricted first stage using X only and the unrestricted first stage using all retained instruments.
4. Compare residual sums of squares to calculate partial R-squared and the classical partial F statistic.
5. Calculate an HC1 sandwich covariance for the unrestricted first stage and a joint Wald F statistic for the excluded instrument coefficients.
6. Read the robust statistic narrowly: it is heteroskedasticity-robust under independent-observation asymptotics, not a Kleibergen–Paap rk statistic and not spatial-HAC robust.

A low statistic is a warning, not a mechanical decision rule. Instrument exogeneity is a separate substantive condition; more spatial lags can add collinearity and many-instrument bias rather than useful identification.


## 11. Spatial-lag Anderson–Rubin inference

Open `spatial_lag_anderson_rubin.py`.

1. Supply a candidate value \(\rho_0\) and transform the response to \(y-\rho_0Wy\).
2. Construct \([X,WX,\ldots,W^qX]\), retaining independent columns in stable order so a lagged intercept is not counted twice.
3. Regress the transformed response on X for the restricted model and on the full instrument matrix for the unrestricted model.
4. Compare the two residual sums of squares to obtain the classical partial F for joint exclusion of the added spatial instruments.
5. Calculate an HC1 sandwich covariance for the unrestricted transformed regression and form the robust Wald chi-square statistic for those same excluded coefficients.
6. Interpret the classical test only under its iid homoskedastic Gaussian assumptions; the HC1 version is asymptotic under independent-observation sampling and does not correct spatial residual dependence.

The null-size argument does not require a strong first stage, but excluded instruments must still be valid. This routine tests one candidate coefficient. Confidence-set inversion is intentionally separate because valid Anderson–Rubin sets can be unbounded or disconnected.


## 12. Heteroskedastic spatial-error generalized moments

Open `heteroskedastic_spatial_error_gm.py`.

1. Supply a consistent predictor of the regression disturbance. This matters: in a model with an endogenous spatial lag, ordinary OLS residuals are not automatically a valid predictor.
2. Compute \(v=W\tilde u\), \(w=Wv\), and the column-wise squared norms of W.
3. Build the two Kelejian–Prucha (2010) moment restrictions. Their zero-diagonal quadratic-form construction removes the unknown observation-specific innovation-variance contribution from the moment expectations.
4. Expand the two sample moments into the coefficient vector \([\lambda,\lambda^2]\) and minimise their squared residual norm with identity weighting.
5. Constrain the search to a conservative nonsingularity interval for \(I-\lambda W\), and reject a rank-deficient moment coefficient matrix.

This is a disturbance-parameter point estimator only. It does not report the full joint asymptotic covariance, feasible generalized 2SLS or standard errors; those remain separate work rather than being approximated by the homoskedastic KP (1999) covariance.


## 13. Three-step heteroskedastic SARAR GTSLS

Open `spatial_sarar_gtsls.py`.

1. Build the endogenous regression matrix \(Z=[X,Wy]\) and instrument matrix \(H=[X,WX,\ldots,W^qX]\), dropping dependent columns.
2. Estimate the initial SAR regression by 2SLS and retain its residual predictor for the disturbance process.
3. Estimate the spatial-error coefficient with the heteroskedastic two-moment KP routine. The zero-diagonal quadratic restrictions allow unknown diagonal innovation variances.
4. Apply \(I-\hat\lambda W\) to both the response and the full endogenous regressor matrix.
5. Re-estimate the transformed equation by 2SLS using the original H matrix.
6. The result retains the conditional HC1 sandwich for comparison and also reports the Kelejian–Prucha joint covariance, ordered `[beta..., rho, lambda]`. The joint calculation includes generated-residual correction vectors, heteroskedastic quadratic-moment covariance and cross-covariance with the final transformed IV score.
7. The joint covariance is an asymptotic plug-in result under the paper's assumptions; it is not finite-sample exact, not the optional efficient-GM weighting scheme, and not spatial HAC.

The implementation is restricted to the common-weights case \(M=W\).


## 14. Spatial HAC covariance for spatial-lag 2SLS

Open `spatial_2sls_hac.py`.

1. Build \(H=[X,WX,\ldots,W^qX]\) and the endogenous regression matrix \(Z=[Wy,X]\).
2. Project Z onto H to obtain \(\hat Z=P_HZ\), then estimate the SAR coefficients by 2SLS.
3. Supply projected planar coordinates and a bandwidth in the same linear unit.
4. Calculate pairwise distances and the compact-support Wendland C2 kernel.
5. Form score vectors \(g_i=\hat z_i\hat u_i\), combine their cross-products using the kernel, and sandwich with \((\hat Z'Z)^{-1}\).
6. Report standard errors alongside the bandwidth and number of nonzero off-diagonal kernel pairs.

The covariance permits heteroskedasticity and residual cross-correlation within the declared support. It does not make weak or invalid spatial instruments reliable. Repeat the analysis across defensible bandwidths and ensure coordinates are projected rather than longitude/latitude degrees.
