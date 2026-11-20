# Sequences, series and approximation for spatial science

**Foundation domain:** Mathematics for spatial science  
**Subject ID:** SM-FND-001  
**Module:** 08  
**Status:** Initial public foundation; further technical review and expansion required

## 1. Why sequences and approximation matter

Spatial computation often replaces a continuous or complicated problem with a finite sequence of manageable steps. A numerical algorithm may repeatedly update an estimate. A raster represents a continuous region through cells. A curve may be approximated by short straight segments. A simulation advances a system through discrete time steps. A numerical solver may stop when successive estimates differ by less than a specified tolerance.

These practices rely on ideas from sequences, series, limits and approximation.

A **sequence** is an ordered list of terms indexed by integers, commonly written:
$
a_0,a_1,a_2,\ldots
$

A **series** is the sum of terms from a sequence. A **limit** describes the value approached by a sequence or function under a specified process. An **approximation** is a substitute representation or value that is useful for a stated purpose but is not identical to the exact object.

The concepts are connected but not interchangeable. A sequence can converge even when its terms are not summed; a series can converge or diverge; and a numerical approximation can be useful without being a convergent sequence.

## 2. Sequences and their notation

A sequence can be defined by a formula, a recurrence relation or an explicit list.

### 2.1 Explicit definition

For example:
$
a_n=2n+1,\qquad n=0,1,2,\ldots
$

The terms are 1, 3, 5, 7, and so on.

### 2.2 Recursive definition

A sequence can instead be defined from an initial value and a rule:
$
a_0=1,\qquad a_{n+1}=a_n+2.
$

The same sequence is produced. The recursive form makes the repeated update explicit.

### 2.3 Spatial example: repeated coordinate update

Suppose an illustrative one-dimensional position estimate is updated by adding a fixed displacement of 5 m:
$
x_0=100\;\mathrm{m},\qquad x_{n+1}=x_n+5\;\mathrm{m}.
$

Then $x_1=105\,\mathrm{m}$, $x_2=110\,\mathrm{m}$ and $x_3=115\,\mathrm{m}$. This is a simple deterministic sequence. It does not by itself describe measurement noise, uncertainty or a real moving object's trajectory.

## 3. Arithmetic and geometric sequences

An arithmetic sequence has a constant difference d between consecutive terms:
$
a_n=a_0+nd.
$

A geometric sequence has a constant ratio r between consecutive non-zero terms:
$
a_n=a_0r^n.
$

### Example: arithmetic sequence

A grid coordinate starts at $0\,\mathrm{m}$ and increases by $10\,\mathrm{m}$ at each step. The sequence is $0,10,20,30,\ldots$. It can represent regularly spaced sample positions along one axis.

### Example: geometric sequence

A hypothetical raster cell width is repeatedly halved:
$
w_n=100\left(\frac12\right)^n\;\mathrm{m}.
$

The first values are 100 m, 50 m, 25 m and 12.5 m. This illustrates a scale refinement sequence. It does not mean that halving cell width always halves computational cost or improves a result by a predictable amount.

## 4. Limits and convergence

A sequence converges to L if its terms approach L as the index increases:
$
\lim_{n\to\infty}a_n=L.
$

Informally, terms can be made as close to $L$ as desired by taking $n$ sufficiently large.

For example:
$
a_n=\frac{1}{n+1}
$

converges to zero. Its terms are positive but become smaller.

A sequence that does not approach a finite limit may diverge. It may grow without bound, oscillate without settling, or behave in another non-convergent way.

### 4.1 Convergence is not the same as accuracy

A sequence of estimates can converge to the wrong answer if the model or update rule is wrong. Convergence describes the behaviour of the sequence, not whether its limiting value represents reality.

Likewise, an algorithm can stop because it reached a maximum iteration count without having converged. A stopping condition should therefore be reported separately from a claim of convergence.

### 4.2 Monotonicity and boundedness

A sequence $(a_n)$ is monotonically increasing if $a_{n+1}\geq a_n$ for every applicable index. It is monotonically decreasing if $a_{n+1}\leq a_n$.

