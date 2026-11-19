# Exercise J — Monte Carlo comparison of robust estimators

**Status:** Reproducible synthetic Monte Carlo experiment  
**Dataset:** Reuses the [Exercise C synthetic vertical-control network](../../data/measurement/exercise-c-synthetic-control-network.csv)  
**Implementation:** [analyze_exercise_j.py](../../scripts/measurement/analyze_exercise_j.py)  
**Scope:** Repeated comparison of ordinary least squares (LS), iterative data snooping and Huber IRLS under clean and contaminated observations, for baseline and augmented network designs.

> **All observations, errors and design changes are synthetic.** This is a teaching simulation, not field evidence, a survey specification or a universal ranking of estimators.

## 1. Research question

Exercise I showed how three methods behave in a few fixed cases. Exercise J asks whether those outcomes persist across repeated random realisations, and whether their performance changes with observation geometry, redundancy, gross-error location and sign.

The experiment runs 500 trials for each combination of network design and contamination scenario, using a fixed random seed (20261119). The reported Monte Carlo standard error (MC SE) makes the finite simulation precision visible.

## 2. Network designs and simulation model

The baseline is the nine-observation Exercise C network, with A fixed at 100.000 m and constructed reference elevations B = 101.200 m, C = 102.000 m, D = 101.700 m and E = 102.400 m.

The augmented design adds a hypothetical independent B–E height-difference observation with an assumed standard uncertainty of 1.6 mm. This is a design experiment only; it is not a real field observation or a prescribed survey configuration.

For each trial, every observation is regenerated around its reference height difference with independent Gaussian noise and the observation's stated a-priori standard uncertainty. Gross errors are then injected into selected observations:

- clean observations;
- one +20 mm error on CE;
- one +20 mm error on AB;
- two +15 mm errors on BD and CE;
- +15 mm on BD and −15 mm on CE.

The same scenario definitions and seed are used for both designs. The augmented network includes one additional observation and therefore has a different observation count and residual geometry.

## 3. Methods and evaluation

1. **LS:** ordinary weighted least squares using the original a-priori standard uncertainties.
2. **Iterative data snooping:** the Exercise I sequential diagnostic procedure, using standardised residuals and a two-sided Bonferroni threshold recalculated for the active observations at each round. Suspect observations are diagnostically withheld, not erased.
3. **Huber IRLS:** Huber equivalent weights with c = 1.345, using residuals scaled by the original a-priori standard uncertainties. Observations are downweighted, not deleted.

The primary estimation metric is the mean across trials of the four-coordinate RMSE, in millimetres, against the constructed reference elevations. The MC SE is the sample standard deviation of trial RMSE divided by the square root of the number of trials.

For snooping, the clean-data rate is the proportion of trials with at least one false flag (family-wise false-flag frequency). In contaminated cases, the rate is the proportion of trials in which every injected observation appears in the withheld set (exact-set identification). Exact-set identification is deliberately stricter than detecting at least one true error. Binomial MC SE is reported for these rates.

## 4. Results

<text>For 500 trials per design and scenario, the implementation produced the following mean coordinate RMSE values (mm). MC SE values are in parentheses.</text>

| Scenario | Design | LS | Iterative snooping | Huber IRLS |
|---|---|---:|---:|---:|
| Clean | Baseline | 0.981 (0.020) | 0.986 (0.020) | 0.990 (0.020) |
| Clean | Augmented | 0.936 (0.019) | 0.945 (0.020) | 0.948 (0.020) |
| CE +20 mm | Baseline | 3.118 (0.021) | 1.044 (0.020) | 1.281 (0.024) |
| CE +20 mm | Augmented | 2.532 (0.018) | 0.984 (0.020) | 1.086 (0.021) |
| AB +20 mm | Baseline | 6.237 (0.034) | 1.154 (0.024) | 1.740 (0.035) |
| AB +20 mm | Augmented | 6.097 (0.035) | 1.099 (0.025) | 1.595 (0.037) |
| BD +15, CE +15 mm | Baseline | 4.419 (0.021) | 1.521 (0.078) | 2.195 (0.036) |
| BD +15, CE +15 mm | Augmented | 3.213 (0.018) | 1.067 (0.021) | 1.379 (0.024) |
| BD +15, CE −15 mm | Baseline | 3.452 (0.016) | 1.171 (0.022) | 1.572 (0.024) |
| BD +15, CE −15 mm | Augmented | 3.408 (0.016) | 1.026 (0.019) | 1.462 (0.023) |

