# Exercise L — Block-robust generalized least squares with correlated observations

**Status:** Reproducible synthetic worked experiment  
**Prerequisite:** [Exercise K — correlated errors and generalized least-squares adjustment](exercise-k-correlated-errors-and-generalized-least-squares.md)  
**Dataset:** [Exercise D synthetic session-grouped network](../../data/measurement/exercise-d-stochastic-control-network.csv)  
**Implementation:** [analyze_exercise_l.py](../../scripts/measurement/analyze_exercise_l.py)

> **All observations, covariance assumptions, contamination and simulation trials are synthetic.** This is a bounded teaching experiment, not a validated production estimator, field specification or universal robust-adjustment recommendation.

## 1. Research question

Exercises I–J studied robust estimation with independent observation errors. Exercise K introduced shared session effects and covariance-aware generalized least squares (GLS). Exercise L combines these concerns:

- Can a session-level contamination be handled without pretending correlated observations are independent?
- What happens when a single observation is contaminated inside a correlated session?
- Does a block-robust estimator retain efficiency on clean data while reducing the influence of contaminated groups?

The experiment compares covariance-aware GLS, a diagonal WLS model that ignores off-diagonal covariance, and an illustrative block-Huber GLS estimator.

## 2. Observation and covariance model

The network reuses the nine directed height differences and two session groups from Exercise D. A is tied to a stochastic control observation with value 100.001 m and assumed standard uncertainty 2.0 mm. The synthetic reference elevations are A = 100.000 m, B = 101.200 m, C = 102.000 m, D = 101.700 m and E = 102.400 m.

For a height-difference observation:

[
l_i=H_{to(i)}-H_{from(i)}+epsilon_i+u_{s(i)}
]

where (epsilon_i) is observation-specific noise and (u_{s(i)}) is a shared additive session error. The session-common standard uncertainty is 0.35 mm. The covariance matrix includes each observation's individual variance and the common session covariance for observations belonging to the same session. The stochastic control is an independent singleton block.

The full covariance is retained in GLS and in the whitening step used by the block estimator. The diagonal comparison deliberately drops off-diagonal session covariance while retaining the same marginal variances.

## 3. Methods

### 3.1 Covariance-aware GLS

GLS minimises the quadratic residual form using the complete covariance matrix:

[
hat x=(A^TQ^{-1}A)^{-1}A^TQ^{-1}l
]

### 3.2 Diagonal WLS comparison

This method uses only the diagonal of the covariance matrix. It is included as a deliberately misspecified baseline when common session effects exist, not as a recommended approach.

### 3.3 Block-Huber GLS

The observation vector and design matrix are whitened separately within each covariance block using a Cholesky factorisation. The two session blocks are kept intact; the stochastic control is a third singleton block.

At each IRLS iteration, the estimator computes the Euclidean norm of the whitened residual vector for each block, divided by the square root of the number of observations in that block. It then applies a Huber-style equivalent block weight:

[
t_g=rac{|r_g^*|}{sqrt{m_g}}, qquad
w_g=min(1,c/t_g), qquad c=1.5
]

The block weight multiplies the entire whitened block contribution to the normal equations. It does not assign independent robust weights to correlated raw rows. A low block weight downweights the session's contribution as a whole.

**Important limitation:** this is an illustrative block-Huber objective, not a calibrated block-level hypothesis test. The normalised residual norm is affected by parameter fitting and block leverage; the threshold (c=1.5) is a chosen teaching parameter, not a universal cutoff. With only two session blocks, robust group identification is intrinsically weak. The experiment must not be read as evidence that two groups are enough for reliable operational robust estimation.

## 4. Monte Carlo design

The script performs 5,000 trials per scenario using seed 20261119. Each trial generates observation-specific noise, shared session effects and the stochastic-control error from the full covariance model. The same simulated observations are processed by all three estimators.

Four cases are compared:

1. **Clean:** no injected gross error.
2. **Single-row contamination:** +20 mm is added to observation CE.
3. **Session contamination:** +4 mm is added to every S1 observation, representing a shared session-level offset.
4. **Opposing session contamination:** +3 mm is added to S1 and −3 mm to S2.

The primary metric is the mean five-coordinate RMSE against the constructed reference elevations. Monte Carlo standard errors (MC SE) are standard errors of the mean trial RMSE. The script also reports average final block weights for the block-Huber estimator; 1.0 means no downweighting.

