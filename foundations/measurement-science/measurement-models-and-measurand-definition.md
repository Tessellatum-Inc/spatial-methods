# Measurement models and measurand definition

**Version:** 0.1  
**Status:** Curated educational module; worked example checked analytically; not an instrument procedure  
**Primary subject:** SM-FND-011 — Measurement science, accuracy and uncertainty  
**Parent foundation:** [Measurement principles and field verification](measurement-principles-and-field-verification.md)  
**Source basis:** JCGM 100:2008 (GUM), clauses 4.1 and 5.1–5.2. The 2008 text is the legacy core of the broader GUM suite; consult the current suite and applicable amendments for work requiring current metrological guidance.

## 1. Why define the measurand first?

A measurement does not begin with a sensor reading or a coordinate in a file. It begins by deciding what quantity is intended to be measured and under what conditions.

A statement such as “measure the road width” is incomplete for a defensible measurement. It leaves open questions such as:

- Width between which physical boundaries?
- At what chainage or cross-section?
- Is the quantity horizontal, slope, clear, paved or kerb-to-kerb width?
- At what time and under what surface or environmental conditions?
- What reference direction, datum or convention defines the result?
- What use will the result support, and what level of uncertainty is acceptable?

A measurand should be described precisely enough that another competent person can understand what quantity the result represents. The definition may need to include the object, location, time, geometry, state and relevant conditions. These are not administrative details: they determine the mathematical quantity being estimated.

## 2. From a vague task to an operational definition

Consider a request to inventory the width of a roadside bus-stop bay.

A weak definition is:

> Measure the width of the bay.

A more operational definition might be:

> The horizontal planimetric distance, at the nominated cross-section, between the surveyed back-of-kerb line and the surveyed road-edge boundary of the paved bay, at the observation time.

This still requires a project-specific rule for choosing the cross-section and identifying the road-edge boundary. If the physical boundary is irregular or ambiguous, the definition must say how it is represented. The measurement team must not silently substitute an easier-to-observe feature.

A good measurand definition therefore has three practical tests:

1. **Unambiguous:** different observers can identify the same intended quantity.
2. **Observable:** a stated measurement method can obtain information relevant to that quantity.
3. **Fit for purpose:** the definition matches the decision or analysis the result is intended to support.

The operational definition is not the measurement model. It establishes what is wanted; the model describes how observations and other inputs are related to the result.

## 3. The measurement model

A measurement model expresses the relationship between the measurand and the input quantities used to estimate it.

In general form:

\[
Y = f(X_1, X_2, \ldots, X_N)
\]

Here:

- \(Y\) is the output quantity or estimate of the measurand;
- \(X_i\) are input quantities;
- \(f\) is the mathematical or computational relationship.

Inputs can include direct observations, calibration corrections, environmental quantities, instrument constants, reference values, geometric parameters and quantities obtained from other measurements.

A model is not merely an equation chosen because it is convenient. Its terms should correspond to the actual measurement process and the operational definition of the measurand.

### 3.1 Observation, correction and result

Keep these concepts distinct:

- **Indication or observation:** what the instrument or procedure produces.
- **Correction:** an estimated adjustment applied to account for a recognised effect.
- **Input quantity:** a value used by the model, which may be observed, corrected, calibrated or supplied from another source.
- **Measurement result:** the value attributed to the measurand, together with the information needed to interpret its uncertainty.

A correction is not automatically known exactly. If its value is uncertain and materially affects the result, that uncertainty belongs in the model.

### 3.2 A model must include relevant dependencies

Suppose a rectangular test area has measured length \(L\) and width \(W\). Its area is modelled as:

\[
A = LW
\]

The simplicity of this equation does not remove the need to define the rectangle's boundaries, orientation, measurement conditions and corner construction. Nor does it mean the two input dimensions are necessarily independent.

If both dimensions are derived from the same control network, instrument setup, scale correction or environmental condition, their errors may share a common component. The covariance between inputs can then affect the uncertainty of the area.

## 4. Worked example: uncertainty in a rectangular area

This is a synthetic teaching example. It is not a field measurement or a claim about any particular instrument.

Assume the operationally defined rectangle has:

| Input | Estimate | Standard uncertainty |
|---|---:|---:|
| Length \(L\) | 20.000 m | 0.005 m |
| Width \(W\) | 10.000 m | 0.004 m |

The estimated area is:

\[
A = LW = 20.000 \times 10.000 = 200.000\;\text{m}^2
\]

For small uncertainties and a first-order linear approximation, the combined variance is:

\[
u_c^2(A) =
W^2u^2(L) + L^2u^2(W)
+ 2LW\,\operatorname{cov}(L,W)
\]

Equivalently, if the correlation coefficient is \(\rho_{LW}\):

\[
\operatorname{cov}(L,W)=\rho_{LW}u(L)u(W)
\]

### Case 1 — Treat the inputs as independent

If the model and evidence justify zero correlation:

\[
u_c(A)=
\sqrt{10^2(0.005)^2+20^2(0.004)^2}
\]

\[
u_c(A)\approx 0.0943\;\text{m}^2
\]

