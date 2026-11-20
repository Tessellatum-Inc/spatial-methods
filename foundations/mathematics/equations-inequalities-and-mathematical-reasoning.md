# Equations, inequalities and mathematical reasoning

**Foundation domain:** Mathematics for spatial science  
**Subject ID:** SM-FND-001  
**Module:** 04  
**Status:** Initial public foundation; further technical review and expansion required

## 1. From a spatial question to a mathematical statement

A spatial problem often begins in ordinary language:

- Which locations are within 500 m of a facility?
- How much material is needed to cover a site?
- At what distance does a sensor meet a detection threshold?
- Which candidate sites satisfy a set of minimum requirements?
- How many observations are needed to cover a route at a specified interval?

Mathematics makes the conditions explicit. An equation states equality between expressions. An inequality states an ordering or bound. A solution is a value or set of values that makes the statement true.

A correct solution is not automatically a useful spatial answer. The variables, units, assumptions, domain and meaning of the model must also be appropriate.

## 2. Expressions, equations and identities

An **expression** combines numbers, variables and operations. For example:
$$
3x+12
$$

An **equation** states that two expressions are equal:
$$
3x+12=42.
$$

An **identity** is an equality that holds for every value in its stated domain. For example:
$$
a(b+c)=ab+ac.
$$

An equation may hold only for particular values. Solving an equation means finding all values in its domain that make it true.

### 2.1 Variables, parameters and constants

A variable represents a quantity that may vary. A parameter is a value treated as fixed within a particular model, even if it could vary between models or scenarios. A constant is fixed in the mathematical context being considered.

For a map-distance relationship:
$$
G=sM,
$$

where G is ground distance, M is map distance and s is the scale denominator. In one map calculation, s is a fixed parameter. M may vary from one measured map segment to another.

Use symbols consistently. Define each symbol, its unit, domain and role before manipulating an equation.

## 3. Solving a simple equation

Consider:
$$
3x+12=42.
$$

Subtract 12 from both sides:
$$
3x=30.
$$

Divide both sides by 3:
$$
x=10.
$$

The solution is checked by substitution:
$$
3(10)+12=42.
$$

The central principle is that an equation remains equivalent when the same valid operation is applied to both sides. Operations must be reversible on the stated domain if no solutions are to be lost or introduced.

### 3.1 Equivalent transformations

Common operations include:

- adding or subtracting the same quantity on both sides;
- multiplying or dividing both sides by the same non-zero quantity;
- expanding or factorising expressions;
- collecting like terms;
- applying a function that is one-to-one over the relevant domain.

Some transformations require additional care. Squaring both sides, for example, can introduce solutions that do not satisfy the original equation. Dividing by an expression that might be zero can remove a valid case.

Always check candidate solutions in the original statement.

## 4. Rearranging formulas

Spatial work frequently uses formulas whose subject must be changed to answer a different question.

Suppose:
$$
A=lw,
$$

where A is rectangular area, l is length and w is width. If area and length are known and l is non-zero:
$$
w=\frac{A}{l}.
$$

For the map-scale relationship:
$$
G=sM,
$$

the equivalent rearrangements are:
$$
M=\frac{G}{s},\qquad s=\frac{G}{M},
$$

where the denominators must be non-zero and map and ground distances must use compatible units.

### Worked example: estimating a missing dimension

A rectangular survey plot has a stated area of 1,800 m² and a measured length of 60 m. Under the rectangular model:
$$
w=\frac{1{,}800\;\mathrm{m^2}}{60\;\mathrm{m}}=30\;\mathrm{m}.
$$

The dimensional check gives $\mathrm{m}^2/\mathrm{m}=\mathrm{m}$. The answer is mathematically consistent with the model. It does not establish that the real plot is exactly rectangular or that the input area and length are accurate.

## 5. Equations with units

An equation representing a physical or spatial relationship must be dimensionally consistent: terms added or equated must have compatible dimensions.

For example:
$$
d=vt
$$

is dimensionally consistent when d is distance, v is speed and t is time:
$$
\mathrm{m}=(\mathrm{m\,s^{-1}})(\mathrm{s}).
$$

