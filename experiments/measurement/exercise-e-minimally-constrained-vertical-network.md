# Exercise E — minimally constrained vertical networks and datum defects

**Version:** 0.1  
**Status:** Reproducible synthetic worked experiment; not field evidence  
**Prerequisite:** [Exercise C — weighted least-squares adjustment of a vertical control network](exercise-c-weighted-control-network.md) and [Exercise D — stochastic control and correlated observations](exercise-d-stochastic-control-and-correlation.md)  
**Dataset:** Reuses [Exercise C's synthetic observation network](../../data/measurement/exercise-c-synthetic-control-network.csv)  
**Analysis:** [Reproducible Python implementation](../../scripts/measurement/analyze_exercise_e.py)

## 1. Purpose

Exercises C and D introduced a fixed datum and a stochastic control observation. Exercise E asks a more basic question: what can the height-difference observations determine before any external vertical datum is attached?

A connected network of height differences determines relative heights. It does not determine the common absolute height offset. If every station height is increased by the same constant, every observed height difference remains unchanged. The normal matrix therefore has one datum defect.

This exercise demonstrates:

1. the rank deficiency of a free vertical network;
2. a minimally constrained / inner-constrained solution;
3. the distinction between relative and absolute height;
4. a common vertical translation onto an external control value;
5. the effect of finite external-control uncertainty on absolute and relative quantities.

All observations and control values are synthetic. No field survey was performed.

## 2. Observation model and datum defect

For an observation from point i to point j:

\[
l_{ij}=H_j-H_i+e_{ij}
\]

For the five-point network A, B, C, D and E, the unknown vector is:

\[
\mathbf{x}=[H_A,H_B,H_C,H_D,H_E]^T
\]

The nine observations are reused unchanged from Exercise C. The design matrix has one row per directed height difference, with -1 at the origin and +1 at the destination.

If \(\mathbf{1}\) is a vector of five ones, then:

\[
\mathbf{A}\mathbf{1}=\mathbf{0}
\]

Therefore, if \(\hat{\mathbf{x}}\) is a solution, so is:

\[
\hat{\mathbf{x}}+c\mathbf{1}
\]

for any constant c. The observations cannot distinguish these solutions. For this connected height network, the design matrix rank is 4 rather than 5, and the normal matrix \(\mathbf{N}=\mathbf{A}^T\mathbf{P}\mathbf{A}\) is singular with one vertical-translation datum defect.

This is not a lack of observations or a numerical bug. It is a property of the measurement model. A disconnected network would introduce additional defects.

## 3. Inner constraint: selecting a free-network origin

To obtain a unique numerical representative without importing an external benchmark height, impose the inner constraint:

\[
\sum_{i=1}^{5}H_i=0
\]

This sets the arithmetic mean of the five adjusted heights to zero. It is a coordinate convention, not a physical statement that the average elevation is zero and not an external datum observation.

The constrained least-squares system is solved using Lagrange multipliers:

\[
\begin{bmatrix}
\mathbf{N}&\mathbf{C}^T\\
\mathbf{C}&\mathbf{0}
\end{bmatrix}
\begin{bmatrix}
\hat{\mathbf{x}}\\
\boldsymbol{\lambda}
\end{bmatrix}
=
\begin{bmatrix}
\mathbf{A}^T\mathbf{P}\mathbf{l}\\
\mathbf{0}
\end{bmatrix}
\]

where \(\mathbf{C}=[1,1,1,1,1]\). The constraint removes the single translation defect.

The script first attempts to solve the unconstrained normal system and confirms that it is singular, then solves the augmented constrained system.

## 4. Stochastic model

The nine observations and their assumed standard uncertainties are exactly those in Exercise C. The same diagonal observation covariance is retained:

\[
\mathbf{Q}_{ll}=\operatorname{diag}(\sigma_1^2,\ldots,\sigma_9^2)
\]

with:

\[
\sigma_i=1.5\sqrt{L_i}\;\mathrm{mm}
\]

where line length L is in kilometres. These are synthetic teaching assumptions, not equipment specifications or a survey standard. Observation independence is retained only to isolate the datum issue; Exercise D demonstrates a simple correlated-observation model.

There are nine observations, five unknown heights and one datum defect. The effective parameter count is four, giving:

\[
r=n-\operatorname{rank}(\mathbf{A})=9-4=5
\]

degrees of freedom for residual diagnostics.

## 5. Free-network solution

Run from the repository root:

~~~bash
python scripts/measurement/analyze_exercise_e.py
~~~

Expected free-network heights, rounded to the micrometre:

| Point | Inner-constrained height (m) |
|---|---:|
| A | -1.460669 |
| B | -0.259813 |
| C | +0.539797 |
| D | +0.240307 |
| E | +0.940378 |

Their arithmetic mean is zero by construction. These are not elevations in a recognised national or local vertical datum.

The observation residuals are the same as in Exercise C because adding a common constant to every point does not change any height difference. The inner constraint changes the parameter origin, not the network fit.

## 6. Covariance and datum dependence

The augmented constrained system yields a covariance matrix for the chosen inner-constrained parameterisation. The script reports it in square millimetres.

Important: the covariance of the individual free-network heights depends on the chosen datum convention. The sum-to-zero constraint induces correlations between the estimated heights. Do not interpret the diagonal elements as absolute-height uncertainty in a real vertical datum.

Relative heights are datum-invariant. For points p and q:

\[
\Delta H_{pq}=H_q-H_p
\]

and:

\[
u^2(\Delta H_{pq})=C_{pp}+C_{qq}-2C_{pq}
\]

The script reports selected relative-height standard uncertainties for B–C, B–D and C–E. These remain unchanged by a common vertical translation.

## 7. Transforming onto an external vertical datum

For demonstration, introduce one external control value:

\[
H_A^{\mathrm{control}}=100.001\;\mathrm{m}
\]

with assumed standard uncertainty:

\[
u_A=2.0\;\mathrm{mm}
\]

The control value and uncertainty are invented. They do not represent a Kenyan benchmark, KENREF realisation, published height or actual survey control.

With one vertical control value, the transformation is a common translation:

\[
t=H_A^{\mathrm{control}}-\hat{H}_A^{\mathrm{free}}
\]

\[
H_i^{\mathrm{transformed}}=\hat{H}_i^{\mathrm{free}}+t
\]

This produces:

| Point | Transformed height (m) |
|---|---:|
| A | 100.001000 |
| B | 101.201857 |
| C | 102.001466 |
| D | 101.701976 |
| E | 102.402048 |

This is a datum transfer demonstration, not a multi-control transformation or a control-network validation. One control point determines the vertical offset but cannot reveal a discrepancy at that same point. Independent check control is still required.

## 8. Propagating external-control uncertainty

For this simplified model, assume the external control error is independent of the network observation errors. Its uncertain vertical offset is common to all transformed heights. The illustrative transformed covariance is:

\[
\mathbf{C}_{\mathrm{transformed}}
=
\mathbf{C}_{\mathrm{inner}}
+
u_A^2\mathbf{1}\mathbf{1}^T
\]

The common-mode term increases the uncertainty of absolute heights. It cancels in relative-height differences:

\[
u^2[(H_j+t)-(H_i+t)]=u^2(H_j-H_i)
\]

Thus, an uncertain datum can make every absolute elevation less certain without changing the network's relative-height information. This statement assumes the external control uncertainty is independent of the network and that the transformation is a pure vertical translation.

## 9. What this teaches

- Height-difference observations alone do not establish an absolute vertical datum.
- A datum defect is a rank deficiency in the observation model, not an error in the measurements.
- An inner constraint selects a convenient mathematical origin; it does not create external geodetic control.
- Relative height estimates are invariant to a common vertical translation.
- External control attaches the free network to a datum and imports the control's uncertainty.
- A single control point can transfer an offset but cannot independently test the network against that control.
- Multiple controls may reveal inconsistencies, but their compatibility, stability, realisation, epoch and covariance must be evaluated before they are imposed.

## 10. Limitations

This exercise assumes a connected, linear height-difference network, independent observations, known a-priori standard uncertainties and one translation datum defect. It does not model uncertain multiple controls, correlated control, vertical datum distortions, time-dependent benchmark motion, variance-component estimation or a full statistical testing workflow.

The inner-constrained covariance is tied to the chosen sum-to-zero gauge. For more general geodetic networks, datum defects may include translations, rotations and scale, depending on the observation types. Do not carry the single-translation result over to horizontal or three-dimensional networks without deriving their nullspaces.

## 11. Sources and further reading

- Intergovernmental Committee on Surveying and Mapping, [Guideline for the Adjustment and Evaluation of Survey Control (SP1), Version 2.2](https://www.icsm.gov.au/sites/default/files/2020-12/Guideline-for-Adjustment-and-Evaluation-of-Survey-Control_v2.2.pdf). Recommends minimally constrained testing before fully constrained datum propagation in control-survey workflows.
- R. E. Deakin, [Inner Constraints for 3-D Survey Networks](https://www.mygeodesy.id.au/documents/Inner%20Constraints.pdf). Explains rank deficiency, datum defects and Lagrange-multiplier inner constraints.
- John O. Ogundare, [Datum Problem and Free Network Adjustment](https://doi.org/10.1002/9781119501459.ch14), in *Understanding Least Squares Estimation and Geomatics Data Analysis* (2018). Discusses free-network adjustment, inner constraints and transformations between datums.
- [Free network adjustment: Minimum inner constraints and Pseudo-inverse approaches](https://revistas.udistrital.edu.co/index.php/UDGeo/article/view/16309). Reviews free adjustment and datum transformation.

The mathematical concepts are based on these references; the network observations, uncertainty assumptions and control value are synthetic teaching material.
