# Measurement principles and field verification

**Version:** 0.1  
**Status:** Foundational synthesis — initial scope and conceptual model; detailed technical review and worked examples pending  
**Primary subject:** SM-FND-011 — Measurement science, accuracy and uncertainty  
**Connected subjects:** SM-COL-001, SM-COL-002, SM-COL-003, SM-ALG-018, SM-REC-008, SM-REC-017  
**Source register:** [Surveying and field measurement source map](../../catalog/surveying-field-measurement-source-map.md)

## 1. Why measurement science comes first

Surveying is not simply the act of collecting coordinates. It is the controlled process of making observations, relating them to a defined reference, estimating quantities from those observations, evaluating uncertainty, and demonstrating that the resulting information is fit for a stated purpose.

A coordinate can look precise and still be wrong. A survey can close mathematically and still be biased. A receiver can report a fixed GNSS solution while the project result remains inconsistent with an independent control check. An instrument can pass a field repeatability test without proving that the entire survey network is accurate.

Measurement science gives us the language and reasoning needed to distinguish these situations.

This collection uses the International Vocabulary of Metrology (VIM) for terminology and the Guide to the Expression of Uncertainty in Measurement (GUM) as the general framework for evaluating and reporting uncertainty. Survey-specific standards and professional guidance then apply these principles to particular instruments, procedures and project requirements.

## 2. The measurement chain

A defensible spatial measurement can be represented as a chain:

1. **Purpose and requirement** — what decision or product must the measurement support, and what performance is required?
2. **Measurand** — what exact quantity is intended to be measured, under what conditions and with what definition?
3. **Reference** — relative to which datum, coordinate reference frame, epoch, benchmark, calibration standard or control network?
4. **Measurement model** — how do observations, corrections, environmental effects and unknown parameters relate to the measurand?
5. **Observation design** — which instruments, geometry, sample size, observation duration, redundancy and field procedure are appropriate?
6. **Acquisition** — what raw observations were actually recorded, with which instrument, operator, setup, time and conditions?
7. **Reduction and estimation** — how are observations corrected, transformed, combined and adjusted to estimate the required quantities?
8. **Uncertainty evaluation** — what sources of uncertainty contribute, how are they represented, and how do they propagate?
9. **Verification and validation** — what independent checks show that the procedure and resulting data satisfy the stated requirement?
10. **Delivery and provenance** — can another competent person understand, reproduce, inspect and use the result?

Each stage constrains the next. A sophisticated adjustment cannot rescue an undefined measurand, an unsuitable reference frame or missing raw observations.

## 3. Core concepts that must not be conflated

### 3.1 Error, uncertainty and correction

- **Measurement error** is the difference between a measured value and a reference quantity value. In practical field work, the exact true value is generally not known.
- **Measurement uncertainty** characterises the dispersion of values that could reasonably be attributed to the measurand, based on the information available. It is not the same thing as an error estimate.
- **Correction** is a compensating value applied for an estimated systematic effect. Applying a correction does not make the uncertainty associated with that correction disappear.
- **Residual** is the difference between an observed value and the corresponding value calculated from an estimated model. Residuals are diagnostic evidence, not direct proof that the model is correct.

A reported coordinate should not be described as error-free merely because corrections have been applied or residuals are small.

### 3.2 Precision, repeatability and reproducibility

- **Precision** concerns agreement among repeated indications or measured values under specified conditions.
- **Repeatability** concerns precision under repeatability conditions, typically involving the same procedure, operator, measuring system, location and short time interval.
- **Reproducibility** concerns precision under changed conditions, such as different operators, equipment, locations or times, as defined by the applicable procedure.

Precision is not synonymous with accuracy. Repeated observations can be tightly grouped around a biased result.

### 3.3 Accuracy and trueness

Accuracy is a qualitative concept describing closeness of agreement between a measured quantity value and a true quantity value. It is not itself a numerical uncertainty measure. Trueness concerns closeness of agreement between the average of many repeated measured values and a reference value. Precision and trueness describe different aspects of measurement performance.

For survey reporting, avoid using “accuracy” as a substitute for a complete uncertainty statement or as a bare label without a stated test, reference and acceptance criterion.

### 3.4 Calibration, adjustment and verification

- **Calibration** establishes, under specified conditions, a relation between reference quantity values and instrument indications, including associated uncertainties.
- **Adjustment** changes a measuring system so that it provides prescribed indications. In surveying, “instrument adjustment” may also refer to mechanical/optical adjustment or mathematical estimation; the intended meaning must be explicit.
- **Verification** provides objective evidence that specified requirements have been fulfilled.
- **Field testing** evaluates performance under specified field procedures and conditions. Its conclusions are limited to the test design and measured performance characteristics.

A field check is not automatically a calibration. A manufacturer's calibration certificate is not a substitute for checking whether the full field procedure is fit for a particular survey.

## 4. Measurement models

A measurement result is produced through a model connecting observations and input quantities to the measurand.