A sequence is bounded if all terms lie within some finite interval.

A useful result in real analysis is that a monotone bounded sequence converges. This is a theoretical guarantee under the stated conditions; it does not automatically provide a practical convergence rate or a useful stopping iteration.

## 5. Series and partial sums

A series adds terms of a sequence:
$
\sum_{n=0}^{\infty}a_n.
$

An infinite series is studied through its sequence of partial sums:
$
S_N=\sum_{n=0}^{N}a_n.
$

The series converges if the partial sums approach a finite limit as $N\to\infty$.

### 5.1 Finite arithmetic series

For an arithmetic sequence with first term $a_0$ and common difference $d$, the sum of terms from index 0 through index $N$ is:
$
S_N=\frac{N+1}{2}(a_0+a_N).
$

### 5.2 Finite geometric series

For the terms $a_0,a_0r,\ldots,a_0r^N$, where $r\neq 1$:
$
S_N=a_0\frac{1-r^{N+1}}{1-r}.
$

If $r=1$, the sum is $(N+1)a_0$.

### 5.3 Infinite geometric series

For $|r|<1$:
$
\sum_{n=0}^{\infty}a_0r^n=\frac{a_0}{1-r}.
$

For $|r|\geq 1$ and $a_0\neq 0$, this geometric series diverges. If $a_0=0$, every term is zero and the series converges to zero.

### Example

A simplified model assigns successively smaller contributions 1, 0.5, 0.25, 0.125, ... . The infinite sum is:
$
1+0.5+0.25+\cdots=\frac{1}{1-0.5}=2.
$

A finite partial sum is less than 2. This example explains a convergent sum; it is not a universal model for spatial influence, error or decay.

## 6. Approximation and error

An exact quantity may be replaced by an approximation when exact computation is impossible, unnecessary or too costly.

Let x be the exact value and \hat{x} an approximation. The signed error is:
$
e=\hat{x}-x.
$

The absolute error is:
$
|e|=|\hat{x}-x|.
$

When $x\neq 0$, relative error is:
$
e_r=\frac{|\hat{x}-x|}{|x|}.
$

Relative error is undefined when the exact reference value is zero. A percentage relative error is $100e_r\%$.

Error terminology requires care. The difference between an approximation and an exact mathematical value is not automatically the same as measurement error, model error or uncertainty. Those concepts have distinct meanings in measurement science and modelling.

### Example: rounded distance

Suppose an exact planar distance in a worked calculation is 123.456 m, but a report displays 123.5 m.

The displayed value has absolute rounding difference 0.044 m. The rounded display may be adequate for a summary but not for a task requiring centimetre-level reporting.

Rounding the display does not improve or degrade the underlying observation; it changes the representation communicated to the reader.

## 7. Sources of numerical approximation

Spatial workflows can introduce several distinct forms of approximation:

- **Discretisation:** representing a continuous domain with cells, nodes, segments or time steps.
- **Truncation:** omitting terms from an infinite series or finite mathematical expansion.
- **Rounding:** replacing a value with a nearby representable or displayed value.
- **Interpolation:** estimating values between known samples under a specified rule or model.
- **Approximate solution:** solving a problem iteratively or with a method that does not return an exact symbolic result.
- **Model simplification:** replacing a complex real system with a tractable mathematical representation.

These sources should not be merged into one generic “accuracy” figure without a defensible model of how they affect the result.

## 8. Raster resolution as discretisation

A raster represents a spatial domain using a finite arrangement of cells. For a regular grid with square cell width h, each cell represents an area:
$
A_{cell}=h^2.
$

If $h=10\,\mathrm{m}$, a square cell covers $100\,\mathrm{m}^2$ in the planar grid representation. If $h$ is halved to $5\,\mathrm{m}$, cell area becomes $25\,\mathrm{m}^2$: one quarter of the original area. Over the same region, the number of cells is approximately four times as large, ignoring boundary and alignment effects.

