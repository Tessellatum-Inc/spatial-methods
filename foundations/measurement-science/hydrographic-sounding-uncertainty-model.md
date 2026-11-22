# Hydrographic sounding uncertainty: measurement model and covariance budget

**Status:** Technical foundation, version 0.1; desk-derived model; no instrument-specific TPU or field validation  
**Applies to:** Multibeam and single-beam sounding measurement chains  
**Prerequisite:** [Covariance, correlated observations and generalized least squares](covariance-correlated-observations-and-gls.md)  
**Workflow:** [Multibeam bathymetry recipe](../../recipes/multibeam-bathymetry/README.md)

## 1. The measurand comes before the uncertainty number

A sounding is not just a range measurement. It is a seabed point expressed in a declared horizontal reference frame and vertical datum, at a stated epoch and under a stated sign convention. Its uncertainty depends on the complete chain from acoustic observation through platform pose, sensor geometry, geodetic transformation and vertical reduction.

The relevant chain is:

**raw acoustic observation → range/beam solution → water-column ray model → transducer-relative vector → vessel pose and lever-arm transform → geodetic position → vertical-reference reduction → sounding covariance → surface and independent validation**

The measurement model must identify:
- the actual measurand (for example, seabed elevation or positive-down depth at a defined horizontal location);
- coordinate frame, axes, units, epoch and vertical datum;
- sensor reference points and all lever-arm definitions;
- attitude convention, rotation order and timing;
- acoustic ray and sound-speed assumptions;
- corrections and their sources;
- stochastic components and shared-error mechanisms.

An uncertainty number detached from these definitions is not portable or interpretable.

## 2. A general geometric observation model

A useful abstract model separates the navigation solution from the transducer-relative acoustic vector. In a local Cartesian frame, write

\[
\mathbf{p}_b
=
\mathbf{r}_n
+
\mathbf{R}_{n\leftarrow b}
\left(
\boldsymbol{\ell}_{b}
+
\mathbf{s}_{b}
\right),
\]

where:
- \(\mathbf{p}_b\) is the sounding point in the navigation/local frame;
- \(\mathbf{r}_n\) is the navigation reference-point position in that frame;
- \(\mathbf{R}_{n\leftarrow b}\) rotates vectors from the body frame to the navigation frame;
- \(\boldsymbol{\ell}_{b}\) is the body-frame lever arm from the navigation reference point to the acoustic origin;
- \(\mathbf{s}_{b}\) is the body-frame acoustic vector from the acoustic origin to the seabed detection.

This is a frame-explicit structural equation, not a complete vendor beam model. The definition of the body frame, navigation frame, rotation order, positive axes, lever-arm direction and timestamp must be fixed before implementation. If the navigation solution is referenced to the GNSS antenna and the IMU is at another point, the complete chain may require more than one rigid-body transform.

The acoustic vector \(\mathbf{s}_{b}\) is itself a function of observations and models, for example

\[
\mathbf{s}_{b}
=
g(\rho,\alpha,\boldsymbol{c}(z),\boldsymbol{\eta}),
\]

where \(\rho\) is measured range, \(\alpha\) is beam direction/angle, \(\boldsymbol{c}(z)\) represents the sound-speed profile and \(\boldsymbol{\eta}\) collects other acoustic parameters and corrections. The exact function depends on sonar architecture, beam-angle convention, ray-tracing model and processing system. Do not replace it with a straight ray unless the approximation is justified for the case.

The vertical datum reduction is a further model:

\[
h_D = q(\mathbf{p}_b,\boldsymbol{w},\boldsymbol{d},\boldsymbol{v}),
\]

where \(h_D\) is the declared vertical measurand, \(\boldsymbol{w}\) represents water-level or vertical-separation information, \(\boldsymbol{d}\) draft/dynamic-draft terms and \(\boldsymbol{v}\) other required vertical-reference parameters. A project may use ellipsoidally referenced bathymetry or a tide-/water-level-reduced depth workflow; these are not interchangeable and require different observation models.

## 3. First-order covariance propagation

Collect uncertain inputs into one vector \(\mathbf{x}\), with a joint covariance matrix \(\mathbf{C}_{xx}\). Let the complete coordinate/sounding model be \(\mathbf{y}=f(\mathbf{x})\). Linearising at the chosen expansion point gives