A general observation model can be written:

\[
\mathbf{l}=\mathbf{f}(\mathbf{x},\mathbf{c})+\boldsymbol{\varepsilon}
\]

where:

- \(\mathbf{l}\) is the vector of observations;
- \(\mathbf{x}\) is the vector of unknown parameters;
- \(\mathbf{c}\) represents known or measured corrections and ancillary quantities;
- \(\mathbf{f}\) is the functional model;
- \(\boldsymbol{\varepsilon}\) represents observation deviations not explained by the model.

The model must describe the relevant physics and geometry, not merely fit the available data. Examples include:
- a distance observation corrected for atmospheric conditions, slope and instrument/reflector constants;
- a direction observation related to station orientation and target coordinates;
- a levelling observation related to height differences, instrument setup and systematic effects;
- a GNSS observation model relating carrier phase or code observations to receiver/satellite states, clocks, atmosphere, antenna effects and ambiguities.

The **functional model** describes how quantities relate. The **stochastic model** describes the expected uncertainty and covariance structure of observations. Both are necessary for defensible estimation.

## 5. Uncertainty evaluation

The GUM framework distinguishes uncertainty evaluation by statistical analysis of repeated observations (Type A) from evaluation using other information (Type B). These are methods of evaluation, not categories of error.

Examples of information that may contribute include:
- repeated observations and empirical dispersion;
- instrument specifications and calibration information;
- resolution and quantisation;
- environmental measurements and correction models;
- centring, levelling and target setup;
- reference-station coordinates and their covariance;
- antenna calibration and phase-centre models;
- uncertainty in transformation parameters or geoid models;
- operator procedure and field conditions.

For a measurement model \(y=f(x_1,\ldots,x_n)\), a first-order uncertainty propagation approximation is:

\[
u_c^2(y)\approx \mathbf{J}\,\mathbf{U}_x\,\mathbf{J}^{T}
\]

where \(\mathbf{J}\) is the Jacobian of sensitivity coefficients and \(\mathbf{U}_x\) is the covariance matrix of input quantities. This expression makes an important point: correlations matter. Treating correlated observations or shared reference errors as independent can produce misleading uncertainty estimates.

For a single output quantity with independent inputs, the familiar approximation reduces to:

\[
u_c^2(y)\approx\sum_i\left(\frac{\partial f}{\partial x_i}\right)^2u^2(x_i)
\]

This is not a universal substitute for the full model. Strong nonlinearity, non-Gaussian distributions, bounded quantities or complex correlations may require more appropriate methods, including Monte Carlo propagation.

Expanded uncertainty is commonly expressed as \(U=k u_c\), where the coverage factor \(k\) and its interpretation must be stated. Do not assume that a particular value of \(k\) guarantees a universal coverage probability irrespective of the distribution and degrees of freedom.

**Current source note:** BIPM's guide catalogue lists the 2008 GUM, supplements for Monte Carlo propagation and multiple outputs, GUM-6 on measurement models, and a 2026 Amendment 1 addressing nonlinearity. This collection must review the amendment rather than silently treating the 2008 text as the entire current guidance set.

## 6. Error sources in field surveying

A useful first classification is:

| Source family | Examples | Typical treatment |
|---|---|---|
| Instrument/system | Collimation, compensator, EDM scale/additive constants, encoder effects, antenna calibration, receiver clock and tracking behaviour | Calibration, adjustment, field verification, correction models and uncertainty contributions |
| Environment | Temperature, pressure, humidity, refraction, multipath, wind, vibration, magnetic effects, atmospheric delay | Measure conditions, model effects, choose suitable observation windows and procedures |
| Geometry/setup | Centring, levelling, target height, antenna height, prism constant, instrument height, poor intersection geometry | Standardised setup, redundant measurements, independent checks and explicit metadata |
| Reference/control | Datum realisation, epoch, station coordinates, benchmark stability, transformation parameters, geoid model | Use authoritative reference information, propagate reference uncertainty, preserve frame/epoch metadata |
| Observer/procedure | Point identification, target pointing, booking, feature coding, transcription and procedural deviations | Training, checklists, independent readings, structured field records and audit trails |
| Processing/model | Incorrect functional model, unsuitable weights, omitted corrections, bad constraints, wrong units or CRS | Independent model review, residual diagnostics, sensitivity analysis, reproducible processing |

Random and systematic effects are not always separable by inspection. A systematic effect may vary with time or conditions; a random-looking residual pattern may reveal a model defect. Gross mistakes (for example a wrong antenna height or point ID) require detection and investigation, not routine absorption into a statistical uncertainty budget.

## 7. Redundancy and independent checks

Redundancy means collecting more information than is minimally required to solve for the unknowns. It supports:
- estimation of unknowns;
- internal consistency checks;
- detection of some gross errors;
- estimation of precision and covariance under the adopted model;
- assessment of network geometry and reliability.

