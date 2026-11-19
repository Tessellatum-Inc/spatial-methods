# Exercise K — Correlated errors and generalized least-squares network adjustment

**Status:** Reproducible synthetic worked experiment  
**Prerequisite:** [Exercise D — stochastic control and correlated observations](exercise-d-stochastic-control-and-correlation.md)  
**Dataset:** [Exercise D synthetic session-grouped network](../../data/measurement/exercise-d-stochastic-control-network.csv)  
**Implementation:** [analyze_exercise_k.py](../../scripts/measurement/analyze_exercise_k.py)

> **All observations, control values, covariance assumptions and Monte Carlo trials are synthetic.** This is a teaching experiment, not field evidence, a survey specification or a universal model of session errors.

## 1. Research question

Exercise D introduced a covariance matrix with shared session effects and showed that generalized least squares (GLS) changes the adjustment relative to an independent-observation model. Exercise K makes the consequence more explicit:

- What happens when a network is adjusted with the covariance structure that generated the observations?
- What happens when the same marginal standard uncertainties are retained but correlations are ignored?
- Do the resulting formal uncertainties describe the actual repeated-simulation errors?

The central lesson is that a covariance model is part of the measurement model. Correlation is not a cosmetic adjustment to a table of standard deviations.

## 2. Observation and covariance model

The network contains five unknown elevations A–E and nine directed height differences. A is connected to a stochastic control observation with value 100.001 m and assumed standard uncertainty 2.0 mm. This gives the height-difference network an external datum reference without treating A as exact.

For each height difference:

[
l_i=H_{to(i)}-H_{from(i)}+epsilon_i+u_{s(i)}
]

where:

- (epsilon_i) is an observation-specific random error;
- (u_{s(i)}) is a common additive error for the session assigned to observation (i);
- the two session effects are independent of each other and of the observation-specific errors.

The individual standard uncertainties are those recorded in the Exercise D dataset. The synthetic session-common standard uncertainty is (	au=0.35) mm. The control observation has an independent 2.0 mm standard uncertainty.

The observation covariance matrix is:

[
mathbf Q_{ll}=mathbf D+	au^2mathbf Zmathbf Z^T
]

with an additional independent control-observation variance. D contains the individual observation variances, while Z identifies session membership. Within-session off-diagonal covariances equal (	au^2); between-session covariances are zero in this simplified model.

This model represents one possible shared additive session effect. It is not a universal levelling covariance model. A real model must be derived from instrument setups, staff calibration, operator and environmental effects, reduction procedures, temporal correlation and other actual shared error sources.

## 3. Two adjustment models

**Model 1 — covariance-aware GLS**

[
hat{mathbf x}_{GLS}=
(mathbf A^Tmathbf Q_{ll}^{-1}mathbf A)^{-1}
mathbf A^Tmathbf Q_{ll}^{-1}mathbf l
]

[
mathbf C_{hat x,GLS}=
(mathbf A^Tmathbf Q_{ll}^{-1}mathbf A)^{-1}
]

**Model 2 — diagonal weighted least squares**

The comparison model retains the same marginal variances but sets all off-diagonal covariances to zero. It is deliberately misspecified when session-common effects are present. It demonstrates the consequence of pretending correlated measurements are independent.

Both models use the same observations, stochastic control and marginal standard uncertainties. The only difference is whether the shared session covariance is represented.

## 4. Repeated simulation

The script runs 5,000 trials with fixed seed 20261119. Each trial generates independent observation-specific noise, two shared session errors and an independent stochastic-control error using the full covariance model. Both adjustment methods then process the same simulated observations.

For each coordinate, the experiment reports:

- empirical bias;
- empirical RMSE;
- formal standard uncertainty from the assumed adjustment model;
- empirical coverage of the nominal estimate ±1.96 formal standard uncertainties.

Coverage is a calibration diagnostic: under a well-specified Gaussian model and correctly computed formal uncertainty, the nominal 95% intervals should cover the constructed true coordinate at approximately the expected rate over repeated trials. Finite Monte Carlo variation remains.

## 5. Reference results

Run:

```bash
python scripts/measurement/analyze_exercise_k.py
```

