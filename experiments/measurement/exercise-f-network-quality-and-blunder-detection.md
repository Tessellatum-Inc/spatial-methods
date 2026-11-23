# Exercise F — Network quality, statistical testing and blunder detection

**Status:** Reproducible synthetic worked experiment  
**Dataset:** Reuses [Exercise C synthetic vertical-control network](../../data/measurement/exercise-c-synthetic-control-network.csv)  
**Implementation:** [analyze_exercise_f.py](../../scripts/measurement/analyze_exercise_f.py)  
**Scope:** Global chi-square testing, local standardized residuals, multiple testing, gross-error propagation, withholding sensitivity and independent checking.

> **All observations in this exercise are synthetic.** The +20 mm error and independent check are deliberately constructed teaching values. No instrument was operated and no field survey was performed. This is not a survey specification or evidence of compliance with a standard.

## 1. Question

A least-squares adjustment always produces a best fit under its mathematical model. That does not establish that the observations, stochastic assumptions, datum or field procedures are sound.

This exercise asks:

1. Is the network's total weighted residual energy compatible with the a-priori stochastic model?
2. Which individual observations are locally suspicious?
3. How does one gross error affect the residuals of other observations?
4. What is lost when an observation is withheld?
5. What can an independent check establish that internal residuals cannot?

## 2. Network and assumptions

The network is the nine-observation, four-unknown vertical network from Exercise C:

- Fixed datum: A = 100.000 m, treated as exact for this constrained teaching model.
- Unknown heights: B, C, D and E.
- Observations: AB, BC, CA, BD, DA, CD, DE, EA and CE.
- Degrees of freedom: 9 observations − 4 unknown heights = **5**.
- Each observation retains its Exercise C a-priori standard uncertainty.
- Observation covariance is diagonal: observations are assumed independent.
- The variance factor used for the tests is fixed at its a-priori value, σ₀² = 1. The exercise does not estimate a new scale and then use that same estimate to conceal a poor fit.

The independence assumption is deliberately simple. If observations share setups, sessions, instruments, environmental effects or common corrections, a defensible non-diagonal covariance model may be needed. Do not add correlations merely to improve a test result.

## 3. Global test

Let (v) be the adjusted observation residual vector, (P=Q_{ll}^{-1}) the weight matrix, and (r=n-u=5) the redundancy.

[
Q = v^T P v
]

Under the stated linear model, Gaussian errors and correct a-priori covariance, (Q/σ_0^2) follows a chi-square distribution with five degrees of freedom.

At a two-sided 95% confidence level, the approximate critical interval is:

[
0.831 leq Q leq 12.833
]

Interpret both tails:

- Above the upper limit: residual energy is too large for the assumed model and uncertainties.
- Below the lower limit: residual energy is unusually small; the assumed uncertainties may be conservative, or the particular synthetic realisation is unusually smooth.
- Inside the interval: the global test does not reject the model at this level. It does not prove the model is true or that no blunder exists.

The original Exercise C synthetic network has (Q=0.642256), below the lower limit. This is a useful warning against labelling every non-upper-tail result a clean pass. The original dataset is an illustrative construction, not a random field sample calibrated to a known probability model.

## 4. Local tests and residual covariance

The residual covariance is not the observation covariance. Adjustment absorbs some observation error into the estimated heights and leaves the remainder in the residuals.

For the linear model:

[
Q_{vv}=Q_{ll}-A(A^T P A)^{-1}A^T
]

With the a-priori variance factor fixed at one, the standardized residual for observation (i) is:

[
w_i = rac{v_i}{sqrt{(Q_{vv})_{ii}}}
]

A residual is therefore judged relative to its own expected residual uncertainty, not simply by comparing raw millimetres. The residuals are mutually correlated because they share estimated parameters. A large (|w_i|) is a diagnostic, not proof of the cause or identity of a blunder.

### Multiple testing

Testing nine observations independently at an unadjusted 5% level does not preserve a 5% family-wise false-alarm probability. A simple conservative Bonferroni illustration uses a two-sided per-test level of (0.05/9), giving an approximate normal threshold of (|w|>2.773). This is a teaching threshold, not a substitute for a fully specified geodetic data-snooping procedure.

The tests are correlated, and Bonferroni is conservative. More rigorous approaches include Baarda-style data snooping with explicitly defined test statistics and power, simultaneous multiple-outlier tests, and robust estimation as a sensitivity analysis. Multiple simultaneous errors can mask one another or distribute residuals across the network. A single largest residual is not guaranteed to identify the correct observation.

## 5. Deliberately contaminated case

The script adds **+20 mm** to the CE height difference, leaving its stated a-priori uncertainty unchanged. This is a controlled gross-error injection.

Expected reproduced results (rounding may vary in the final printed decimal):