Snooping's clean-data false-flag frequency was 0.8% for the baseline design and 1.4% for the augmented design (nominal per-round alpha 1%). Exact-set identification rates were:

| Contamination | Baseline | Augmented |
|---|---:|---:|
| CE +20 mm | 100.0% | 100.0% |
| AB +20 mm | 100.0% | 100.0% |
| BD +15, CE +15 mm | 94.4% | 100.0% |
| BD +15, CE −15 mm | 99.6% | 99.8% |

These rates are specific to the selected network, error magnitudes, test rule and 500-trial simulation. A 100% observed rate does not establish a true 100% probability; the finite sample still has uncertainty.

## 5. Interpretation

- Under the clean Gaussian model, LS has the smallest mean RMSE in both designs, as expected from its role under the assumed stochastic model. Robust methods have a small efficiency cost in this simulation.
- Under the selected gross-error cases, iterative snooping gives the smallest mean RMSE, while Huber IRLS consistently improves on LS. This does not establish snooping as universally superior: the selected errors are relatively large and the iterative procedure is tailored to flag them.
- The AB contamination produces a larger LS effect than CE contamination. This illustrates that error impact depends on network geometry and redundancy, not only on the injected magnitude.
- The augmented link reduces mean RMSE in most tested contaminated cases and improves exact identification in the selected same-sign two-error case. It does not remove the influence of a gross error on AB.
- Same-sign and opposite-sign multiple errors produce different residual patterns. Exact identification is therefore sensitive to error configuration and cannot be inferred from a single-error detectability measure.
- The methods solve different problems. Snooping flags and withholds observations under a test rule; Huber limits influence; LS is the reference estimator under the assumed Gaussian model.

## 6. Limitations

This is a deliberately bounded simulation:

- only 500 trials per design/scenario; Monte Carlo uncertainty is reported, but rare-event probabilities are not estimated precisely;
- independent Gaussian random errors with known standard uncertainties;
- exact datum and linear observation equations;
- one fixed network and one illustrative added link;
- fixed gross-error locations and magnitudes;
- no correlated sessions, shared instrument errors, uncertain control, systematic effects, non-Gaussian tails or estimated robust scale;
- sequential data snooping uses the Exercise I heuristic; recalculating a Bonferroni threshold after each removal is not an exact overall sequential family-wise guarantee;
- no automatic deletion is justified by a statistical flag alone.

A future experiment should introduce defensible correlated observation groups, uncertain control, multiple gross-error locations and magnitudes, alternative robust estimators and design-cost constraints. Correlated observations must be modelled with a valid covariance structure and appropriate robust treatment, not treated as independent rows.

## 7. Reproduction

From the repository root:

```bash
python scripts/measurement/analyze_exercise_j.py
```

The script uses only the Python standard library, reads the Exercise C CSV and does not modify source data. The seed and trial count are explicit in the implementation.

## 8. Research context

This experiment extends, but does not reproduce, published comparisons of quality-control and robust-estimation methods:

1. Veronez, M. R. et al. (2015), “On evaluation of different methods for quality control of correlated observations,” *Survey Review*, 47(340), 28–35. [DOI](https://doi.org/10.1179/1752270614Y.0000000089).
2. Pokarowska, J. (2016), “Comparison of robust estimators for leveling networks in Monte Carlo simulations,” *Reports on Geodesy and Geoinformatics*. [DOI](https://doi.org/10.1515/rgg-2016-0023).
3. Baselga, S. et al. (2020), comparison of least-squares, iterative and global L1 approaches for multiple-outlier identification. [DOI](https://doi.org/10.13168/AGG.2020.0031).
4. “Minimum-variance-based outlier detection method using forward-search model error in geodetic networks” (2024), *Geoscientific Model Development*, 17, 2187. [Open article](https://gmd.copernicus.org/articles/17/2187/2024/).
5. Hekimoglu, S. et al. (2026), “Enhancing the Reliability of M-Estimation through Redundancy Design,” *Journal of Surveying Engineering*, 152(2). [DOI](https://doi.org/10.1061/JSUED2.SUENG-1654).

The implementation is an original teaching simulation. Its numerical outcomes should not be transferred to a real survey without a project-specific stochastic model, field evidence and independent validation.
