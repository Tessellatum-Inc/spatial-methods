# Floating-point numbers, rounding and computational error

**Subject identity:** `SM-FND-016` — Numerical analysis and scientific computing  
**Module:** 01  
**Status:** Initial public teaching resource; independent numerical-analysis review and learner testing outstanding.

## 1. Why numerical analysis matters in spatial science

A spatial computation usually begins with quantities represented by finite strings of bits: coordinates, elevations, angles, reflectances, distances, covariance entries or model parameters. Mathematical models often treat these quantities as real numbers. Computers generally do not store arbitrary real numbers exactly.

This difference matters. A coordinate transformation may accumulate rounding error; a geometric predicate may classify a nearly collinear configuration differently after rounding; an iterative solver may stop before reaching a useful solution; and a raster derivative may amplify small input perturbations.

Numerical analysis provides a disciplined way to ask four different questions:

1. **Representation:** can the computer store the input value exactly?
2. **Problem sensitivity:** how much can the correct answer change when the input changes slightly?
3. **Algorithmic stability:** how much additional error does the chosen procedure introduce?
4. **Decision fitness:** is the computed result accurate enough for the spatial purpose?

These questions are related but not interchangeable.

## 2. Real numbers and finite representations

The real numbers form a continuous mathematical system. A digital computer has a finite set of representable values for each numeric data type.

A common format is IEEE 754 binary64 (often called double precision). It uses 64 bits: one sign bit, 11 exponent bits and 52 explicitly stored fraction bits, with an implicit leading significand bit for normal numbers. Its significand precision is therefore 53 binary digits.

The spacing between adjacent representable numbers depends on magnitude. Near 1, adjacent normal binary64 numbers are separated by \(2^{-52}\). At larger magnitudes the spacing grows; at smaller magnitudes it shrinks until the subnormal range is reached.

The format can represent many integers exactly, but not every integer of arbitrary size. All integers with magnitude no greater than \(2^{53}\) are exactly representable in binary64; above that threshold, not every consecutive integer is representable.

A decimal fraction such as \(0.1\) has no finite binary expansion. Its stored binary64 value is a nearby representable number, not exactly one tenth. Consequently, an expression such as

\[
0.1 + 0.2
\]

may produce a stored result whose decimal display is slightly different from \(0.3\). The display formatting may hide or reveal that difference; formatting does not change the underlying value.

**Important:** a displayed decimal is not a complete account of the stored binary value. Inspect the data type and, when necessary, use a representation that exposes the stored value.

## 3. Rounding and unit roundoff

A basic model for a correctly rounded floating-point operation is

\[
\operatorname{fl}(a \circ b)
=
(a \circ b)(1+\delta),
\qquad |\delta| \leq u,
\]

where:

- \(\circ\) is an arithmetic operation;
- \(\operatorname{fl}\) denotes the computed floating-point result;
- \(u\) is the unit roundoff;
- \(\delta\) is the relative rounding error for that operation.

For binary64 under round-to-nearest, the unit roundoff is

\[
u = 2^{-53} \approx 1.11\times 10^{-16}.
\]

The bound is a useful local model, not a universal guarantee for every expression. It assumes a normal finite result and the specified rounding behaviour. Overflow, underflow, subnormal values, invalid operations, non-default rounding modes and library functions require additional care.

Do not confuse unit roundoff \(u\) with machine epsilon. In common numerical software, machine epsilon is the gap between 1 and the next larger representable number, \(2^{-52}\) for binary64. Under round-to-nearest, unit roundoff is half that spacing.

## 4. Absolute and relative error

If \(x\) is the exact value and \(\hat{x}\) is an approximation, the absolute error is

\[
E_{\mathrm{abs}} = |\hat{x}-x|.
\]

When \(x\neq 0\), the relative error is

\[
E_{\mathrm{rel}} =
\frac{|\hat{x}-x|}{|x|}.
\]

Absolute error is expressed in the units of the quantity. Relative error is dimensionless and describes the error in relation to the magnitude of the exact value.

Neither measure is sufficient in every situation. Relative error becomes uninformative when the exact value is zero or very close to zero. Absolute error can be misleading when values span several orders of magnitude.

For a spatial quantity, always interpret error against the purpose and units. A 0.02 m error may be material for setting out a building corner, negligible for a regional overview, and unacceptable for a high-precision control network. The acceptable tolerance is a property of the task and its acceptance criteria, not a universal property of floating-point arithmetic.

## 5. Cancellation and loss of significant digits

Subtraction of nearly equal numbers can remove leading significant digits. This is called cancellation. The operation may expose errors already present in the inputs.

