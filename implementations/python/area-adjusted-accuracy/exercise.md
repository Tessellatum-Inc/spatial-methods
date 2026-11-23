# Exercise: assessing a stratified land-cover map

**Level:** Advanced undergraduate / postgraduate  
**Estimated time:** 2–3 hours  
**Data:** Synthetic teaching sample; not a real map or field survey.

## Scenario

A hypothetical 1,000-hectare study area is mapped into forest (60% of area) and other (40%). Four reference units were selected by simple random sampling within each mapped-class stratum. The sample is in [sample.csv](sample.csv).

For this exercise assume independent simple random sampling within each stratum, independent stratum samples, complete response, known mapped-area weights and error-free reference labels. These are teaching assumptions, not claims about a real assessment.

## Tasks

1. Define the target population, sampling unit, strata and response variable.
2. Explain why equal sample sizes in the two strata are disproportionate to mapped area.
3. Construct the raw sample-count confusion matrix (rows mapped, columns reference).
4. Calculate reference-class proportions within each mapped stratum.
5. Weight each row by its mapped-area proportion to obtain the area-proportion error matrix. Check that it sums to one.
6. Calculate overall accuracy, user's accuracy by mapped class and producer's accuracy by reference class.
7. Estimate reference forest and other area proportions and convert them to hectares.
8. Calculate standard errors for overall accuracy and reference forest proportion using the stratified variance formula in the method note.
9. Calculate a 95% Wald interval for reference forest proportion and convert it to hectares.
10. Compare unweighted sample accuracy with area-adjusted accuracy. Explain why they coincide in this example and why that does not justify ignoring design weights.
11. Identify at least four omitted uncertainty sources or design limitations.
12. Write a short conclusion that reports the design, estimates, uncertainty and limitations without certifying the map.

Submit the matrices, calculations, a one-page interpretation and a design/response limitations statement.

## Worked solution

### Raw count matrix

| Mapped class | Reference forest | Reference other | Total |
|---|---:|---:|---:|
| Forest | 3 | 1 | 4 |
| Other | 1 | 3 | 4 |
| Total | 4 | 4 | 8 |

### Area-proportion error matrix

Within forest stratum, proportions are 0.75 forest and 0.25 other. Within other stratum, proportions are 0.25 forest and 0.75 other. Weight rows by 0.60 and 0.40:

| Mapped class | Reference forest | Reference other |
|---|---:|---:|
| Forest | 0.45 | 0.15 |
| Other | 0.10 | 0.30 |
| Total | 0.55 | 0.45 |

The matrix sums to 1.00.

### Accuracy

- Overall accuracy = 0.45 + 0.30 = **75%**.
- Forest user's accuracy = 3/4 = **75%**.
- Other user's accuracy = 3/4 = **75%**.
- Forest producer's accuracy = 0.45/0.55 = **81.82%**.
- Other producer's accuracy = 0.30/0.45 = **66.67%**.

Unweighted sample overall accuracy is 6/8 = 75%. It happens to equal the weighted estimate because both strata have identical observed accuracy. This coincidence does not make design weights optional.

### Reference-class area

- Forest proportion = 0.45 + 0.10 = **0.55**, or **550 ha**.
- Other proportion = 0.15 + 0.30 = **0.45**, or **450 ha**.

These are reference-adjusted estimates, not the mapped class totals of 600 ha and 400 ha.

### Uncertainty

For overall accuracy:

[
\widehat{Var}(\widehat{OA}) =
0.6^2\frac{0.75(0.25)}{3}+
0.4^2\frac{0.75(0.25)}{3}
=0.0325.
]

SE = √0.0325 = **0.1803**, or 18.03 percentage points.

For reference forest proportion, the within-stratum proportions are 0.75 and 0.25:

[
\widehat{Var}(\hat P_{forest}) =
0.6^2\frac{0.75(0.25)}{3}+
0.4^2\frac{0.25(0.75)}{3}
=0.0325.
]

SE = **0.1803**. The 95% Wald interval is:

[
0.55\pm1.96(0.1803)=[0.1966,0.9034].
]

For 1,000 ha, the interval is approximately **197–903 ha**. The sample is tiny, so the Wald approximation is fragile and the interval is wide.

### Example conclusion

> Under the stated hypothetical design of independent simple random sampling within mapped-class strata, estimated overall map accuracy is 75%. The area-adjusted reference forest proportion is 55%, corresponding to 550 ha of the 1,000 ha study area. Its estimated standard error is 18.0 percentage points and its approximate 95% Wald interval is 19.7%–90.3%. These estimates are highly uncertain because the illustrative sample is very small. The calculations assume known mapped-class area proportions and correct reference labels; they do not quantify interpretation uncertainty or other omitted sources. They should not be interpreted as map certification.

## Marking guide (20 points)

| Criterion | Points |
|---|---:|
| Population, units and design description | 3 |
| Raw count matrix and within-stratum proportions | 3 |
| Correct area-proportion matrix | 4 |
| Accuracy estimates | 3 |
| Area and uncertainty calculations | 4 |
| Interpretation and limitations | 3 |
| **Total** | **20** |
