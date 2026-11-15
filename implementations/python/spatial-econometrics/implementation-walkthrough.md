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

## 4. Concentrated maximum likelihood\n\nOpen `maximum_likelihood.py`.\n\n1. SAR profiles the Gaussian likelihood over the spatial-lag parameter, including the Jacobian term `log|I-rho W|`.\n2. SEM transforms both the response and design by `I-lambda W`.\n3. SDM transforms the response by `I-rho W` and regresses on the augmented `[X, WX]` design, dropping redundant spatial-lag columns in stable order.\n4. SARAR/SAC applies both filters, `A_lambda A_rho`, to the response and `A_lambda` to the design. Its likelihood includes both log-determinants. A two-dimensional coarse grid is refined by alternating local golden-section searches around the best grid cell.\n5. All estimators use a conservative norm-bounded interval and dense matrix operations. They are teaching baselines, not scalable production likelihoods; they do not provide coefficient covariance or robust inference.\n\n## 5. Gaussian proper-CAR regression

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

## 8. Tests and verification

\`test_spatial_econometrics.py\` checks the LM formulas against independently assembled matrix expressions, rejects invalid inputs, checks SAR/SDM impact identities, tests parametric impact uncertainty, and generates synthetic SAR, SDM and SARAR processes for estimator recovery tests.

Run:

~~~bash
python -m pip install -r requirements.txt
python -m pytest -q
~~~

The CI workflow includes this package and executes the companion notebook. A successful local or CI test run should be recorded separately from static inspection.