Consider two large coordinates whose difference is small. If the coordinates have already been rounded to a spacing larger than the separation of interest, subtracting them cannot recover the lost information. For example, in binary64, \(10^{16}+1\) rounds to the same representable value as \(10^{16}\) under round-to-nearest. Their computed difference can therefore be zero even though the exact mathematical difference is one.

This example is deliberately extreme, but the principle applies to any coordinate system or numeric field whose magnitude is large relative to the precision needed for local differences.

A common mitigation is to work in a suitable local coordinate frame or subtract a local origin before subsequent calculations. This can reduce the magnitude of intermediate values and improve numerical behaviour. It does **not** recover precision already lost when the original coordinates were created, parsed or stored. Preserve the source values and document any local-origin transformation.

Cancellation is not always evidence of a defective algorithm: sometimes the desired result is intrinsically small relative to the inputs. It is a warning to examine the problem's conditioning and the algorithm's formulation.

## 6. Overflow, underflow and exceptional values

Floating-point arithmetic has finite range.

- **Overflow** occurs when a result is too large to be represented as a finite value in the selected format. It may produce positive or negative infinity.
- **Underflow** occurs when a non-zero result is too small to be represented as a normal value. Subnormal values extend the range with reduced precision; sufficiently small results may round to zero.
- **Not-a-Number (NaN)** represents an undefined or unrepresentable numeric result, such as \(0/0\) or \(\sqrt{-1}\) in a real-valued calculation.
- **Infinity** may propagate through later operations and can make an output appear numeric while being unusable.

Spatial pipelines should explicitly check for non-finite values before accepting outputs. A raster with a few infinities, a coordinate table containing NaNs, or an optimisation result with non-finite objective values should not silently pass a quality gate.

Missing data and NaN are not always interchangeable. File formats and libraries may use explicit NoData sentinels, masks, nulls or NaN values. The chosen representation must be handled consistently.

## 7. Conditioning is a property of the problem

A problem is well-conditioned when small relative changes in its input produce comparably small relative changes in its answer. It is ill-conditioned when small input changes can produce large answer changes.

For a differentiable scalar function \(y=f(x)\), a local relative condition number is

