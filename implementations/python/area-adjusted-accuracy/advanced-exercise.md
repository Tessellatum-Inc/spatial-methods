# Advanced exercise: disproportionate sampling and area-adjusted map accuracy

**Level:** advanced undergraduate to postgraduate  
**Suggested time:** 2–3 hours  
**Status:** Synthetic teaching case; not an assessment of a real map.

## Scenario

A land-cover map contains three mapped classes. A reference sample was selected by independent simple random sampling within each mapped-class stratum. The rare mapped class, water, was deliberately oversampled to obtain enough observations for class-specific assessment.

The map-area proportions are known for this exercise:

| Mapped stratum | Mapped-area proportion | Sample size |
|---|---:|---:|
| Forest | 0.70 | 20 |
| Agriculture | 0.25 | 20 |
| Water | 0.05 | 40 |
| **Total** | **1.00** | **80** |

The water stratum supplies 50% of the sample but represents only 5% of mapped area. The observations are in [advanced-sample.csv](advanced-sample.csv). Rows are sampled units; columns are `sample_id`, `map_class` and `reference_class`.

For the calculations, assume:
- the target is the mapped area represented by these three exhaustive classes;
- the mapped-area proportions are known without error;
- selection is independent SRS within each mapped-class stratum;
- every sampled unit has a valid reference label;
- reference labels are treated as correct;
- the strata are independent.

These assumptions are deliberately strong and are part of the problem, not facts established by the CSV.

## Tasks

1. Reconstruct the raw count confusion matrix, with mapped classes as rows and reference classes as columns. Check all row totals against the stated sample sizes.
2. Calculate the unweighted, count-based overall accuracy. Calculate user's accuracy by mapped class and producer's accuracy by reference class from the raw counts.
3. Explain why the raw count matrix represents the sample allocation rather than the mapped-area composition. Identify the disproportionate allocation.
4. For each mapped stratum, calculate its within-stratum reference-class proportions.
5. Multiply each row of within-stratum proportions by that mapped stratum's area proportion. Construct the area-proportion error matrix.
6. Calculate area-adjusted overall accuracy and compare it with the raw count-based value. Explain the difference in percentage points.
7. Calculate area-adjusted user's accuracy for each mapped class.
8. Estimate reference-class area proportions and, for a total mapped area of 12,000 hectares, estimated reference-class areas.
9. Calculate area-adjusted producer's accuracy by dividing each diagonal area-proportion cell by its reference-class column total. Compare these values with the raw count-based producer's accuracies.
10. Calculate the standard error and approximate 95% Wald interval for overall accuracy and each reference-class area proportion. State why these intervals are only approximate.
11. Explain why the water class's sample share, mapped-area share, user's accuracy and producer's accuracy answer different questions.
12. Write a short assessment conclusion. Separate sampling uncertainty from reference-label uncertainty, map-area uncertainty, temporal mismatch and spatial-support issues.

## Worked solution

### 1–2. Raw count matrix

| Mapped class | Reference forest | Reference agriculture | Reference water | Row total |
|---|---:|---:|---:|---:|
| Forest | 17 | 2 | 1 | 20 |
| Agriculture | 6 | 12 | 2 | 20 |
| Water | 15 | 5 | 20 | 40 |
| **Column total** | **38** | **19** | **23** | **80** |

Raw count-based overall accuracy is ((17+12+20)/80=0.6125), or **61.25%**.

Raw user's accuracy is 85% for forest, 60% for agriculture and 50% for water. Raw count-based producer's accuracy is 17/38 = 44.74% for forest, 12/19 = 63.16% for agriculture and 20/23 = 86.96% for water.

These raw producer's accuracies are sample-count ratios. Under disproportionate stratification, they are not the area-adjusted producer's accuracies.

### 3–6. Area-proportion error matrix and overall accuracy

The within-stratum proportions are:

| Mapped stratum | Ref. forest | Ref. agriculture | Ref. water |
|---|---:|---:|---:|
| Forest | 0.85 | 0.10 | 0.05 |
| Agriculture | 0.30 | 0.60 | 0.10 |
| Water | 0.375 | 0.125 | 0.50 |

Weight each row by its mapped-area proportion (0.70, 0.25 and 0.05):

| Mapped stratum | Ref. forest | Ref. agriculture | Ref. water | Row total |
|---|---:|---:|---:|---:|
| Forest | 0.59500 | 0.07000 | 0.03500 | 0.70000 |
| Agriculture | 0.07500 | 0.15000 | 0.02500 | 0.25000 |
| Water | 0.01875 | 0.00625 | 0.02500 | 0.05000 |
| **Column total** | **0.68875** | **0.22625** | **0.08500** | **1.00000** |