But this expression is not consistent:
$$
d=v+t,
$$

because speed and time have different dimensions and cannot be added as physical quantities.

Dimensional consistency is necessary, but not sufficient. A formula can have correct units and still be based on an inappropriate model or incorrect assumptions.

## 6. Linear equations in spatial contexts

A linear equation in one variable has the form:
$$
ax+b=c,
$$

where a, b and c are fixed coefficients or quantities, and a ≠ 0 for a unique solution.

### Example: a distance threshold

Suppose a simplified one-dimensional model places a facility at coordinate $x=0$. A point lies at coordinate $x$ along the same axis. Its distance from the facility is:
$$
d=|x|.
$$

The condition that the point is exactly 500 m away is:
$$
|x|=500,
$$

so:
$$
x=500\;\mathrm{m}\quad\text{or}\quad x=-500\;\mathrm{m}.
$$

Both sides of the facility satisfy the equation. A single positive solution would incorrectly discard one side.

This is a one-dimensional illustration. In two or three dimensions, distance depends on all coordinate components and the coordinate reference and units must be appropriate.

## 7. Quadratic equations and geometric relationships

A quadratic equation has the form:
$$
ax^2+bx+c=0,\qquad a\ne0.
$$

It may have two distinct real roots, one repeated real root or no real roots, depending on the discriminant:
$$
\Delta=b^2-4ac.
$$

- If $\Delta>0$, there are two distinct real roots.
- If $\Delta=0$, there is one repeated real root.
- If $\Delta<0$, there are no real roots.

The quadratic formula is:
$$
x=\frac{-b\pm\sqrt{b^2-4ac}}{2a}.
$$

### Example: circle intersection with a straight line

A circle centred at the origin with radius r satisfies:
$$
x^2+y^2=r^2.
$$

On the horizontal axis, $y=0$, so:
$$
x^2=r^2.
$$

For $r>0$:
$$
x=\pm r.
$$

The two solutions are the intersections of the circle with the horizontal axis. This simple example shows how an equation can describe a geometric locus and how multiple solutions can represent distinct spatial locations.

The deeper treatment of circles, conics, coordinate geometry and geometric constructions belongs in the coordinate-geometry and geometry foundations.

## 8. Systems of equations

A system contains two or more equations that must hold together. A solution must satisfy every equation in the system.

Consider the illustrative system:
$$
x+y=10
$$
$$
x-y=2.
$$

Adding the equations gives:
$$
2x=12\Rightarrow x=6.
$$

Substituting into the first equation:
$$
6+y=10\Rightarrow y=4.
$$

The solution is $x,y$ = $6,4$.

### Spatial interpretation

A system may represent two independent constraints on two unknown quantities. For example, a simplified allocation problem might require two site areas to sum to a fixed total while their difference is known.

In spatial adjustment, coordinate estimation, network analysis and many other methods, systems can contain many variables and equations. Their matrix representation, rank, conditioning, least-squares solution and constraint structure belong primarily in **SM-FND-002 Linear algebra and matrix methods** and the relevant algorithms. This module introduces the reasoning, not the full computational theory.

A system can have:
- one unique solution;
- no solution because the constraints conflict;
- infinitely many solutions because the equations do not determine all unknowns.

Do not assume a system has a unique solution merely because it contains the same number of equations as unknowns.

## 9. Inequalities

An inequality compares expressions using:

- < : less than;
- ≤ : less than or equal to;
- > : greater than;
- ≥ : greater than or equal to.

For example:
$$
x\leq500
$$

describes all real values no greater than 500, not just the value 500.

### 9.1 Solving inequalities

Consider:
$$
2x+4\leq18.
$$

Subtract 4:
$$
2x\leq14.
$$

Divide by positive 2:
$$
x\leq7.
$$

If both sides are multiplied or divided by a negative number, the inequality sign must reverse. For example:
$$
-2x\leq10
$$

dividing by −2 gives:
$$
x\geq-5.
$$

This sign reversal is essential.

### 9.2 Interval notation

The solution $x\leq7$ can be written:
$$
(-\infty,7].
$$

