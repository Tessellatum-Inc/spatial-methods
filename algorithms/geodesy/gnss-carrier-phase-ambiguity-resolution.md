# GNSS carrier-phase integer ambiguity resolution

**Status:** Algorithm specification linked to an educational implementation; not a complete GNSS processing engine.

## 1. Problem definition

Carrier-phase GNSS observations are precise range-like measurements, but their initial phase contains an unknown integer number of wavelengths. After a float estimation stage has estimated the real-valued ambiguity vector and its covariance, integer ambiguity resolution seeks the most plausible integer vector under that stochastic model.

Let the float ambiguity estimate be \(\hat{\mathbf{a}}\in\mathbb{R}^{n}\), with positive-definite covariance matrix \(\mathbf{Q}_{\hat a}\). The integer least-squares (ILS) problem is:

\[
\check{\mathbf{a}}
=
\underset{\mathbf{a}\in\mathbb{Z}^{n}}{\operatorname{arg\,min}}
\left(
\mathbf{a}-\hat{\mathbf{a}}
\right)^{T}
\mathbf{Q}_{\hat a}^{-1}
\left(
\mathbf{a}-\hat{\mathbf{a}}
\right)
\]

The solution is the integer lattice point with the smallest squared Mahalanobis distance from the float estimate. This is not equivalent to independently rounding each ambiguity to its nearest integer: the covariance describes correlated uncertainty and changes the joint optimum.

## 2. Why decorrelation is useful

When ambiguities are strongly correlated, direct search in the original coordinate system can be inefficient. LAMBDA (Least-squares AMBiguity Decorrelation Adjustment) applies an integer unimodular transformation to obtain a better-conditioned search problem.

For an integer transformation matrix \(\mathbf{Z}\) with determinant \(+1\) or \(-1\), define:

\[
\mathbf{z}=\mathbf{Z}^{T}\mathbf{a},\qquad
\hat{\mathbf{z}}=\mathbf{Z}^{T}\hat{\mathbf{a}},\qquad
\mathbf{Q}_{\hat z}=\mathbf{Z}^{T}\mathbf{Q}_{\hat a}\mathbf{Z}
\]

The transformation is invertible over the integers, so integer candidates in the transformed domain map one-to-one to integer candidates in the original domain. After searching for \(\check{\mathbf{z}}\), recover:

\[
\check{\mathbf{a}}=\mathbf{Z}^{-T}\check{\mathbf{z}}
\]

The reduction and permutation operations are designed to reduce correlation and improve search efficiency without changing the underlying integer least-squares problem.

## 3. Conceptual algorithm

1. Obtain a float ambiguity estimate and its covariance from an upstream GNSS estimator.
2. Validate dimensions, finiteness, symmetry and positive definiteness of the covariance.
3. Factor the covariance and apply integer Gauss transformations and permutations to decorrelate the ambiguity system.
4. Search the transformed integer lattice for the best candidate(s) under the quadratic objective.
5. Transform the selected integer vector back to the original ambiguity basis.
6. Evaluate candidate separation and ambiguity success diagnostics under a project-appropriate validation strategy.
7. If accepted, use the fixed ambiguities in the downstream position/baseline solution and retain the float solution and diagnostics for audit.

The search is a discrete optimisation problem. Search bounds and candidate enumeration must be controlled so that the implementation returns the actual best candidate under its stated search procedure rather than silently truncating the lattice.

## 4. Acceptance is a separate decision

Finding an ILS minimiser does not by itself prove that the ambiguity vector is correct. The float model may be biased or misspecified; cycle slips, multipath, unmodelled atmospheric effects, wrong antenna models, signal biases and poor geometry can invalidate the candidate distribution.

A ratio test compares the best and second-best candidate objective values, but a universal threshold should not be assumed. Thresholds depend on the ambiguity dimension, stochastic model, desired failure rate and validation context. A ratio statistic is not a substitute for checking the float solution, residuals, observation continuity, geometry and independent positions.

Preserve at least:

- float ambiguities and covariance;
- transformed covariance and transformation metadata;
- best and second-best integer candidates and objective values;
- search configuration and termination status;
- acceptance statistic and threshold rationale;
- cycle-slip and observation-quality diagnostics;
- fixed-solution residuals and independent check results.

If acceptance criteria fail, retain a float solution or mark the ambiguity solution unresolved; do not force a fixed solution to satisfy a desired accuracy claim.

## 5. Related observation combinations and cycle-slip screening

Dual-frequency combinations can help isolate observation behaviour, but they have different noise and bias properties:

- geometry-free phase differences are sensitive to ionospheric variation and phase discontinuities;
- wide-lane combinations change the effective wavelength and ambiguity structure;
- Melbourne–Wübbena combinations combine code and phase information and retain code noise, multipath and hardware-bias effects.

A cycle-slip detector flags candidate discontinuities; it does not automatically identify the exact integer slip or repair the carrier-phase arc. A detected event should trigger documented handling of the affected observations and ambiguity state.

## 6. Implementation and boundaries

The repository's [GNSS ambiguity implementation](../../implementations/python/gnss-ambiguity/README.md) includes a transparent Cholesky sphere-enumeration baseline, a LAMBDA-reduced integer least-squares solver, selected dual-frequency combinations and candidate cycle-slip screens.

The implementation accepts a supplied float ambiguity vector and positive-definite covariance. It does **not** estimate float ambiguities from raw GNSS observations, implement a complete GNSS observation model, repair integer slips, or provide a complete PPP-AR engine. The package is an educational computational component, not a field-validated or certified GNSS processor.

## 7. Further connections

- [GNSS positioning and navigation observation](../../collection/gnss-positioning-and-navigation-observation.md) — acquisition modes, field records, reference frames and independent quality checks.
- [Measurement models and measurand definition](../../foundations/measurement-science/measurement-models-and-measurand-definition.md) — observation models and model-dependent uncertainty.
- [Covariance and generalized least squares](../../foundations/measurement-science/covariance-correlated-observations-and-gls.md) — the role of covariance in estimation and correlated observations.

## References

- Teunissen, P. J. G. (1995). The least-squares ambiguity decorrelation adjustment: a method for fast GPS integer ambiguity estimation. *Journal of Geodesy*, 70, 65–82.
- Verhagen, S. and Teunissen, P. J. G. (2013). The ratio test for future GNSS ambiguity resolution. *GPS Solutions*, 17, 535–548.

The algorithm statement describes the integer estimation problem and a standard decorrelation strategy. Operational acceptance, stochastic modelling and end-to-end positioning remain application- and receiver-workflow-specific.
