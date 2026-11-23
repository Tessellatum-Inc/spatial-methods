# Exercise M — Multi-session network adjustment and robustness

**Status:** Reproducible synthetic Monte Carlo experiment  
**Prerequisite:** [Exercise L — block-robust GLS with correlated observations](exercise-l-block-robust-gls-with-correlated-observations.md)  
**Dataset basis:** [Exercise D synthetic vertical-control observations](../../data/measurement/exercise-d-stochastic-control-network.csv)  
**Implementation:** [analyze_exercise_m.py](../../scripts/measurement/analyze_exercise_m.py)

> **All observations, session effects, contamination and simulation trials are synthetic.** This experiment demonstrates a controlled model. It is not field evidence, a survey specification, a validated production estimator or a universal recommendation for robust network adjustment.

## 1. Research question

Exercise L showed why robust estimation should respect the covariance blocks created by shared measurement processes. Its main limitation was that the teaching network had only two session groups.

Exercise M expands the experiment to twelve independent sessions, each repeating the same nine-observation vertical network. It asks:

- How does covariance-aware GLS behave when clean repeated sessions are pooled?
- What happens when one observation or an entire session is contaminated?
- Does block-Huber GLS reduce the influence of contaminated sessions?
- How often does it downweight clean sessions?
- What happens when more than one session is contaminated?

The larger design makes group-level behaviour measurable, while retaining a small network whose model can be inspected.

## 2. Network and stochastic model

The network has five points, A–E, with A fixed at 100.000 m and four unknown elevations. Each session repeats the nine directed height differences in the Exercise D dataset. The synthetic reference elevations are:

| Point | Reference elevation |
|---|---:|
| A | 100.000 m |
| B | 101.200 m |
| C | 102.000 m |
| D | 101.700 m |
| E | 102.400 m |

There are 12 independent sessions and 9 observations per session: 108 observations in total. The individual observation standard uncertainties are reused from the Exercise D dataset. For this experiment, all nine observations in a repeat are treated as belonging to one session-level covariance block; the original Exercise D S1/S2 labels are not carried into the repeated-session model.

Within a session, the covariance is:

[
Q_g=D+	au^2mathbf{1}mathbf{1}^T
]

where D contains the observation-specific variances and the session-common standard uncertainty is (	au=0.50) mm. Different sessions are independent. The shared effect is an illustrative additive common-mode error applied to the nine height differences in a session. It is not asserted to represent every levelling or surveying session process.

A is held fixed in this experiment to keep the repeated network focused on relative height estimation. This differs from Exercise K/L, where A was connected through a stochastic control observation.

## 3. Estimators compared

### 3.1 Covariance-aware GLS

Each session's full covariance matrix is retained. The independent session blocks are pooled to estimate the common four-coordinate vector by generalized least squares.

### 3.2 Diagonal WLS

The comparison method retains each observation's marginal variance but discards within-session off-diagonal covariance. It is deliberately misspecified under the simulated common-mode error.

### 3.3 Block-Huber GLS

Each session's observations and design matrix are whitened using that session's covariance matrix. A single robust weight is then assigned to the complete whitened session block:

[
s_g=rac{lVert r_g^*Vert}{sqrt{m_g}}, qquad
w_g=min(1,c/s_g), qquad c=1.5
]

Here (r_g^*) is the whitened residual vector, (m_g=9) is the number of observations in the session and c is the chosen Huber tuning constant. The weight multiplies the entire session contribution to the normal equations.

This is a block-level robust objective, not nine independent row-wise Huber weights. A session weight below 0.8 is used only as a descriptive marker in the simulation summaries; it is not a formal hypothesis-test decision or a calibrated false-alarm threshold.

## 4. Monte Carlo scenarios

The script runs 3,000 trials per scenario with fixed seed 20261119. Each trial generates 12 independent session blocks from the full covariance model, then applies the same simulated data to all three estimators.

1. **Clean:** no injected gross errors.
2. **One-row error:** +20 mm added to observation CE in session 03.
3. **One-session error:** +4 mm added to all nine observations in session 04.
4. **Two opposing session errors:** +3 mm added to session 03 and −3 mm to session 09.
5. **Three same-direction session errors:** +3 mm added to sessions 02, 06 and 11.

The primary performance metric is the mean RMSE of the four estimated elevations against their constructed reference values. The Monte Carlo standard error (MC SE) describes uncertainty in the estimated mean RMSE across trials. The script also reports average session weights and the fraction of trials in which each session receives a weight below 0.8.

## 5. Reproduced results

Mean coordinate RMSE in millimetres; MC SE in parentheses.

