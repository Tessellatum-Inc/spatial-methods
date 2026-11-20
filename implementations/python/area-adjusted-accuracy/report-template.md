# Map accuracy and reference-area assessment report

> Replace every bracketed prompt and remove guidance text before publication.

## 1. Executive summary

- Map/product, version and date: [ ]
- Study area, boundary and area unit: [ ]
- Assessment purpose and intended decision: [ ]
- Sampling design and strata: [ ]
- Sample size overall and by stratum: [ ]
- Overall accuracy, standard error and interval method: [ ]
- Key reference-class area estimates and uncertainty: [ ]
- Principal limitations: [ ]

## 2. Map and target population

Describe the map producer, version, date, classification scheme, study boundary, total area, CRS, target population, spatial/temporal support and mapped-class area weights.

| Mapped class / stratum | Mapped area | Area proportion W_i | Frame size, if known |
|---|---:|---:|---:|
| [class] | [ ] | [ ] | [ ] |

Confirm area proportions sum to one and document exclusions or unclassified areas.

## 3. Sampling design

- Sampling frame and unit: [ ]
- Probability selection procedure: [ ]
- Within-stratum design: [ ]
- Sample size by stratum: [ ]
- Inclusion probabilities and weights: [ ]
- Replacement and nonresponse policy: [ ]
- Selection seed and reproducibility record: [ ]
- Deviations from planned design: [ ]

Do not describe a convenience sample as a probability sample. If the actual design differs from independent SRS within mapped classes, do not apply the companion estimator unchanged.

## 4. Reference response protocol

- Reference sources and dates: [ ]
- Temporal alignment: [ ]
- Reference resolution and positional quality: [ ]
- Class definitions and interpretation key: [ ]
- Interpreter procedures and qualifications: [ ]
- Independent interpretation/adjudication: [ ]
- Ambiguous and mixed units: [ ]
- Reference-label uncertainty: [ ]

Explain positional mismatch, mixed pixels, temporal change and interpreter disagreement.

## 5. Sample disposition

| Stratum | Selected | Interpreted | Nonresponse | Excluded | Final n |
|---|---:|---:|---:|---:|---:|
| [class] | [ ] | [ ] | [ ] | [ ] | [ ] |

Explain departures and their effect on inference.

## 6. Error matrix and estimates

State orientation: rows = mapped classes; columns = reference classes.

- Raw sample-count matrix: [insert]
- Area-proportion error matrix: [insert]
- Overall accuracy: [ ]
- User's accuracy by mapped class: [ ]
- Producer's accuracy by reference class: [ ]
- Reference-class area proportions and areas: [ ]

Explain why design weights were applied and why raw sample counts are not population area proportions.

## 7. Uncertainty and inference

For each estimate state the variance estimator, assumptions, standard error, interval method, confidence level, finite-population correction (if used), and treatment of nonresponse, unequal inclusion probabilities and reference uncertainty.

Separate sampling uncertainty from measurement, interpretation, mapped-area-weight and model uncertainty. Do not present a Wald interval as exact.

## 8. Results and interpretation

Discuss class-specific errors, area estimates, uncertainty, precision relative to intended use, rare classes and any material spatial/temporal error patterns. Avoid claims such as “accurate everywhere” or “certified” unless an applicable independent process supports them.

## 9. Limitations and deviations

Record frame coverage, design deviations, nonresponse, reference limitations, spatial/temporal mismatch, area-weight uncertainty, variance-estimator limitations and omitted uncertainty sources.

## 10. Reproducibility and attachments

Attach or reference map version/checksum, frame and sample IDs, selection code/seed/inclusion probabilities, reference interpretations/adjudication, input CSV, area weights, software version, code commit, command, generated report and independent review.

## 11. Conclusion

State what the evidence supports, for which population, geography, time and use. State principal uncertainty and limitations. Distinguish statistical assessment from certification, regulatory acceptance or fitness-for-purpose decisions.