The square bracket indicates that 7 is included. A parenthesis indicates an excluded endpoint. For example, $0<x\leq10$ is:
$$
(0,10].
$$

Intervals are useful for expressing admissible ranges of values, such as permitted distances, elevations, slopes or sensor readings.

## 10. Absolute-value inequalities and distance bands

Absolute value measures magnitude without sign. On the real number line:
$$
|x|=\begin{cases}x,&x\geq0\\-x,&x<0\end{cases}
$$

For a non-negative threshold a:
$$
|x|\leq a
$$

is equivalent to:
$$
-a\leq x\leq a.
$$

Likewise:
$$
|x|\geq a
$$

means:
$$
x\leq-a\quad\text{or}\quad x\geq a.
$$

### Example: a one-dimensional service zone

A facility is at $x=0$. Locations within $500\,\mathrm{m}$ satisfy:
$$
|x|\leq500.
$$

Therefore:
$$
-500\leq x\leq500.
$$

Locations more than 500 m away satisfy |x| > 500, giving two separate intervals.

In two dimensions, the Euclidean distance condition for a circular zone centred at (x₀,y₀) is:
$$
\sqrt{(x-x_0)^2+(y-y_0)^2}\leq r.
$$

Squaring both non-negative sides gives the equivalent disk condition:
$$
(x-x_0)^2+(y-y_0)^2\leq r^2.
$$

This defines a planar Euclidean buffer only when the coordinate system and units make planar distance appropriate. A 500 m threshold in longitude/latitude degrees is not equivalent to a 500 m planar threshold. Geodesic or suitable projected methods may be required depending on location, extent and accuracy needs.

## 11. Constraints and feasible sets

A constraint is a mathematical condition that a candidate solution must satisfy. A feasible set is the collection of all candidates satisfying every stated constraint.

Suppose a hypothetical site must satisfy:
$$
A\geq2\;\mathrm{ha}
$$
$$
D\geq500\;\mathrm{m}
$$
$$
S\leq10\%
$$

where A is usable area, D is distance from a specified hazard boundary, and S is a defined slope measure.

A candidate site is feasible under this simplified model only if all three conditions hold. Passing these conditions does not establish overall suitability. Legal, environmental, access, ownership, data-quality and engineering criteria may also apply.

### 11.1 Logical combinations

- **AND** means every condition must be true.
- **OR** means at least one condition must be true.
- **NOT** means a condition must be false.

For example, a candidate might be retained if it is within an allowed administrative area AND outside a restricted zone. The exact spatial predicate, boundary treatment, distance model and data validity must be specified.

A threshold is not a complete decision model. The choice of threshold, its evidence, uncertainty and consequences should be documented.

## 12. Domains, ranges and admissible solutions

A solution must be interpreted within the domain of the original problem.

For example, a computed travel time of −4 minutes may solve an unconstrained algebraic equation but is not a valid elapsed travel time in an ordinary forward-time model.

Likewise:
- a number of assets must be a non-negative integer;
- an area cannot be negative;
- a probability must lie between 0 and 1;
- a logarithm's argument must be positive;
- a physical distance is non-negative.

The domain can remove algebraic candidates that have no meaning in the application.

## 13. Mathematical reasoning and verification

A disciplined solution process is:

1. **Define the question.** State what is unknown and what is being asked.
2. **Define symbols.** Give each variable a meaning, unit and domain.
3. **State assumptions.** Identify the model, geometry, reference and simplifications.
4. **Translate.** Write the equation, inequality or system.
5. **Solve.** Use valid equivalent transformations.
6. **Check.** Substitute into the original statement and inspect units.
7. **Interpret.** Explain what the solution means in the spatial context.
8. **Test plausibility.** Check sign, magnitude, bounds and edge cases.
9. **Communicate limitations.** State what the mathematical result does not establish.

### 13.1 A worked threshold decision

A simplified screening rule retains a candidate when its measured distance d from a specified feature is at least 250 m and no more than 1,000 m:
$$
250\;\mathrm{m}\leq d\leq1{,}000\;\mathrm{m}.
$$

