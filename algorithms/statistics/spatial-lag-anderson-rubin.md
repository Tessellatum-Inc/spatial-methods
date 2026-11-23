# Anderson–Rubin inference for a spatial-lag coefficient

## Model and null hypothesis

Consider the spatial autoregressive model

\[
y=\rho Wy+X\beta+u,
\]

with one endogenous regressor, the spatial lag \(Wy\). Let the excluded instruments be spatial lags of exogenous covariates, for example \(WX,\ldots,W^qX\), after removing columns linearly dependent on \(X\).

For a candidate value \(\rho_0\), the null hypothesis is

\[
H_0:\rho=\rho_0.
\]

Under this null, transform the response:

\[
y_0(\rho_0)=y-\rho_0Wy.
\]

If the instruments are valid under the maintained model, the transformed equation is

\[
y_0(\rho_0)=X\beta+u,
\]

so the excluded spatial-lag instruments should have zero coefficients in the auxiliary regression of \(y_0(\rho_0)\) on \([X,WX,\ldots,W^qX]\).

## Test statistics

Let \(q_e\) be the number of linearly independent excluded instrument columns, \(p\) the total number of retained columns and \(N\) the sample size. Let \(SSR_R\) and \(SSR_U\) denote the restricted and unrestricted residual sums of squares.

The classical Anderson–Rubin statistic is

\[
F_{AR}=\frac{(SSR_R-SSR_U)/q_e}{SSR_U/(N-p)}.
\]

Under iid homoskedastic Gaussian errors and the maintained instrument-validity assumptions, this has the usual finite-sample \(F_{q_e,N-p}\) reference distribution.

For heteroskedasticity-robust inference, estimate the unrestricted auxiliary regression covariance with HC1:

\[
\widehat V_{HC1}=\frac{N}{N-p}
(X_Z'X_Z)^{-1}
\left[\sum_i z_i z_i'\hat u_i^2\right]
(X_Z'X_Z)^{-1}.
\]

The robust Anderson–Rubin statistic is the Wald quadratic form for the excluded coefficients:

\[
AR_{HC1}=\hat\pi_E'
\widehat V_{HC1}(\hat\pi_E)^{-1}
\hat\pi_E.
\]

It is reported against an asymptotic chi-square reference with \(q_e\) degrees of freedom. This is not a finite-sample exact test and is not spatial-HAC robust.

## Why this helps with weak instruments

The null transformation places the candidate \(\rho_0\) in the response rather than estimating it by dividing through a potentially weak first stage. Under the null and valid-instrument assumptions, the excluded-instrument restrictions can be tested without a strong-first-stage approximation. Inverting the test over candidate values produces an identification-robust confidence set; that set can be unbounded, disconnected or empty. This implementation tests one candidate only and deliberately does not manufacture a bounded interval.

## Assumptions and limitations

- Excluded spatial lags must be valid: they must be uncorrelated with the structural disturbance under the null. Anderson–Rubin inference does not rescue invalid instruments.
- The classical F reference is exact only under the conventional iid homoskedastic Gaussian auxiliary-regression assumptions.
- HC1 is robust to heteroskedasticity under independent-observation asymptotics. It does not account for spatial dependence in the auxiliary-regression errors.
- The implementation supports one endogenous spatial lag and a caller-specified finite instrument order. It does not implement conditional likelihood-ratio inference, multiple endogenous regressors or confidence-set inversion.
- Rank checks remove redundant instrument columns; they do not establish relevance, exclusion validity or correct model specification.
- Dense matrix operations are intended for small teaching examples.

## Implementation

The NumPy reference implementation is `implementations/python/spatial-econometrics/spatial_lag_anderson_rubin.py`. It returns the candidate value, classical partial F and degrees of freedom, HC1 robust Wald chi-square and degrees of freedom, retained instrument counts and transformed-regression coefficients.

## References

- Anderson, T. W., & Rubin, H. (1949). Estimation of the parameters of a single equation in a complete system of stochastic equations. *The Annals of Mathematical Statistics*, 20(1), 46–63.
- Staiger, D., & Stock, J. H. (1997). Instrumental variables regression with weak instruments. *Econometrica*, 65(3), 557–586.
- Keane, M. P., & Neal, T. (2024). A practical guide to weak instruments. *Annual Review of Economics*, 16, 185–212. https://doi.org/10.1146/annurev-economics-092123-111021.
