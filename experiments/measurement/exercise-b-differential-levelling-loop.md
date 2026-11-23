# Exercise B — differential levelling, loop misclosure and adjustment

**Version:** 0.1  
**Status:** Reproducible synthetic worked experiment; not field evidence  
**Primary subjects:** SM-FND-011, SM-COL-001, SM-COL-003  
**Connected subjects:** SM-ALG-018, SM-REC-008  
**Dataset:** [Synthetic levelling observations](../../data/measurement/exercise-b-synthetic-levelling.csv)  
**Analysis:** [Reproducible Python analysis](../../scripts/measurement/analyze_exercise_b.py)  
**Prerequisite:** [Exercise A — repeated distance and horizontal-angle observations](exercise-a-repeated-distance-and-angle.md)  
**Foundation:** [Measurement principles and field verification](../../foundations/measurement-science/measurement-principles-and-field-verification.md)

## 1. Purpose

This experiment demonstrates a small differential-levelling loop from section observations to adjusted elevations. It covers:

- reducing backsight and foresight totals to observed height differences;
- computing loop misclosure;
- comparing an independently observed reverse run;
- applying a declared stochastic model;
- distributing the closure condition by weighted least squares;
- propagating observation covariance to adjusted point elevations;
- distinguishing internal closure from independent evidence of quality.

Every observation is synthetic. The values do not represent a real instrument, operator, benchmark or field survey.

## 2. Network and datum assumptions

The loop begins and ends on the same assumed benchmark BM-A.

- BM-A adopted elevation: 100.000000 m (treated as exact for this constrained teaching example).
- Forward direction: BM-A → TP1 → TP2 → TP3 → BM-A.
- Reverse direction: BM-A → TP3 → TP2 → TP1 → BM-A.
- Four sections; total loop length: 4.000 km.
- Distances are section lengths, not individual backsight/foresight sight lengths.
- Turning points are assumed stable and identical between forward and reverse runs.
- All height differences are reduced to metres, with positive values indicating rise in the direction of travel.

Treating BM-A as exact is a simplifying datum constraint. A real control survey must account for the uncertainty, stability, datum and provenance of its starting and closing benchmarks. If the two control marks are distinct, their covariance and datum relationship also matter.

## 3. Observation model

For section i:

\[
\Delta h_i = \sum BS_i - \sum FS_i
\]

The forward loop closure condition is:

\[
\sum_{i=1}^{n}\Delta h_i = 0
\]

The forward misclosure is:

\[
f=\sum_i\Delta h_i
\]

A positive f means the computed closing elevation is above the adopted starting elevation. The corrections must sum to -f.

The CSV records section-level sums of backsights and foresights. These are aggregated synthetic totals, not individual setup readings. Consequently, this dataset cannot assess sight-length balance, individual turning-point handling, setup-by-setup blunders or collimation behaviour.

## 4. Synthetic observations

The machine-readable CSV contains both a forward run and a separately simulated reverse run. The reverse observations are reserved as an independent directional check; they are not pooled into the forward-run adjustment.

### Forward run

| Section | From → To | Length (km) | ΣBS (m) | ΣFS (m) | Observed Δh (m) |
|---:|---|---:|---:|---:|---:|
| 1 | BM-A → TP1 | 0.8 | 5.0000 | 3.7655 | +1.2345 |
| 2 | TP1 → TP2 | 1.2 | 5.1000 | 5.5568 | -0.4568 |
| 3 | TP2 → TP3 | 0.6 | 4.9000 | 4.1108 | +0.7892 |
| 4 | TP3 → BM-A | 1.4 | 5.2000 | 6.7650 | -1.5650 |

The observed forward sum is +0.001900 m, so the computed closing elevation is 100.001900 m. The loop misclosure is +1.900 mm.

### Independent reverse run

| Section | From → To | Length (km) | Observed Δh (m) |
|---:|---|---:|---:|
| 1 | BM-A → TP3 | 1.4 | +1.5657 |
| 2 | TP3 → TP2 | 0.6 | -0.7895 |
| 3 | TP2 → TP1 | 1.2 | +0.4571 |
| 4 | TP1 → BM-A | 0.8 | -1.2350 |

The reverse run sum is -0.001700 m, or -1.700 mm. Combining the directional results gives +0.200 mm. This small directional discrepancy is a useful synthetic consistency check, but it does not establish that either run is free of systematic error.