| Scenario | GLS | Diagonal WLS | Block-Huber GLS |
|---|---:|---:|---:|
| Clean | 0.287 (0.002) | 0.289 (0.002) | 0.287 (0.002) |
| One row +20 mm | 0.372 (0.002) | 0.376 (0.002) | 0.310 (0.002) |
| One session +4 mm | 0.300 (0.002) | 0.324 (0.002) | 0.295 (0.002) |
| Two sessions, opposing ±3 mm | 0.287 (0.002) | 0.289 (0.002) | 0.288 (0.002) |
| Three sessions +3 mm each | 0.350 (0.003) | 0.447 (0.003) | 0.341 (0.003) |

### 5.1 Session-level downweighting

Average block weights (1.0 means no downweighting):

| Scenario | Session(s) of interest | Mean weight |
|---|---|---:|
| Clean | All 12 | Approximately 0.999 |
| One row +20 mm | Session 03 | 0.428 |
| One session +4 mm | Session 04 | 0.755 |
| Opposing ±3 mm | Sessions 03 and 09 | 0.889 and 0.892 |
| Three sessions +3 mm | Sessions 02, 06 and 11 | 0.902 each |

In clean trials, the fraction of trials in which any individual session received a weight below 0.8 was approximately zero for most sessions and 0.1% for session 12. For the targeted sessions, the corresponding frequencies were:

- One-row error, session 03: 100%.
- One-session +4 mm, session 04: 68.3%.
- Opposing ±3 mm, sessions 03 and 09: 23.5% and 22.3%.
- Three sessions +3 mm, sessions 02, 06 and 11: 19.8%, 19.6% and 20.0%.

These are empirical frequencies under this particular model and tuning constant, not general detection probabilities.

## 6. Interpretation

1. **Clean-data behaviour:** GLS and block-Huber GLS have practically identical RMSE in this experiment. The chosen block tuning does not visibly penalise the clean repeated network.
2. **Single-row contamination:** block-Huber GLS improves RMSE substantially, but it downweights the entire session containing the bad CE observation. It does not isolate the individual bad row.
3. **One contaminated session:** block-Huber GLS reduces the average coordinate RMSE relative to ordinary GLS and diagonal WLS. The targeted session is downweighted in about 68% of trials at the descriptive 0.8 threshold, not every time.
4. **Opposing session errors:** their effects partly cancel in the pooled estimate. The block method only moderately downweights either session. Cancellation in the final coordinates must not be mistaken for proof that both sessions are sound.
5. **Several contaminated sessions:** block-Huber GLS performs better than the two non-robust comparisons in this constructed case, but its mean weights show only moderate downweighting. Robust estimation is not a substitute for independent checks or adequate redundancy.
6. **Correlation matters:** diagonal WLS performs worse in several contaminated cases, especially the three-session case. The magnitude is model- and geometry-dependent; ignoring correlation does not guarantee one fixed direction or size of error.

The experiment illustrates both the value and the limitation of group robustness. A session-level estimator can protect a network from a contaminated acquisition group, but it may discard useful observations from that group. It can also fail to strongly downweight moderate contamination, especially when multiple groups are affected or errors partly cancel.

## 7. What this experiment does not establish

- The 12 sessions are simulated independent repeats of one small network, not real field sessions.
- The common-mode error is a simple additive model. Real session effects may be heterogeneous, time-dependent, correlated across sessions or tied to particular instruments, setups, operators and processing steps.
- The covariance parameters are known by construction; the experiment does not estimate variance components from real repeat data.
- The fixed datum and network geometry are assumed correct.
- The block-Huber tuning constant is selected for demonstration, not optimised or calibrated for a target false-alarm rate.
- The RMSE metric is available only because the simulation supplies true coordinates. Robust-estimator uncertainty coverage and formal false-alarm calibration are not evaluated here.
- A low block weight is a diagnostic signal, not proof of a blunder, its cause or permission to delete the session.

## 8. Reproduction

From the repository root:

```bash
python scripts/measurement/analyze_exercise_m.py
```

The script uses only the Python standard library, reads the Exercise D CSV without modifying it, generates the twelve repeated sessions in memory and uses a fixed random seed.

## 9. Research direction

The next step should not simply add more robust estimators. It should test whether the assumed session covariance structure can be estimated and validated from repeated field observations. Useful extensions include heterogeneous session variances, instrument- and setup-level random effects, partially shared sessions, covariance-component estimation, independent check observations, and robust methods that can distinguish a single bad observation from a contaminated acquisition group.

A production workflow should preserve raw observations, model the acquisition process, report diagnostics and uncertainty, and require documented human review before withholding data.
