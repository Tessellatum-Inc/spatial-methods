# Root finding and nonlinear equation solving

**Subject identity:** `SM-FND-016` — Numerical analysis and scientific computing  
**Module:** 05  
**Status:** Initial public teaching resource; independent numerical-analysis review and learner testing outstanding.

## 1. The root-finding problem

A scalar root-finding problem seeks a value \(x^\ast\) such that

\[
f(x^\ast)=0.
\]

Root finding appears in spatial computation whenever an unknown quantity is defined implicitly. Examples include solving a ray or profile intersection equation, finding a threshold crossing along a continuous path, inverting a monotone transformation, or solving one equation inside a larger nonlinear estimation problem.

The numerical task is not simply to make \(f(x)\) small. A reliable method must consider whether a root exists in the interval of interest, whether it is unique, how sensitive it is to perturbations, whether the iteration converges, and whether the computed result satisfies the actual application requirements.

For a system of equations \(F(x)=0\), root finding becomes a nonlinear-system problem. Newton-type methods for systems were introduced in [Module 04](convergence-iterative-methods-and-stopping-criteria.md). This module concentrates on scalar problems and the important distinctions among bracketing, open and safeguarded methods.

## 2. Existence, uniqueness and root conditioning

If \(f\) is continuous on \([a,b]\) and

\[
f(a)f(b)<0,
\]

the intermediate value theorem guarantees at least one root in \((a,b)\). It does not guarantee that the root is unique.

A sign change is a powerful practical certificate, but it is not a necessary condition for a root. For example, \(f(x)=(x-2)^2\) has a root at \(x=2\) without changing sign across that root.

Uniqueness can sometimes be established if \(f\) is strictly monotone on the interval. For a differentiable function, a derivative that keeps one strict sign throughout the interval is a sufficient condition for strict monotonicity.

For a simple root, a small perturbation \(\delta f\) in the function value produces, to first order,