Redundancy is not the same as independence. Repeating the same setup with the same unrecognised bias may produce many observations but little additional evidence.

A good field design therefore combines:
- repeated observations under defined conditions;
- different observation geometry or independent setups where practical;
- ties to independently established control;
- check points withheld from adjustment where appropriate;
- closure and loop checks;
- independent methods or equipment when the consequences justify them.

The checks must be designed before the fieldwork. A survey should not invent acceptance criteria after seeing the results.

## 8. Field verification is procedure-specific

ISO 17123 is a family of field procedures, not a universal certificate of survey accuracy.

The current source register identifies:
- ISO 17123-1 for the general theory behind field testing and uncertainty;
- ISO 17123-5 for total-station coordinate-measurement precision;
- ISO 17123-8 for RTK GNSS field measurement-system repeatability;
- ISO 17123-11:2025 for a GNSS instrument field-verification approach based on comparison of measured 3D coordinates with reference coordinates.

These parts address different equipment and test questions. Their scopes must not be collapsed into a generic statement that an instrument is “ISO certified” or “accurate to X”.

For every field verification record, capture:
- the instrument and ancillary equipment identity;
- firmware/software and relevant configuration;
- test site and reference values, including their source and uncertainty;
- operator, date, environmental conditions and setup;
- the exact procedure and observation schedule;
- calculations, test statistics and acceptance criteria;
- deviations, failures, corrective action and retest outcome;
- the limited conclusion supported by the test.

## 9. A practical measurement-design template

Before collecting data, write a short measurement plan:

| Planning question | Required record |
|---|---|
| What is being measured? | Measurand definition and units |
| Why is it needed? | Intended decision, product and fitness-for-purpose requirement |
| What reference is used? | Datum/frame, realisation, epoch, benchmark/control source and height system |
| What method is selected? | Instrument, observation mode, procedure and rationale |
| What influences the result? | Functional model, corrections and expected uncertainty contributors |
| How will the data be checked? | Redundancy, independent checks, acceptance criteria and failure handling |
| What must be preserved? | Raw observations, field notes, metadata, calibration/verification records and processing history |
| What will be delivered? | Coordinates/measurements, CRS metadata, uncertainty/quality statement, limitations and provenance |

This template is a planning aid, not a substitute for a project specification, statutory requirements or a qualified surveyor's professional judgement.

## 10. How the concepts connect to the Spatial Methods pillars

- **Theoretical Foundations:** metrology, probability, statistics, adjustment theory, geodesy and numerical methods explain the measurement process.
- **Spatial Data Collection:** instruments and field procedures generate observations under physical and operational constraints.
- **Spatial Algorithms:** reductions, transformations, least-squares estimation, covariance propagation and quality tests process and evaluate observations.
- **Spatial Recipes:** a survey plan integrates reference selection, instrument verification, observation design, field capture, processing, independent checking and delivery.

Applications such as cadastral mapping, engineering construction, transport infrastructure, environmental monitoring and deformation analysis impose different measurands, tolerances, legal constraints and evidence requirements. They reuse the same measurement principles without becoming identical workflows.

## 11. Open technical questions for the next revision

1. How should uncertainty budgets be structured for total-station traverses, precise levelling and GNSS control networks?
2. How do reference-frame realisation, coordinate epoch, plate motion and datum transformation uncertainty enter project results?
3. Which field verification procedures are appropriate for different equipment classes and project risks?
4. How should internal precision, external accuracy, network reliability and independent check-point results be reported together?
5. Which Kenyan regulations, LSB guidelines and project specifications establish mandatory requirements for different survey classes?
6. How should the knowledge base represent raw observations, corrections, adjusted values, covariance and provenance in interoperable data models?

## 12. Source trail and review status

Primary sources:
- [BIPM — Guides in Metrology](https://www.bipm.org/en/web/guest/publications/guides), including GUM, its supplements, GUM-6 and the 2026 nonlinearity amendment.
- [BIPM — JCGM 200:2012, International Vocabulary of Metrology](https://www.bipm.org/en/doi/10.59161/jcgm200-2012).
- [ISO 17123 series](https://www.iso.org/standard/64156.html) for field procedures; consult the relevant part for the instrument under study.
- [RICS — Use of GNSS in Land Surveying and Mapping, 3rd edition](https://www.rics.org/profession-standards/rics-standards-and-guidance/sector-standards/land-standards/guidelines-for-the-use-of-gnss-in-land-surveying-and-mapping).
- [Surveying and field measurement source map](../../catalog/surveying-field-measurement-source-map.md) for Kenyan legislation/guidance, reference-frame sources and source-status cautions.

This is an original educational synthesis, not a reproduction of the GUM, VIM or ISO text. The source map records which documents need full review. Detailed equations, worked examples, numerical implementations and field procedures will be added only after the relevant source passages, assumptions and acceptance criteria have been checked.

**Current maturity:** conceptual foundation drafted; terminology and source review in progress; no instrument-specific field procedure implemented or validated.
