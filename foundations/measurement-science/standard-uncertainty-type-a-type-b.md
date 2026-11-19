# Standard uncertainty: Type A and Type B evaluation

**Version:** 0.1  
**Status:** Curated educational module; arithmetic checked; synthetic example only  
**Primary subject:** SM-FND-011 — Measurement science, accuracy and uncertainty  
**Prerequisite:** [Measurement models and measurand definition](measurement-models-and-measurand-definition.md)  
**Related experiment:** [Exercise A — repeated distance and horizontal-angle observations](../../experiments/measurement/exercise-a-repeated-distance-and-angle.md)

## 1. The purpose of uncertainty evaluation

A measurement model identifies how the result depends on input quantities. Uncertainty evaluation estimates the uncertainty associated with those inputs and combines their contributions into an uncertainty statement for the result.

The Guide to the Expression of Uncertainty in Measurement (GUM) distinguishes two methods of evaluating uncertainty:

- **Type A:** evaluation by statistical analysis of a series of observations.
- **Type B:** evaluation by methods other than statistical analysis of a series of observations.

These labels describe the evaluation method. They do not classify errors as random or systematic. A Type B evaluation may describe an uncertainty contribution associated with a recognised systematic effect; a Type A evaluation may be used to estimate variability associated with a measurement process. Avoid phrases such as “Type A error” and “Type B error”.

Every uncertainty component, regardless of evaluation method, is expressed as a standard uncertainty: a quantity on the scale of a standard deviation.

## 2. Type A evaluation from repeated observations

Suppose a scalar quantity is observed (n) times under sufficiently consistent conditions:

\[
x_1,x_2,\ldots,x_n
\]

The arithmetic mean is:

\[
\bar{x}=\frac{1}{n}\sum_{i=1}^{n}x_i
\]

The sample standard deviation is:

\[
s=\sqrt{\frac{1}{n-1}\sum_{i=1}^{n}(x_i-\bar{x})^2}
\]

If the observations can reasonably be treated as independent, drawn from a stable process and representative of the same measurand under the same conditions, the standard uncertainty of the mean is:

\[
u_A(\bar{x})=\frac{s}{\sqrt{n}}
\]

The sample standard deviation describes the spread of individual observations. The standard uncertainty of the mean describes the statistical uncertainty assigned to the estimated mean under the model. They are not interchangeable.

### 2.1 Example from repeated distance observations

The existing synthetic Exercise A contains eight repeated distance observations:

- Mean: 50.000000 m.
- Sample standard deviation: 1.309 mm.
- Standard uncertainty of the mean: 0.463 mm.

The value 0.463 mm is obtained from the sample standard deviation divided by \(\sqrt{8}\). It describes the Type A contribution to the mean under the exercise's simplified assumptions.

It does not account automatically for every effect shared by the eight readings. The observations use one notional station and target setup. Repeating readings without changing the setup does not make common centring, prism, calibration, scale or environmental effects disappear.

### 2.2 When the simple formula is not enough

The formula \(s/\sqrt{n}\) should not be applied mechanically. Investigate the observation design when there is:

- time-dependent drift or changing environmental conditions;
- serial correlation between consecutive observations;
- multiple operators, setups, instruments or sessions;
- distinct observation groups or levels of replication;
- outliers or non-stationary behaviour;
- a measurement model that requires regression, adjustment or another statistical estimator.

Type A evaluation can use other valid statistical methods, including least-squares estimation and analysis of variance. The appropriate method follows the design and stochastic model, not a preference for a familiar formula.

## 3. Type B evaluation from other information

A Type B evaluation uses relevant information other than statistical analysis of the current observation series. Examples include:

- calibration certificates and calibration reports;
- instrument or equipment specifications;
- resolution and quantisation limits;
- reference data and handbook values;
- previous measurement data;
- documented experience with the measurement process;
- environmental limits or correction information.

The information must be interpreted. A quoted number is not automatically a standard uncertainty. First determine what the number represents: a standard deviation, an expanded uncertainty, a confidence interval, a tolerance, a maximum permissible error, a resolution increment or something else.

The conversion to standard uncertainty depends on the stated quantity and the defensible probability model.

### 3.1 Rectangular distribution

If the available information supports treating a quantity as equally likely anywhere between lower and upper limits \(a_-\) and \(a_+\), the rectangular model has:

\[
x=\frac{a_++a_-}{2}
\]

\[
u_B=\frac{a_+-a_-}{2\sqrt{3}}=\frac{a}{\sqrt{3}}
\]

where \(a\) is the half-width of the interval.

For example, if rounding to a 1 mm increment is modelled as an unknown rounding error uniformly distributed between -0.5 mm and +0.5 mm:

\[
u_{res}=\frac{0.5}{\sqrt{3}}=0.289\;\text{mm}
\]