\[
\delta x \approx -\frac{\delta f}{f'(x^\ast)}.
\]

Thus a root is sensitive when \(|f'(x^\ast)|\) is small. A multiple root has \(f'(x^\ast)=0\), so this first-order expression is not applicable and ordinary root-finding methods may converge slowly or behave differently.

The condition of the mathematical root and the stability of a numerical algorithm are distinct. A well-designed algorithm cannot make an intrinsically ill-conditioned root insensitive to data perturbations.

## 3. Bracketing methods

Bracketing methods maintain an interval known to contain at least one root. If continuity and a sign change are preserved, the root remains enclosed as the interval is reduced.

### 3.1 Bisection

Given \(f(a)f(b)<0\), calculate the midpoint

\[
m_k=\frac{a_k+b_k}{2}.
\]

Evaluate \(f(m_k)\), then retain the half-interval whose endpoints have opposite signs. Repeat until a chosen interval-width or other acceptance criterion is met.

After \(n\) bisections, the interval width is

\[
b_n-a_n=\frac{b_0-a_0}{2^n}.
\]

The midpoint therefore has an absolute root-location error no greater than

\[
|m_n-x^\ast|\le\frac{b_0-a_0}{2^{n+1}},
\]

provided the initial interval contains a root and the exact sign logic is maintained.

Bisection is dependable and has a predictable reduction in interval width. Its convergence is linear, and it does not exploit derivative information. In floating-point implementations, the midpoint should be computed in a way that avoids overflow, and termination must account for the possibility that no representable number lies strictly between the endpoints.

### 3.2 Regula falsi (false position)

The false-position method uses the secant line through the bracket endpoints and takes its intersection with the horizontal axis:

\[
x_k=
b_k-
f(b_k)\frac{b_k-a_k}{f(b_k)-f(a_k)}.
\]

It retains a bracket by replacing the endpoint that has the same sign as \(f(x_k)\). The interpolation can make faster progress than bisection in some cases, but one endpoint may remain fixed for many iterations. This endpoint stagnation can make the method unexpectedly slow.

Modified variants such as Illinois-type methods adjust retained function values to reduce this stagnation. Their implementation details and convergence behaviour should be documented rather than assumed.

## 4. Open methods

Open methods use one or more estimates but do not maintain a guaranteed root-containing interval. They can converge rapidly near a suitable root, but they may diverge or converge to a different root.

### 4.1 Newton's method

For a differentiable scalar function,

\[
x_{k+1}=x_k-\frac{f(x_k)}{f'(x_k)}.
\]

Near a simple root, Newton's method is locally quadratically convergent under standard smoothness assumptions. It requires derivative evaluation and a sufficiently good initial estimate. It can fail when the derivative is zero or very small, when the step leaves the domain, or when the starting point is outside the method's basin of attraction.

### 4.2 Secant method

The secant method approximates the derivative using two previous iterates:

\[
x_{k+1}
=
x_k-
f(x_k)\frac{x_k-x_{k-1}}{f(x_k)-f(x_{k-1})}.
\]

It avoids explicit derivative evaluation. Its local convergence is generally superlinear for a simple root under suitable assumptions, but it does not preserve a bracket and can fail if successive function values are too similar or the sequence moves away from the desired root.

### 4.3 Multiple roots

For a root of multiplicity \(m>1\), ordinary Newton iteration generally loses its usual quadratic convergence and may become only linearly convergent. If the multiplicity is known, a modified update is

\[
x_{k+1}=x_k-m\frac{f(x_k)}{f'(x_k)}.
\]

The multiplicity is rarely known exactly in applied problems. A small derivative or unusually slow convergence should prompt investigation, not an unverified assumption about multiplicity.

## 5. Safeguarded methods

A safeguarded method combines the reliability of bracketing with the speed of interpolation or derivative-based steps. Brent's method is a widely used example: it combines bisection, secant-like interpolation and inverse quadratic interpolation while maintaining a bracket.

The general strategy is:

1. Establish a valid bracket where continuity and a sign change are supported.
2. Propose a faster interpolation or Newton-like step.
3. Reject the proposed step if it violates safeguard conditions or makes inadequate progress.
4. Fall back to a bracketing step.
5. Update the bracket and continue monitoring convergence.

Safeguards improve robustness, but they do not remove the need for a valid function evaluation, a meaningful interval, or appropriate tolerances. A bracket may contain multiple roots, and the method may converge to any root consistent with its updates.

## 6. Choosing a stopping criterion

A root solver should not stop solely because successive iterates are close. A small step may indicate convergence, but it may also indicate stagnation or finite-precision limits.

Useful diagnostics include:

**Residual**

\[
r_k=|f(x_k)|.
\]

This measures how closely the computed point satisfies the evaluated equation. A small residual does not necessarily imply a small root-location error when the root is ill-conditioned.

**Step size**

\[
s_k=|x_{k+1}-x_k|.
\]

This measures progress between iterates, not distance to the true root.

**Bracket width**

\[
w_k=b_k-a_k.
\]

For a valid bracket, this directly bounds the root location: any root retained in the interval lies no farther than \(w_k/2\) from its midpoint.

A scale-aware mixed tolerance may be written

\[
|x_{k+1}-x_k|
\le
\tau_{\mathrm{abs}}+
\tau_{\mathrm{rel}}|x_{k+1}|,
\]

where \(\tau_{\mathrm{abs}}\) and \(\tau_{\mathrm{rel}}\) are selected for the problem's units and scale.

A robust policy should also include a maximum evaluation or iteration budget, non-finite-value checks, stagnation detection and explicit failure states. For bracketing methods, report the final bracket and its width. For open methods, report the residual, step history and stopping reason.

## 7. Spatial example: finding a continuous threshold crossing

Suppose a continuous model \(h(s)\) gives a predicted elevation or depth along a path parameterised by distance \(s\). We want the position where the model reaches a threshold \(h_0\):

\[
f(s)=h(s)-h_0=0.
\]

If the path interval \([s_a,s_b]\) has a sign change and the model is continuous, a root exists in the interval. Bisection or a safeguarded method can narrow the crossing location without requiring a derivative.

Before interpreting the result as a real-world crossing, establish:

- that the model is meaningful and continuous over the interval;
- that the path parameter and elevation units are consistent;
- that the interval is in the intended spatial segment;
- whether more than one crossing may occur;
- whether the model's sampling or interpolation resolution supports the requested location precision;
- whether input and model uncertainty dominate the numerical tolerance.

A numerical root can be located to millimetres in a mathematical model while the underlying terrain, path or observations are uncertain by metres. Reporting excessive numerical digits would then misrepresent the evidence.

## 8. Practical method-selection guide

| Situation | Suitable starting point | Important qualification |
|---|---|---|
| Continuous function and reliable sign-changing interval | Bisection | Predictable and robust; needs a valid bracket |
| Bracket available and faster interpolation desired | Brent-type safeguarded method | Check implementation and stopping diagnostics |
| Derivative available and initial estimate is good | Newton | Local method; safeguard if failure is costly |
| Derivative unavailable but two good estimates exist | Secant | No guaranteed bracket; monitor divergence |
| Multiple roots or nearly flat function | Bracketing plus conditioning analysis | Residual and step size can be deceptive |
| Several coupled nonlinear unknowns | Nonlinear system method | Examine Jacobian, scaling and constraints |

No single method is best for every problem. Selection should follow from the mathematical structure, the cost of function evaluation, the reliability of derivatives, the availability of a bracket and the consequences of failure.

## 9. Exercises

### Exercise 1 — Existence versus uniqueness

A continuous function satisfies \(f(1)=-2\) and \(f(5)=3\). What can be concluded about roots in \((1,5)\)? Can uniqueness be concluded?

### Exercise 2 — Bisection accuracy

An initial bracket has width 8 units. How many bisection steps are sufficient to guarantee a midpoint error no greater than \(0.001\) units?

### Exercise 3 — Even-multiplicity root

Explain why a sign-change search can miss a root of \(f(x)=(x-3)^2\). Name one additional strategy that could help detect such a root.

### Exercise 4 — Residual interpretation

A solver reports \(|f(x_k)|=10^{-10}\). Explain why this does not, by itself, establish that \(x_k\) is accurate to ten decimal places.

### Exercise 5 — Method selection

A continuous spatial profile has a known interval with opposite signs at its endpoints. Derivative evaluation is expensive, and a dependable crossing location is required. Recommend a method and explain why.

## 10. Answers and discussion

1. At least one root exists by the intermediate value theorem. The endpoint signs alone do not establish uniqueness; monotonicity or another suitable argument would be needed.
2. The midpoint error bound is \(8/2^{n+1}\). Require \(8/2^{n+1}\le0.001\), so \(n+1\ge\log_2(8000)\), and 12 steps are sufficient.
3. The function is non-negative on both sides of the root, so no sign change occurs. Examine stationary points, use derivative information, minimise \(|f|\) over a suitable interval, or use problem-specific root isolation.
4. The root may be ill-conditioned, with a small derivative, or the residual may be scaled in a way that hides location error. Relate residual to root error using derivative bounds or a condition analysis, and check the model and arithmetic.
5. Bisection is a strong baseline because the bracket guarantees containment under continuity and its error bound follows from interval width. A tested Brent-type method may accelerate progress while preserving the bracket.

## 11. Connections to other Spatial Methods resources

- [Convergence, iterative methods and stopping criteria](convergence-iterative-methods-and-stopping-criteria.md) develops general convergence concepts and solver diagnostics.
- [Sensitivity and perturbation analysis](sensitivity-and-perturbation-analysis.md) explains how perturbations affect computed quantities.
- [Numerical stability and backward error](numerical-stability-and-backward-error.md) distinguishes residuals, backward error and forward accuracy.
- [Calculus and differential methods](../calculus-and-differential-methods/README.md) is the broader mathematical home for derivatives and local function behaviour; this link is a planned domain destination.
- [Coordinate transformation and CRS axis order](../../algorithms/geodesy/crs-transformation.md) provides an applied computational context where transformation direction and model assumptions matter.

## 12. Further reading

- Richard L. Burden, J. Douglas Faires and Annette M. Burden, *Numerical Analysis*, 10th edition, Cengage Learning, 2016.
- John H. Mathews and Kurtis D. Fink, *Numerical Methods Using MATLAB*, 4th edition, Prentice Hall, 2004.
- Richard P. Brent, *Algorithms for Minimization Without Derivatives*, Prentice-Hall, 1973.

These are starting points for technical review, not claim-by-claim citations. The module remains an initial teaching resource pending independent review and learner testing.