\[
\mathbf{J}
=
\left.\frac{\partial f}{\partial\mathbf{x}}\right|_{\mathbf{x}_0},
\qquad
\mathbf{C}_{yy}
\approx
\mathbf{J}\mathbf{C}_{xx}\mathbf{J}^{T}.
\]

The diagonal entries give marginal variances; off-diagonal entries retain covariance between output coordinates or derived quantities. For a scalar depth measurand with sensitivity vector \(\mathbf{c}\),

\[
u_c^2(h_D)\approx
\mathbf{c}^{T}\mathbf{C}_{xx}\mathbf{c}.
\]

This expression requires the full joint covariance, not a list of marginal standard uncertainties alone. A correlation term can either increase or reduce an output variance depending on the signs and directions of the sensitivities.

The repository's dependency-free [covariance propagation implementation](../../implementations/python/uncertainty-propagation/README.md) evaluates the matrix expression for a supplied Jacobian and covariance matrix. It validates matrix dimensions, symmetry and positive semidefiniteness, including singular positive-semidefinite covariance matrices. It does not derive a hydrographic Jacobian, estimate instrument covariance or validate a sonar model.

## 4. Build a physically defensible input budget

Use the following as a component inventory, not a universal list of independent random variables.

| Component | Potential input representation | Questions to resolve |
|---|---|---|
| Acoustic range | Range observation, timing, scale and detection parameters | What is the range estimator, resolution, noise model and calibration evidence? |
| Beam direction | Beam angle, steering, alignment or beamforming parameters | Is the angle supplied by vendor processing, estimated, calibrated or reconstructed? |
| Sound speed | Surface sound speed and profile parameters | How representative are profile location/time/depth and the ray model? |
| GNSS position | Position/trajectory covariance and reference-frame parameters | Is the covariance epoch-specific? Are corrections, atmosphere and reference stations shared? |
| Heading and attitude | Heading, roll, pitch and heave estimates | What are the sensor covariance, correlations, latency and filtering effects? |
| Lever arms and boresight | Calibration parameter vector and covariance | Were offsets measured in the correct frames and rechecked after installation changes? |
| Timing | Sensor latency and synchronisation parameters | Which streams share a clock, and which timing errors are common? |
| Draft and squat | Static draft, loading and dynamic correction parameters | How do loading, speed, trim and sea state affect the correction? |
| Water level / vertical reference | Gauge observations, transfer parameters or separation model | What is the datum tie, spatial/temporal representativeness and common reference uncertainty? |
| Processing and detection | Model, filtering and bottom-detection parameters | Which uncertainty is represented by the stochastic model, and which remains a possible bias/model discrepancy? |

For each component record its unit, frame, epoch, source, calibration/estimation method, uncertainty type, covariance partners and evidence. Separate random observation noise, calibration-parameter uncertainty, common-mode reference uncertainty and unmodelled systematic effects. Do not count a correction uncertainty twice if it is already represented in the joint parameter covariance.

## 5. Correlation is expected in parts of the chain

Plausible shared-error mechanisms include:
- one GNSS/INS trajectory solution contributing to many beams and pings;
- a common heading, roll/pitch or heave estimate applied to an entire ping or line;
- common lever-arm, boresight, patch-test or latency parameters;
- a sound-speed profile applied to many pings or a survey block;
- common water-level observations, benchmark ties or vertical-separation models;
- shared calibration, timing and reference-frame parameters across lines.

A simplified conceptual decomposition is

\[
\mathbf{x}_i
=
\mathbf{x}_{i,\mathrm{local}}
+
\mathbf{B}_i\boldsymbol{\gamma},
\]

where \(\mathbf{x}_{i,\mathrm{local}}\) contains observation-specific terms and \(\boldsymbol{\gamma}\) contains shared uncertain parameters. The shared term induces covariance between soundings. This is a modelling pattern, not a claim that every component is additive or that one common random effect captures the actual system.

The covariance structure should follow the acquisition and processing lineage. A profile shared by a line may induce within-line correlation; a datum parameter may induce block-wide correlation; a per-ping attitude estimate may induce a different pattern. The grouping and correlation length must be justified, not guessed.

## 6. Horizontal and vertical uncertainty are coupled

A vertical uncertainty budget alone is insufficient for an oblique beam or sloping seabed. Errors in range, beam direction, attitude, position and sound speed can shift the sounding horizontally and vertically. Horizontal displacement can also change the seabed location at which the depth is interpreted.

For a local surface represented by \(z=z(x,y)\), a small horizontal displacement produces a first-order apparent vertical change

