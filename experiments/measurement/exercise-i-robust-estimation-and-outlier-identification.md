# Exercise I — Robust estimation and iterative outlier identification

**Status:** Reproducible synthetic comparison  
**Dataset:** Reuses the [Exercise C synthetic vertical-control network](../../data/measurement/exercise-c-synthetic-control-network.csv)  
**Implementation:** [analyze_exercise_i.py](../../scripts/measurement/analyze_exercise_i.py)  
**Scope:** Ordinary least squares, iterative data snooping and Huber iteratively reweighted least squares (IRLS), tested on uncontaminated, single-error and multiple-error versions of the same network.

> **All observations and injected errors are synthetic.** The reference elevations are known only because this is a constructed teaching dataset. This is not field evidence, a survey specification or a claim that one estimator is universally superior.

## 1. The question

Exercise H showed that simultaneous gross errors can mask each other under a one-shot residual test. Exercise I compares three approaches that respond differently to suspicious observations:

1. **Ordinary least squares (LS):** retains the original observation weights and minimises the weighted sum of squared residuals.
2. **Iterative data snooping:** repeatedly adjusts the network, identifies the largest absolute standardised residual, tests it, and diagnostically withholds it if it exceeds the current threshold.
3. **Huber M-estimation by IRLS:** iteratively changes equivalent observation weights, reducing the influence of large normalised residuals without deleting observations.

These approaches do not answer exactly the same question. Data snooping is a hypothesis-testing and identification procedure. Huber IRLS is a robust estimation procedure. A small Huber weight is evidence that an observation has exerted unusual influence under the chosen model; it is not proof of a blunder or its cause.

## 2. Synthetic network and known reference

The network has four unknown elevations, B, C, D and E, tied to fixed A = 100.000 m. It uses the nine Exercise C height-difference observations and their original a-priori standard uncertainties.

The constructed reference elevations are:

| Point | Reference elevation |
|---|---:|
| A | 100.000 m |
| B | 101.200 m |
| C | 102.000 m |
| D | 101.700 m |
| E | 102.400 m |

The original CSV observations are close to these reference differences, with small synthetic perturbations. Two contaminated copies are created in memory; the source CSV is never modified:

- **Single-error case:** add +20 mm to CE.
- **Multiple-error case:** add +15 mm to BD and −15 mm to CE.

Coordinate RMSE is calculated against the constructed reference elevations. It is an evaluation metric available only because the true values are known in this synthetic exercise; real surveys generally do not have this luxury.

## 3. Method details

### 3.1 Ordinary least squares

For design matrix A, observation vector l and diagonal weight matrix P:

\[
\hat{x}_{LS}=(A^T P A)^{-1}A^T P l
\]

All observations retain their original a-priori weights. Large residuals can therefore exert substantial influence on the estimated elevations.

### 3.2 Iterative data snooping

The implementation uses two-sided standardised residuals from the original diagonal a-priori covariance model. At each round:

1. Adjust the currently active observations.
2. Compute the absolute standardised residuals.
3. Calculate a two-sided Bonferroni threshold for the current number of active observations, using per-round alpha = 0.01.
4. If the largest residual exceeds the threshold, diagnostically withhold that observation and repeat.
5. Stop when no residual exceeds the current threshold or when another removal would leave no residual degrees of freedom.

The initial nine-observation threshold is approximately 3.261. Subsequent thresholds are recalculated for the smaller active set.

**Important statistical qualification:** recalculating a Bonferroni threshold at each round does not create a simple overall family-wise guarantee for the entire sequential procedure. The procedure is presented as a transparent iterative diagnostic heuristic, not as an exact sequential multiple-testing solution. The withheld observations are retained in the original source dataset and are not automatically declared invalid.

### 3.3 Huber M-estimation

Huber IRLS uses the influence function:

\[
\psi(u)=
\begin{cases}
u,& |u|\leq c\\
c\,\operatorname{sign}(u),& |u|>c
\end{cases}
\]