This has practical consequences:
- finer grids can represent smaller spatial variation, if the source data support it;
- finer grids increase storage and processing requirements;
- cell size does not by itself determine positional accuracy or thematic accuracy;
- resampling to a finer grid does not create new observed detail;
- the appropriate resolution depends on the phenomenon, source data, intended analysis and scale of decision.

Raster cell size is a discretisation choice, not a guarantee of information content.

## 9. Approximating curves and paths

A curved path can be approximated by a sequence of straight line segments. This is common in map rendering, route geometry and numerical integration.

For a smooth curve, sufficiently short segments may provide a close geometric approximation. However, the required segment length depends on curvature and the tolerated deviation.

### Example: circular arc

A circle of radius R can be approximated by a regular polygon with n sides. Each side is a chord. As n increases, the polygon boundary approaches the circle in a geometric sense.

For a circle, the perimeter of an inscribed regular n-gon is:
$
P_n=2nR\sin\left(\frac{\pi}{n}\right).
$

The circumference is $2\pi R$. As $n$ increases, $P_n$ approaches $2\pi R$ from below.

This illustrates a convergent geometric approximation. A polygonal approximation is not the exact curve, and the number of segments needed depends on the required tolerance.

## 10. Iterative algorithms and stopping criteria

An iterative method generates a sequence of estimates:
$
x_0,x_1,x_2,\ldots
$

A common stopping test checks whether successive estimates have changed by less than a tolerance $\varepsilon$:
$
|x_{n+1}-x_n|<\varepsilon.
$

For vector estimates, one may use a norm:
$
\|\mathbf{x}_{n+1}-\mathbf{x}_n\|<\varepsilon.
$

The tolerance must be interpreted in context. Its units, scale and relationship to the problem matter.

A small update does not always imply a small solution error. For example, an algorithm may stagnate, converge slowly, be poorly conditioned or approach a non-solution fixed point. A robust implementation may also check:
- a residual or objective-function criterion;
- feasibility of constraints;
- maximum iteration count;
- change in objective value;
- numerical warnings and failure states.

### Worked example: successive estimate

An iterative calculation produces 10.0, 10.5, 10.75, 10.875, ... . Each update halves the remaining difference to 11. The sequence converges to 11.

The difference between consecutive terms decreases, but a real solver should test the residual or a problem-specific criterion as well. This simple sequence is an illustration, not a universal convergence guarantee.

## 11. Time discretisation and simulation

A continuous process may be represented at discrete time steps:
$
t_n=t_0+n\Delta t.
$

A model then updates its state at each step. The choice of Δt can affect numerical stability, computational cost and the fidelity with which rapid changes are represented.

For example, a vehicle movement model sampled at $\Delta t=1\,\mathrm{s}$ may miss short events that occur between samples. A smaller time step can capture more temporal detail, but it also increases data volume and computation. Whether it improves the model depends on the process and measurement design.

A time step is not the same as the temporal accuracy of the input observations.

## 12. Approximation and spatial decision-making

A spatial result should be interpreted relative to its purpose. A coarse grid may be sufficient for regional screening but unsuitable for parcel-level design. A simplified road geometry may be sufficient for a schematic map but inadequate for engineering setting-out.

A useful approximation statement identifies:
1. the exact or intended target quantity;
2. the approximation method;
3. the resolution, tolerance or truncation rule;
4. the assumptions and domain where the approximation is valid;
5. the known sources of error or limitation;
6. the decision for which the approximation is considered adequate.

There is no universally correct resolution or tolerance independent of the application.

## 13. Common errors

- Treating a finite number of iterations as proof of convergence.
- Treating convergence as proof that the result is accurate or physically valid.
- Confusing a sequence with the series formed by summing its terms.
- Assuming every infinite series converges.
- Applying the infinite geometric-series formula when |r| is not less than one.
- Reporting relative error when the reference value is zero.
- Treating raster cell size as positional accuracy or as proof of additional information.
- Assuming finer resolution is always better.
- Ignoring units when setting numerical tolerances.
- Using a small change between iterations as the only stopping criterion.
- Confusing numerical approximation with measurement uncertainty.
- Failing to report the model domain and conditions under which an approximation is valid.