## 5. Quality assessment before adjustment

The forward and reverse runs are independent observation series in this constructed dataset. Compare:
- the forward loop misclosure;
- the reverse loop misclosure;
- the sum of the two directed loop results;
- section-by-section differences after putting both runs into a common direction.

A real project must specify an applicable survey class, procedure and acceptance tolerance before observing. There is no universal allowable misclosure. Published criteria vary by survey class, equipment, procedure and distance. For example, NOAA's geodetic levelling manual applies class-specific tolerance factors multiplied by the square root of section length; the Hong Kong control-survey specification likewise lists different criteria for different vertical-control classes.

This exercise does **not** declare the synthetic loop compliant with any standard. It provides no forward/backward setup counts, sight-length balance, rod calibration, temperature/refraction observations, benchmark stability evidence or full field-book record. Do not use a generic rule such as a fixed number of millimetres per square root kilometre as a substitute for the governing project specification.

## 6. Stochastic model and weights

For the worked adjustment, assume independent section height-difference errors with standard uncertainties:

\[
u_i = 2.0\sqrt{L_i}\;\text{mm}
\]

where L_i is section length in kilometres. This is an illustrative model chosen to show distance-dependent uncertainty; it is not a claimed levelling specification or measured instrument performance.

The section variances are:

\[
q_i=u_i^2=4L_i\;\text{mm}^2
\]

and the weights are inversely proportional to variance:

\[
p_i=\frac{1}{q_i}\propto\frac{1}{L_i}
\]

Longer sections receive larger variance and therefore lower weight. The independence assumption is a simplification; real levelling errors may include correlated effects such as rod scale, collimation, refraction, temperature and common benchmark errors.

## 7. Weighted least-squares closure adjustment

Let c_i be the correction applied to observed section height difference i. The adjustment minimises:

\[
\min_{\mathbf{c}}\;\mathbf{c}^{T}\mathbf{Q}^{-1}\mathbf{c}
\]

subject to:

\[
\mathbf{1}^{T}(\Delta\mathbf{h}+\mathbf{c})=0
\]

For independent observations with covariance matrix Q, the solution is:

\[
c_i=-f\frac{q_i}{\sum_j q_j}
=-f\frac{L_i}{\sum_j L_j}
\]

The corrections are therefore proportional to section length under this specific variance model. This is not an arbitrary rule: it follows from the assumed stochastic model and closure constraint.

For this dataset:

| Section | Length (km) | Correction (mm) | Adjusted Δh (m) |
|---:|---:|---:|---:|
| 1 | 0.8 | -0.380 | +1.234120 |
| 2 | 1.2 | -0.570 | -0.457370 |
| 3 | 0.6 | -0.285 | +0.788915 |
| 4 | 1.4 | -0.665 | -1.565665 |
| **Total** | **4.0** | **-1.900** | **0.000000** |

The adjusted height differences now satisfy the loop condition exactly, subject to numerical rounding.

## 8. Adjusted elevations

Starting from the adopted BM-A elevation of 100.000000 m:

| Point | Cumulative adjusted height difference (m) | Adjusted elevation (m) |
|---|---:|---:|
| BM-A | 0.000000 | 100.000000 |
| TP1 | +1.234120 | 101.234120 |
| TP2 | +0.776750 | 100.776750 |
| TP3 | +1.565665 | 101.565665 |
| BM-A (closure) | 0.000000 | 100.000000 |

The last line is the constrained closing benchmark, not a second independent estimate of BM-A.

## 9. Covariance and uncertainty of adjusted elevations

The unconstrained section covariance matrix is diagonal under the assumed independence model:

\[
\mathbf{Q}=\operatorname{diag}(q_1,q_2,q_3,q_4)
\]

With the exact loop closure condition, the adjusted increment covariance is:

\[
\mathbf{Q}_{adj}
=\mathbf{Q}
-\frac{(\mathbf{Q}\mathbf{1})(\mathbf{Q}\mathbf{1})^T}
{\mathbf{1}^T\mathbf{Q}\mathbf{1}}
\]

This matrix is singular because the four adjusted increments must sum to zero. The covariance of the first three cumulative point elevations is obtained by applying the cumulative-sum design matrix A:

\[
\mathbf{C}_{H}=\mathbf{A}\mathbf{Q}_{adj}\mathbf{A}^{T}
\]

For this example, the standard uncertainties of the adjusted elevations relative to the fixed BM-A are:

| Point | Standard uncertainty (mm) |
|---|---:|
| TP1 | 1.600 |
| TP2 | 2.000 |
| TP3 | 1.908 |

These are conditional standard uncertainties under the synthetic section-variance model and exact-start-benchmark assumption. They do not include uncertainty of BM-A, turning-point instability, systematic corrections, datum realisation or other omitted effects. The covariance between adjusted point elevations is non-zero; the full covariance matrix is retained in the script output so downstream relative-height uncertainty can be computed correctly.

## 10. Independent check and interpretation

The reverse run provides an independent directional comparison:
- forward loop sum: +1.900 mm;
- reverse loop sum: -1.700 mm;
- combined directional discrepancy: +0.200 mm.

This check is distinct from the forward loop closure used in the adjustment. However, both runs share the same synthetic network definition and assumed stable marks. A real independent check should preserve separate raw records and document whether the route, setup, operator, equipment or observation conditions differ.

The adjusted forward loop closes by construction. That is an algebraic consequence of the constraint, not a validation result. Quality evidence comes from the unadjusted misclosures, independent observations, field procedure, model adequacy, reference quality and acceptance criteria.

## 11. Field procedure for a real levelling loop

A real field exercise should use the instrument manufacturer's procedure and the governing survey specification. At minimum:

1. Confirm the purpose, required height quality, datum and acceptance criteria.
2. Verify benchmark identity, stability, published elevation, datum and source.
3. Reconnoitre the route and choose stable turning points.
4. Check instrument and staff condition, calibration/verification status and accessories.
5. Balance backsight and foresight lengths as required by the chosen procedure.
6. Record every setup's BS, FS, point IDs, staff readings, distances, time, instrument, staff, operator and environmental notes.
7. Preserve raw readings and calculate section reductions independently.
8. Run the return observations as specified; retain forward and backward records separately.
9. Evaluate section and total misclosures against the predeclared criteria before adjustment.
10. Investigate suspected blunders, unstable marks, rod errors, refraction, collimation and procedural deviations.
11. Adjust only after the observations pass the chosen quality assessment.
12. Report adjusted elevations, covariance/uncertainty, constraints, corrections, checks, datum and limitations.

This document is not a substitute for a complete levelling standard, field manual, cadastral requirement or engineering survey specification.

## 12. What this exercise demonstrates — and does not

**Demonstrates:** reduction of aggregate BS/FS values; loop misclosure; a separate reverse-run comparison; a constrained weighted least-squares adjustment; distance-based weights derived from an explicit variance model; and covariance propagation to adjusted elevations.

**Does not demonstrate:** actual field observations, compliance with any survey class, instrument or staff calibration, absence of systematic error, datum accuracy, benchmark stability, or suitability for engineering construction or cadastral work.

## 13. Sources and further reading

- NOAA, *Geodetic Leveling, Manual NOS NGS 3* — forward/backward misclosure, class-specific tolerance and re-running procedures: https://www.ngs.noaa.gov/PUBS_LIB/Geodeticleveling_nos_3.pdf
- Intergovernmental Committee on Surveying and Mapping, *Guideline for Control Surveys by Differential Levelling, SP1* — distance-dependent error, forward/backward comparisons and control connections: https://icsm-prod.oxide.co/sites/default/files/2020-12/Guideline-for-Control-Surveys-by-Differential-Levelling_v2.2.pdf
- USACE, *EM 1110-2-1009: Structural Deformation Surveying* — least-squares adjustment, observation weights and uncertainty propagation: https://www.publications.usace.army.mil/portals/76/publications/engineermanuals/em_1110-2-1009.pdf
- R. E. Deakin, *Notes on Least Squares* — height-difference variance and weights inversely proportional to levelling distance: https://www.mygeodesy.id.au/documents/Notes%20on%20Least%20Squares%202005.pdf

## 14. Next experiment

Exercise C will extend the same logic from a single constrained loop to a small control network with multiple routes and redundant observations. The goal will be to solve for unknown point elevations using a general observation model, form the normal equations, inspect residuals and redundancy, and report the full covariance of the adjusted network.