with equivalent weight:

\[
w(u)=\frac{\psi(u)}{u}
=\min\left(1,\frac{c}{|u|}\right)
\]

The tuning constant is c = 1.345, a conventional normal-theory choice associated with approximately 95% asymptotic efficiency under ideal Gaussian conditions. The normalised residual used for the weights is the adjusted residual divided by the original a-priori observation standard uncertainty. The scale reference is held fixed through iterations.

The weights are updated until their maximum absolute change is below 10⁻¹⁰ or 100 iterations are reached. A weight near one leaves an observation's original relative weight essentially unchanged; a smaller weight reduces its influence. Huber IRLS does not remove an observation.

This implementation is a deliberately clear diagonal-covariance teaching version. It is not a general robust estimator for correlated observations. Correlated groups require an appropriate multivariate robust model rather than independent row-by-row weights.

## 4. Reproduced results

### 4.1 Original synthetic observations

All three approaches return the same solution because no observation is sufficiently unusual to trigger snooping or Huber downweighting.

| Method | B (m) | C (m) | D (m) | E (m) | Coordinate RMSE |
|---|---:|---:|---:|---:|---:|
| LS | 101.200857 | 102.000466 | 101.700976 | 102.401048 | 0.87 mm |
| Iterative data snooping | 101.200857 | 102.000466 | 101.700976 | 102.401048 | 0.87 mm |
| Huber IRLS | 101.200857 | 102.000466 | 101.700976 | 102.401048 | 0.87 mm |

Huber weights remain one for all nine observations. Data snooping withholds none.

### 4.2 Single gross error: CE +20 mm

| Method | B error | C error | D error | E error | Coordinate RMSE |
|---|---:|---:|---:|---:|---:|
| LS | +0.17 mm | −2.54 mm | +1.06 mm | +6.08 mm | 3.34 mm |
| Iterative data snooping | +0.84 mm | +0.40 mm | +0.98 mm | +1.17 mm | 0.89 mm |
| Huber IRLS | +0.69 mm | −0.25 mm | +1.00 mm | +2.24 mm | 1.28 mm |

Data snooping identifies CE as the largest standardised residual and withholds it diagnostically. After refitting, the maximum absolute standardised residual is 0.751. Huber IRLS converges in 12 iterations and reduces CE's equivalent weight to 0.143, while retaining it in the adjustment.

For this deliberately clear single-error case, both robust approaches substantially reduce coordinate error relative to ordinary LS. Data snooping is closer to the reference solution in this one constructed example, but that is not evidence of universal superiority.

### 4.3 Two gross errors: BD +15 mm and CE −15 mm

| Method | B error | C error | D error | E error | Coordinate RMSE |
|---|---:|---:|---:|---:|---:|
| LS | −3.19 mm | +3.23 mm | +4.79 mm | −1.05 mm | 3.34 mm |
| Iterative data snooping | +1.31 mm | +0.37 mm | +0.58 mm | +0.94 mm | 0.88 mm |
| Huber IRLS | +0.29 mm | +1.07 mm | +1.55 mm | +0.42 mm | 0.97 mm |

The sequential snooping procedure withholds BD and CE in successive rounds. Huber IRLS retains all observations but reduces the equivalent weights of BD to 0.124 and CE to 0.182. Both methods substantially reduce the coordinate RMSE in this particular two-error scenario.

The two contaminated observations are not the only source of uncertainty in a real survey. Model misspecification, shared systematic effects, incorrect control, wrong point identities and non-normal noise can all produce residual patterns that these simple methods may misinterpret.

## 5. What this comparison teaches