### Case 2 — Include a positive correlation

Now suppose, purely for illustration, the input correlation is \(\rho_{LW}=0.5\).

\[
\operatorname{cov}(L,W)=0.5(0.005)(0.004)
=0.000010\;\text{m}^2
\]

The covariance contribution to the area variance is:

\[
2(20)(10)(0.000010)=0.0040\;\text{m}^4
\]

Therefore:

\[
u_c(A)=\sqrt{0.0025+0.0064+0.0040}
\approx 0.1136\;\text{m}^2
\]

<text> </text>

| Assumption | Combined standard uncertainty |
|---|---:|
| Independent inputs | 0.0943 m² |
| Correlation 0.5 | 0.1136 m² |

The positive correlation increases the estimated uncertainty in this example. A different correlation structure can have a different effect.

**The correlation coefficient is an assumed teaching input here, not an empirically estimated property.** In a real project, covariance should be derived from a defensible stochastic model, repeated observations, shared error sources or other relevant evidence. Do not invent a correlation merely to make a model appear sophisticated.

## 5. First-order propagation and its limits

For a sufficiently well-behaved model, first-order propagation uses the sensitivity coefficients:

\[
c_i = \frac{\partial f}{\partial X_i}
\]

and the input covariance matrix \(\boldsymbol{\Sigma}_X\):

\[
u_c^2(Y) \approx
\mathbf{J}\boldsymbol{\Sigma}_X\mathbf{J}^{T}
\]

where \(\mathbf{J}\) is the row vector of partial derivatives evaluated at the input estimates.

For the area example:

\[
\mathbf{J} = \begin{bmatrix} W & L \end{bmatrix}
\]

This approximation is useful, but it is not universally adequate. Strong nonlinearity, non-Gaussian input distributions, discontinuities, large relative uncertainties or complex output distributions can require a more careful treatment. Monte Carlo propagation is one alternative to investigate when the first-order approximation is inadequate; it is not automatically superior for every problem.

The 2026 GUM suite and amendment on nonlinearity should be considered when developing advanced material on these cases. This introductory module does not attempt to interpret the amendment's detailed provisions.

## 6. A practical model-building checklist

Before calculating an uncertainty budget, write down:

1. **Measurand:** the exact quantity and operational definition.
2. **Measurement boundary:** which physical features, epochs, coordinate frames or conditions are included.
3. **Observation process:** what is directly observed and by which method.
4. **Model inputs:** every observation, correction, constant and externally supplied quantity.
5. **Functional relationship:** the equation or computational procedure mapping inputs to the result.
6. **Assumptions:** approximations, neglected effects and chosen conventions.
7. **Dependencies:** shared sources of error and plausible correlations.
8. **Evidence:** calibration records, specifications, repeated observations, reference data or justified prior information.
9. **Intended use:** the decision the result supports and the required uncertainty or quality threshold.
10. **Model limitations:** conditions under which the model should not be used.

If a relevant input or correction is omitted, the uncertainty calculation can be internally consistent and still fail to represent the actual measurement process.

## 7. Common modelling mistakes

- Defining the measurand as “whatever the instrument reports”.
- Mixing horizontal, slope, grid and ground distances without stating the conversion.
- Treating a coordinate as meaningful without its reference system, epoch and coordinate convention.
- Omitting corrections because they are inconvenient to obtain.
- Assuming all inputs are independent because the software accepts a diagonal covariance matrix.
- Treating instrument specifications as a complete uncertainty budget for the measured quantity.
- Reporting a numerical uncertainty without explaining the model and assumptions.
- Using a more complicated model without evidence that its extra parameters are identifiable or relevant.

## 8. Relationship to the rest of the collection

This module establishes the model before uncertainty evaluation. The intended progression is:

1. Measurement models and measurand definition — this module.
2. Standard uncertainty and Type A / Type B evaluation.
3. Covariance and correlated observations.
4. Linear and nonlinear uncertainty propagation.
5. Monte Carlo propagation and distributional interpretation.
6. Coverage intervals and reporting.
7. Instrument- and application-specific examples.

These topics are connected, not a rigid sequence. A practitioner may need to revisit the measurand definition after discovering that the available observation method cannot support it.

## 9. Evidence and limitations

The core model-based treatment is grounded in the legacy GUM, particularly clauses 4.1 and 5.1–5.2. The GUM is now presented by JCGM as a broader suite; this module does not claim that JCGM 100:2008 alone represents every current development.

- [JCGM 100:2008 — Guide to the expression of uncertainty in measurement](https://www.bipm.org/en/doi/10.59161/jcgm100-2008)
- [BIPM GUM publications and suite overview](https://www.bipm.org/en/measurement-units/measurement-uncertainty)

The numerical example is original and reproducible from the equations shown. It is a first-order analytical illustration with stipulated input standard uncertainties and a stipulated correlation coefficient. It does not establish field performance, instrument calibration, or compliance with a surveying standard.

**Maturity:** introductory module drafted; equations and numerical arithmetic checked; source-to-claim links recorded for the model and covariance principles; independent technical review and further worked examples remain outstanding.