This is a model of rounding uncertainty, not evidence that the instrument's complete measurement error is bounded by ±0.5 mm.

### 3.2 Triangular distribution

If values near the centre are more plausible than values near the limits, and a symmetric triangular model is justified, then:

\[
u_B=\frac{a}{\sqrt{6}}
\]

For the same half-width of 0.5 mm:

\[
u_B=\frac{0.5}{\sqrt{6}}=0.204\;\text{mm}
\]

The triangular model should not be chosen merely because it produces a smaller uncertainty. The distribution must reflect the available evidence about the quantity.

### 3.3 Normal distribution and quoted expanded uncertainty

If a certificate reports an expanded uncertainty \(U\) and a coverage factor \(k\), the corresponding standard uncertainty is commonly obtained as:

\[
u=\frac{U}{k}
\]

This conversion is appropriate only when the certificate's definition and coverage information support it. Check the reported measurand, units, correction, coverage factor, distributional assumptions and any effective degrees of freedom. Do not assume every certificate uses \(k=2\) or that \(k=2\) always means exactly 95% coverage.

A manufacturer's tolerance or maximum permissible error is not automatically an expanded uncertainty. It requires a justified model before it can be converted.

### 3.4 Choose the distribution from evidence

| Information available | Possible model | Standard uncertainty |
|---|---|---:|
| Equal plausibility within ±a | Rectangular | \(a/\sqrt{3}\) |
| Centre more plausible, symmetric triangular shape | Triangular | \(a/\sqrt{6}\) |
| Stated standard deviation | Normal or stated model | Already standard uncertainty |
| Expanded uncertainty with stated coverage factor | As documented by issuer | \(U/k\), if justified |

These are examples, not an automatic lookup table. A bounded interval alone does not prove a rectangular distribution. A certificate's stated coverage information should take precedence over an invented generic assumption.

## 4. Combining Type A and Type B components

Type A and Type B components are combined using the measurement model and the relevant covariance information. They are not separate classes that require separate final uncertainty statements.

For uncorrelated input quantities in a suitable first-order model:

\[
u_c(y)=\sqrt{\sum_{i=1}^{N}c_i^2u^2(x_i)}
\]

where \(c_i\) is the sensitivity coefficient for input \(x_i\).

For correlated inputs, covariance terms must also be included:

\[
u_c^2(y)=
\sum_i c_i^2u^2(x_i)
+2\sum_{i<j}c_ic_j\,\operatorname{cov}(x_i,x_j)
\]

This is the law of propagation of uncertainty in its first-order form. The independence assumption must be justified, not selected simply because it makes the arithmetic easier.

### 4.1 Worked synthetic distance budget

Use the same illustrative budget in Exercise A. All Type B values below are stipulated teaching inputs, not specifications for an actual instrument or prism.

| Component | Evaluation | Standard uncertainty |
|---|---|---:|
| Mean of eight repeated readings | Type A | 0.463 mm |
| 1 mm display increment, rectangular rounding model | Type B | 0.289 mm |
| Prism-constant contribution | Type B, assumed | 0.500 mm |
| EDM scale contribution at 50 m | Type B, assumed | 0.100 mm |

Under the explicit simplifying assumption that these contributions are uncorrelated:

\[
u_c=\sqrt{0.463^2+0.289^2+0.500^2+0.100^2}
\]

\[
u_c\approx0.747\;\text{mm}
\]

The arithmetic is a root-sum-of-squares combination. It is not justified if relevant covariance has been omitted or if the measurement model is inadequate.

For illustration only, if a coverage factor of 2 is adopted:

\[
U=ku_c=2(0.747)=1.494\;\text{mm}
\]

This gives an illustrative expanded uncertainty of about 1.5 mm. The interpretation of the coverage factor depends on the distribution and degrees-of-freedom context. It is not a universal guarantee of 95% coverage.

## 5. Avoiding double counting and omissions

An uncertainty budget is a model of the measurement process, not a list of every number found in documents.

Before adding a component, ask:

1. What physical or computational effect does it represent?
2. Is it already included in another component?
3. Does it apply to an individual observation, the mean, a correction or the final result?
4. Is it common to all observations or does it vary between observations?
5. Is it correlated with another component?
6. Does the source provide a standard uncertainty, expanded uncertainty, limit or tolerance?
7. What evidence supports the assigned distribution and magnitude?

For example, do not add a calibration uncertainty twice if the quoted instrument specification already includes that calibration contribution and the scope is documented. Conversely, do not omit a calibration correction merely because it is supplied as a fixed number: the correction may itself have uncertainty.

A repeated-observation standard error should not be used to shrink a component that is common to every observation. The common contribution must be modelled at the appropriate level.

## 6. Degrees of freedom and the limits of a small sample

