# Exercise H — Monte Carlo reliability and design simulation

**Status:** Reproducible synthetic simulation  
**Dataset:** Reuses the [Exercise C synthetic vertical-control network](../../data/measurement/exercise-c-synthetic-control-network.csv)  
**Implementation:** [analyze_exercise_h.py](../../scripts/measurement/analyze_exercise_h.py)  
**Scope:** Empirical single-error detection, family-wise false alarms, correct identification, multiple-error masking and a comparison of two network designs.

> **All results are synthetic.** No field observations were collected. The assumed observation uncertainties, exact datum, independent Gaussian error model and proposed B–E link are teaching assumptions, not a survey specification or evidence of real-world performance.

## 1. Why simulate after calculating reliability?

Exercise G calculated redundancy numbers, minimal detectable biases (MDBs) and external effects from the network model. Those quantities are useful design diagnostics, but they do not by themselves show the full behaviour of a decision procedure across repeated noisy realisations.

This exercise asks:

- How often does a test flag an observation when no gross error exists?
- How often is a deliberately biased observation detected?
- Does the procedure identify the correct observation, or flag other observations as well?
- What changes when two gross errors occur together?
- Does adding the hypothetical B–E link change detection behaviour, not just the analytical reliability indicators?

Monte Carlo simulation is an established way to examine the operating characteristics of geodetic outlier-detection procedures. Published studies have used repeated simulated scenarios to assess detection success, false decisions, correlated observations and multiple outliers. The exercise here is deliberately smaller and transparent rather than a reproduction of any published experiment.

## 2. Network models

Two designs are compared:

1. **Baseline:** the nine-observation, four-unknown Exercise C network, with five degrees of freedom.
2. **Augmented:** the same network plus a hypothetical independent B–E height-difference observation with an assumed standard uncertainty of 1.6 mm, giving ten observations and six degrees of freedom.

Point A is treated as exact. The original observation standard uncertainties are retained. Each simulated observation error is independently drawn from a zero-mean normal distribution with its stated a-priori standard uncertainty. Gross errors are then added to selected observations.

The experiment does not simulate uncertain control, common-mode errors, non-normal tails, instrument drift, environmental effects or correlations between the original observations. Those are important extensions for a later experiment.

## 3. Test procedure and multiple-testing control

For each simulated observation vector, the script performs a weighted least-squares adjustment and computes the complete residual vector. It standardises each residual by its model-based standard uncertainty and applies a two-sided threshold.

The family-wise false-alarm probability is set to **0.01**. A Bonferroni threshold is used:

\[
c = \Phi^{-1}\left(1-\frac{0.01}{2n}\right)
\]

where \(n\) is the number of observations and \(\Phi^{-1}\) is the standard normal quantile function. The resulting critical values are 3.261 for the nine-observation network and 3.291 for the ten-observation network.

Bonferroni control does not require the residual tests to be independent. More importantly, the simulation does not pretend they are independent: each trial generates one complete vector of observation errors, adjusts the network once, and derives all standardised residuals from that same vector. Their covariance and dependence are therefore retained.

This is a **one-shot, two-sided standardised-residual screening procedure**. It is not a full iterative data-snooping algorithm, a robust estimator, or a multiple-hypothesis identification procedure. No observation is automatically deleted.

### Relationship to Exercise G MDB

Exercise G used \(\delta_0=4.13\), approximately a single-test two-sided \(\alpha=0.001\), power 0.80 design criterion. That is not the same test design as a 1% family-wise error rate across nine or ten observations.

For this simulation, a family-wise 80%-power planning MDB is calculated using:

\[
\delta_{FWER,80}=c+\Phi^{-1}(0.80)
\]

\[
MDB_{FWER,80,i}=\delta_{FWER,80}\frac{\sigma_i}{\sqrt{r_i}}
\]

This is a normal-theory approximation for the marginal test of an individual observation. Because residual tests are correlated and the decision is made across the complete set, empirical joint outcomes need not equal the nominal marginal power exactly.

