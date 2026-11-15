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

The coefficients are assumed to come from a separately fitted model. This package does not propagate estimation uncertainty.

## 4. Tests and verification

\`test_spatial_econometrics.py\` checks the LM formulas against independently assembled matrix expressions, rejects invalid inputs, checks SAR/SDM impact identities and generates a synthetic SAR process for a 2SLS recovery test.

Run:

~~~bash
python -m pip install -r requirements.txt
python -m pytest -q
~~~

The CI workflow includes this package and executes the companion notebook. A successful local or CI test run should be recorded separately from static inspection.
