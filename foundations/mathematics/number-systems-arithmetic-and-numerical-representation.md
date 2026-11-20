# Number systems, arithmetic and numerical representation

**Foundation domain:** Mathematics for spatial science  
**Subject ID:** `SM-FND-001`  
**Module:** 02  
**Status:** Initial public foundation; further technical review and expansion required

## 1. Why number representation matters in spatial work

Spatial datasets are full of numbers: coordinates, elevations, distances, areas, pixel values, population counts, timestamps, probabilities, spectral measurements and model outputs.

Yet a number in a file or on a map is not the quantity itself. It is a representation produced by choices about units, scale, storage type, rounding and measurement. Those choices can affect what can be represented, what information is retained and what conclusions are justified.

Consider three values:

- A building height stored as `12` metres.
- A GNSS-derived coordinate stored to eight decimal places.
- A satellite image pixel stored as the integer `143`.

The first may be a rounded measurement, the second may display more decimal places than its uncertainty supports, and the third may be a scaled digital number rather than a direct physical reflectance. The digits alone do not tell us what the values mean.

This module develops the number concepts needed to interpret spatial data responsibly. Detailed floating-point error analysis, numerical conditioning and algorithmic stability are treated in [Numerical analysis and scientific computing](../README.md#subject-map), subject `SM-FND-016`.

## 2. Number systems

A number system defines the values available for counting, measuring or calculation. Different sets of numbers support different operations and have different limitations.

### 2.1 Natural numbers and integers

Natural numbers are commonly used for counting: 1, 2, 3, and so on. Some conventions include zero in the natural numbers; others begin at one. State the convention when it matters.

Integers include negative whole numbers, zero and positive whole numbers:
$$
\mathbb{Z}={\ldots,-3,-2,-1,0,1,2,3,\ldots}
$$

Spatial examples include:

- the number of buildings in a feature collection;
- row and column indices in a raster grid;
- signed offsets from a reference coordinate;
- a count of observations or network edges.

An integer count cannot represent half a building, but a density or estimated population may be non-integer. The appropriate number type depends on the meaning of the quantity.

### 2.2 Rational numbers

A rational number can be expressed as a ratio of two integers, with a non-zero denominator:
$$
\mathbb{Q}=\left\{\frac{p}{q}:p,q\in\mathbb{Z},\ q\neq0\right\}
$$

Examples include:
$$
\frac{1}{2}=0.5,\qquad \frac{3}{4}=0.75,\qquad \frac{1}{3}=0.333\ldots
$$

Rational numbers include terminating and repeating decimal expansions. They are useful for exact fractions, proportions and ratios.

A decimal that terminates in base ten is not necessarily represented exactly in a computer's binary floating-point format. The mathematical number (0.1), for example, has no finite binary expansion. A computer may therefore store a nearby representable value.

### 2.3 Irrational and real numbers

An irrational number cannot be expressed as a ratio of integers. Its decimal expansion neither terminates nor repeats. Examples include $\sqrt{2}$ and $\pi$.

The real numbers, $\mathbb{R}$, include both rational and irrational numbers. They provide the usual mathematical setting for continuous quantities such as idealised lengths, angles and surface values.

In practical computation, real numbers are represented with finite storage. A computer does not store every real number exactly. It stores values from a finite representable set, usually using integer or floating-point formats.

### 2.4 Exact values, defined values and measured values

It is important to distinguish:

- **Exact mathematical values:** values defined by mathematics, such as the integer 8 or the fraction (1/4).
- **Defined or stipulated values:** values adopted by definition or as an explicit model input.
- **Measured values:** values obtained through an observation process and subject to measurement uncertainty.
- **Computed values:** outputs produced by applying a calculation to inputs; their reliability depends on input quality and computational method.

For example, a raster may have a cell width defined as exactly 10 coordinate units in its grid specification. That does not mean the ground footprint is known with zero uncertainty. The coordinate reference, georeferencing, projection and source data may all have their own limitations.

An exact calculation using uncertain inputs does not produce an exact knowledge of the real world.

## 3. Place value and numeral bases

Our everyday decimal system uses base ten. Each digit's position represents a power of ten.

For example:
$$
4{,}207.35 =
4(10^3)+2(10^2)+0(10^1)+7(10^0)
+3(10^{-1})+5(10^{-2})
$$

Computers commonly use binary (base two), whose digits are 0 and 1. Each position represents a power of two.
$$
1011_2=1(2^3)+0(2^2)+1(2^1)+1(2^0)=11_{10}
$$

Hexadecimal (base sixteen) is also widely used in computing. It provides a compact way to express binary values because each hexadecimal digit corresponds to four binary bits.

Why this matters to spatial practitioners:

- data formats specify how numeric values are encoded;
- integer pixel values may use signed or unsigned storage;
- coordinate and attribute fields may have different numeric types;
- binary floating-point cannot exactly represent every decimal fraction;
- software may convert values between storage types when reading, processing or exporting data.

A value's textual appearance does not reveal its underlying representation. Inspect the data type and metadata.

## 4. Arithmetic and order of operations

Arithmetic combines numbers through operations such as addition, subtraction, multiplication and division.

The conventional order of operations is:

1. Parentheses and other explicitly grouped expressions.
2. Exponents and roots.
3. Multiplication and division, evaluated from left to right.
4. Addition and subtraction, evaluated from left to right.

For example:
$$
3+4\times2=3+8=11
$$

whereas:
$$
(3+4)\times2=7\times2=14
$$

In spatial workflows, a missing pair of parentheses can change an area calculation, a coordinate offset, a map-scale conversion or a raster expression. Make precedence explicit in code and technical documentation.

### 4.1 Arithmetic with units

Units should be carried through calculations.

For a rectangular area:
$$
A=lw
$$

If $l=80\,\mathrm{m}$ and $w=25\,\mathrm{m}$:
$$
A=80 \mathrm{m}\times25 \mathrm{m}
=2{,}000 \mathrm{m^2}
$$

For a conversion:
$$
2{,}000 \mathrm{m^2}\times
\frac{1 \mathrm{ha}}{10{,}000 \mathrm{m^2}}
=0.2 \mathrm{ha}
$$

The square-metre units cancel, leaving hectares. Treating units as part of the expression helps catch errors.

### 4.2 Negative values and direction

Negative values often encode a relationship to a chosen origin or convention. They are not inherently errors.

Examples include:

- negative elevation relative to a chosen vertical datum;
- a negative coordinate offset relative to an origin;
- negative temperature in a scale that permits it;
- a signed residual indicating direction of discrepancy;
- a negative change in an environmental measurement.

Always establish what the sign means. A negative residual may mean observed minus computed, or computed minus observed, depending on the defined convention.

## 5. Fractions, decimals and percentages

A fraction expresses a part relative to a whole. A decimal is one way of writing a number in base ten. A percentage expresses a ratio per hundred.
$$
\frac{3}{5}=0.6=60%
$$

These forms are mathematically equivalent, but the choice of representation affects readability and can hide the denominator or reference population.

### Example: classification accuracy

Suppose a hypothetical land-cover assessment correctly classifies 840 of 1,000 reference samples.
$$
\text{Proportion correct}=\frac{840}{1000}=0.84
$$
$$
\text{Percentage correct}=0.84\times100=84%
$$

The percentage is meaningful only with the assessment design and class distribution. It does not, by itself, describe the accuracy of every class or the quality of the reference labels.

## 6. Rounding, truncation and quantisation

These are related but distinct operations.

- **Rounding** replaces a value with a nearby value according to a specified rule.
- **Truncation** removes digits beyond a chosen position without rounding to the nearest value.
- **Quantisation** maps a range of possible values into a finite set of representable levels.

For example, rounding 12.746 to two decimal places gives 12.75 under the usual nearest-value rule. Truncating it to two decimal places gives 12.74.

The rounding rule must be known, especially for values exactly halfway between two representable increments. Different systems may use different tie-breaking conventions, such as ties-to-even or ties-away-from-zero.

### 6.1 Rounding is not measurement improvement

Suppose a distance estimate is 125.4837 m. Reporting it as 125.48 m changes the presentation, not the underlying measurement quality.

If the standard uncertainty is 0.8 m, four decimal places are not informative about the actual knowledge of the distance. Conversely, if a high-quality instrument and method support millimetre-level uncertainty, reporting only whole metres may discard useful information.

Choose reporting precision in relation to the purpose, uncertainty, data specification and downstream use.

### 6.2 Quantisation in raster and sensor data

A sensor or raster data product may store measurements using discrete integer levels. A scale factor and offset can map stored integers to physical values:
$$
x_{\text{physical}}=s\,x_{\text{stored}}+o
$$

where $s$ is the scale factor and $o$ is the offset.

For illustration, if a stored value is 143, the scale factor is 0.01 and the offset is 0:
$$
x_{\text{physical}}=0.01(143)+0=1.43
$$

The physical unit and interpretation must come from the product metadata. The number 143 alone is not a reflectance, temperature or elevation.

Quantisation introduces finite resolution. Its effect depends on the quantisation interval, encoding rule and processing chain. It should not be confused with all other sources of sensor or measurement uncertainty. The distinction between stored values and spatial grid dimensions is developed in Module 08's [raster-resolution worked example](sequences-series-and-approximation.md#81-worked-example-grid-refinement-and-resampling).

## 7. Significant figures and decimal places

**Decimal places** count digits after the decimal point. **Significant figures** describe the digits retained to express a number's magnitude at a stated precision.

For example:

- 12.30 has two decimal places and four significant figures.
- 0.00450 has five decimal places and three significant figures.
- 4,500 may be ambiguous without a convention or scientific notation.

Scientific notation helps remove ambiguity:
$$
4.5\times10^3
$$

has two significant figures, while:
$$
4.500\times10^3
$$

has four significant figures.

Significant figures are a communication convention, not a complete uncertainty model. They do not replace a stated uncertainty, data-quality description or measurement model.

### 7.1 Reporting a measured result

A result and its uncertainty should be rounded and presented consistently. The exact convention depends on the applicable discipline or reporting standard.

For example, if an illustrative result is:
$$
x=125.4837 \mathrm{m},\qquad u=0.78 \mathrm{m}
$$

one possible presentation is:
$$
x=(125.5\pm0.8) \mathrm{m}
$$

where the uncertainty is a standard uncertainty, not necessarily an expanded interval. The report must state what the $\pm$ quantity represents.

Do not round intermediate calculations prematurely if that can affect the final result. Retain suitable internal precision, then round the reported result according to the reporting convention.

## 8. Integer and floating-point storage

Digital spatial systems use finite storage types. Two broad numeric families are common.

### 8.1 Integers

Integer types represent whole numbers within a finite range. The range depends on the number of bits and whether the type is signed or unsigned.

An unsigned 8-bit integer represents values from 0 to 255. A signed 8-bit two's-complement integer represents values from -128 to 127.

These ranges matter when storing:

- raster class codes;
- image digital numbers;
- row and column indices;
- counts and categorical attributes;
- scaled integer measurements.

If a value exceeds the type's range, software may reject it, flag an error, wrap it or convert it, depending on the format and operation. Never assume overflow is handled safely.

### 8.2 Floating-point numbers

Floating-point formats represent a wide range of values using a finite number of significant binary digits and an exponent. They support approximate real-number arithmetic over a large range.

Most decimal fractions cannot be represented exactly in binary floating point. A familiar example is 0.1. Its stored value is a nearby binary approximation, not the exact rational value one tenth.

Consequently, a calculation may produce a result such as 0.30000000000000004 instead of a displayed 0.3. This is not necessarily evidence of a faulty algorithm; it can be a consequence of finite representation.

For ordinary spatial workflows, the practical lessons are:

- do not test floating-point equality casually when a tolerance-based comparison is appropriate;
- do not assume repeated calculations preserve exact decimal values;
- do not use more decimal places as evidence of greater accuracy;
- inspect the declared data type when importing, transforming or exporting data;
- understand the effects of conversion between integer and floating-point formats.

The deeper theory of floating-point arithmetic, cancellation, conditioning, error propagation and numerical stability belongs in `SM-FND-016`.

## 9. Coordinate magnitude, precision and resolution

Coordinate values may be large because of the chosen coordinate system and origin. A small local displacement can be represented as the difference between two large coordinate values.

For example, consider two projected easting values:
$$
E_1=500{,}000.000 \mathrm{m}
$$
$$
E_2=500{,}000.025 \mathrm{m}
$$

Their difference is:
$$
\Delta E=E_2-E_1=0.025 \mathrm{m}
$$

The difference is 25 mm. The number of decimal places displayed does not establish that the positions are known to 1 mm, nor does it establish that the coordinate values were stored or processed without numerical effects.

Keep these concepts distinct:

- **Precision of representation:** the granularity or fineness with which a value can be represented or stored.
- **Measurement precision:** the closeness of repeated indications under specified conditions.
- **Measurement accuracy:** closeness of agreement between a measured value and a true quantity value, with the usual metrological caveats.
- **Resolution:** the smallest change in a quantity that produces a perceptible change in an indication or representation, as defined for the relevant system.
- **Uncertainty:** a parameter characterising the dispersion of values attributed to a measurand, based on the information used.

These terms are related but not interchangeable. A coordinate field with many decimal places may hold a low-quality position. A coarser display may still represent a high-quality measurement adequately for a particular purpose.

## 10. Worked spatial examples

### Example A — Raster storage and scale factor

A hypothetical elevation raster stores the integer value 2,347. Its metadata specifies a scale factor of 0.1 and an offset of 0.
$$
z=0.1(2347)+0=234.7
$$

If the metadata specifies metres, the decoded value is 234.7 m. Without the scale factor and unit, reporting 2,347 m would be incorrect.

This example is illustrative. Actual raster products may use different scaling, offsets, units, NoData codes and processing conventions.

### Example B — Converting a count to density

A study area contains 7,250 mapped building footprints within an area of 2.5 km².
$$
D=\frac{7250}{2.5}=2900 \mathrm{buildings/km^2}
$$

This is a count density of mapped building footprints, not a population density or a measure of building floor area. It depends on the feature definition, completeness of the building dataset and study boundary.

### Example C — Rounding a coordinate for display

A coordinate value is stored as 36.8219467 degrees. A map label displays 36.8219 degrees.

The display has been rounded to four decimal places. It does not follow that the source coordinate is accurate to four decimal places, nor that the rounded value should replace the stored source value in analysis.

For latitude, a degree corresponds to roughly 111 km, but the ground distance represented by a degree of longitude varies with latitude. This is one reason angular coordinate precision should not be casually interpreted as a fixed ground precision.

## 11. A practical checklist for numeric spatial data

When receiving or publishing a spatial dataset, ask:

1. What does each numeric field represent?
2. What are its units, scale factor and offset?
3. Is the field an integer, floating-point value, decimal or text encoding?
4. Is the value measured, computed, estimated, classified or stipulated?
5. What are the permitted range and missing-value conventions?
6. Has rounding, truncation, quantisation or rescaling occurred?
7. What precision is needed for the intended analysis?
8. What uncertainty or quality information accompanies the value?
9. Have conversions or exports changed the storage type or value?
10. Are the displayed digits appropriate to the evidence and use?

## 12. Common mistakes

| Mistake | Why it is problematic | Better practice |
|---|---|---|
| Treating every decimal as exact | Finite storage and measurement processes may make it approximate | Identify how the value was defined, measured and stored |
| Equating decimal places with accuracy | Display precision says little about closeness to truth | Use measurement quality and uncertainty information |
| Ignoring scale factors and offsets | Stored digital numbers may not be physical quantities | Read product metadata before interpreting pixel values |
| Converting integer data without checking range | Values may overflow, be clipped or lose information | Inspect types and test conversions |
| Rounding intermediate values repeatedly | Small changes can accumulate or affect later calculations | Retain appropriate working precision |
| Comparing floating-point values by exact equality | Approximate binary representation can make equality tests fragile | Use a justified tolerance or suitable comparison method |
| Treating a raster's integer code as a measurement unit | Class codes and digital numbers may be categorical or scaled | Read the band description and data specification |
| Reporting too many digits | Implies a level of knowledge not supported by the data | Match reporting precision to purpose and uncertainty |

## 13. Exercises

### Exercise 1 — Identify the number type

Classify each item as an integer, rational number, irrational number or approximate digital representation. More than one description may apply depending on context.

1. The count of 87 road segments.
2. The fraction $1/3$.
3. The value $\pi$ used in a circular-area formula.
4. A sensor value stored as an unsigned 16-bit integer.
5. A coordinate stored in a floating-point field.

Explain what additional information is needed to interpret each as a spatial quantity.

### Exercise 2 — Scale factor

A raster stores a pixel value of 3,680. Its metadata states a scale factor of 0.01 and an offset of -5.

1. Calculate the decoded value.
2. What unit is the answer in?
3. Why can the unit not be inferred from the arithmetic?
4. What could go wrong if the scale factor were ignored?

### Exercise 3 — Precision and uncertainty

A report gives a distance as 1,234.56789 m, with a stated expanded uncertainty of 0.12 m.

1. Explain why the number of decimal places is misleading.
2. Suggest a more consistent presentation.
3. State what additional information is required to interpret the expanded uncertainty.

### Exercise 4 — Storage range

A categorical raster uses an unsigned 8-bit integer type.

1. What is its representable integer range?
2. Can it represent the class code 260?
3. What alternative storage choice could accommodate that code?
4. Why should NoData codes be considered when selecting a data type?

### Exercise 5 — Coordinate display

A dataset stores longitude as 36.8219467 degrees, but a map label shows 36.822 degrees.

1. What operation produced the displayed value?
2. Has the source dataset necessarily changed?
3. Does the displayed precision establish positional accuracy?
4. Name the metadata needed before interpreting the coordinate geographically.

### Exercise 6 — Diagnose a numeric workflow

A GIS workflow reads a 16-bit integer elevation raster, converts it to an 8-bit integer, divides by 10 and exports the result.

Identify at least five questions you would ask before accepting the output. Consider range, negative values, rounding, scale, NoData, units and information loss.

## 14. Connections to other foundations and methods

- **Measurement science (`SM-FND-011`):** distinguishes measured values, uncertainty, resolution and reporting.
- **Numerical analysis (`SM-FND-016`):** develops floating-point representation, rounding error, conditioning, stability and numerical algorithms.
- **Remote sensing physics (`SM-FND-012`):** explains the physical meaning of radiometric quantities and the interpretation of sensor digital numbers.
- **Signal processing (`SM-FND-014`):** develops sampling, quantisation, discretisation and signal representation.
- **Linear algebra (`SM-FND-002`):** uses numeric vectors and matrices in coordinate transformations, adjustment and spatial modelling.
- **Spatial algorithms:** use numeric data types, tolerances and arithmetic in geometric predicates, raster processing and optimisation.
- **Spatial data collection:** produces measurements and observations whose resolution, calibration and uncertainty must be understood.
- **Spatial recipes:** should document input types, scaling, conversions, precision and output semantics.

## 15. Summary

Number representation is part of spatial reasoning. Integers, fractions, real-number models and finite digital formats serve different purposes. Rounding, truncation, quantisation and storage conversion can change the information available to later analysis.

A responsible spatial workflow does not interpret digits in isolation. It asks what the number represents, how it was produced, how it is stored, what units and metadata govern it, and what precision the evidence supports.

## Further reading and related resources

- [Mathematical language, quantities and spatial models](mathematical-language-quantities-and-spatial-models.md)
- [Mathematics for spatial science roadmap](README.md)
- [Measurement science foundations](../measurement-science/measurement-principles-and-field-verification.md)
- [Standard uncertainty: Type A and Type B evaluation](../measurement-science/standard-uncertainty-type-a-type-b.md)
- [Master subject index](../../catalog/master-subject-index.md)

This module introduces numeric representation and reporting. It does not provide a full treatment of floating-point error analysis, numerical conditioning or computational stability; those belong in the numerical analysis foundation.


## References and further reading

The explanations and spatial examples in this module are original Spatial Methods teaching material. These references support the treatment of quantities, SI units and digital numeric representation.

1. **Bureau International des Poids et Mesures (BIPM).** (2026). *The International System of Units (SI Brochure)*, 9th edition, version 4.01. [Official publication](https://www.bipm.org/en/si-brochure-9). Relevant sections: 2.3.3–2.3.4 and 5.4, including the expression of quantity values, units and uncertainty.
2. **IEEE Standards Association.** (2019). *IEEE Standard for Floating-Point Arithmetic*, IEEE Std 754-2019. [Standard catalogue record](https://standards.ieee.org/ieee/754/6210/). The public catalogue describes the scope of binary and decimal floating-point formats and operations. The normative standard text was not accessed for this module; no clause-level claims are made.
3. **Goldberg, D.** (1991). “What Every Computer Scientist Should Know About Floating-Point Arithmetic.” *ACM Computing Surveys*, 23(1), 5–48. [Oracle-hosted reprint](https://docs.oracle.com/cd/E19957-01/806-3568/ncg_goldberg.html). Used for finite binary representation and rounding behaviour. Copyright remains with ACM; this is a link-only reference.
4. **Thompson, A. and Taylor, B. N.** (2008). *Guide for the Use of the International System of Units (SI)*, NIST Special Publication 811. [NIST publication record](https://doi.org/10.6028/NIST.SP.811e2008). A practical guide to SI usage; consult the current BIPM brochure where later updates matter.

**Source register:** `SM-SRC-000022`, `SM-SRC-000023`, `SM-SRC-000025`, `SM-SRC-000027`.

**Limitations:** This is an introductory treatment, not a full account of floating-point arithmetic, numerical error analysis or storage-format specifications. IEEE 754 is a technical standard; its public catalogue page does not provide the complete normative text.