1. **LS is an important baseline, not a universal outlier remedy.** Under the assumed Gaussian model with no gross errors, LS is an efficient estimator. Its sensitivity to contamination is the reason to test alternatives.
2. **Data snooping explicitly identifies and tests suspicious observations.** Its decisions depend on the test family, threshold, model and sequence of removal.
3. **Huber IRLS limits influence rather than deleting data.** It can protect estimates from large residuals, but a reduced weight is not a causal diagnosis.
4. **Multiple-error cases need separate attention.** A method that works well for one large outlier is not automatically reliable when several errors interact.
5. **Robust estimation does not repair a bad stochastic model.** Shared instrument errors, correlated sessions and uncertain control need to be represented in the model.
6. **Preserve raw observations.** Any withheld or downweighted observation should remain traceable, with the decision, evidence and subsequent independent checks documented.

## 6. Limitations and next work

The experiment uses a small linear vertical network, exact A control, diagonal independent observation covariance, known synthetic reference elevations and deliberately injected gross errors. It does not model correlated observation groups, uncertain control, non-normal noise, systematic effects, robust scale estimation, leverage-specific multivariate procedures or a fully controlled sequential multiple-testing procedure.

A more advanced follow-up should:
- compare the methods over Monte Carlo ensembles rather than only selected fixed contamination cases;
- evaluate sensitivity to outlier magnitude, location, sign and number;
- test correlated observation groups and uncertain control;
- compare Huber with redescending estimators such as Tukey's biweight and with Danish weighting;
- examine minimum-L1 or exhaustive subset methods for difficult multiple-error cases;
- track parameter uncertainty and coverage, not coordinate RMSE alone;
- retain independent field checks as the final arbiter of suspected measurement problems.

## 7. Reproduction

From the repository root:

\`\`\`bash
python scripts/measurement/analyze_exercise_i.py
\`\`\`

The implementation uses only the Python standard library. It reads the Exercise C CSV and constructs the contaminated cases in memory; it does not alter the source dataset.

## 8. References

1. Pokarowska, M. (2016), “Comparison of robust estimators for leveling networks in Monte Carlo simulations,” *Reports on Geodesy and Geoinformatics*, 101, 70–81. Compares LS, Pope's iterative data snooping and Huber M-estimation in levelling networks. [DOI](https://doi.org/10.1515/rgg-2016-0023). <Cite refs={["turn718204search1","turn718204search14"]}/>
2. Baselga, S., Klein, I., Suraci, S. S., de Oliveira, L. C., Matsuoka, M. T. and Rofatto, V. F. (2020), “Performance comparison of least squares, iterative and global L₁ norm minimization and exhaustive search methods for outlier detection in leveling networks,” *Acta Geodynamica et Geomaterialia*, 17(4), 425–438. Discusses the limitations of iterative data snooping for multiple outliers and compares robust and exhaustive approaches. [DOI](https://doi.org/10.13168/AGG.2020.0031). <Cite refs={["turn718204search12"]}/>
3. Veronez, M. R. et al. (2015), “On evaluation of different methods for quality control of correlated observations,” *Survey Review*, 47(340), 28–35. Compares data snooping, multiple-outlier tests and robust approaches under correlated GNSS observations and simulated multiple errors. [DOI](https://doi.org/10.1179/1752270614Y.0000000089). <Cite refs={["turn718204search0"]}/>
4. “Minimum-variance-based outlier detection method using forward-search model error in geodetic networks” (2024), *Geoscientific Model Development*, 17, 2187. Reviews and compares robust and iterative detection approaches in geodetic adjustment. [Open article](https://gmd.copernicus.org/articles/17/2187/2024/). <Cite refs={["turn718204search2"]}/>
5. Huber, P. J. (1964), “Robust Estimation of a Location Parameter,” *The Annals of Mathematical Statistics*, 35(1), 73–101. Foundational paper for Huber's robust M-estimation. [DOI](https://doi.org/10.1214/aoms/1177703732).

This is an original, limited teaching implementation informed by the cited literature. It is not a complete production adjustment package, and the selected examples do not establish a universally best estimator.