The area-adjusted overall accuracy is the diagonal sum:

[
0.595+0.150+0.025=mathbf{0.7700}quad(77.00%).
]

The raw count-based value is 61.25%, a difference of **15.75 percentage points**. The difference is not a software correction: it follows from the unequal sampling fractions and the known mapped-area weights. The rare water stratum was intentionally oversampled and has lower user's accuracy than the other strata, so its 50% sample share must not be treated as 50% of the mapped area.

### 7. Area-adjusted user's accuracy

Because each row is a mapped-class stratum, user's accuracy is the diagonal within-stratum proportion:
- Forest: 17/20 = **85.00%**.
- Agriculture: 12/20 = **60.00%**.
- Water: 20/40 = **50.00%**.

### 8. Reference-class area

The column totals estimate reference-class area proportions:
- Forest: 0.68875 = **68.875%**, or **8,265 ha** of 12,000 ha.
- Agriculture: 0.22625 = **22.625%**, or **2,715 ha**.
- Water: 0.08500 = **8.500%**, or **1,020 ha**.

These are estimated reference-class areas, not the original mapped-class areas (which were 70%, 25% and 5%).

### 9. Area-adjusted producer's accuracy

Divide each diagonal cell by its reference-class column total:
- Forest: 0.595/0.68875 = **86.39%**.
- Agriculture: 0.150/0.22625 = **66.30%**.
- Water: 0.025/0.085 = **29.41%**.

In particular, the raw count-based water producer's accuracy (86.96%) is not a valid substitute for the area-adjusted estimate (29.41%). The oversampled water stratum changes the sample column composition substantially. Producer's accuracy is defined relative to reference-class area, so its denominator must use the area-adjusted column total.

### 10. Sampling uncertainty

Using the implementation's variance estimator for independent SRS within mapped strata, the approximate results are:

| Estimate | Estimate | Standard error | Approx. 95% Wald interval |
|---|---:|---:|---:|
| Overall accuracy | 0.7700 | 0.0640 | [0.6446, 0.8954] |
| Reference forest proportion | 0.68875 | 0.0632 | [0.5649, 0.8126] |
| Reference agriculture proportion | 0.22625 | 0.0558 | [0.1168, 0.3357] |
| Reference water proportion | 0.08500 | 0.0392 | [0.0082, 0.1618] |

Intervals are normal-approximation Wald intervals clipped to [0,1]. They may have poor coverage for small samples or estimates near boundaries. No finite-population correction is applied because stratum population sizes are not supplied. The intervals do not account for uncertainty in the mapped-area weights or reference labels.

### 11–12. Interpretation

The water stratum is 5% of mapped area, 50% of the reference sample, has 50% user's accuracy and only 29.41% area-adjusted producer's accuracy. Those figures refer to four distinct quantities: mapped prevalence, sample allocation, reliability of mapped water labels, and completeness of reference water captured by the map.

A defensible conclusion would report the 77.0% area-adjusted overall accuracy and the class-specific estimates, while noting that the 80-unit sample was disproportionately allocated and the results depend on the stated stratified-SRS design and reference protocol. The water class has a low estimated producer's accuracy despite its high raw count-based value. Sampling intervals do not quantify interpretation disagreement, reference-data error, map-area uncertainty, temporal mismatch, geolocation error or mismatch in minimum mapping unit/spatial support. These require separate design and evidence.

## Reproducibility check

Run the companion from this directory:

```bash
python area_adjusted_accuracy.py advanced-sample.csv \
  --area-weights '{"forest":0.70,"agriculture":0.25,"water":0.05}' \
  --total-area 12000 --json-out advanced-report.json
```

The output's area-proportion matrix, overall accuracy and reference-class area proportions should match the worked values above. The program does not calculate raw count-based metrics; calculate those directly from the sample confusion matrix.

## Marking guide (20 points)

| Criterion | Points |
|---|---:|
| Correct raw count matrix and raw metrics | 3 |
| Correct within-stratum proportions and area-proportion matrix | 4 |
| Correct area-adjusted overall and user's accuracy | 3 |
| Correct reference-class areas and producer's accuracy | 4 |
| Correct uncertainty calculations and interpretation | 3 |
| Clear explanation of design, limitations and evidence boundaries | 3 |
| **Total** | **20** |

**Instructor note:** Accept small rounding differences. Award interpretation credit only where the learner distinguishes sample counts from mapped-area weights and does not generalise the estimator to unsupported designs.