## 4. Simulation design

- **Random seed:** 20261119.
- **Trials:** 20,000 per scenario.
- **Noise-only trials:** used to estimate the family-wise false-alarm rate.
- **Single-error trials:** inject a positive gross error into the weakest- and strongest-redundancy observations in each design, at 0.5, 1.0, 1.5 and 2.0 times that observation's family-wise 80%-power MDB.
- **Multiple-error trials:** inject two simultaneous gross errors into the two observations with the lowest redundancy numbers in each design. Both are set to their own family-wise MDB, once with the same sign and once with opposite signs.

At a detection probability near 80%, the Monte Carlo standard error with 20,000 trials is approximately 0.28 percentage points. At a false-alarm probability near 1%, it is approximately 0.07 percentage points. Reported percentages should therefore be read as simulation estimates, not exact probabilities.

## 5. Reproduced results

### 5.1 Noise-only family-wise false alarms

| Design | Critical value | Simulated family-wise false-alarm rate |
|---|---:|---:|
| Baseline, 9 observations | 3.261 | 0.9% |
| Augmented, 10 observations | 3.291 | 0.9% |

Both empirical estimates are consistent with the nominal 1% family-wise target at this trial count.

### 5.2 MDB comparison

| Indicator | Baseline | Add B–E |
|---|---:|---:|
| Weakest redundancy number | 0.437 | 0.508 |
| MDB at weakest observation, Exercise G criterion | 8.38 mm | 7.77 mm |
| MDB at weakest observation, family-wise 80% criterion | 8.33 mm | 7.78 mm |
| Largest family-wise 80% MDB in the network | 10.06 mm | 9.61 mm |

The additional link improves the weakest redundancy number and lowers the largest family-wise MDB under these assumptions. The analytical values are close across the two criteria for this particular network, but the criteria are conceptually different and should not be interchanged in other designs.

### 5.3 Single gross errors

At one times the family-wise 80%-power MDB:

| Design and injected observation | True observation detected | Exactly correct flagged set | At least one other observation flagged |
|---|---:|---:|---:|
| Baseline — BD | 79.5% | 45.6% | 35.2% |
| Baseline — DA | 79.9% | 64.1% | 16.7% |
| Augmented — BD | 80.5% | 60.4% | 21.1% |
| Augmented — CE | 80.2% | 68.7% | 12.2% |

The simulated probability of detecting the injected observation is close to the 80% marginal planning target. But that is not the same as identifying the correct error set. In a substantial fraction of trials, other observations also cross the threshold.

The proportion of additional flags rises sharply at larger injected biases. That is not evidence that the injected observation becomes harder to detect: its detection probability approaches 100%, while the gross error also propagates through the adjustment into other residuals. This is a practical warning against interpreting every flagged residual as an independent blunder.

At half the family-wise MDB, the injected observation was detected in about 11% of trials in the representative cases. At 1.5 times MDB, detection was approximately 99.8–99.9%. These are simulation outcomes for the selected observations and assumptions, not universal detection rates.

### 5.4 Two simultaneous gross errors

The multiple-error experiment exposes a more serious limitation of single-error screening. Each injected bias is set to its own family-wise 80%-power MDB. The selected pair is the two observations with the lowest redundancy in each design.

| Design | Pair and signs | Both true errors detected | Exact flagged set | At least one missed |
|---|---|---:|---:|---:|
| Baseline | BD + AB, same sign | 99.9% | 35.4% | 0.1% |
| Baseline | BD + AB, opposite signs | 0.0% | 0.0% | 100.0% |
| Augmented | BD + CD, same sign | 1.9% | 0.0% | 98.1% |
| Augmented | BD + CD, opposite signs | 98.7% | 47.1% | 1.3% |

The selected pair differs between designs, so these rows are not a controlled head-to-head comparison of the same two observations. They demonstrate that the interaction between simultaneous errors depends on the network geometry and the error-sign pattern.

