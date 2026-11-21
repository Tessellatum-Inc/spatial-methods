# Numerical stability and backward error

**Subject identity:** \`SM-FND-016\` — Numerical analysis and scientific computing  
**Module:** 03  
**Status:** Initial public teaching resource; independent numerical-analysis review and learner testing outstanding.

## 1. Accuracy is not only about the number of digits

A numerical algorithm transforms represented inputs into a computed result. Each operation may introduce rounding, and the sequence of operations can amplify, suppress or redistribute those errors.

An algorithm is **numerically stable** when it controls the errors introduced by computation in a meaningful sense. Stability is not the same as exactness, and it is not the same as the conditioning of the mathematical problem:

- **Conditioning** describes how sensitive the mathematical answer is to perturbations in the input.
- **Stability** describes how the computational algorithm behaves in the presence of finite-precision arithmetic.
- **Accuracy** describes how close the computed result is to the intended exact or reference result under a stated error measure.

A well-conditioned problem can be solved poorly by an unstable algorithm. An ill-conditioned problem can be solved by a stable algorithm, but the attainable forward accuracy may still be limited by the problem's sensitivity.

## 2. Forward error and backward error

Let \(x\) be the exact solution to a problem and \(\hat{x}\) the computed approximation. The **forward error** measures the difference between the computed and exact answers. In a norm,

\[
E_{\mathrm{forward}}=\|\hat{x}-x\|.
\]

Forward error is often what an application ultimately cares about, but the exact answer may not be available.

Backward error asks a different question: is the computed answer the exact solution to a nearby problem? For a problem defined by \(F(x)=b\), one may seek a perturbation \(\Delta b\), or perturbations to both \(F\) and \(b\), such that

\[
F(\hat{x})=b+\Delta b.
\]

The size of the smallest admissible perturbation, measured relative to the problem data and under a stated model, is a backward-error measure.

For a linear system \(Ax=b\), the residual is

\[
r=b-A\hat{x}.
\]

Thus,

\[
A\hat{x}=b-r.
\]

The computed vector \(\hat{x}\) is the exact solution of a system with a perturbed right-hand side \(b-r\), provided \(A\) is treated as exact. The residual is therefore directly related to one form of backward error. A normwise relative residual is commonly reported as

\[
\eta =
\frac{\|b-A\hat{x}\|}
{\|A\|\,\|\hat{x}\|+\|b\|},
\]

when the denominator is non-zero. This is a useful scale-aware diagnostic, but the exact definition of backward error depends on which parts of the data may be perturbed and how those perturbations are measured.

A small residual does not automatically imply a small forward error.

## 3. The link between conditioning, backward error and forward error

For a nonsingular linear system, a stable method may produce a solution with a small backward error. The condition number then determines how strongly that small perturbation can affect the solution.

A standard first-order relationship is

\[
\frac{\|\hat{x}-x\|}{\|x\|}
\lesssim
\kappa(A)\,\eta,
\]

where \(\kappa(A)=\|A\|\,\|A^{-1}\|\), and \(\eta\) represents an appropriate relative backward error. This is a conceptual bound under a consistent normwise perturbation model; precise bounds include denominator factors and assumptions on the perturbation size.

The practical interpretation is important:

- If \(\kappa(A)\) is moderate and \(\eta\) is small, good forward accuracy may be expected.
- If \(\kappa(A)\) is large, even a very small backward error may correspond to substantial forward error.
- If the problem is singular or nearly singular, the solution may not be uniquely or reliably determined.

Do not compare a residual from one scaling or norm with a condition number from another and assume the product has a rigorous interpretation. Norms, scaling, perturbation model and units must be compatible.

## 4. Why operation order matters

Floating-point arithmetic is not associative. In exact arithmetic,

\[
(a+b)+c=a+(b+c),
\]

but the two floating-point evaluation orders can produce different results because each intermediate sum is rounded.

For example, when a very large value and a much smaller value are added, the smaller value may be lost at the precision of the larger one. If a later operation subtracts the large value, the lost contribution cannot be recovered.

This matters in spatial data processing when aggregating values with very different magnitudes, summing areas or weights, accumulating long coordinate offsets, or evaluating expressions that subtract nearly equal quantities.

Changing operation order is not automatically an improvement. A reformulation should be justified mathematically, tested against reference cases and evaluated over the expected input range.

## 5. Summation and compensated arithmetic

A naive floating-point sum evaluates a sequence of additions and rounds each intermediate result. Its error can grow with the number of terms and with cancellation.

A compensated summation method, such as Kahan summation, maintains a correction for low-order information lost during addition. A common form is:

\[
s_0=0,\qquad c_0=0,
\]

and for each input \(x_i\),

\[
y_i=x_i-c_i,
\]

\[
t_i=s_{i-1}+y_i,
\]

\[
c_i=(t_i-s_{i-1})-y_i,
\]

\[
s_i=t_i.
\]

The final \(s_n\) is the compensated sum. This method can substantially improve accuracy for many sequences, but it is not exact and does not eliminate all possible error. The best summation strategy depends on data, precision, ordering and implementation. Pairwise or tree-based summation can also reduce error growth and may parallelise efficiently.

For raster aggregation, weighted statistics or large point collections, record the summation method when numerical reproducibility or small differences matter.

## 6. Stable reformulation: the quadratic formula

Consider the quadratic equation

\[
ax^2+bx+c=0,
\]

with discriminant

\[
D=b^2-4ac.
\]

The textbook roots are

\[
x_{\pm}=\frac{-b\pm\sqrt{D}}{2a}.
\]

When \(b\) and \(\sqrt{D}\) are close in magnitude, one numerator can subtract nearly equal quantities. This cancellation can destroy significant digits in that root.

A common stable reformulation defines

\[
q=-\frac{1}{2}\left(b+\operatorname{sign}(b)\sqrt{D}\right),
\]

then computes

\[
x_1=\frac{q}{a},
\qquad
x_2=\frac{c}{q},
\]

for the real-root case where the expression is valid and \(q\neq0\). This avoids the cancellation-prone numerator for one root and obtains the other through the product relation \(x_1x_2=c/a\).

A production implementation must still handle degenerate cases, zero coefficients, discriminant rounding, overflow/underflow and complex roots. This example illustrates the principle: algebraically equivalent expressions can have very different numerical behaviour.

## 7. Least squares: avoid squaring the condition number unnecessarily

For an overdetermined linear least-squares problem,

\[
\min_x \|Ax-b\|_2,
\]

one might form the normal equations

\[
A^\mathsf{T}Ax=A^\mathsf{T}b.
\]

In the 2-norm, for full-column-rank \(A\),

\[
\kappa_2(A^\mathsf{T}A)=\kappa_2(A)^2.
\]

Forming the normal equations therefore squares the condition number. If \(A\) is already poorly conditioned, this can make the numerical problem substantially worse.

QR factorisation solves the least-squares problem without explicitly forming \(A^\mathsf{T}A\). Singular value decomposition (SVD) provides further diagnostic information about rank and near-dependence, though it is generally more computationally expensive.

This does not mean normal equations are never appropriate. They may be acceptable for well-conditioned problems where computational cost, structure and precision justify their use. The method choice should be based on conditioning, rank, scale, required accuracy and available solver guarantees.

## 8. Geometric predicates and near-degenerate configurations

Computational geometry often makes discrete decisions from floating-point quantities. An orientation test, for example, may use the sign of a determinant:

\[
\operatorname{orient}(a,b,c)=
\begin{vmatrix}
b_x-a_x & b_y-a_y\\
c_x-a_x & c_y-a_y
\end{vmatrix}.
\]

The sign distinguishes clockwise, counter-clockwise and collinear configurations in exact planar arithmetic. If the points are nearly collinear, rounding can change the sign and therefore change a topological or combinatorial decision.

This is not merely a small coordinate error: it can alter whether segments are considered to intersect, whether a polygon is valid, or how a triangulation is constructed.

Robust geometric systems may use adaptive precision, filtered predicates, exact arithmetic for critical decisions, or carefully defined precision models. A fixed arbitrary epsilon is not a universal solution: its meaning depends on coordinate scale, units and the predicate. Consult the repository's geometry precision-model resources for the domain-specific treatment.

## 9. Stable does not mean universally correct

A stable numerical method can faithfully solve the wrong model. It can also faithfully process incorrectly referenced coordinates, inconsistent units, biased observations or invalid geometry.

Before accepting a computed spatial result, ask:

1. Is the mathematical model appropriate for the physical quantity?
2. Are the inputs correctly referenced, scaled and unit-consistent?
3. Is the problem well-conditioned over the actual data range?
4. Does the algorithm have suitable stability properties?
5. Is the residual or backward error acceptable?
6. Does an independent validation test support the result?
7. Is the resulting accuracy sufficient for the decision?

Numerical stability is one part of a complete evidence chain, not a substitute for domain validation.

## 10. Practical stability assessment

For a spatial algorithm or implementation:

- identify the arithmetic precision and relevant library routines;
- identify cancellation-prone expressions and long accumulations;
- inspect conditioning and scaling;
- prefer stable factorizations and tested numerical kernels;
- report residuals and backward-error measures where appropriate;
- test ill-conditioned, near-degenerate and extreme-magnitude cases;
- compare with analytic, high-precision or independently derived reference cases;
- distinguish numerical tolerance from measurement uncertainty and application acceptance criteria;
- record software versions and configuration needed to reproduce the result.

Tests should include cases where a method is expected to fail or lose accuracy. A suite containing only ordinary inputs cannot establish robust numerical behaviour.

## 11. Exercises

### Exercise 1 — Residual interpretation

For \(A\hat{x}\) close to \(b\), explain what a small residual establishes and why it does not by itself establish a small forward error.

### Exercise 2 — Conditioning

A stable solver produces a relative backward error of approximately \(10^{-12}\) for a system with condition number \(10^8\). Explain why the forward error may be much larger than the backward error. Treat the product as an order-of-magnitude warning, not a guaranteed exact bound.

### Exercise 3 — Summation

Explain why the sequence \(10^{16}, 1, -10^{16}\) may sum differently under different floating-point evaluation orders. What does compensated summation attempt to preserve?

### Exercise 4 — Least squares

Explain why forming \(A^\mathsf{T}A\) can be undesirable when \(A\) is ill-conditioned. Name two alternative factorizations and describe one trade-off.

### Exercise 5 — Geometric decisions

Explain why a near-zero orientation determinant is a robustness problem rather than merely a request to choose a smaller epsilon.

## 12. Answers and discussion

1. A small residual shows that the computed vector nearly satisfies the represented equations under the chosen residual measure. If the system is ill-conditioned, a small perturbation in the equations can correspond to a large solution change.
2. The product \(\kappa\eta\) is about \(10^{-4}\), illustrating that a small backward error may permit a much larger forward error for a sensitive system. Exact bounds depend on the perturbation model and assumptions.
3. Adding 1 to \(10^{16}\) may round back to \(10^{16}\), so that contribution can disappear before the final subtraction. A different order can preserve it. Compensated summation tracks part of the low-order information lost during addition.
4. The normal equations square the 2-norm condition number. QR avoids explicitly forming the normal equations; SVD also reveals near-rank-deficiency but typically costs more.
5. The sign of the determinant drives a discrete geometric classification. When the exact determinant is close to zero, rounding can change the sign. Robust predicates need a scale-aware error strategy or stronger arithmetic, not an arbitrary universal threshold.

## 13. Connections to other Spatial Methods resources

- [Linear algebra and matrix methods](../linear-algebra/README.md) explains matrix factorisation, rank and least squares.
- [Least squares and constrained systems](../linear-algebra/least-squares-and-constrained-systems.md) provides the mathematical and estimation context.
- [Precision models and snap rounding](../../algorithms/geometry/precision-models.md) addresses robust geometric computation.
- [Covariance GLS implementation](../../implementations/python/covariance-gls/README.md) connects numerical solution to covariance-aware estimation.
- [Coordinate transformation and CRS axis order](../../algorithms/geodesy/crs-transformation.md) illustrates why stable arithmetic must be combined with correct spatial reference semantics.

## 14. Further reading

- Nicholas J. Higham, *Accuracy and Stability of Numerical Algorithms*, 2nd edition, SIAM, 2002. DOI: [10.1137/1.9780898718027](https://doi.org/10.1137/1.9780898718027).
- James W. Demmel, *Applied Numerical Linear Algebra*, SIAM, 1997. DOI: [10.1137/1.9781611971446](https://doi.org/10.1137/1.9781611971446).
- Jonathan Richard Shewchuk, “Adaptive Precision Floating-Point Arithmetic and Fast Robust Geometric Predicates,” *Discrete & Computational Geometry*, 1997. DOI: [10.1007/PL00009321](https://doi.org/10.1007/PL00009321).

These references are starting points for technical review, not a claim that every statement has been independently checked against the full texts.
