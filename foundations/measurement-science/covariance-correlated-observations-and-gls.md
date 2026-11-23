# Covariance, correlated observations and generalized least squares

**Version:** 0.1  
**Status:** Curated educational module; equations checked; examples refer to synthetic experiments  
**Primary subject:** SM-FND-011 — Measurement science, accuracy and uncertainty  
**Prerequisite:** [Standard uncertainty: Type A and Type B evaluation](standard-uncertainty-type-a-type-b.md)  
**Related experiments:** [Exercise D — stochastic control and correlated observations](../../experiments/measurement/exercise-d-stochastic-control-and-correlation.md); [Exercise K — correlated errors and generalized least-squares network adjustment](../../experiments/measurement/exercise-k-correlated-errors-and-generalized-least-squares.md)

## 1. Why covariance matters

A standard uncertainty describes the marginal spread assigned to one quantity. It does not, by itself, describe how that quantity varies with another.

Two observations can have the same individual standard uncertainties under two different stochastic models, yet carry different amounts of independent information because their errors may be related. Treating correlated observations as independent can therefore change an adjustment, its formal covariance and the interpretation of its uncertainty.

Covariance is not an optional refinement to add whenever a model looks sophisticated. It belongs in the stochastic model when the measurement process provides a defensible reason to expect shared or related errors.

## 2. Covariance and correlation

For two random quantities X and Y with finite second moments:

\[
\operatorname{cov}(X,Y)=E[(X-E[X])(Y-E[Y])]
\]

The covariance has the product of the units of X and Y. The correlation coefficient is the dimensionless standardised covariance:

\[
\rho_{XY}=\frac{\operatorname{cov}(X,Y)}{u(X)u(Y)}
\]

when both standard uncertainties are non-zero. It lies between -1 and +1.

- Positive covariance means deviations from the respective expectations tend to occur in the same direction.
- Negative covariance means deviations tend to occur in opposite directions.
- Zero covariance means no linear covariance, but does not in general prove statistical independence.
- Independence implies zero covariance when the relevant moments exist; the converse is not generally true.

The sign and effect of covariance depend on the quantities and the measurement model. Correlation is not automatically harmful, and a high correlation does not imply every derived uncertainty must increase.

## 3. Covariance matrices

For a vector of random quantities \(\mathbf{x}=[X_1,\ldots,X_n]^T\), the covariance matrix is:

\[
\mathbf{\Sigma}_{xx}
=E[(\mathbf{x}-E[\mathbf{x}])(\mathbf{x}-E[\mathbf{x}])^T]
\]

Its diagonal contains variances; its off-diagonal entries contain covariances. A valid covariance matrix is symmetric and positive semidefinite. It may be singular: exact linear relationships or shared components can produce zero-variance directions. Positive definiteness is a stronger condition, often needed for an ordinary matrix inverse, but is not a universal requirement for a covariance matrix to be valid.

For example, a simple session-common error model is:

\[
\mathbf{\Sigma}_{ll}=\mathbf{D}+\tau^2\mathbf{Z}\mathbf{Z}^T
\]

where:
- \(\mathbf{D}\) contains observation-specific variances;
- \(\mathbf{Z}\) identifies which observations share a session;
- \(\tau\) is the standard uncertainty of a common additive session effect.

Observations in the same session then share covariance \(\tau^2\), while observations in different sessions have no session-common covariance in this simplified model. The model does not say that all errors in a real session are identical; it isolates one assumed shared component.

## 4. Where shared errors arise

Potential shared-error mechanisms include:

- repeated readings without changing instrument and target centring;
- measurements made with the same instrument calibration or prism constant;
- observations sharing a GNSS session, antenna setup, correction stream or atmospheric conditions;
- levelling observations sharing a staff calibration, setup sequence or environmental condition;
- repeated remote-sensing measurements sharing geolocation, calibration or reference-data errors;
- field observations processed using the same uncertain correction or transformation parameters.

These are hypotheses to investigate, not automatic covariance assignments. A shared instrument or operator does not prove a particular numerical correlation. Record the physical mechanism, observation grouping, evidence and assumptions. Distinguish a common bias or correction uncertainty from random session-to-session variation, and avoid counting the same component twice.

## 5. Propagation with correlated inputs

For a first-order scalar measurement model \(y=f(\mathbf{x})\), let \(\mathbf{c}\) be the vector of sensitivity coefficients. Then:

\[
u_c^2(y)\approx\mathbf{c}^T\mathbf{\Sigma}_{xx}\mathbf{c}
\]

For two inputs this expands to:

\[
u_c^2(y)\approx
c_1^2u^2(x_1)+c_2^2u^2(x_2)
+2c_1c_2\operatorname{cov}(x_1,x_2)
\]

The covariance term can increase or decrease the result depending on its sign and on the sensitivity coefficients. The approximation is first-order; assess nonlinearity and the suitability of the model where those effects matter.

For a difference \(\Delta=X_2-X_1\):

\[
u^2(\Delta)=u^2(X_2)+u^2(X_1)-2\operatorname{cov}(X_1,X_2)
\]

A shared component can partly cancel in a difference. Conversely, a common error may remain important for absolute coordinates even when relative differences are stable. Always identify the actual quantity whose uncertainty is being reported.

## 6. Generalized least squares

Consider the linear observation model:

\[
\mathbf{l}=\mathbf{A}\mathbf{x}+\mathbf{e},
\qquad
\operatorname{Cov}(\mathbf{e})=\mathbf{\Sigma}_{ll}
\]

If the covariance matrix is known, nonsingular and correctly specified, and the design matrix has the required rank, generalized least squares (GLS) gives:

