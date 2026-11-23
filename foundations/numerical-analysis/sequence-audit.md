# Numerical analysis sequence audit

**Subject identity:** \`SM-FND-016\` — Numerical analysis and scientific computing  
**Audit type:** Repository-level desk audit  
**Status:** Initial sequence audit completed; independent technical review, executable verification and learner testing remain outstanding.  
**Audit scope:** Modules 01–08, the numerical-analysis roadmap and the theoretical-foundations subject index.

## 1. Purpose and audit boundary

This audit treats the eight published modules as one developing curriculum rather than eight independent articles. It checks the sequence's conceptual progression, topic boundaries, mathematical notation, internal navigation, shared terminology, spatial relevance and remaining validation work.

This is a desk audit of repository content and structure. It is not an independent peer review, a proof-check of every derivation, a software test report, or a certification of numerical correctness. A balanced LaTeX delimiter count is a formatting check, not evidence that a formula is mathematically correct.

## 2. Sequence map

| Module | Main question | Core concepts | Downstream use |
|---|---|---|---|
| 01. Floating-point numbers, rounding and computational error | What does a computer actually calculate? | Finite representation, rounding, absolute/relative error, cancellation, range, conditioning and stability | All subsequent numerical computations |
| 02. Sensitivity and perturbation analysis | How do changes in inputs affect the answer? | Jacobians, perturbation bounds, condition numbers, scaling and covariance propagation | Error budgets, transformations, parameter estimation and model interpretation |
| 03. Numerical stability and backward error | How much error does the algorithm introduce? | Forward/backward error, residuals, stable reformulation, summation and least-squares factorisation | Solver selection, robust geometry and trustworthy diagnostics |
| 04. Convergence, iterative methods and stopping criteria | Does an iterative procedure converge, and when should it stop? | Fixed-point iteration, contraction, spectral radius, convergence rates, Newton iteration, residual and step tests | Iterative solvers and nonlinear numerical procedures |
| 05. Root finding and nonlinear equation solving | How can a scalar nonlinear equation be solved reliably? | Bracketing, bisection, regula falsi, Newton, secant, safeguarding and root conditioning | Thresholds, crossings and implicit spatial models |
| 06. Numerical differentiation | How can derivatives be estimated from formulas or samples? | Finite differences, truncation/roundoff balance, stencils, noise, gradients and automatic differentiation | Terrain derivatives, local sensitivity, fluxes and optimisation |
| 07. Numerical integration and quadrature | How can a continuous quantity be accumulated numerically? | Riemann sums, midpoint/trapezoid/Simpson, Gaussian and adaptive quadrature, multidimensional measures | Area, mass, volume, loads and raster aggregation |
| 08. Interpolation and approximation | How can a field be estimated between finite observations? | Polynomial and piecewise interpolation, splines, scattered-data methods, regression, resampling and validation | Surface construction, raster transformation and spatial prediction |

## 3. Dependency logic

The modules are not a strict prerequisite chain. Their useful conceptual dependencies are:

- **01 underpins all modules.** Every later numerical method operates with finite precision.
- **02 and 03 are complementary.** Conditioning describes sensitivity of the mathematical problem; stability describes the behaviour of the algorithm. Neither substitutes for the other.
- **04 provides general convergence tools.** Module 05 applies them to scalar root finding, while also explaining why bracketing methods are valuable when local convergence conditions are uncertain.
- **06 and 07 are paired numerical operators.** Differentiation estimates local change; integration accumulates quantities. Their errors, units and sampling assumptions differ.
- **08 consumes and constructs sampled representations.** Interpolation may supply values for differentiation or integration, but it also introduces a model between observations. It must not be treated as new measurement information.
- **Measurement uncertainty remains a separate layer.** Numerical error, model error, sampling limitations and observational uncertainty may all affect an output, but should be identified separately before they are combined in an uncertainty budget.

A reader may enter through a practical task and follow links backwards to the relevant foundations. The sequence is therefore a conceptual map, not a mandatory course order.

## 4. Cross-module consistency checks

### 4.1 Error vocabulary

Use these terms consistently:

- **Roundoff error:** error introduced by finite-precision representation and arithmetic.
- **Truncation error:** error introduced when an exact mathematical process is replaced by a finite approximation, such as a finite-difference stencil or quadrature rule.
- **Forward error:** difference between the computed result and the exact solution to the stated problem.
- **Backward error:** size of the perturbation to the input problem for which the computed result is an exact solution.
- **Residual:** a computable measure of how closely a candidate satisfies the stated equations; a small residual alone does not guarantee small forward error.
- **Conditioning:** sensitivity of the mathematical problem to input perturbations.
- **Stability:** control of errors introduced by the numerical algorithm.
- **Measurement uncertainty:** uncertainty associated with the measurand, observations and measurement model, not a synonym for floating-point error.

When several sources matter, report them separately before deciding whether a combined error or uncertainty model is justified.

### 4.2 Tolerances

A tolerance is not a universal measure of accuracy. It should be interpreted with the quantity's units, scale, conditioning, algorithm, data quality and decision requirement. Relative tolerances are insufficient near zero; absolute tolerances alone may be unsuitable across quantities with very different scales. A stopping condition should state what is measured and what it does—and does not—guarantee.

### 4.3 Spatial units and measures

The spatial examples should consistently state whether coordinates are planar or geographic, whether distances and areas are grid or ground quantities, and whether an observation represents a point sample, cell value, cell average or total. Numerical precision cannot repair an inappropriate CRS, a wrong spatial measure, missing coverage or a mismatch in data support.

### 4.4 Formula and notation policy

- Use inline math as \`\\(...\\)\` and display math as \`\\[...\\]\`.
- Define symbols near first use and avoid reusing one symbol for unrelated quantities without explanation.
- Include units for physical examples and dimensionless quantities for relative errors and condition numbers.
- State assumptions beside formulas whose error bounds require smoothness, nonzero values, matrix nonsingularity or a particular norm.
- Distinguish exact identities from approximations and asymptotic orders.
- Rendered formula review is still required; delimiter balance alone does not verify rendering or mathematics.

## 5. Repository checks performed

The desk audit performed these structural checks:

1. Confirmed the eight module files and the domain roadmap are present.
2. Checked inline and display-math delimiter counts in all eight modules; opening and closing counts match in each file.
3. Checked for escaped-backtick sequences in all eight modules; none were found in this pass.
4. Resolved every relative Markdown link in the eight modules against the current repository tree; all 53 link occurrences point to existing files.
5. Confirmed that the roadmap lists Modules 01–08 and retains an explicit statement that independent review and learner testing are outstanding.
6. Identified and corrected a malformed, duplicated-conjunction summary in the main theoretical-foundations index.

These checks establish repository integrity at the time of the audit. They do not verify external links, every anchor fragment, mathematical derivations, code execution, numerical results or the truth of all referenced claims.

## 6. Remaining technical review priorities

The following require a qualified reviewer or executable validation rather than another editorial pass:

| Priority | Review target | Required check |
|---|---|---|
| High | Module 01 | Verify binary64 representation, machine epsilon/unit roundoff distinction, floating-point model assumptions and coordinate examples |
| High | Modules 02–03 | Check perturbation bounds, condition-number definitions, residual/backward-error relationships and least-squares stability statements |
| High | Modules 04–05 | Verify convergence hypotheses, spectral-radius statements, stopping rules, bracketing guarantees and multiple-root behaviour |
| High | Modules 06–07 | Verify finite-difference truncation orders and step-size discussion; quadrature error orders, adaptive error estimators and spatial measure examples |
| High | Module 08 | Review interpolation assumptions, spline boundary conditions, spatial validation guidance, support and raster resampling distinctions |
| High | All modules | Independently recompute worked examples and exercise answers; inspect rendered formulas in the target GitHub/Markdown presentation |
| Medium | All modules | Add small reproducible code companions where they materially improve understanding, with deterministic tests and pinned dependency/version context |
| Medium | All modules | Add primary/authoritative references for important claims and map references to the claims they support |
| Medium | Sequence | Test the learning order with readers of different mathematical backgrounds and revise prerequisite explanations accordingly |

## 7. Scope gaps: do not mistake the eight modules for a complete subject

The current sequence is a working numerical core. It does not yet provide full coverage of:

- numerical linear algebra beyond the relevant stability and iterative-method connections;
- direct methods, preconditioning and Krylov methods in a systematic standalone treatment;
- eigenvalue and singular-value computation;
- numerical solution of ordinary and partial differential equations;
- finite-volume, finite-element and finite-difference discretisation for spatial physical models;
- optimisation algorithms and constrained numerical optimisation;
- Monte Carlo error analysis and quasi-Monte Carlo methods in greater depth;
- uncertainty quantification and propagation across complete computational workflows;
- reproducible computational experiments, benchmarking and numerical regression testing.

Some of these topics belong in neighbouring foundations, such as linear algebra, calculus, probability, optimisation or physical modelling. The subject map should determine ownership before new modules are created, to avoid duplicate or shallow coverage.

## 8. Recommended next development sequence

1. Obtain independent technical review of Modules 01–08 and correct any substantive issues found.
2. Build a small, reproducible numerical companion suite for selected examples: floating-point cancellation, perturbation, stable least squares, iterative convergence, root solving, finite differences, quadrature and interpolation.
3. Add tests that check invariants, analytic cases, convergence behaviour and known failure modes; avoid relying only on agreement between two libraries.
4. Conduct learner testing and improve prerequisite explanations and exercises.
5. Decide whether the next module belongs here or in an adjacent domain. Prioritise numerical linear algebra, ODE/PDE methods and discretisation only after mapping their boundaries against linear algebra, calculus and physical-science foundations.

## 9. Audit conclusion

The eight modules form a coherent introductory sequence: representation → sensitivity → algorithmic stability → convergence and nonlinear solution → differentiation and integration → interpolation and approximation. The spatial examples connect the mathematics to coordinates, terrain, raster fields, measured observations and spatial prediction.

The sequence is suitable as an initial public learning resource, not as a complete or independently validated numerical-analysis reference. The next quality milestone is technical verification and executable examples—not simply increasing the module count.