\[
\delta z \approx
\frac{\partial z}{\partial x}\,\delta x
+
\frac{\partial z}{\partial y}\,\delta y.
\]

This is a local geometric relation, not an additional independent noise term to add automatically. Whether and how it enters depends on the measurand, surface model and validation question. Avoid double counting horizontal-to-vertical effects already present in the full three-dimensional observation model.

Report the horizontal and vertical components, their confidence convention and any relevant cross-covariances. A single scalar “position accuracy” can conceal important anisotropy and coupling.

## 7. Linearisation limits and alternatives

First-order propagation is appropriate only when the model is sufficiently smooth over the uncertainty region and the local linear approximation is adequate. Warning signs include:
- large attitude or beam-angle uncertainty;
- steep or rapidly changing sound-speed gradients;
- critical/turning ray conditions;
- nonlinear bottom detection or ambiguous returns;
- discontinuous filtering, rejection or feature-selection rules;
- strongly non-Gaussian or multimodal navigation/acoustic solutions.

Where these effects matter, use a validated nonlinear propagation approach with a joint sampler that preserves the dependencies among inputs. Independent uniform sampling of each parameter is not a substitute for a correlated measurement model. Monte Carlo results also depend on the chosen distributions, correlations, truncations and model fidelity.

## 8. Cross-line checks, independent validation and common-mode error

Cross-line or overlapping-swath comparisons assess relative consistency under the geometry and conditions represented by those lines. They do not by themselves establish absolute accuracy. If all lines share a datum offset, calibration error, trajectory bias or sound-speed error, they may agree with one another while all being displaced.

Keep distinct:
1. **Internal precision and consistency** — repeatability, residuals and overlap behaviour.
2. **Relative accuracy** — agreement between observations or surfaces under the tested geometry.
3. **Absolute accuracy** — agreement with a suitably independent reference in the same frame and datum.
4. **Coverage and feature detection** — whether the required seabed area and features were observed.
5. **Specification compliance** — whether the defined acceptance criteria are met.

Independent checks need their own uncertainty budget and must not be used to tune the same observations and then presented as independent validation. The uncertainty of the check reference matters in interpreting differences.

## 9. Practical implementation sequence

1. Declare the sounding measurand, frames, vertical reference, units, epochs and sign conventions.
2. Draw the sensor/reference-point geometry and record all transformations.
3. Define the acoustic vector model and its input parameters.
4. Build a component inventory and identify shared parameters from data lineage.
5. Assemble the joint covariance with documented units and assumptions.
6. Derive or numerically verify the Jacobian; test derivatives against finite differences where appropriate.
7. Propagate covariance and inspect output covariance, anisotropy and sensitivity.
8. Compare first-order results with dependence-preserving Monte Carlo where nonlinearity may matter.
9. Validate with independent observations and report both common-mode and local error evidence.
10. Preserve model version, inputs, covariance, Jacobian, software, assumptions and validation results with the sounding products.

## 10. What this module does not claim

This module is not an instrument-specific TPU model, an IHO compliance calculation, a CUBE estimator, a patch-test procedure or a substitute for an operational hydrographic processing system. It contains no measured sensor covariance, vessel geometry, calibration certificate, real sound-speed profile, field dataset or independently validated Jacobian. The generic covariance implementation is a matrix calculation utility, not proof that a chosen hydrographic stochastic model is correct.

## 11. References

- IHO, [S-44 Standards for Hydrographic Surveys](https://iho.int/en/standards-and-specifications), for survey-order requirements and uncertainty/coverage conventions. Use the currently adopted edition and the competent authority's instructions.
- JCGM, [JCGM 100:2008 — Guide to the expression of uncertainty in measurement](https://www.bipm.org/en/doi/10.59161/jcgm100-2008), Sections 5.1–5.2, for first-order propagation and covariance terms.
- NIST, [TN 1297 Appendix A — Law of propagation of uncertainty](https://www.nist.gov/pml/nist-technical-note-1297/nist-tn-1297-appendix-law-propagation-uncertainty).
- Repository [covariance foundation](covariance-correlated-observations-and-gls.md), [covariance propagation implementation](../../implementations/python/uncertainty-propagation/README.md), and [multibeam bathymetry recipe](../../recipes/multibeam-bathymetry/README.md).

Independent hydrographic and metrological technical review is required before using this framework to support operational survey acceptance.
