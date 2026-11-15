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

## 4. Concentrated maximum likelihood\n\nOpen `maximum_likelihood.py`.\n\n1. SAR profiles the Gaussian likelihood over the spatial-lag parameter, including the Jacobian term `log|I-rho W|`.\n2. SEM transforms both the response and design by `I-lambda W`.\n3. SDM transforms the response by `I-rho W` and regresses on the augmented `[X, WX]` design, dropping redundant spatial-lag columns in stable order.\n4. SARAR/SAC applies both filters, `A_lambda A_rho`, to the response and `A_lambda` to the design. Its likelihood includes both log-determinants. A two-dimensional coarse grid is refined by alternating local golden-section searches around the best grid cell.\n5. All estimators use a conservative norm-bounded interval and dense matrix operations. They are teaching baselines, not scalable production likelihoods; they do not provide coefficient covariance or robust inference.\n\n## 5. Tests and verification

\`test_spatial_econometrics.py\` checks the LM formulas against independently assembled matrix expressions, rejects invalid inputs, checks SAR/SDM impact identities, tests parametric impact uncertainty, and generates synthetic SAR, SDM and SARAR processes for estimator recovery tests.

Run:

~~~bash
python -m pip install -r requirements.txt
python -m pytest -q
~~~

The CI workflow includes this package and executes the companion notebook. A successful local or CI test run should be recorded separately from static inspection.
