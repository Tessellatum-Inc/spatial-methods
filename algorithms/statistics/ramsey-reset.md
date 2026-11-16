# Ramsey RESET functional-form diagnostic

## Question answered

Ramsey's Regression Specification Error Test (RESET) asks whether powers of the restricted model's fitted values add explanatory power. It is a general diagnostic for neglected nonlinearities and other functional-form errors in an OLS baseline. It does **not** identify the omitted variable, distinguish every possible misspecification, test spatial dependence, or establish that SAR/SEM/SDM is appropriate.

## Partial F test

Fit the restricted model \(y=X\beta+u\), obtaining \(\hat y\) and restricted residual sum of squares \(RSS_R\). Form the augmented design by adding \(\hat y^2,\ldots,\hat y^p\), then calculate its residual sum of squares \(RSS_U\). The joint test is

\[
F=\frac{(RSS_R-RSS_U)/q}{RSS_U/(n-r_U)},
\]

where \(q=r_U-r_X\) is the actual rank increase and \(r_U\) is the augmented design rank. The p-value uses the corresponding central F reference distribution.

The implementation scales fitted values before exponentiation to reduce overflow, detects redundant added terms through matrix rank, and computes the F survival probability through a regularized incomplete-beta continued fraction. This keeps the package NumPy-only.

## Interpretation and limits

A small p-value is evidence that the restricted linear specification is inadequate under the classical partial-F assumptions. It is not a direct test of spatial autocorrelation and should be considered alongside residual diagnostics, theory, robust covariance estimates and spatial LM tests. RESET can have low power against some alternatives and can reject for several different forms of misspecification.

Runnable reference: [ramsey_reset.py](../../implementations/python/spatial-econometrics/ramsey_reset.py).

## Validation

Tests compare the partial F statistic with an independently constructed nested OLS comparison, exercise a nonlinear data-generating process, verify the F-tail calculation at known critical values, and cover rank and input failures.

## Reference

Ramsey, J. B. (1969). Tests for specification errors in classical linear least-squares regression analysis. *Journal of the Royal Statistical Society: Series B*, 31(2), 350–371.