A candidate with $d=720\,\mathrm{m}$ satisfies the numerical condition. A candidate with $d=1{,}020\,\mathrm{m}$ does not.

Before applying this to real data, the analyst must define:
- the feature from which distance is measured;
- whether distance is straight-line, network or geodesic;
- the coordinate reference and units;
- how boundaries and uncertain positions are treated;
- whether the thresholds are justified by policy or evidence.

The inequality makes the rule explicit. It does not justify the rule.

## 14. Common errors

- Performing an operation on one side of an equation but not the other.
- Dividing by an expression that could be zero without considering that case.
- Squaring both sides and accepting extraneous solutions.
- Forgetting to reverse an inequality when multiplying or dividing by a negative value.
- Treating an inequality as if it identifies one exact value.
- Ignoring units or adding quantities with incompatible dimensions.
- Accepting a mathematical solution outside the problem's domain.
- Assuming a system has a unique solution without checking consistency and independence.
- Treating a threshold as scientifically or legally justified merely because it is expressed precisely.
- Applying planar distance constraints to geographic coordinates without checking whether the method is appropriate.
- Reporting a feasible candidate as fully suitable when only a subset of criteria has been tested.

## 15. Exercises

Show the transformations and check each answer in the original statement. Use units and state any assumptions.

### Exercise 1 — Rearranging a spatial formula

A rectangular field has area $A=2{,}400\,\mathrm{m}^2$ and width $w=40\,\mathrm{m}$.

1. Starting from A = lw, rearrange the equation to make l the subject.
2. Calculate the length.
3. Check the dimensions and substitute the answer back into the area equation.

### Exercise 2 — Map-scale equation

A map has representative fraction $1:20{,}000$. A route is represented by a map length $M=6.5\,\mathrm{cm}$.

1. Write an equation for ground distance G in centimetres.
2. Calculate G in metres.
3. Rearrange the relationship to make M the subject.
4. Explain why the result does not establish positional accuracy.

### Exercise 3 — Quadratic solutions

A circle centred at the origin has radius 12 m.

1. Write its equation.
2. Find its intersections with the x-axis.
3. Explain why there are two solutions.
4. State the units of the coordinates.

### Exercise 4 — Inequality and service range

A simplified one-dimensional facility model is centred at $x=0$. A service range includes all locations no more than $750\,\mathrm{m}$ away.

1. Express the rule using absolute value.
2. Express the solution as a double inequality.
3. Write the interval notation.
4. Explain how the model would change in two dimensions.

### Exercise 5 — Constraint screening

A hypothetical site must have usable area of at least 3 ha, distance of at least 400 m from a restricted boundary, and slope no greater than 8%.

Three candidates have:

| Candidate | Usable area | Distance | Slope |
|---|---:|---:|---:|
| A | 3.4 ha | 520 m | 7% |
| B | 4.0 ha | 390 m | 5% |
| C | 2.8 ha | 900 m | 6% |

1. Express the three constraints mathematically.
2. Identify which candidates satisfy all three.
3. Explain why passing the simplified screen does not establish final site suitability.

### Exercise 6 — Detecting an invalid transformation

A learner solves $x^2=9$ by taking the square root and reports only $x=3$.

1. Find all real solutions.
2. Explain what was omitted.
3. Substitute both solutions into the original equation.

### Exercise 7 — Equation, inequality or system?

For each question, decide whether an equation, inequality or system is the most natural first mathematical representation. Explain why.

1. A route must be exactly 12 km long.
2. A sensor reading must be below a maximum threshold.
3. Two land parcels must sum to a fixed total area, and one must be twice the other.
4. A point is exactly 500 m from a fixed origin in a one-dimensional model.
5. A candidate site must satisfy minimum area, maximum slope and minimum separation conditions.

## 16. Answers and checks