\[
\hat{\mathbf{x}}=
(\mathbf{A}^T\mathbf{\Sigma}_{ll}^{-1}\mathbf{A})^{-1}
\mathbf{A}^T\mathbf{\Sigma}_{ll}^{-1}\mathbf{l}
\]

with formal parameter covariance:

\[
\mathbf{C}_{\hat{x}}=
(\mathbf{A}^T\mathbf{\Sigma}_{ll}^{-1}\mathbf{A})^{-1}
\]

This expression assumes an unconstrained full-rank problem and the stated covariance model. Exact constraints, rank defects or singular covariance require an appropriate constrained formulation, factorisation or generalised-inverse treatment. Do not apply an ordinary inverse blindly.

If the covariance matrix is diagonal, GLS reduces to ordinary weighted least squares with independent observation errors. If off-diagonal terms are present, replacing the full matrix with its diagonal discards the modelled relationships. It is a different stochastic model, even if every observation retains the same marginal standard uncertainty.

For larger systems, use numerically stable matrix factorisations and sparse methods. Explicitly forming dense matrix inverses is generally not the preferred production implementation.

## 7. Follow the evidence from Exercises D and K

The repository's synthetic experiments make the distinction concrete:

- **Exercise D** compares a fixed datum, a stochastic control observation, and a stochastic control combined with two session groups sharing a common additive error. Its purpose is to show how assumptions about control and observation covariance affect the adjustment. The session model is deliberately simplified.
- **Exercise K** compares covariance-aware GLS with diagonal weighted least squares while preserving the same marginal standard uncertainties. It simulates 5,000 trials under the specified session-common model. For that particular network and modest assumed session effect, numerical differences are small and empirical coverage remains near the nominal level for both approaches.

The Exercise K result is not evidence that correlation can safely be ignored. It demonstrates that the numerical impact depends on geometry, grouping and covariance magnitude, and that a misspecified model can look plausible in one limited experiment. The simulation uses known synthetic covariance parameters, only two session groups and a fixed linear network; it does not establish performance for real surveys or other designs.

## 8. A practical modelling workflow

Before selecting a diagonal or full covariance model:

1. Define the measurands and observation equations.
2. Map each observation to its instrument, setup, operator, session, calibration, correction and processing lineage.
3. Identify plausible shared-error mechanisms and distinguish common effects from observation-specific noise.
4. Decide which components are random variables, corrections, constraints or unknown biases.
5. Build the covariance matrix from the documented model; check units, symmetry, diagonal variances and positive semidefiniteness.
6. Check whether the matrix is singular or ill-conditioned before selecting a numerical solution.
7. Compare a defensible alternative model where the data support it; do not choose a covariance structure only because it produces smaller residuals.
8. Preserve independent check observations or repeat sessions for validation.
9. Report the covariance assumptions, estimated or assumed parameters, limitations and sensitivity of the result to plausible alternatives.

A useful question is: *what changed between these observations that would make their errors independent?* If the answer is unclear, independence is an assumption to examine, not a fact to silently inherit.

## 9. Application across spatial methods

- **Surveying and levelling:** common instrument, staff, setup, calibration, refraction and session effects.
- **GNSS:** session-level effects, antenna setup, correction services, shared satellite/environmental conditions and reference-frame parameters.
- **Remote sensing:** shared calibration, geolocation, atmospheric correction and reference-data uncertainty across pixels or scenes.
- **Mobile mapping and LiDAR:** trajectory, boresight, timing, strip adjustment and shared platform calibration.
- **Field inventories:** repeated measurements by the same team or device, shared feature interpretation and common positional reference.

The structure differs by technology. A levelling session random effect should not simply be copied into a GNSS or remote-sensing model. Derive the stochastic model from the actual acquisition and processing chain.

## 10. Common mistakes

- Assuming repeated observations are independent merely because they are separate rows.
- Treating zero covariance as proof of independence.
- Assuming a valid covariance matrix must be positive definite rather than positive semidefinite.
- Assigning correlations from intuition without a physical, empirical or statistical basis.
- Replacing a full covariance matrix with its diagonal without acknowledging the changed model.
- Assuming correlation always increases uncertainty.
- Confusing shared systematic corrections with random common-mode effects.
- Using a singular covariance matrix in an ordinary inverse without addressing its structure.
- Treating a good internal fit as independent validation.

## 11. Sources and limitations

The uncertainty propagation treatment is grounded in the covariance terms of the legacy GUM core, read in the context of the broader current GUM suite. The GLS equations and session-effect model are presented as standard linear-model derivations and are illustrated by the repository's own synthetic Exercises D and K.

Sources:
- BIPM/JCGM, [JCGM 100:2008 — Guide to the expression of uncertainty in measurement](https://www.bipm.org/en/doi/10.59161/jcgm100-2008), especially Sections 5.1–5.2. This is the legacy GUM core, not the complete current GUM suite.
- NIST, [Technical Note 1297 — Appendix A: Law of propagation of uncertainty](https://www.nist.gov/pml/nist-technical-note-1297/nist-tn-1297-appendix-law-propagation-uncertainty). NIST guidance adapted to its institutional policy; not a surveying standard or Kenyan legal requirement.
- [Exercise D](../../experiments/measurement/exercise-d-stochastic-control-and-correlation.md) and [Exercise K](../../experiments/measurement/exercise-k-correlated-errors-and-generalized-least-squares.md), both synthetic and limited to their stated assumptions.

The module is an educational introduction, not a universal stochastic model or field specification. Covariance magnitudes must be supported by measurement design, calibration information, repeated sessions or a defensible physical/statistical model. Independent technical review remains outstanding.
