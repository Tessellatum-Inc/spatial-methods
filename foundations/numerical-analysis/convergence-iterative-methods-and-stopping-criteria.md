# Convergence, iterative methods and stopping criteria

**Subject identity:** \`SM-FND-016\` — Numerical analysis and scientific computing  
**Module:** 04  
**Status:** Initial public teaching resource; independent numerical-analysis review and learner testing outstanding.

## 1. Why iteration is used

Many spatial problems cannot be solved conveniently by a short, direct sequence of arithmetic operations. A model may involve a large sparse linear system, a nonlinear transformation, an optimisation objective or a discretised physical process. An iterative method starts with an approximation and repeatedly applies a computational rule to produce a sequence:

\[
x_0,\;x_1,\;x_2,\ldots
\]

The central questions are:

- Does the sequence converge?
- If it converges, what does it converge to?
- How quickly does it approach that limit?
- How can computation detect that sufficient accuracy has been reached?
- What evidence is available if convergence fails?

An iteration producing smaller changes is not, by itself, proof that the answer is accurate. The iteration may stagnate, converge to an unintended solution, or approach a solution of an incorrectly specified model.

## 2. Fixed-point formulation

A fixed point of a mapping \(g\) is a value \(x^\ast\) satisfying

\[
x^\ast=g(x^\ast).
\]

A fixed-point iteration applies

\[
x_{k+1}=g(x_k).
\]

The iteration is useful only when the chosen mapping and starting value produce a sequence with suitable convergence behaviour.

For a scalar differentiable mapping, a common local condition is

\[
|g'(x^\ast)|<1.
\]

Near the fixed point, this condition generally makes small errors contract from one iteration to the next. It is a local condition: it does not guarantee convergence from every starting value.

For a vector mapping, the corresponding local condition is that the spectral radius of the Jacobian at the fixed point is less than one:

\[
\rho\!\left(J_g(x^\ast)\right)<1.
\]

Here \(J_g\) is the Jacobian matrix and \(\rho\) denotes the largest absolute eigenvalue. This is a local convergence criterion under differentiability and suitable neighbourhood assumptions.

## 3. Contraction mappings and an error bound

A stronger and especially useful result is obtained when \(g\) is a contraction on a closed set \(D\): there is a constant \(q\) with \(0\le q<1\) such that

\[
\|g(x)-g(y)\|\le q\|x-y\|
\quad\text{for all }x,y\in D,
\]

and \(g\) maps \(D\) into itself.

Under these conditions, the Banach fixed-point theorem guarantees a unique fixed point in \(D\), and repeated iteration from any \(x_0\in D\) converges to it.

The successive-step difference can provide an a posteriori bound:

\[
\|x^\ast-x_k\|
\le
\frac{q}{1-q}\|x_k-x_{k-1}\|.
\]

This bound is meaningful only when the contraction assumptions and a valid bound \(q<1\) are established. In ordinary applications, a small step difference is often used as a practical indicator, but it should not be presented as a rigorous error bound without those assumptions.

## 4. Convergence rate

Convergence describes whether an approximation approaches a limit. The convergence rate describes how quickly its error decreases.

Let \(e_k=x_k-x^\ast\). Common patterns include:

**Linear convergence**

\[
\|e_{k+1}\|\le C\|e_k\|,
\qquad 0<C<1,
\]

for sufficiently large \(k\). Roughly, a fixed fraction of the error remains after each iteration.

**Superlinear convergence**

\[
\lim_{k\to\infty}
\frac{\|e_{k+1}\|}{\|e_k\|}=0.
\]

The error eventually decreases faster than any fixed linear factor.

**Quadratic convergence**

\[
\|e_{k+1}\|\le C\|e_k\|^2
\]

near the solution. Once sufficiently close, the number of correct digits can increase rapidly.

The order of convergence is a local asymptotic description. It does not tell us how many iterations are required to reach the convergence region, and it does not guarantee good behaviour from a poor initial value.

## 5. Iterative methods for linear systems

Consider

\[
Ax=b.
\]

For a large sparse matrix, storing or factorising the full system may be expensive. Iterative methods can exploit sparsity and matrix structure.

### 5.1 Jacobi iteration

Write \(A=D+L+U\), where \(D\) is diagonal, \(L\) is strictly lower triangular and \(U\) is strictly upper triangular. If all diagonal entries are non-zero, the Jacobi update is

\[
x^{(k+1)}
=
D^{-1}\left[b-(L+U)x^{(k)}\right].
\]

Each component is computed from the previous iteration's vector. This structure can support parallel computation.

Jacobi iteration converges for some important matrix classes, including strictly diagonally dominant matrices and certain symmetric positive-definite cases under appropriate conditions. It does not converge for every nonsingular matrix.

### 5.2 Gauss–Seidel iteration

The Gauss–Seidel method uses newly updated components as soon as they are available:

\[
(D+L)x^{(k+1)}=b-Ux^{(k)}.
\]

This is a sequential update in its standard form. It often converges in cases where Jacobi does, and can converge faster, but convergence is still dependent on matrix properties and ordering.

### 5.3 Stationary iteration and spectral radius

Many linear stationary iterations can be written as

\[
x^{(k+1)}=Bx^{(k)}+c.
\]

If \(x^\ast\) is a fixed point, the error evolves as

\[
e_{k+1}=Be_k.
\]

Convergence for every initial vector is guaranteed when

\[
\rho(B)<1.
\]

The spectral radius is therefore a key theoretical criterion. A method's convergence should not be inferred merely from the fact that the original matrix \(A\) is invertible.

### 5.4 Conjugate gradients

For a symmetric positive-definite matrix \(A\), the conjugate-gradient method solves \(Ax=b\) by constructing mutually conjugate search directions. In exact arithmetic, it terminates in at most \(n\) steps for an \(n\)-dimensional system. In practical floating-point computation, convergence is gradual and finite-precision effects matter.

Conjugate gradients is especially useful for large sparse symmetric positive-definite systems. It is not a generic solver for arbitrary matrices. Preconditioning can improve convergence by transforming the system so that its effective spectrum or condition is more favourable.

## 6. Nonlinear equations and Newton's method

For a nonlinear system

\[
F(x)=0,
\]

Newton's method linearises \(F\) around the current estimate \(x_k\). It solves

\[
J_F(x_k)\,\Delta x_k=-F(x_k)
\]

and updates

\[
x_{k+1}=x_k+\Delta x_k.
\]

For a sufficiently smooth scalar function with a simple root, Newton's method has local quadratic convergence under standard assumptions. For systems, similar local results require a nonsingular Jacobian at the solution and a sufficiently close starting point.

Newton's method can fail or behave poorly when:

- the initial estimate is far from a root;
- the Jacobian is singular or ill-conditioned;
- the step leaves the physically or mathematically valid domain;
- the nonlinear model is not sufficiently smooth;
- finite-precision arithmetic makes the linear solve unreliable.

Damped Newton methods replace the full step with

\[
x_{k+1}=x_k+\alpha_k\Delta x_k,
\qquad 0<\alpha_k\le1,
\]

where a line search or trust-region strategy chooses a step intended to improve progress. Damping can improve global behaviour, but does not remove the need to check assumptions and convergence.

Spatial examples include nonlinear parameter estimation, bundle adjustment, geodetic network models, coordinate transformations with nonlinear observation equations and physical-model inversion. Solver convergence does not establish that the model, observations or reference system are correct.

## 7. Residuals, step sizes and stopping criteria

A numerical method needs a stopping rule. Stopping too early can leave unacceptable error; stopping too late wastes resources and may amplify round-off or stagnation effects.

For a linear system, define the residual at iteration \(k\):

\[
r_k=b-Ax_k.
\]

A scale-aware relative residual can be written

\[
\eta_k=
\frac{\|b-Ax_k\|}
{\|A\|\,\|x_k\|+\|b\|},
\]

provided the denominator is non-zero. This is a useful normwise diagnostic; the norm and scaling should be stated.

A relative step measure is often monitored as well:

\[
s_k=
\frac{\|x_{k+1}-x_k\|}
{\max(\|x_{k+1}\|,s_{\mathrm{scale}})},
\]

where \(s_{\mathrm{scale}}>0\) is an explicitly chosen scale that prevents division by zero and reflects the problem's units or magnitude.

For nonlinear systems, monitor a residual norm such as \(\|F(x_k)\|\), the step size, and any application-specific constraint violations or objective function.

A robust stopping policy generally combines several conditions:

1. **Residual or defect tolerance:** the computed solution sufficiently satisfies the represented equations.
2. **Step tolerance:** the updates have become sufficiently small relative to a meaningful scale.
3. **Maximum iteration count:** the method stops if progress is not achieved within a defined budget.
4. **Stagnation detection:** the residual or objective ceases to improve meaningfully.
5. **Divergence or invalid-state detection:** values become non-finite, constraints are violated, or residuals grow persistently.
6. **Application acceptance criteria:** the result meets the accuracy required by the spatial task.

A small step alone is not enough. A method can take tiny steps because it is stagnating, because the system is badly scaled, or because progress has effectively stopped far from the solution. A small residual alone may also be misleading for an ill-conditioned problem, as discussed in [Numerical stability and backward error](numerical-stability-and-backward-error.md).

Tolerances should not be chosen merely because a software package supplies a default. They should be related to data scale, units, conditioning, model accuracy and the consequences of the decision.

## 8. Worked conceptual example: iterative solution of a spatial grid model

Suppose a discretised physical model on a raster grid produces a sparse linear system

\[
Au=b.
\]

The vector \(u\) contains unknown values at grid cells, \(A\) encodes the discretised relationships between cells and boundary conditions, and \(b\) contains source terms and known contributions.

An iterative solver may be appropriate because each cell interacts with only a small neighbourhood, making \(A\) sparse.

A defensible computational record should include:

- the physical model and discretisation that produced \(A\) and \(b\);
- grid spacing, units and boundary conditions;
- whether \(A\) is symmetric positive-definite or has another structure;
- the solver and preconditioner, including software versions;
- initialisation and iteration limit;
- residual norm, tolerance and stopping reason;
- convergence history or sufficient diagnostics;
- independent checks such as boundary-condition satisfaction and a manufactured-solution test where applicable.

A converged solution to the discrete equations is not automatically an accurate representation of the continuous physical system. Discretisation error, input uncertainty, boundary assumptions and model adequacy remain separate questions.

## 9. Practical convergence assessment

When evaluating an iterative spatial method:

- establish the mathematical problem and its solution conditions first;
- identify the iteration mapping or solver assumptions;
- check matrix structure, scaling and conditioning where relevant;
- distinguish local convergence claims from global guarantees;
- choose tolerances in relation to units and application requirements;
- monitor residuals, steps and convergence history;
- detect stagnation, divergence, non-finite values and constraint violations;
- test several initial values when initialisation may affect the result;
- compare with direct, analytic, manufactured or higher-accuracy reference cases where possible;
- record why the solver stopped, not merely that it returned a result.

A software status of “success” is evidence about the solver's internal stopping logic. It is not independent proof of physical validity or application-level accuracy.

## 10. Exercises

### Exercise 1 — Fixed-point convergence

For \(g(x)=\cos x\), explain why the fixed-point iteration \(x_{k+1}=g(x_k)\) is expected to converge near its fixed point. What role does the derivative play?

### Exercise 2 — Linear iteration

A stationary iteration is written \(x^{(k+1)}=Bx^{(k)}+c\). State the spectral-radius condition that guarantees convergence for every initial vector.

### Exercise 3 — Solver selection

Explain why conjugate gradients is appropriate for a symmetric positive-definite sparse system but should not be selected indiscriminately for any square matrix.

### Exercise 4 — Stopping rules

A nonlinear solver reports very small successive steps, but the residual remains large. Give two possible explanations and describe what should be checked before accepting the result.

### Exercise 5 — Spatial grid model

A raster-based physical model converges to a stable discrete solution. List at least three reasons why this does not, by itself, establish that the result accurately represents the real-world process.

## 11. Answers and discussion

1. The fixed point satisfies \(x^\ast=\cos(x^\ast)\). Since \(g'(x)=-\sin x\), the magnitude of the derivative at the fixed point is less than one, giving local contraction behaviour. A contraction argument on a suitable interval can establish stronger guarantees.
2. \(\rho(B)<1\).
3. Conjugate gradients relies on the symmetric positive-definite structure for its standard convergence theory and minimisation interpretation. An arbitrary square matrix may violate those assumptions; another Krylov method or factorisation may be required.
4. The iteration may have stagnated, be poorly scaled, or be taking tiny damped steps without reducing the defect. Inspect residual scaling, Jacobian conditioning, constraints, progress history and the solver's stopping reason.
5. The discrete model may have discretisation error; inputs or boundary conditions may be wrong; the physical model may be incomplete; parameters may be uncertain; or the numerical solution may be sensitive to grid resolution. Convergence addresses only part of the evidence chain.

## 12. Connections to other Spatial Methods resources

- [Floating-point numbers, rounding and computational error](floating-point-numbers-rounding-and-computational-error.md) explains finite-precision effects in repeated arithmetic.
- [Sensitivity and perturbation analysis](sensitivity-and-perturbation-analysis.md) explains how input changes affect solutions.
- [Numerical stability and backward error](numerical-stability-and-backward-error.md) connects residuals and conditioning to forward accuracy.
- [Linear algebra and matrix methods](../linear-algebra/README.md) provides the matrix concepts and factorisations used by iterative solvers.
- [Least squares and constrained systems](../linear-algebra/least-squares-and-constrained-systems.md) develops estimation problems that may require iterative solution.
- [Covariance GLS implementation](../../implementations/python/covariance-gls/README.md) connects numerical solving to covariance-aware estimation.

## 13. Further reading

- Yousef Saad, *Iterative Methods for Sparse Linear Systems*, 2nd edition, SIAM, 2003. DOI: [10.1137/1.9780898718003](https://doi.org/10.1137/1.9780898718003).
- Richard S. Varga, *Matrix Iterative Analysis*, 2nd revised edition, Springer, 2000. DOI: [10.1007/978-3- métodos](https://doi.org/10.1007/978-3-642-05156-2).
- Lloyd N. Trefethen and David Bau III, *Numerical Linear Algebra*, SIAM, 1997. DOI: [10.1137/1.9780898719574](https://doi.org/10.1137/1.9780898719574).

These references are starting points for technical review. The module remains an initial teaching resource pending independent review and learner testing.