The script prints a direct comparison on the committed Exercise D observations, followed by the Monte Carlo table. The latter is generated reproducibly from the stated seed and trial count; the output is the authoritative numerical result for the current implementation.

### Reproduced Monte Carlo results

The committed implementation was executed for 5,000 trials. RMSE and formal standard uncertainty are in millimetres; coverage is the empirical proportion of nominal 95% intervals containing the true coordinate.

| Point | GLS RMSE | GLS formal u | GLS coverage | Diagonal WLS RMSE | Diagonal formal u | Diagonal coverage |
|---|---:|---:|---:|---:|---:|---:|
| A | 1.996 | 2.000 | 94.94% | 1.996 | 2.000 | 94.94% |
| B | 2.266 | 2.267 | 94.84% | 2.267 | 2.275 | 94.94% |
| C | 2.242 | 2.261 | 95.22% | 2.243 | 2.264 | 95.28% |
| D | 2.230 | 2.245 | 95.16% | 2.230 | 2.255 | 95.36% |
| E | 2.330 | 2.333 | 95.24% | 2.330 | 2.345 | 95.34% |

For this particular network and modest 0.35 mm session-common term, the numerical differences are small. The diagonal model slightly overstates several coordinate standard uncertainties here, while its empirical coverage remains close to 95%. This is an important result in itself: ignoring correlation does not guarantee an obvious or uniformly optimistic error. The effect depends on how the shared error projects through the network geometry and observation groups. The GLS solution is the statistically coherent estimator under the covariance model used to generate these trials; the diagonal model is misspecified even where its numerical results happen to be close.

Interpret the results by comparing empirical RMSE with formal standard uncertainty and by examining interval coverage. A diagonal model can produce plausible-looking coordinate estimates while misrepresenting their uncertainty because it fails to account for common information shared by observations. The direction and magnitude of the effect depend on the network geometry, session membership and covariance magnitudes; do not assume that every formal uncertainty will always be smaller or always be larger.

## 6. Interpretation and practical implications

1. **Repeated measurements are not automatically independent.** Observations sharing a setup, session, instrument, calibration, operator or correction can share error.
2. **Marginal standard deviations are not enough.** Two datasets with identical per-observation standard deviations can contain different information if their covariance differs.
3. **GLS uses the covariance structure explicitly.** It changes the weighting and the formal covariance of estimated coordinates.
4. **Misspecified covariance can undermine uncertainty statements.** A close-looking adjusted coordinate is not evidence that its standard uncertainty is calibrated.
5. **The covariance model needs evidence.** Shared-error terms should be justified from measurement procedures, calibration records, repeat-session experiments or a defensible physical/statistical model.
6. **Redundancy must be genuinely independent.** Adding another observation from the same session may add less independent information than a measurement made under a different setup or session.

## 7. Limitations and next extension

This experiment uses only two synthetic session groups, one common additive error per group, independent observation-specific noise, known covariance parameters, a linear model and a stochastic control prior. It does not estimate covariance parameters from data, model time-correlated sequences, include cross-session systematics or test a real instrument/field procedure.

Robust estimation under correlated errors is deliberately not claimed here. Row-wise Huber weights applied to correlated raw observations are not automatically covariance-aware; whitening and robustification also require careful treatment of the covariance structure and the chosen residual basis. A later experiment should investigate defensible block-robust or covariance-aware robust procedures, including their sensitivity to group definition and covariance misspecification.

The original CSV is read only and is never modified. The implementation uses Python's standard library and explicit matrix operations suitable for this small teaching network. Production networks should use stable matrix factorizations and specialist adjustment software rather than dense matrix inversion.

## 8. Research context

This experiment builds on the correlated-observation quality-control literature and the prior project exercises:

- Veronez et al. (2015), “On evaluation of different methods for quality control of correlated observations,” *Survey Review*, 47(340), 28–35. [https://doi.org/10.1179/1752270614Y.0000000089](https://doi.org/10.1179/1752270614Y.0000000089).
- Exercise D in this repository, which introduced uncertain control and a transparent session-common covariance model.
- Exercise H, which explicitly noted that correlated residuals arise because residuals share the same simulated observation vector and must not be treated as independent tests.

This is an original, bounded teaching simulation. Its numerical outcomes are not transferable to field work without a project-specific stochastic model, measurement evidence and independent validation.