| Diagnostic | Original | CE contaminated by +20 mm |
|---|---:|---:|
| Weighted residual sum (Q) | 0.642256 | 63.980547 |
| Variance factor (Q/5) | 0.128451 | 12.796109 |
| Global 95% two-sided test | Below lower limit | Above upper limit |
| Largest absolute standardized residual | 0.767 | 7.961 |

In the contaminated adjustment, the CE residual is approximately −11.682 mm, but the adjustment also redistributes error into other observations. DE and EA become suspicious as well. The residual of an observation is not equal to the gross error injected into it.

The script reports all standardized residuals so the pattern, not just the largest value, can be examined.

## 6. Withholding sensitivity is not a deletion rule

The script also performs a diagnostic refit with CE withheld. This illustrates how the estimated network changes when that observation is not used.

With CE withheld, the remaining network still has eight observations, four unknowns and four degrees of freedom. The resulting E height estimate is about 102.401166 m.

This is **not** a recommendation to delete CE. Withholding changes the model and its redundancy. A real investigation should first inspect the observation record, field book, station identity, units, instrument and prism constants, setup and turning-point procedures, timing, environmental conditions, session effects and any independent repeat. If the observation is corrected, preserve the original value, correction rationale, evidence and version history. If it is downweighted, document the stochastic reason and compare the sensitivity of the result.

## 7. Independent external check

A separate synthetic A-to-E height-difference check of +2.4010 m is included in the script but excluded from every adjustment.

It is compared with the E-minus-A height predicted by the contaminated-network diagnostic refit. The prediction differs from the check by approximately +0.166 mm in this constructed example.

The purpose is conceptual: a check observation that was not used to estimate the network provides evidence that internal residuals cannot provide. In a real survey, independence must be designed, not merely claimed. Repeating the same setup or reusing the same systematic error source may not provide a genuinely independent check.

The example check is deliberately synthetic and should not be interpreted as validation of the contaminated data or as a real survey result.

## 8. What this experiment demonstrates

- Global and local tests answer different questions.
- A global test can detect a network-level inconsistency without identifying its cause.
- Local standardized residuals account for the residual covariance induced by adjustment.
- Residuals can spread and mask gross errors.
- Multiple testing changes the false-alarm problem.
- Deleting an observation changes network geometry, redundancy and uncertainty.
- An independent check is fundamentally different from an internal residual.
- A statistical flag should initiate investigation, not automate a field decision.

## 9. Reproduction

From the repository root:

```bash
python scripts/measurement/analyze_exercise_f.py
```

The implementation uses only the Python standard library. It reads the Exercise C CSV, performs weighted least squares, computes the residual covariance diagonal, reports global and local diagnostics, injects the CE error and runs the withholding sensitivity analysis.

## 10. Limitations and next work

This is a small linear vertical network with one exact datum, diagonal observation covariance and five degrees of freedom. It does not implement a complete production-grade Baarda data-snooping suite, correlated multiple-outlier testing, robust M-estimation, variance-component estimation or field-specific observation models. The Bonferroni threshold is explicitly a conservative illustration.

A stronger next experiment should compare single and multiple gross errors, vary their magnitudes and locations, quantify detection power and minimal detectable bias, introduce defensible session correlations, and evaluate how network design changes reliability. A real field exercise should then collect independent observations with documented procedures and instrument checks.

## 11. References

1. Intergovernmental Committee on Surveying and Mapping (ICSM), *Guideline for the Adjustment and Evaluation of Survey Control*, Special Publication 1, Version 2.2. Sections 5.1–5.2 discuss local and global tests and chi-square evaluation. [Official PDF](https://www.icsm.gov.au/sites/default/files/2020-12/Guideline-for-Adjustment-and-Evaluation-of-Survey-Control_v2.2.pdf).
2. U.S. Army Corps of Engineers, *EM 1110-2-1009: Structural Deformation Surveying* (1 February 2018), Chapter 9. Discusses network adjustment, degrees of freedom, residuals, statistical testing and goodness of fit. [Official manual](https://www.publications.usace.army.mil/Portals/76/Publications/EngineerManuals/EM_1110-2-1009.pdf).
3. Kok, J. J. (1984), *On Data Snooping and Multiple Outlier Testing*, NOAA Technical Report NOS NGS 30. [NOAA repository record](https://repository.library.noaa.gov/view/noaa/23359/).
4. Schwarz, C. R. and Kok, J. J. (1993), “Blunder Detection and Data Snooping in LS and Robust Adjustments,” *Journal of Surveying Engineering*, 119(4). [DOI](https://doi.org/10.1061/(ASCE)0733-9453(1993)119:4(127)).
5. “On evaluation of different methods for quality control of correlated observations” (2014), *Survey Review*. Compares data snooping, multiple-outlier tests and robust approaches for correlated GNSS observations. [Publisher page](https://www.tandfonline.com/doi/full/10.1179/1752270614Y.0000000089).

These sources inform the concepts; the exercise is an original, deliberately bounded educational implementation, not a reproduction of a complete standard procedure.