In the baseline opposite-sign case and the augmented same-sign case, the two errors largely mask one another in residual space under this screening procedure. In the other cases, both true errors are usually flagged, but innocent observations are also frequently flagged. This is why a single-outlier MDB cannot be used as a guarantee for multiple-outlier identification.

## 6. What the experiment establishes

1. **The noise-only false-alarm control behaves as intended.** The empirical family-wise rate was 0.9% for both designs, close to the nominal 1%.
2. **The family-wise MDB is a useful planning scale, not a guarantee.** At its nominal 80% design level, empirical single-error detection was approximately 80% for the representative observations.
3. **Detection and identification are different.** Detecting the true biased observation does not ensure that the flagged set contains only that observation.
4. **Multiple gross errors can mask each other.** The selected two-error cases produced detection rates ranging from 0% to 99.9%, depending on design and sign pattern.
5. **More redundancy can improve reliability, but does not eliminate model risk.** The added link improved analytical indicators and several single-error outcomes; it did not make the one-shot test reliable for every multiple-error configuration.
6. **A flag is an investigation signal.** Field notes, independent checks, instrument records, repeat occupations and physical evidence are needed before rejecting or correcting an observation.

## 7. Limitations and next experiments

This experiment assumes a linear model, exact datum, independent Gaussian random errors, known a-priori standard uncertainties and a one-shot standardised-residual test. It does not model uncertain control, correlated observations, systematic errors, non-normal noise, iterative re-adjustment, robust estimation, or a full multiple-outlier procedure.

Further work should compare:
- iterative data snooping and robust estimators against the one-shot screen;
- multiple-outlier likelihood-ratio or subset tests;
- explicitly correlated observation groups, including common setups and shared instruments;
- uncertain control and datum alternatives;
- external effects on project-critical height differences;
- candidate link designs under cost, access and field-time constraints.

The next field-facing validation must use independently collected observations with documented equipment, calibration, procedures, control provenance and environmental conditions. Synthetic simulations cannot substitute for that evidence.

## 8. Reproduction

From the repository root:

```bash
python scripts/measurement/analyze_exercise_h.py
```

The implementation uses only the Python standard library. It reads the Exercise C CSV, builds both design matrices, simulates observation errors, computes correlated standardised residuals, applies the Bonferroni threshold and reports empirical outcomes.

## 9. References

1. Veronez, M. R. et al. (2015), “On evaluation of different methods for quality control of correlated observations,” *Survey Review*, 47(340), 28–35. The study compares quality-control procedures under correlated observations and multiple outliers using Monte Carlo scenarios. [DOI](https://doi.org/10.1179/1752270614Y.0000000089).
2. “A Monte Carlo-Based Outlier Diagnosis Method for Sensitivity Analysis” (2020), *Remote Sensing*, 12(5), 860. Examines the probability levels of iterative outlier elimination, including the role of test-statistic correlation and reliability indicators. [Open article](https://www.mdpi.com/2072-4292/12/5/860).
3. “Minimum-variance-based outlier detection method using forward-search model error in geodetic networks” (2024), *Geoscientific Model Development*, 17, 2187. Discusses iterative standardised-residual testing and the masking/swamping difficulties caused by multiple outliers. [Open article](https://gmd.copernicus.org/articles/17/2187/2024/).
4. Baarda, W. (1968), *A Testing Procedure for Use in Geodetic Networks*, Netherlands Geodetic Commission, Publications on Geodesy, New Series, Vol. 2, No. 5. Foundational work on statistical testing and reliability in geodetic networks.
5. TU Delft OPEN Publishing (2024), *Network Quality Control*. Open textbook on geodetic network adjustment, quality control, reliability and design. [DOI](https://doi.org/10.59490/tb.100).

This is an original, deliberately limited teaching simulation. It is not a reproduction of the cited studies, and its results should not be transferred to a real survey without a project-specific stochastic model and validation.