## 14. Exercises

### Exercise 1 — Sequence definition

A sampling point begins at $x_0=250\,\mathrm{m}$ and each subsequent point is $15\,\mathrm{m}$ farther along a straight baseline.

1. Write a recurrence relation.
2. Write an explicit formula for x_n.
3. Calculate x_8.
4. State why this sequence does not describe the uncertainty of the sampled positions.

### Exercise 2 — Geometric sequence

A hypothetical grid spacing begins at $80\,\mathrm{m}$ and is halved at each refinement.

1. Write the nth-term formula, taking n=0 as the first grid.
2. Calculate the spacing at n=4.
3. Calculate the square-cell area at n=4.
4. By what factor does the number of cells over a fixed planar area increase compared with n=0?

### Exercise 3 — Convergence

Consider $a_n=5+12/(n+1)$.

1. Calculate a_0, a_1 and a_3.
2. Find the limit as n approaches infinity.
3. Explain why convergence does not establish that 5 is an accurate representation of a real spatial quantity.

### Exercise 4 — Geometric series

A sequence of hypothetical contributions is 8, 4, 2, 1, ...

1. Identify a_0 and r.
2. Calculate the sum of the first four terms.
3. Calculate the infinite sum.
4. State the condition that makes the infinite sum valid.

### Exercise 5 — Approximation error

An exact reference length is $250.0\,\mathrm{m}$. An approximation is $249.2\,\mathrm{m}$.

1. Calculate the signed error.
2. Calculate the absolute error.
3. Calculate the relative error as a percentage.
4. Explain why this numerical difference alone does not identify the source of error.

### Exercise 6 — Raster refinement

A square raster cell has width $20\,\mathrm{m}$. A second grid uses $5\,\mathrm{m}$ cells over the same planar region.

1. Calculate the cell area in each grid.
2. Calculate the ratio of the cell areas.
3. Estimate the factor by which cell count changes over a fixed region.
4. Explain why the finer grid does not necessarily contain four times as much observed information.

### Exercise 7 — Iterative stopping

An iterative scalar solver produces estimates $20.0,22.0,23.0,23.5,23.75$.

1. Calculate the successive absolute changes.
2. Does the sequence appear to converge?
3. If the stopping tolerance is 0.3 in the same units, at which update would the successive-change test first pass?
4. Give two reasons why a residual or additional diagnostic may still be needed.

## 15. Answers and checks

1. **Sampling sequence:** $x_0=250$ and $x_{n+1}=x_n+15$. Explicitly, $x_n=250+15n$. Thus $x_8=370\,\mathrm{m}$. The formula describes nominal positions only; no stochastic observation or positional uncertainty model is supplied.
2. **Grid refinement:** $h_n=80(1/2)^n\,\mathrm{m}$. At $n=4$, $h_4=5\,\mathrm{m}$. Cell area is $25\,\mathrm{m}^2$. Cell width is reduced by a factor of 16, so cell area is reduced by a factor of 16²=256 and cell count over a fixed area increases by approximately 256. Each halving of cell width produces four times as many cells over a fixed planar area. Boundary effects and grid alignment can alter the exact count.
3. **Limit:** $a_0=17$, $a_1=11$, $a_3=8$. The limit is $5$. It is the limit of this mathematical sequence, not evidence that an external measurement or model target equals 5.
4. **Series:** $a_0=8$, $r=1/2$. First four terms sum to $8+4+2+1=15$. Infinite sum is $8/(1-1/2)=16$. The formula requires $|r|<1$.
5. **Error:** signed error is $249.2-250.0=-0.8\,\mathrm{m}$. Absolute error is $0.8\,\mathrm{m}$. Relative error is $0.8/250.0=0.0032=0.32\%$. The difference could reflect rounding, approximation, measurement, model or other effects; the comparison alone does not identify a cause.
6. **Raster:** $20\,\mathrm{m}$ cells cover $400\,\mathrm{m}^2$; $5\,\mathrm{m}$ cells cover $25\,\mathrm{m}^2$. The cell-area ratio is 16:1. Approximately 16 times as many cells are needed for the same area. Resampling cannot create new observations or recover detail absent from the source.
7. **Iteration:** changes are $2.0,1.0,0.5,0.25$. The sequence appears to approach $24$. The 0.3 successive-change test first passes on the final update (23.5 to 23.75). A residual is needed because small updates can occur away from a solution; also check constraints, stagnation, numerical failure or the maximum-iteration condition.