## 5. Reproduced results

Mean coordinate RMSE in millimetres; MC SE in parentheses.

| Scenario | GLS | Diagonal WLS | Block-Huber GLS |
|---|---:|---:|---:|
| Clean | 1.891 (0.016) | 1.891 (0.016) | 1.891 (0.016) |
| CE +20 mm | 3.311 (0.012) | 3.350 (0.012) | 3.247 (0.014) |
| S1 common +4 mm | 1.989 (0.017) | 2.041 (0.017) | 1.992 (0.017) |
| S1 +3 mm, S2 −3 mm | 2.002 (0.016) | 2.032 (0.016) | 2.028 (0.016) |

Mean final block-Huber weights, in block order S1, S2, stochastic control:

| Scenario | S1 | S2 | Control |
|---|---:|---:|---:|
| Clean | 1.000 | 0.999 | 1.000 |
| CE +20 mm | 0.999 | 0.366 | 1.000 |
| S1 common +4 mm | 0.672 | 0.999 | 1.000 |
| S1 +3 mm, S2 −3 mm | 0.804 | 0.926 | 1.000 |

Values are rounded; the implementation output is authoritative.

## 6. Interpretation

- On clean data, all three methods have practically indistinguishable mean RMSE in this experiment. The block estimator's chosen tuning does not create a visible efficiency penalty at the displayed precision.
- For the single CE gross error, block-Huber GLS reduces mean RMSE relative to ordinary GLS and downweights S2. Because CE belongs to S2, the whole session is downweighted, including its uncontaminated observations. This is the cost of protecting against a contaminated correlated block.
- For a common S1 offset, block-Huber GLS reduces the influence of S1 and performs close to GLS in this simulation.
- When both sessions are shifted in opposite directions, both session blocks receive lower weights. With only two sessions, there is little independent group information to distinguish which block, if either, is trustworthy. The robust estimator does not solve an unidentifiable or poorly supported diagnosis problem.
- Diagonal WLS is not consistently worse by a large margin in this particular network. The covariance model matters, but the numerical impact depends on the size and pattern of correlation and contamination.

The experiment illustrates a trade-off: block robustness protects against a contaminated group but can sacrifice clean observations within that same group. The appropriate block definition must reflect the actual shared error mechanism.

## 7. Limitations and next research questions

This simulation has only two session groups, a simple common additive session effect, known covariance parameters, a fixed network, a stochastic control prior and a chosen block-Huber tuning constant. It does not estimate covariance parameters, handle many independent sessions, model cross-session systematic effects, or provide calibrated false-alarm and detection probabilities.

The whitening basis is tied to the defined covariance blocks. Robustifying transformed components independently would introduce basis dependence; this implementation instead applies one weight to each pre-defined whitened block. The method is still dependent on the defensibility of those blocks and the chosen loss.

A stronger follow-up should use a network with many independently repeated sessions, compare alternative block losses and tuning rules, estimate or validate covariance components from repeat data, and evaluate false downweighting, missed contamination, coordinate bias, uncertainty coverage and sensitivity to block definitions. Correlation-aware robust methods should be selected from the measurement process, not merely because a numerical routine is available.

## 8. Reproduction

From the repository root:

```bash
python scripts/measurement/analyze_exercise_l.py
```

The implementation uses only the Python standard library, reads the Exercise D CSV and does not modify it. The seed, trial count, covariance assumptions, contamination cases and tuning constant are explicit in the script.

## 9. Research context

This experiment is motivated by work on quality control of correlated observations, including:

- Veronez, M. R. et al. (2015), “On evaluation of different methods for quality control of correlated observations,” *Survey Review*, 47(340), 28–35. [https://doi.org/10.1179/1752270614Y.0000000089](https://doi.org/10.1179/1752270614Y.0000000089).
- Pokarowska, J. (2016), “Comparison of robust estimators for leveling networks in Monte Carlo simulations,” *Reports on Geodesy and Geoinformatics*. [https://doi.org/10.1515/rgg-2016-0023](https://doi.org/10.1515/rgg-2016-0023).

The present implementation is an original teaching simulation, not a reproduction of either study and not a validated estimator for operational survey adjustment.