A Type A standard uncertainty estimated from a small number of observations has finite statistical information. In the simple independent normal model, the sample standard deviation has \(n-1\) degrees of freedom.

When several components are combined, the uncertainty in the combined standard uncertainty may need to be considered. The Welch–Satterthwaite approximation is one method used in the GUM framework when its assumptions are appropriate. It should not be applied without understanding the component distributions, independence assumptions and degrees of freedom.

This module does not calculate effective degrees of freedom for the synthetic distance budget because the assumed Type B inputs have not been assigned defensible degrees of freedom. Consequently, the illustrative \(k=2\) result is not presented as a rigorously established 95% interval.

## 7. Practical uncertainty-budget template

Use a table like this for each measurement model. Keep the source and reasoning visible.

| Component | Estimate or correction | Standard uncertainty | Evaluation method | Distribution / basis | Correlation / notes |
|---|---:|---:|---|---|---|
| Repeated observations |  |  | Type A | Statistical model |  |
| Calibration |  |  | Type B or documented mixed basis | Certificate |  |
| Resolution |  |  | Type B | Justified quantisation model |  |
| Environmental correction |  |  | Type A / Type B as evaluated | Observations or reference information |  |
| Geometry / centring |  |  | Type A / Type B as evaluated | Setup and observation model |  |
| Other input |  |  |  |  |  |

Do not force every project into these rows. Add, remove or split components to reflect the actual measurement process. A component's Type A or Type B designation is determined by how its uncertainty was evaluated, not by the name of the physical effect.

## 8. Application to spatial measurement

The same principles apply across the Spatial Methods collection:

- **Surveying:** repeated angles and distances, centring, calibration, prism constants, atmospheric corrections and control uncertainty.
- **GNSS:** session repeatability, antenna reference-point offsets, satellite geometry, correction services, reference-frame realisation and shared atmospheric or modelling effects.
- **Levelling:** staff scale and temperature effects, collimation, setup variation, refraction and benchmark uncertainty.
- **Remote sensing:** reference data, radiometric calibration, geolocation, classification validation and sampling design.
- **Field data collection:** sensor resolution, mounting geometry, operator effects, timing, feature interpretation and reference observations.

The uncertainty budget must follow the actual measurand and collection method. A generic list of uncertainty components should never be copied unchanged from one technology to another.

## 9. Common mistakes

- Treating Type A as random error and Type B as systematic error.
- Assuming every Type B component is a rectangular distribution.
- Dividing a manufacturer's accuracy specification by \(\sqrt{3}\) without establishing that it is a valid bound for a rectangular model.
- Treating a maximum permissible error as a standard uncertainty without justification.
- Combining components by root-sum-of-squares while ignoring known correlations.
- Dividing every component by \(\sqrt{n}\), including shared setup or calibration effects.
- Treating the sample standard deviation as the standard uncertainty of the mean.
- Reporting \(k=2\) as an exact 95% coverage statement without checking the relevant conditions.
- Adding a component twice because it appears under different names in different documents.

## 10. Evidence and limitations

The core distinctions and examples in this module are based on:

- NIST Technical Note 1297, Sections 2–5 and Appendix A, which describe the Type A / Type B distinction, distribution-based Type B evaluation, and combination of uncertainty components.
- JCGM 100:2008, the legacy GUM core, which should be read in the context of the broader GUM suite and applicable amendments.
- The existing synthetic Exercise A, which provides the repeated-distance observations and an explicitly illustrative budget.

Sources:

- [NIST TN 1297 — Type A evaluation](https://www.nist.gov/pml/nist-technical-note-1297/nist-tn-1297-3-type-evaluation-standard-uncertainty)
- [NIST TN 1297 — Type B evaluation](https://www.nist.gov/pml/nist-technical-note-1297/nist-tn-1297-4-type-b-evaluation-standard-uncertainty)
- [NIST TN 1297 — Combined standard uncertainty](https://www.nist.gov/pml/nist-technical-note-1297/nist-tn-1297-5-combined-standard-uncertainty)
- [NIST TN 1297 — Appendix A: Law of propagation of uncertainty](https://www.nist.gov/pml/nist-technical-note-1297/nist-tn-1297-appendix-law-propagation-uncertainty)
- [BIPM/JCGM 100:2008 — GUM](https://www.bipm.org/en/doi/10.59161/jcgm100-2008)

NIST TN 1297 is a useful, accessible explanatory guide, but it is not a surveying instrument test standard and is not a substitute for the current GUM suite. The synthetic budget is pedagogical and must not be reused as an instrument specification or field accuracy claim.

**Maturity:** introductory module drafted; formulae and worked arithmetic checked; source metadata and claim links recorded; independent technical review and a fuller treatment of degrees of freedom remain outstanding.
