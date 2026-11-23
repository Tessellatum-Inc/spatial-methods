# SAR/SEM/SDM profile-likelihood intervals

Stable ID: SA-STAT-SPATIAL-MLE-PROFILE-INTERVALS · Teaching implementation

## Purpose

A point estimate of the spatial autoregressive coefficient does not describe its uncertainty. A Wald interval can be misleading when the likelihood is asymmetric or the estimate lies near an admissible-parameter boundary. Profile likelihood gives an interval by retaining every parameter value whose likelihood-ratio statistic does not exceed a chi-square reference cutoff.

This implementation covers the scalar spatial parameter in SAR, SEM and SDM models. It does not provide intervals for regression coefficients, SDM covariate-lag coefficients, or the joint SARAR parameter pair.

## Likelihood-ratio set

For a candidate parameter theta, re-estimate the regression coefficients and innovation variance by least squares after the appropriate spatial filter, and calculate the concentrated Gaussian log likelihood ell_p(theta). Let theta_hat maximize the profile likelihood. The confidence set is

\[
\mathcal C=\{\theta:2[\ell_p(\hat\theta)-\ell_p(\theta)]\leq
\chi^2_{1,1-\alpha}\}.
\]

The default cutoff 3.8414588 gives the conventional 95% likelihood-ratio interval under the asymptotic chi-square(1) approximation.

- SAR: transform y by I-rho W, while retaining X.
- SEM: transform both y and X by I-lambda W.
- SDM: transform y by I-rho W and re-estimate coefficients on the independent columns of [X, WX].
- Find each endpoint by bisection on the likelihood-ratio boundary.
- If the LR set reaches the estimator's conservative nonsingularity interval, return that boundary and set the corresponding truncation flag.

## Numerical and inferential limits

The implementation inherits the conservative interval from the SAR/SEM maximum-likelihood estimators, which guarantees nonsingularity but does not cover the full theoretically admissible parameter space. A truncated endpoint is therefore not an ordinary finite confidence bound: it says the LR set continues to the edge of the searched interval. The chi-square calibration is asymptotic and depends on the maintained Gaussian likelihood and regularity conditions. The supplied weights matrix is treated as fixed.

The profile optimum is found by the existing grid-plus-golden-section estimator. Endpoint roots use bisection. Dense matrix operations make this a small-problem teaching implementation.

## Python example

~~~python
from spatial_mle_inference import spatial_parameter_profile_interval

interval = spatial_parameter_profile_interval(y, X, W, model="SDM")
print(interval.estimate, interval.lower, interval.upper)
print(interval.lower_truncated, interval.upper_truncated)
~~~

## Repository implementation

- Implementation: ../../implementations/python/spatial-econometrics/spatial_mle_inference.py
- Tests: ../../implementations/python/spatial-econometrics/test_spatial_econometrics.py
- Concentrated SAR/SEM maximum likelihood: spatial-maximum-likelihood.md