\[
\kappa_f(x)
=
\left|
\frac{x f'(x)}{f(x)}
\right|,
\]

when the expression is defined and the relevant quantities are non-zero.

A large condition number indicates sensitivity. It does not by itself show that an algorithm is poor. Even a numerically stable algorithm cannot generally produce a highly accurate answer to a severely ill-conditioned problem when the input itself is uncertain or rounded.

For a nonsingular linear system

\[
A\mathbf{x}=\mathbf{b},
\]

the condition number of \(A\), in a chosen compatible norm, is

\[
\kappa(A)=\|A\|\,\|A^{-1}\|.
\]

The condition number depends on the norm and can be large when the system is close to singular. Scaling and units matter: rescaling variables can change the numerical condition of a representation, and a physically meaningful model should not be judged from a condition number without understanding the parameterisation.

Conditioning belongs to the mathematical problem and its representation. It is distinct from algorithmic stability.

## 8. Stability is a property of the algorithm

A numerically stable algorithm controls the error introduced by its computational steps. Informally, a backward-stable algorithm returns the exact solution to a nearby problem, where “nearby” is measured in a stated norm or error model.

For a computed solution \(\hat{\mathbf{x}}\) to \(A\mathbf{x}=\mathbf{b}\), the residual is

\[
\mathbf{r}=\mathbf{b}-A\hat{\mathbf{x}}.
\]

A small residual is useful, but it does not guarantee a small forward error \(\|\hat{\mathbf{x}}-\mathbf{x}\|\) when \(A\) is ill-conditioned. Residual size, conditioning and solution error must be considered together.

This distinction explains why a solver can behave stably and still return a solution with limited accuracy for a sensitive problem. It also explains why a small residual alone is not a complete validation test.

## 9. A spatial example: local coordinate differences

Suppose a dataset contains projected coordinates \(E\) and \(N\) in metres. A local displacement between two points is

\[
\Delta E = E_2-E_1,
\qquad
\Delta N = N_2-N_1,
\]

and its planar length is

\[
d = \sqrt{(\Delta E)^2+(\Delta N)^2}.
\]

The formula is exact in the Euclidean plane. A computed value can still be affected by:

- the precision with which the original coordinates were stored;
- rounding during coordinate transformation;
- cancellation when subtracting large, nearly equal values;
- overflow or underflow in squared terms for extreme magnitudes;
- the suitability of the projected coordinate system for the intended distance;
- the fact that grid distance is not necessarily ground distance.

A numerically careful implementation may use a stable hypotenuse function rather than directly evaluating the square root of two squared terms, especially when magnitudes can be extreme. But numerical stability does not resolve projection distortion or measurement uncertainty. Those are separate parts of the model.

## 10. Practical numerical hygiene

For a spatial computation:

1. Record numeric types and coordinate units at input boundaries.
2. Preserve original values before casting, rounding or rescaling.
3. Check for NaN and infinite values explicitly.
4. Use local coordinate origins or appropriate scaling where justified, while preserving the transformation.
5. Prefer well-understood numerical routines over ad hoc formulas for sensitive operations.
6. Select tolerances from the task's accuracy requirement and the algorithm's behaviour, not from a convenient default.
7. Test values near boundaries, degeneracies, zero and the expected magnitude range.
8. Compare against independent checks where possible: analytic cases, higher-precision calculations, invariants, known control values or a separately implemented method.
9. Record software versions, library versions, data types and relevant solver settings.
10. Report numerical tolerance separately from observational uncertainty and acceptance tolerance.

Do not use an arbitrary epsilon to make every comparison “work.” A tolerance should be tied to scale, units, conditioning, algorithm behaviour and the decision being made.

## 11. Exercises

### Exercise 1 — Representation

Explain why decimal \(0.1\) is not exactly representable in binary floating point. Distinguish the stored value from the decimal string displayed by software.

### Exercise 2 — Absolute and relative error

A computed distance is \(100.02\ \mathrm{m}\), while a reference value is \(100.00\ \mathrm{m}\). Calculate absolute and relative error. State why this calculation alone does not determine whether the result is acceptable.

### Exercise 3 — Coordinate magnitude

Explain why subtracting two coordinates with a large common offset can be numerically risky. Describe one mitigation and one limitation of that mitigation.

### Exercise 4 — Residual and conditioning

A linear solver returns a small residual for a system with a large condition number. Explain why the residual alone does not establish an accurate solution.

### Exercise 5 — Error classification

Classify each issue as primarily a representation, conditioning, algorithmic stability, measurement uncertainty or model-validity issue. Some cases may involve more than one:
- decimal input rounded to binary64;
- a nearly singular least-squares design matrix;
- a biased GNSS observation;
- a projection unsuitable for a long ground-distance measurement;
- a cancellation-prone formula.

## 12. Answers and discussion

1. The binary expansion of \(0.1\) repeats indefinitely, so binary64 stores a nearby value. Decimal formatting may display a short rounded string rather than the exact stored value.
2. Absolute error is \(0.02\ \mathrm{m}\). Relative error is \(0.02/100=0.0002\), or \(0.02\%\). Acceptance depends on the intended use, reference quality, measurement uncertainty and stated tolerance.
3. The stored coordinate spacing increases with magnitude, so small differences may be rounded away. A local origin can reduce intermediate magnitudes, but cannot restore precision lost before the shift.
4. A small residual means the computed vector nearly satisfies the represented equations. In an ill-conditioned system, small perturbations in the equations can correspond to large changes in the solution.
5. The decimal conversion is representation; near singularity is conditioning; a biased GNSS observation is measurement uncertainty or systematic measurement error; unsuitable projection is model validity; a cancellation-prone formula is algorithmic stability, with the actual impact also depending on conditioning.

## 13. Connections to other Spatial Methods resources

- [Linear algebra and matrix methods](../linear-algebra/README.md) supplies the algebraic structures used in numerical solution.
- [Measurement science](../measurement-science/measurement-principles-and-field-verification.md) distinguishes observation uncertainty, calibration and verification from computational error.
- [Coordinate transformation and CRS axis order](../../algorithms/geodesy/crs-transformation.md) is a practical location where units, axis order, precision and numerical checks meet.
- [Precision models and snap rounding](../../algorithms/geometry/precision-models.md) addresses finite coordinate precision in geometric computation.
- [Survey-to-spatial-dataset recipe](../../recipes/survey-to-spatial-dataset/README.md) provides an end-to-end context for preserving source data and validating derived outputs.

## 14. Further reading

- David Goldberg, “What Every Computer Scientist Should Know About Floating-Point Arithmetic,” *ACM Computing Surveys*, 1991. DOI: [10.1145/103162.103163](https://doi.org/10.1145/103162.103163).
- Nicholas J. Higham, *Accuracy and Stability of Numerical Algorithms*, 2nd edition, SIAM, 2002. DOI: [10.1137/1.9780898718027](https://doi.org/10.1137/1.9780898718027).
- IEEE, *IEEE Standard for Floating-Point Arithmetic (IEEE 754-2019)*. The standard defines floating-point formats and arithmetic behaviour; consult the licensed standard for normative details.

These references are starting points for review, not a claim that every statement in this module has been independently checked against the full texts.
