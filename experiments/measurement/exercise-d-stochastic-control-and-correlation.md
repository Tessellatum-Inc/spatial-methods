# Exercise D — stochastic control and correlated observations

**Version:** 0.1  
**Status:** Reproducible synthetic worked experiment; not field evidence  
**Prerequisite:** [Exercise C — weighted least-squares adjustment of a vertical control network](exercise-c-weighted-control-network.md)  
**Dataset:** [Synthetic observations and session groups](../../data/measurement/exercise-d-stochastic-control-network.csv)  
**Analysis:** [Reproducible Python implementation](../../scripts/measurement/analyze_exercise_d.py)

## 1. Purpose

Exercise C held benchmark A fixed and assumed independent height-difference observations. Exercise D relaxes both assumptions. We compare three models using the same nine synthetic height differences:

1. A fixed datum at A = 100.000 m, with independent observations.
2. A stochastic control observation for A, with independent height-difference observations.
3. The same stochastic control, but with correlated height-difference observations grouped into two synthetic sessions.

This is a controlled model-comparison experiment. All values, uncertainties and correlation assumptions are synthetic. No field observations were made.

## 2. Network and observation model

The network geometry and nine directed height differences are carried forward from Exercise C. The point set is A, B, C, D and E. For an observation from i to j:

\[
l_{ij}=H_j-H_i+e_{ij}
\]

In matrix form:

\[
\mathbf{l}=\mathbf{A}\mathbf{x}+\mathbf{e}
\]

The sign convention remains positive when the destination is higher than the origin.

## 3. Model A — exact fixed control

The first solution fixes:

\[
H_A=100.000000\;\mathrm{m}
\]

The unknown vector is \([H_B,H_C,H_D,H_E]^T\). This reproduces the datum treatment in Exercise C. It is useful for a controlled comparison, but it assumes that the adopted control value has no uncertainty. Any actual error in A is transferred to all adjusted elevations and is not represented in their formal covariance.

## 4. Model B — stochastic control

Instead of fixing A, include it as an unknown and add a control observation:

\[
l_A=100.001\;\mathrm{m}
\]

with assumed standard uncertainty:

\[
\sigma_A=2.0\;\mathrm{mm}
\]

This is a weighted observation of control, not an exact constraint. The augmented unknown vector is:

\[
\mathbf{x}=[H_A,H_B,H_C,H_D,H_E]^T
\]

The control observation contributes one additional row to the design matrix. Its variance is included in the observation covariance matrix. Because the network height differences alone cannot determine the absolute vertical datum, this stochastic control observation supplies datum information without pretending it is error-free.

The chosen control value and uncertainty are invented for this exercise. They do not describe a Kenyan benchmark, KENREF point, published height or survey control specification.

## 5. Model C — correlated height-difference observations

The nine height differences are divided into two illustrative session groups, S1 and S2. Each observation retains its own independent standard uncertainty:

\[
\sigma_i=1.5\sqrt{L_i}\;\mathrm{mm}
\]

where L is line length in kilometres. A synthetic common additive session effect with standard uncertainty:

\[
\tau=0.35\;\mathrm{mm}
\]

is also shared by observations assigned to the same session.

The observation covariance matrix is therefore:

\[
\mathbf{Q}_{ll}=\mathbf{D}+\tau^2\mathbf{Z}\mathbf{Z}^T
\]

where D is the diagonal matrix of individual observation variances and Z is the session-membership design matrix. This construction makes observations within a session correlated while leaving different sessions uncorrelated in this simplified model.

This is an intentionally transparent teaching model of shared error. It is not asserted to be a complete physical model of levelling-session errors. Real covariance structures must be derived from how observations were acquired, reduced and processed. Shared instrument setups, staff calibration, environmental conditions, common corrections and processing can create more complicated patterns.

## 6. Generalized least-squares solution

For the observation model with full covariance matrix Q:

\[
\mathbf{P}=\mathbf{Q}_{ll}^{-1}
\]

\[
\hat{\mathbf{x}}=
(\mathbf{A}^T\mathbf{P}\mathbf{A})^{-1}
\mathbf{A}^T\mathbf{P}\mathbf{l}
\]

and the formal parameter covariance is:

\[
\mathbf{C}_{\hat{x}}=
(\mathbf{A}^T\mathbf{P}\mathbf{A})^{-1}
\]

The off-diagonal elements of Q are retained. Replacing Q by its diagonal would discard the session covariance and solve a different stochastic model.

The implementation uses standard-library matrix routines and pivoted Gauss-Jordan elimination. It explicitly constructs Q, inverts it for this small teaching example, forms the normal matrix and solves the generalized least-squares system. For large production networks, use numerically stable factorization methods and specialist adjustment software rather than explicitly forming dense inverses.

## 7. Comparing the three solutions

Run from the repository root:

~~~bash
python scripts/measurement/analyze_exercise_d.py
~~~

The script prints adjusted elevations, formal standard uncertainties, residuals, covariance matrices and degrees of freedom for all three models. With the committed dataset and stated assumptions, the reference results are:

| Point | Model A elevation (m) | Model B elevation (m) | Model C elevation (m) |
|---|---:|---:|---:|
| A | Fixed at 100.000000 | 100.001000 | 100.001000 |
| B | 101.200857 | 101.201857 | 101.201873 |
| C | 102.000466 | 102.001466 | 102.001474 |
| D | 101.700976 | 101.701976 | 101.701979 |
| E | 102.401048 | 102.402048 | 102.402051 |

Formal standard uncertainties (mm):

| Point | Model A | Model B | Model C |
|---|---:|---:|---:|
| A | Fixed | 2.000 | 2.000 |
| B | 1.057 | 2.262 | 2.267 |
| C | 1.036 | 2.253 | 2.261 |
| D | 1.018 | 2.244 | 2.245 |
| E | 1.199 | 2.332 | 2.333 |

The correlated model has a slightly different solution and covariance because its session-common error terms change the information structure. The numerical effect is modest for this deliberately small synthetic example; it should not be exaggerated. All three models have five degrees of freedom. Their weighted residual sums are conditional on their respective covariance assumptions and should not be compared as though they were ordinary unweighted sums of squared residuals.

The expected qualitative differences are:

- Model A reports uncertainty conditional on an exact datum; A has no estimated uncertainty.
- Model B propagates the 2 mm control uncertainty into the absolute elevations.
- Model C retains the same stochastic control but also accounts for the specified session-level covariance. Its relative estimates and covariance can differ from Model B.

Because the height-difference network is invariant to a common vertical translation, the uncertain control primarily determines the absolute datum level. Relative height differences are principally informed by the network observations. Correlation affects the effective information content of the observations and therefore can alter relative estimates and their uncertainties.

The posterior variance factor is a diagnostic conditional on the declared covariance model. It should not be used to rescale uncertainties automatically without an appropriate statistical rationale and testing procedure.

## 8. Interpreting covariance

The covariance matrix is not merely a list of individual point uncertainties. Its off-diagonal terms describe how adjusted elevations vary together.

For a relative height:

\[
\Delta H_{ij}=H_j-H_i
\]

\[
u^2(\Delta H_{ij})=
C_{ii}+C_{jj}-2C_{ij}
\]

A shared datum uncertainty may increase the uncertainty of absolute elevations while largely cancelling in relative height differences. Conversely, correlated observation errors can affect relative uncertainty because they change how much independent information the network actually contains.

Do not infer that a higher correlation always increases every reported standard uncertainty by the same amount. The effect depends on network geometry, covariance structure and the quantity being estimated.

## 9. Important distinctions

- **Fixed control:** a mathematical constraint; not a claim that a benchmark is physically perfect.
- **Stochastic control:** prior control information represented with finite uncertainty.
- **Correlated observations:** observations whose random errors are not statistically independent.
- **Formal covariance:** uncertainty implied by the specified mathematical and stochastic models.
- **External validation:** comparison against genuinely independent control or check observations, not merely a good internal fit.

The three adjustments are not competing ways to make residuals look smaller. They represent different assumptions about what is known and how the observations behave.

## 10. Limitations

The exercise assumes a linear height-difference model, one stochastic control observation, independent control and levelling-session errors, two session groups, a single common-mode standard uncertainty and known individual observation variances. It does not model uncertain multiple benchmarks, correlated control, variance-component estimation, time-dependent benchmark movement, setup-level observations or a complete global/local statistical testing procedure.

A real project should derive stochastic relationships from the observation process and source records. It should preserve independent check observations and test the compatibility of control before final constrained adjustment. Never manufacture covariance values merely to make a model appear sophisticated.

## 11. Sources and further reading

- Intergovernmental Committee on Surveying and Mapping, [Guideline for the Adjustment and Evaluation of Survey Control (SP1)](https://icsm-prod.oxide.co/sites/default/files/2018-02/Guideline-for-Adjustment-and-Evaluation-of-Survey-Control_v2.1.pdf). Discusses minimally constrained and fully constrained adjustment, measurement uncertainty, redundancy and testing.
- RICS, [Use of GNSS in land surveying and mapping](https://www.rics.org/content/dam/ricsglobal/documents/standards/Use%20of%20GNSS%20in%20land%20surveying%20and%20mapping_3rd%20edition.pdf), sections on network adjustment, covariance information, weighting and statistical testing.
- Dru Smith, Jacob Heck, Dan Gillins and Kyle Snow, NOAA, [On Least-Squares Adjustments within the Variance Component Model with Stochastic Constraints](https://doi.org/10.25923/dp2q-yp06), NOAA Technical Memorandum NOS NGS 74 (2018).
- U.S. Army Corps of Engineers, [EM 1110-2-1009: Structural Deformation Surveying](https://www.publications.usace.army.mil/Portals/76/Publications/EngineerManuals/EM_1110-2-1009.pdf), Chapter 9.

These sources inform the adjustment concepts. The dataset, numerical control prior and session-correlation model are synthetic teaching material, not copied specifications or real control data.
