# Exercise N — Variance-component estimation from repeated networks

**Status:** Reproducible synthetic Monte Carlo experiment  
**Prerequisite:** [Exercise M — multi-session network adjustment and robustness](exercise-m-multi-session-network-adjustment-and-robustness.md)  
**Dataset basis:** [Exercise D synthetic vertical-control observations](../../data/measurement/exercise-d-stochastic-control-network.csv)  
**Implementation:** [analyze_exercise_n.py](../../scripts/measurement/analyze_exercise_n.py)

> All observations and simulation trials are synthetic. This experiment demonstrates estimation of a deliberately simple stochastic model. It is not field evidence, an instrument calibration, a survey specification or a validated production estimator.

## 1. Research question

Previous exercises supplied the covariance matrix and studied the consequences of getting it wrong. Exercise N asks whether selected parts of that covariance model can be estimated from repeated network observations:

- Can independent observation-noise scale be recovered?
- Can a session-common variance component be distinguished from independent noise?
- How does the number of independent sessions affect estimation precision?
- How often does an unconstrained variance-component estimate become negative?

The experiment is deliberately limited to two components so that identifiability and sampling behaviour remain inspectable.

## 2. Functional and stochastic model

The network has five points A–E. A is fixed at 100.000 m; B–E are unknown. Each independent session repeats the same nine directed height differences in the Exercise D dataset. The synthetic reference elevations are A=100.000 m, B=101.200 m, C=102.000 m, D=101.700 m and E=102.400 m.

For a session observation vector y_g:

```
y_g = A x + e_g
Cov(e_g) = theta_1 D_0 + theta_2 11'
```

- D_0 is the diagonal matrix of squared observation-specific standard uncertainties from Exercise D, expressed in mm².
- theta_1 is a dimensionless scale factor; its true simulation value is 1.0.
- theta_2 is the session-common variance in mm²; its true simulation value is 0.25 mm², equivalent to tau=0.50 mm.
- Different sessions are independent.

The additive common component is intentionally simple: one random offset shared by all nine height-difference observations in a session. It does not represent every real instrument, setup, operator, environmental or processing effect.

## 3. Estimator

The implementation uses a two-component MINQUE-style quadratic estimator with D_0 as the fixed working covariance metric.

Define:

```
W = D_0^-1
P = W - W A (A' W A)^-1 A' W
C_1 = D_0
C_2 = 11'
q_i = sum_g y_g' P C_i P y_g
H_ij = tr(P C_i P C_j)
H theta_hat = q
```

The estimator is a linear solution in the quadratic statistics. It is not a constrained maximum-likelihood estimate. Unconstrained estimates are retained, including negative estimates of theta_2; clipping them to zero would change the estimator and its sampling properties. A negative estimate is an indication that the available residual information does not support a positive component under this unconstrained estimator, not evidence of physically negative variance.

The small dense matrix operations are implemented explicitly using Python's standard library. This is suitable for this tiny teaching network, not a recommendation for large operational networks.

## 4. Monte Carlo design

- Independent session counts: 3, 6, 12, 24 and 48.
- 2,000 trials for each session count.
- Fixed seed: 20261119.
- True independent variance scale: 1.0.
- True session-common variance: 0.25 mm².
- Each trial generates new independent session blocks from the full two-component covariance model.
- The same nine-observation geometry and observation-specific base variances are used throughout.

Reported statistics are the mean estimate, standard deviation across trials, RMSE against the known simulated component, and fraction of trials with a negative unconstrained estimate.

## 5. Reproduced results

| Sessions | Component | Mean estimate | SD | RMSE | Negative fraction |
|---:|---|---:|---:|---:|---:|
| 3 | Independent scale | 0.9967 | 0.4019 | 0.4018 | 0.0% |
| 3 | Session-common variance (mm²) | 0.2602 | 0.5451 | 0.5451 | 36.8% |
| 6 | Independent scale | 0.9901 | 0.2823 | 0.2824 | 0.0% |
| 6 | Session-common variance (mm²) | 0.2365 | 0.3564 | 0.3566 | 27.0% |
| 12 | Independent scale | 0.9973 | 0.2089 | 0.2089 | 0.0% |
| 12 | Session-common variance (mm²) | 0.2489 | 0.2706 | 0.2705 | 17.5% |
| 24 | Independent scale | 1.0035 | 0.1473 | 0.1473 | 0.0% |
| 24 | Session-common variance (mm²) | 0.2523 | 0.1929 | 0.1928 | 7.6% |
| 48 | Independent scale | 0.9988 | 0.1015 | 0.1015 | 0.0% |
| 48 | Session-common variance (mm²) | 0.2493 | 0.1347 | 0.1346 | 2.6% |

## 6. Interpretation

1. **Both components are recovered without material bias in this constructed model.** Across session counts, their Monte Carlo means remain close to the true values.
2. **The independent variance scale is more stable in this design.** Its standard deviation falls from 0.402 with three sessions to 0.102 with 48 sessions.
3. **The common-mode component is harder to estimate.** Its standard deviation falls from 0.545 to 0.135 over the same range. With only three sessions, the unconstrained estimate is negative in 36.8% of trials.
4. **More sessions improve stability, but do not eliminate uncertainty.** Even at 48 sessions, the session-common component has a non-negligible spread.
5. **Negative unconstrained estimates matter.** They expose finite-sample variability and warn against presenting a clipped estimate as though it were the direct result of the stated estimator.

The estimates are conditional on the assumed functional model, the two selected covariance components, the fixed working metric and independent Gaussian session generation. They do not prove that real field errors follow this model.

## 7. What this experiment does not establish

- It does not estimate covariance components from actual field observations.
- It does not test instrument-specific, operator-specific, time-correlated or spatially varying effects.
- It does not estimate cross-session correlation.
- It does not establish a minimum universally sufficient number of sessions.
- It does not provide calibrated confidence intervals or a production-grade constrained VCE implementation.
- It does not test robust VCE under gross errors.
- The known true components are available only because this is a simulation.

A real stochastic-model investigation would require repeated, independently documented observations, acquisition metadata, defensible grouping, independent checks and examination of residual structure. Variance-component estimation cannot rescue a misspecified functional model or turn non-independent repeats into independent evidence.

## 8. Reproduction

From the repository root:

```bash
python scripts/measurement/analyze_exercise_n.py
```

The script uses only the Python standard library and reads the Exercise D CSV without modifying it.

## 9. Research basis

- Teunissen, P. J. G. & Amiri-Simkooei, A. R. (2008). “Least-squares variance component estimation.” *Journal of Geodesy*, 82, 65–82. https://doi.org/10.1007/s00190-007-0157-x
- Guo, D.-M. & Xu, H.-Z. (2015). “Application of variance components estimation to calibrate geoid error models.” *SpringerPlus*, 4, 434. https://doi.org/10.1186/s40064-015-1210-5
- Aydin, C. (2011). “Estimation of Variance Components Using a Step-by-Step Approach.” *Journal of Surveying Engineering*. https://doi.org/10.1061/(ASCE)SU.1943-5428.0000043

These references establish the broader VCE context; the specific two-component teaching implementation and simulation design here are our own simplified construction.