1. **Rectangular field:** $l=A/w=2{,}400\,\mathrm{m}^2/40\,\mathrm{m}=60\,\mathrm{m}$. Check: $60\,\mathrm{m}\times40\,\mathrm{m}=2{,}400\,\mathrm{m}^2$.
2. **Map scale:** $G=6.5\,\mathrm{cm}\times20{,}000=130{,}000\,\mathrm{cm}=1{,}300\,\mathrm{m}$. $M=G/20{,}000$ when $G$ is expressed in the same length unit. Scale conversion does not validate the source geometry or positional accuracy.
3. **Circle:** $x^2+y^2=144\,\mathrm{m}^2$. On the x-axis $y=0$, so $x^2=144$ and $x=-12\,\mathrm{m}$ or $x=+12\,\mathrm{m}$. Both points lie on the circle.
4. **Service range:** $|x|\leq750\,\mathrm{m}$; equivalently $-750\,\mathrm{m}\leq x\leq750\,\mathrm{m}$; interval $[-750,750]\,\mathrm{m}$. In two dimensions the Euclidean disk condition is $(x-x_0)^2+(y-y_0)^2\leq750^2$, subject to an appropriate planar coordinate model.
5. **Screening:** $A\geq3\,\mathrm{ha}$, $D\geq400\,\mathrm{m}$, $S\leq8\%$. Candidate A satisfies all three. B fails the distance condition; C fails the area condition. This is only a simplified screen, not a complete suitability or approval assessment.
6. **Invalidly incomplete root:** $x=-3$ and $x=+3$. Both square to 9; reporting only the principal square root omits the negative solution.
7. **Representation:** (1) equation, $L=12\,\mathrm{km}$; (2) inequality, reading below the maximum; (3) system, $A_1+A_2=A_{\mathrm{total}}$ and $A_1=2A_2$; (4) equation, $|x|=500\,\mathrm{m}$; (5) system of inequalities, because all constraints must hold together.

## 17. Connections across Spatial Methods

- **Spatial algorithms:** threshold queries, spatial filters, geometric intersection, constrained optimisation and rule-based classification.
- **Spatial data collection:** acceptable measurement ranges, sensor thresholds, survey tolerances and field eligibility rules.
- **Spatial recipes:** site screening, proximity analysis, quality checks, route-length constraints and field planning.
- **Theoretical foundations:** linear algebra and matrix methods $SM-FND-002$, coordinate geometry $SM-FND-006$, probability and statistical inference $SM-FND-004$, geodesy and reference systems $SM-FND-008$, measurement science $SM-FND-011$ and numerical analysis $SM-FND-016$.

## 18. Scope and limitations

This module introduces algebraic and logical reasoning for spatial problems. It does not develop matrix solution methods, nonlinear optimisation, formal logic, numerical root-finding, statistical hypothesis testing, geodetic distance computation or legal standards for site selection. Those require dedicated treatment.

All numerical scenarios are hypothetical teaching examples. The screening thresholds are stipulated for illustration and are not professional, regulatory or engineering recommendations.

## 19. Further development

The next module develops functions and relationships: inputs and outputs, domains and ranges, linear and nonlinear models, inverse functions, composition and the interpretation of spatial phenomena as mathematical mappings.


## References and further reading

The explanations and spatial examples are original Spatial Methods teaching material. These sources support the introductory algebraic methods used in this module.

1. **OpenStax.** *Algebra and Trigonometry 2e*. [Chapter 2: Equations and Inequalities](https://openstax.org/books/algebra-and-trigonometry-2e/pages/2-introduction-to-equations-and-inequalities), including linear and quadratic equations, absolute-value inequalities and applications.
2. **OpenStax.** *Algebra and Trigonometry 2e*. [Chapter 11: Systems of Equations and Inequalities](https://openstax.org/books/algebra-and-trigonometry-2e/pages/11-introduction-to-systems-of-equations-and-inequalities). Used for simultaneous equations and feasible sets.
3. **BIPM.** (2026). *The International System of Units (SI Brochure)*, 9th edition, version 4.01. [Official publication]$https://www.bipm.org/en/si-brochure-9$. Used for quantity and unit conventions in dimensional checks.

**Source register:** `SM-SRC-000021`, `SM-SRC-000022`.

**Limitations:** These sources support introductory algebra, not the full treatment of constrained optimisation, linear algebra, numerical solution or formal mathematical proof.