## 16. Connections across Spatial Methods

- **Spatial algorithms:** iterative solvers, rasterisation, curve approximation, numerical integration, simulation and convergence diagnostics.
- **Spatial data collection:** sampling interval, temporal sampling, measurement resolution and the distinction between sampled data and inferred continuous phenomena.
- **Spatial recipes:** selecting raster resolution, setting tolerances, simplifying geometry and documenting approximation choices.
- **Theoretical foundations:** functions and relationships (SM-FND-001), vectors (SM-FND-001), numerical analysis (SM-FND-016), calculus (SM-FND-003), measurement science (SM-FND-011), spatial statistics (SM-FND-005) and computer science (SM-FND-015).

## 17. Scope and limitations

This module introduces elementary sequences, series, convergence and approximation. It does not establish general convergence tests for arbitrary series, Taylor analysis, numerical integration theory, error propagation for numerical algorithms, floating-point representation, conditioning, stability analysis or convergence proofs for specific iterative solvers. These require more specialised mathematical and numerical-analysis treatment.

The raster and curve examples use simplified planar geometry. Real spatial datasets may involve irregular boundaries, projections, anisotropic cells, complex sampling designs and data-dependent resolution choices.

All numerical examples are hypothetical teaching illustrations, not evidence from a field campaign or operational spatial dataset.

## 18. Further development

The next module develops mathematical modelling and dimensional analysis: defining system boundaries, selecting variables and parameters, translating assumptions into equations, checking units and evaluating whether model outputs are plausible. Numerical stability and error analysis will be developed further in SM-FND-016.


## 19. References and further reading

The explanations and examples in this module are original Spatial Methods teaching material. The following sources support the underlying mathematical definitions and the applied discussion. They are references for further study, not sources of the hypothetical numerical examples.

1. **OpenStax.** *Calculus Volume 2*, Chapter 5, “Sequences and Series,” especially [Section 5.1: Sequences](https://openstax.org/books/calculus-volume-2/pages/5-1-sequences) and [Section 5.2: Infinite Series](https://openstax.org/books/calculus-volume-2/pages/5-2-infinite-series). Used for sequence notation, arithmetic and geometric sequences, limits, monotone convergence, partial sums and geometric-series convergence. Open textbook; consult its published licence before reusing text or figures.
2. **Wong, J. (2020; edited by Holden Lee).** *Math 361S Lecture Notes: Nonlinear Equations in 1D*. Duke University, 15 January 2020. [Lecture PDF](https://services.math.duke.edu/~holee/math361-2020/lectures/Lec2-NonlinearEquations.pdf). Used for iterative approximations, bisection, convergence assumptions, error bounds, stopping criteria and the limitations of step-size and residual tests. These notes address particular root-finding methods; they are not a general proof for every iterative algorithm.
3. **Esri.** *Explore imagery – Spatial resolution*. [ArcGIS tutorial](https://learn.arcgis.com/en/projects/explore-imagery-spatial-resolution/). Tutorial last tested 19 May 2026. Used for raster cell interpretation, the relationship between cell size and represented detail, and the trade-offs among resolution, storage and processing. Product-specific examples are illustrative; raster resolution must be selected for the data and application.

**Source register:** `SM-SRC-000018`, `SM-SRC-000019`, `SM-SRC-000020`.

**Source-use boundary:** These references support introductory mathematics and selected GIS examples. They do not replace specialist treatments of numerical analysis, computational geometry, remote sensing, sampling theory or measurement science. The sources have different purposes and authority; a software tutorial should not be treated as a universal scientific standard.
