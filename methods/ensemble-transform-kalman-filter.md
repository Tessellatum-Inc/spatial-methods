# Ensemble transform Kalman filter (ETKF)

## Ensemble representation

An ensemble \(X^f=[x_1^f,\ldots,x_N^f]\) approximates a forecast distribution. Let \(\bar x^f\) be its mean and \(A=X^f-\bar x^f\mathbf 1^T\) its centered anomalies. The sample forecast covariance is

\[
P^f=\frac{AA^T}{N-1}.
\]

For a linear observation model \(y=Hx+\epsilon\), with observation-error covariance \(R\), the ETKF performs the Kalman analysis in the lower-dimensional ensemble subspace. Define \(Y=HA\), innovation \(d=y-H\bar x^f\), and

\[
C=(N-1)I+Y^TR^{-1}Y.
\]

The ensemble-space mean weights and symmetric transform are

\[
w=C^{-1}Y^TR^{-1}d,\qquad
T=(N-1)^{1/2}C^{-1/2}.
\]

Then

\[
\bar x^a=\bar x^f+Aw,\qquad A^a=AT,\qquad
X^a=\bar x^a\mathbf1^T+A^a.
\]

The symmetric positive-definite square root is obtained by eigendecomposition. No perturbed observations are generated.

## Implemented baseline

The NumPy function accepts a state-by-member ensemble, observation vector, linear observation matrix and full positive-definite observation covariance. It returns the analysis ensemble, mean, sample covariance, anomalies, forecast covariance and ensemble-space transform.

The method is a batch ETKF analysis. The implementation is a small dense teaching version and explicitly exposes the transform.

## Stochastic EnKF companion

The companion `enkf_analysis` uses the same forecast ensemble and linear observation model but generates independent perturbed observations with covariance R for each member. The stochastic update preserves the observation-error contribution to the ensemble covariance in expectation; finite ensembles retain Monte Carlo sampling error. It is distinct from the deterministic ETKF transform above.

## Limitations

This implementation does not include forecast propagation, localization, inflation, adaptive inflation, serial observation processing, nonlinear observation operators, model-error treatment, ensemble generation, adaptive observation targeting or cycling. Finite-ensemble sampling error and rank deficiency remain important; a mathematically correct analysis transform does not remove those practical problems. It is not an implementation of every ensemble square-root filter variant: ETKF, EAKF and serial EnSRF have different transformation constructions.

## Reproduction

Run from implementations/python/state-estimation:

~~~bash
python -m pytest -q --import-mode=importlib
~~~

## References

- Bishop, C. H., Etherton, B. J., & Majumdar, S. J. (2001). Adaptive Sampling with the Ensemble Transform Kalman Filter. Part I: Theoretical Aspects. *Monthly Weather Review*, 129(3), 420–436. DOI: 10.1175/1520-0493(2001)129<0420:ASWTET>2.0.CO;2.
- Whitaker, J. S., & Hamill, T. M. (2002). Ensemble Data Assimilation without Perturbed Observations. *Monthly Weather Review*, 130(7), 1913–1924. DOI: 10.1175/1520-0493(2002)130<1913:EDAWPO>2.0.CO;2.

This lesson paraphrases the method and does not reproduce source code, figures or data.
