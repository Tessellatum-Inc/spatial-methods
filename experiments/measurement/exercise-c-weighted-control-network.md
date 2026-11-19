# Exercise C — weighted least-squares adjustment of a small vertical control network

**Version:** 0.1  
**Status:** Reproducible synthetic worked experiment; not field evidence  
**Primary subjects:** SM-FND-002, SM-FND-004, SM-FND-011  
**Connected subjects:** SM-COL-001, SM-COL-003, SM-ALG-018, SM-REC-008  
**Dataset:** [Synthetic control-network observations](../../data/measurement/exercise-c-synthetic-control-network.csv)  
**Analysis:** [Reproducible Python analysis](../../scripts/measurement/analyze_exercise_c.py)  
**Prerequisites:** [Exercise A](exercise-a-repeated-distance-and-angle.md), [Exercise B](exercise-b-differential-levelling-loop.md), [Measurement principles and field verification](../../foundations/measurement-science/measurement-principles-and-field-verification.md)

## 1. Purpose

Exercise C extends a single closed levelling loop into a connected network with multiple routes and redundant height-difference observations. It demonstrates observation equations, design matrices, datum constraints, weighting, normal equations, adjusted elevations, residuals, redundancy, parameter covariance and relative-height uncertainty.

All observations are synthetic. No instrument was operated and no benchmark was occupied.

## 2. Network design

One datum point A is fixed; B, C, D and E are unknown. Nine directed height differences connect the points:

- A → B, B → C, C → A
- B → D, D → A, C → D
- D → E, E → A, C → E

This gives several overlapping routes and closed circuits.

<pre>
                 B -------- C
                / \        / \
               /   \      /   \
              A ---- D -------- E
               \________________/
</pre>

The sketch is conceptual; the CSV defines the observations. There are 9 observations and 4 unknown elevations, so nominal redundancy is:

\[
r=n-u=9-4=5
\]

A fixed datum removes the vertical datum defect. Connectivity is also essential: a disconnected point or component would leave the normal matrix singular even if the observation count appeared sufficient.

## 3. Datum and sign convention

Adopt:

\[
H_A=100.000000\;\text{m}
\]

For an observation directed from i to j:

\[
l_{ij}=H_j-H_i+e_{ij}
\]

Positive height difference means the destination is higher than the origin. A is treated as exact solely to keep this first network example focused. A real network must account for benchmark provenance, stability, datum realisation and uncertainty. Uncertain control should be introduced through a suitable stochastic constraint or a more complete adjustment model, not silently held exact.

## 4. Synthetic observation set

| ID | From → to | Length (km) | Observed Δh (m) | Assumed σ (mm) |
|---|---|---:|---:|---:|
| AB | A → B | 1.0 | +1.2012 | 1.500 |
| BC | B → C | 1.4 | +0.7989 | 1.775 |
| CA | C → A | 1.1 | -2.0006 | 1.573 |
| BD | B → D | 0.8 | +0.5008 | 1.342 |
| DA | D → A | 1.3 | -1.7005 | 1.710 |
| CD | C → D | 1.0 | -0.2997 | 1.500 |
| DE | D → E | 1.2 | +0.7004 | 1.643 |
| EA | E → A | 1.5 | -2.4009 | 1.837 |
| CE | C → E | 1.6 | +0.4003 | 1.897 |

Assumed standard uncertainties follow:

\[
\sigma_i=1.5\sqrt{L_i}\;\text{mm}
\]

where L is in kilometres. This is an illustrative synthetic model, not a levelling specification, equipment claim or measured field precision. Observations are assumed independent, so the observation covariance is diagonal. Real networks can contain correlated errors from shared setups, rods, operators, instruments, environmental conditions or common control.

## 5. Observation equations and design matrix

Unknown parameter vector:

\[
\mathbf{x}=[H_B,H_C,H_D,H_E]^T
\]

For each directed observation i → j, create a row with -1 in the origin column and +1 in the destination column. Omit the fixed A column and move its known contribution to the right-hand side.

The model is:

\[
\mathbf{l}=\mathbf{A}\mathbf{x}+\boldsymbol{e}
\]

For example:

\[
l_{AB}=H_B-H_A+e_{AB}
\]

and, because A is fixed:

\[
l_{AB}+H_A=H_B+e_{AB}
\]

For B → C:

\[
l_{BC}=H_C-H_B+e_{BC}
\]

The script constructs the design matrix from point IDs in the CSV. The full matrix has nine rows and four columns; its rank must be four for all unknown elevations to be estimable under the fixed datum.

## 6. Weighted least squares

For independent observations with standard uncertainties σᵢ:

\[
\mathbf{P}=\mathbf{Q}_{ll}^{-1}
=\operatorname{diag}(1/\sigma_i^2)
\]

The normal equations are:

\[
\mathbf{N}=\mathbf{A}^T\mathbf{P}\mathbf{A},
\qquad
\mathbf{u}=\mathbf{A}^T\mathbf{P}\mathbf{l}
\]

\[
\hat{\mathbf{x}}=\mathbf{N}^{-1}\mathbf{u}
\]

The implementation solves the linear system rather than explicitly inverting the normal matrix to obtain the estimates. It separately computes the inverse normal matrix for formal parameter covariance.

Residual convention:

\[
\mathbf{v}=\mathbf{A}\hat{\mathbf{x}}-\mathbf{l}
\]

A positive residual means the adjusted computed height difference is greater than the observation.

## 7. Adjusted elevations

The reproducible script gives (rounded):

| Point | Adjusted elevation (m) |
|---|---:|
| A | 100.000000 (fixed) |
| B | 101.200857 |
| C | 102.000466 |
| D | 101.700976 |
| E | 102.401048 |

These are estimates under the declared synthetic model, not real-world elevations.

## 8. Residuals and redundancy

There are five degrees of freedom. Approximate residuals are:

| Observation | Residual (mm) |
|---|---:|
| AB | -0.343 |
| BC | +0.710 |
| CA | +0.134 |
| BD | -0.680 |
| DA | -0.476 |
| CD | +0.210 |
| DE | -0.329 |
| EA | -0.148 |
| CE | +0.281 |

The script also reports normalized residuals using the diagonal of the residual covariance:

\[
\mathbf{Q}_{vv}=\mathbf{Q}_{ll}
-\mathbf{A}(\mathbf{A}^T\mathbf{P}\mathbf{A})^{-1}\mathbf{A}^T
\]

Residuals are not independent because the adjustment imposes network relationships. Normalized residuals are diagnostic quantities under the assumed model, not automatic proof of a blunder or proof that no blunder exists. A proper outlier investigation requires an appropriate statistical test, predeclared decision rules, adequate redundancy and examination of raw field evidence. Do not delete an observation merely because doing so improves a statistic.

The posterior variance factor is:

\[
\hat{\sigma}_0^2=\frac{\mathbf{v}^T\mathbf{P}\mathbf{v}}{r}
\]

It is a model diagnostic. Because the a-priori standard uncertainties are invented for teaching, the resulting variance factor is not a field instrument performance assessment or compliance result.

## 9. Parameter covariance and relative-height uncertainty

Under the stated a-priori observation covariance:

\[
\mathbf{C}_{\hat{x}}=(\mathbf{A}^T\mathbf{P}\mathbf{A})^{-1}
\]

The diagonal elements give formal variances of adjusted unknown elevations; off-diagonal elements represent covariance. For relative height between p and q:

\[
\Delta H_{pq}=H_q-H_p
\]

\[
u^2(\Delta H_{pq})=
C_{pp}+C_{qq}-2C_{pq}
\]

The covariance term matters. Treating point elevations as independent would generally misstate the uncertainty of their difference. The script reports the full covariance matrix in mm² and formal relative-height uncertainty for B–C, B–D and C–E.

These results remain conditional on the fixed A datum and synthetic stochastic model. Posterior-scaled point uncertainties are also reported as a diagnostic, not as a replacement for a defensible a-priori error model.

## 10. What redundancy does—and does not—give us

Redundancy permits the network to distribute inconsistencies and provides residual information unavailable in a minimally determined network. Multiple paths allow different routes between points to be compared.

However:
- A network can be internally consistent and still be wrong.
- Common systematic errors may affect many observations similarly and remain difficult to detect internally.
- An erroneous fixed datum transfers its error into every adjusted elevation.
- Incorrect weights distort residual distribution and reported covariance.
- A small residual is not independent validation.
- More observations do not automatically improve a network if they repeat the same weakness or share correlated errors.

A real project should preserve independent check observations, raw field books, instrument and staff records, benchmark descriptions, calibration/verification evidence and applicable acceptance criteria.

## 11. Reproducibility

Run from the repository root:

~~~bash
python scripts/measurement/analyze_exercise_c.py
~~~

The implementation uses only the Python standard library. It reads the CSV, constructs the design matrix, forms and solves the normal equations with pivoted Gauss-Jordan elimination, computes residuals and covariance, and reports adjusted elevations and selected relative-height uncertainties.

## 12. Limitations and next practical step

This is a compact educational network, not a field procedure or survey deliverable. It assumes one exact fixed benchmark, independent observations, a diagonal observation covariance matrix, correctly identified and stable points, a linear height-difference model and known a-priori standard uncertainties.

It does not model uncertain control, correlated observations, multiple variance groups, instrument systematics, refraction, rod scale, setup-level observations or a complete gross-error testing workflow.

The next practical progression is to design and observe a real small levelling network (with appropriate supervision, equipment and permissions), retain setup-level records, include independent check ties and compare field results against a preselected specification. Only then extend to uncertain control constraints, correlated observations and formal outlier testing.

## 13. Sources and further reading

- NOAA, *Geodetic Leveling, Manual NOS NGS 3*: https://www.ngs.noaa.gov/PUBS_LIB/Geodeticleveling_nos_3.pdf
- U.S. Army Corps of Engineers, *EM 1110-2-1009: Structural Deformation Surveying*, Chapter 9, network adjustment, observation weighting and uncertainty propagation: https://www.publications.usace.army.mil/Portals/76/Publications/EngineerManuals/EM_1110-2-1009.pdf
- Zilkoski et al., NOAA discussion of least-squares adjustment of differential levelling networks and degrees of freedom: https://www.ngs.noaa.gov/wp-content/uploads/2018/06/Zilkoski1991-2.pdf

These references inform the mathematical framing; the observations and uncertainty model here are original synthetic teaching assumptions, not copied survey specifications.
