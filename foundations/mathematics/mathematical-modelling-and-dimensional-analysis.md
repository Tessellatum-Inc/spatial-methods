# Mathematical modelling and dimensional analysis for spatial science

**Foundation domain:** Mathematics for spatial science  
**Subject ID:** \`SM-FND-001\`  
**Module:** 09  
**Status:** Initial public foundation; technical review and expansion required  
**Prerequisites:** Modules 01–05 are recommended. Modules 02–03 are especially useful for numerical values, ratios and rates.  
**Related foundations:** Measurement science (\`SM-FND-011\`), linear algebra (\`SM-FND-002\`), calculus (\`SM-FND-003\`), probability and statistics (\`SM-FND-004\`), geodesy (\`SM-FND-008\`), numerical analysis (\`SM-FND-016\`).

## 1. Why modelling matters

Spatial science is not simply the production of maps or the execution of spatial tools. It involves making a representation of some part of the world so that a question can be answered.

Examples include:

- estimating the population within a service area;
- predicting how a measured quantity varies across a surface;
- estimating the distance or time between locations;
- comparing candidate sites against constraints;
- converting sensor observations into a mapped quantity;
- estimating how a landscape variable changes over time.

Each task requires choices. What is the system? Which objects and processes matter? What counts as an input? Which relationships are assumed? What is ignored? What would make the result useful or misleading?

A mathematical model makes some of these choices explicit. It does not reproduce the whole world. It represents selected features of a problem for a stated purpose.

The quality of a model therefore depends on more than algebra. It depends on whether the question, quantities, assumptions, data, mathematical relationships and interpretation fit together.

## 2. What is a mathematical model?

A **mathematical model** is a structured representation of a system or problem using quantities, variables, parameters, relationships, constraints and assumptions.

A model may be as simple as:

$$
d=vt
$$

where distance travelled, average speed and elapsed time are related under specified conditions.

A more involved spatial model might be:

$$
\hat{P}_j = \sum_{i=1}^{n} w_{ij}P_i
$$

where an estimated population quantity for target area \(j\) is assembled from source-area quantities \(P_i\) using allocation weights \(w_{ij}\).

The second expression is not automatically a valid population model. The weights need a defensible interpretation, their construction requires data and assumptions, and the output must be evaluated. The equation only makes the proposed relationship explicit.

### 2.1 A model is not the same as data, an algorithm or a map

These things are related but different:

| Element | What it is | Example |
|---|---|---|
| Real system | The phenomenon or process being studied | People living and moving within a city |
| Question | The information or decision sought | Estimate residents within a defined catchment |
| Data | Recorded or compiled information | Population counts, boundaries and building footprints |
| Conceptual model | A description of the important entities and relationships | Residents are allocated to locations and aggregated by catchment |
| Mathematical model | The formal relationships and assumptions | Allocation weights and a summation rule |
| Algorithm | A procedure for carrying out a computation | Intersect polygons, calculate weights and sum allocated counts |
| Implementation | Executable code or a software workflow | A Python or GIS processing pipeline |
| Output | The result produced | Estimated catchment population |
| Evaluation | Evidence about whether the model is suitable | Comparison with independent counts or sensitivity analysis |

A map is often a way to inspect or communicate a model output. It is not, by itself, evidence that the model is valid.

## 3. Define the problem before choosing equations

A useful model begins with a question that can be interpreted consistently.

Compare:

- “Find underserved neighbourhoods.”
- “Estimate the number of residents in each defined administrative area who are more than a specified network travel time from a selected class of health facility, using a stated population reference date and a specified road-network dataset.”

The second statement is more operational. It identifies a quantity, spatial units, a relationship, a threshold, a facility class and data references. It still requires choices about travel mode, network access, facility status, population allocation and the meaning of “underserved”.

Before modelling, write down:

1. **Purpose:** What question will the model answer, and who will use the result?
2. **Target quantity or decision:** What exactly is to be estimated, predicted, compared or selected?
3. **Spatial domain:** Which locations, boundaries, coordinate references or network areas are included?
4. **Temporal domain:** What date, interval, epoch or time step applies?
5. **Unit of analysis:** Is the model about a point, parcel, raster cell, road segment, administrative area, person or event?
6. **Resolution:** At what spatial and temporal detail are inputs and outputs represented?
7. **Conditions of use:** Under what circumstances should the result be interpreted or not used?

A vague question often produces an elaborate calculation with no clear interpretation.

## 4. Identify the model components

A model becomes easier to inspect when its components are named explicitly.

### 4.1 Variables

A **variable** represents a quantity that may vary within the model.

Examples include:

- \(d\): distance, in metres;
- \(t\): elapsed time, in seconds;
- \(v\): speed, in metres per second;
- \(A\): area, in square metres;
- \(N\): a count of people or objects;
- \(z(x,y)\): a spatially varying surface value.

Every variable should have a definition, unit where applicable, reference and valid domain.

### 4.2 Parameters

A **parameter** is a quantity treated as fixed for a particular model run or formulation.

Examples include:

- a stipulated travel-speed value;
- a distance-decay parameter;
- a sensor calibration coefficient;
- a threshold used to classify locations;
- a cell size chosen for a raster representation.

A parameter is not necessarily a universal constant. It may be estimated from data, taken from a specification, chosen by an analyst or stipulated for a scenario. Its origin and status should be recorded.

### 4.3 Inputs, outputs and intermediate quantities

A model should distinguish:

- **Inputs:** quantities supplied to the model;
- **Parameters:** quantities governing the model relationship;
- **Intermediate quantities:** values calculated along the way;
- **Outputs:** quantities answering the stated question.

This prevents an intermediate calculation from being mistaken for the final target quantity.

### 4.4 Constraints

A **constraint** restricts the combinations of values or solutions that are admissible.

Examples:

- a population count cannot be negative;
- a probability lies between zero and one;
- a selected site must lie within a permitted search area;
- a route must connect to the specified network;
- a modelled speed must satisfy the stated scenario bounds.

A constraint may be mathematical, physical, operational, legal or policy-based. These categories should not be confused. A mathematical constraint does not establish that a legal or policy requirement has been correctly interpreted.

## 5. Build a model in stages

The following workflow is reusable across many spatial tasks.

### Stage 1 — State the question and target

Write the question in a form that identifies the output.

Weak: “Analyse flood risk.”

More precise: “Estimate the depth of surface water at each cell for a specified rainfall scenario, terrain representation, drainage assumption and simulation period.”

The more precise question still needs hydrological and hydraulic theory, appropriate data and validation. Its value is that it makes the modelling target discussable.

### Stage 2 — Draw the system boundary

Specify what is inside and outside the model.

For a travel-time model, for example:

- included: origins, destinations, selected roads, travel mode and assumed speeds;
- possibly excluded: congestion, waiting, access restrictions, road closures, pedestrian conditions and service availability.

An omitted process is not necessarily a flaw. It becomes a problem when the model is used as though the process had been represented.

### Stage 3 — Define variables, parameters and units

Prepare a variable register before calculating.

| Symbol | Meaning | Unit | Source or status |
|---|---|---|---|
| \(d\) | Route distance | m | Calculated from a specified network |
| \(v\) | Assumed average speed | m/s | Scenario parameter |
| \(t\) | Travel time | s | Model output |
| \(t_0\) | Reference time | s | Defined scenario input |

This example assumes a single representative speed. A real journey may require segment-specific speeds, turn delays, waiting time and time-dependent conditions.

### Stage 4 — Choose relationships

Select a mathematical relationship that reflects the intended process and available evidence.

For a constant-speed journey:

$$
t=\frac{d}{v}
$$

This is a simple deterministic model. It assumes that the distance and speed are defined consistently and that the chosen speed represents the journey over the modelled interval.

A more detailed model might sum segment travel times:

$$
t_{\mathrm{total}}=\sum_{i=1}^{n}\frac{d_i}{v_i}
$$

This still omits delays unless they are represented explicitly. A more complex equation is not automatically a better model.

### Stage 5 — Check dimensions, units and references

Before calculating, verify that the relationship is dimensionally consistent and that values use compatible units and references.

For spatial quantities, check coordinate reference systems, measurement basis, time reference, boundary definition and data alignment as appropriate.

### Stage 6 — Solve and implement

Carry out the mathematical calculation or implement the algorithm.

Keep the model definition separate from the software procedure. This makes it possible to inspect whether a coding error, data-processing choice or model assumption caused an unexpected result.

### Stage 7 — Inspect and evaluate

Ask:

- Are outputs within plausible ranges?
- Are constraints satisfied?
- Does the result change sensibly when inputs change?
- Does the model behave sensibly in limiting or edge cases?
- Can results be compared with independent observations or another defensible reference?
- Are errors, uncertainty and data limitations important to the intended use?

### Stage 8 — Interpret and communicate

Report what the result means, for which domain, time, data and assumptions.

Do not report a model output as though it were a direct observation. Label estimates, predictions, scenarios and classifications accurately.

## 6. Dimensional analysis: checking the structure of equations

Dimensional analysis examines the physical dimensions of quantities in a mathematical relationship.

Common dimensions include:

| Quantity | Dimension |
|---|---|
| Length | \(L\) |
| Time | \(T\) |
| Mass | \(M\) |
| Area | \(L^2\) |
| Volume | \(L^3\) |
| Speed | \(LT^{-1}\) |
| Acceleration | \(LT^{-2}\) |
| Density by area (count per area) | \(L^{-2}\) for a dimensionless count |
| Volumetric flow rate | \(L^3T^{-1}\) |

The notation \(L,T,M\) represents dimensions, not specific units. A length may be expressed in metres, kilometres or another compatible length unit.

### 6.1 Dimensional homogeneity

For an equation representing a physical relationship, the terms being added or equated must have compatible dimensions.

Consider:

$$
d=vt
$$

The dimensions are:

$$
[d]=L
$$

$$
[v][t]=(LT^{-1})(T)=L
$$

The dimensions agree.

Now consider the proposed expression:

$$
d=v+t
$$

Speed and time have different dimensions, so they cannot be added as written to represent a distance.

Dimensional inconsistency is a strong warning that an equation is wrong or incompletely specified.

Dimensional consistency is **necessary in physical equations but not sufficient to establish correctness**. Many incorrect equations are dimensionally consistent.

### 6.2 Addition and subtraction

Quantities added or subtracted must be compatible in dimension and must represent quantities that can meaningfully be combined.

For example:

$$
250\,\mathrm{m}+0.4\,\mathrm{km}
$$

Convert to a common unit:

$$
250\,\mathrm{m}+400\,\mathrm{m}=650\,\mathrm{m}
$$

But adding \(250\,\mathrm{m}\) to \(0.4\,\mathrm{m}^2\) is not meaningful as a length calculation.

Even equal dimensions do not guarantee semantic compatibility. Two quantities may both be lengths but refer to different objects, epochs, paths or measurement bases.

### 6.3 Products and quotients

Dimensions combine under multiplication and division.

For a rectangular area:

$$
[A]=[l][w]=L^2
$$

For average speed:

$$
[v]=\frac{[d]}{[t]}=LT^{-1}
$$

For a count density over area:

$$
[\rho]=\frac{1}{L^2}=L^{-2}
$$

Here, the count is treated as a dimensionless count of entities. The unit still communicates the meaning, such as residents per square kilometre.

### 6.4 Dimensionless quantities

A quantity is dimensionless when its dimensions cancel.

Examples include:

- a ratio of two lengths expressed on the same basis;
- a percentage;
- a map scale ratio;
- a probability;
- a ratio of areas.

Dimensionless does not mean meaningless. A scale ratio, probability and percentage describe different concepts even though each is dimensionless.

## 7. Units and conversion

A unit is the defined reference used to express a quantity. A conversion changes the numerical representation without changing the quantity.

For example:

$$
1\,\mathrm{km}=1000\,\mathrm{m}
$$

If a route length is \(2.4\,\mathrm{km}\), then:

$$
2.4\,\mathrm{km}\times
\frac{1000\,\mathrm{m}}{1\,\mathrm{km}}
=2400\,\mathrm{m}
$$

The kilometre units cancel, leaving metres.

### 7.1 Use conversion factors as ratios equal to one

A conversion factor must preserve the quantity.

For a speed of \(36\,\mathrm{km/h}\):

$$
36\,\frac{\mathrm{km}}{\mathrm{h}}
\times
\frac{1000\,\mathrm{m}}{1\,\mathrm{km}}
\times
\frac{1\,\mathrm{h}}{3600\,\mathrm{s}}
=10\,\mathrm{m/s}
$$

The units cancel to metres per second.

A common error is to convert only the numerator or denominator of a compound unit. Always write the conversion factor and inspect the remaining units.

### 7.2 Derived units

Derived units combine base units. For example:

$$
1\,\mathrm{m/s}=1\,\mathrm{m}\,\mathrm{s}^{-1}
$$

$$
1\,\mathrm{m^2}=1\,\mathrm{m}\times1\,\mathrm{m}
$$

The SI system defines named derived units for many quantities. Spatial work also uses domain-specific units and conventions. The meaning of a unit must be read together with the quantity definition.

### 7.3 Coordinate units require special care

Coordinates may be expressed in angular units, linear units or local engineering units. A numerical coordinate value does not become a distance merely because it contains a number.

For example, a longitude difference in degrees cannot be treated as a constant east-west distance in metres at every latitude. Coordinate reference systems, map projections and geodetic calculations determine how coordinate values relate to distances and areas.

Dimensional analysis cannot replace a correct coordinate reference system or geodetic method.

## 8. Scaling and spatial resolution

Scaling examines how a modelled quantity changes when one or more inputs are multiplied by a factor.

Suppose a square cell has side length \(s\) and area:

$$
A=s^2
$$

If the cell width is multiplied by \(k\), the area becomes:

$$
A'=(ks)^2=k^2A
$$

If cell width is halved, cell area becomes one quarter of its former value.

For a fixed planar region, the approximate number of cells therefore increases by a factor of four when cell width is halved, assuming the same coverage and ignoring boundary and alignment effects.

This is a geometric scaling relationship. It does not imply that the finer raster is more accurate or contains more observed information. The value of finer resolution depends on the source data, measurement process, phenomenon and analytical purpose.

### Worked example: cell count

A square study region is represented by a grid of 100 m cells. Consider a grid with 50 m cells over the same region.

The linear cell width is halved:

$$
k=\frac{50}{100}=0.5
$$

The cell-area ratio is:

$$
\frac{A'}{A}=k^2=0.25
$$

Each new cell covers one quarter of the original area. The approximate number of cells over the fixed region is therefore four times as large.

The exact count can differ because of grid alignment, extent rounding, boundary handling and the shape of the study area.

## 9. A complete worked example: estimating mean population density

This example illustrates model construction and dimensional checks. All values are hypothetical.

### 9.1 Question

What is the mean population density of a defined study area at a specified population reference date?

### 9.2 Scope and assumptions

- The study boundary is fixed and defined.
- The population count refers to that boundary and a stated reference date.
- The area is supplied in square kilometres on a stated area basis.
- The example treats the total population and area as known inputs.
- Within-area population variation is not modelled.

### 9.3 Variables and model

Let:

- \(N=18{,}000\) residents;
- \(A=4.5\,\mathrm{km^2}\);
- \(\rho\) be mean population density.

The model is:

$$
\rho=\frac{N}{A}
$$

The dimension is:

$$
[\rho]=L^{-2}
$$

The practical unit is residents per square kilometre.

### 9.4 Calculation

$$
\rho=\frac{18{,}000\,\mathrm{residents}}
{4.5\,\mathrm{km^2}}
=4{,}000\,\mathrm{residents\,km^{-2}}
$$

### 9.5 Interpretation

The total population divided by the total area is 4,000 residents per square kilometre.

This is an area-wide average. It does not say that each square kilometre contains exactly 4,000 residents. It does not identify where people live, estimate daytime population, describe access to services or establish population distribution within the boundary.

### 9.6 Sensitivity to the area input

If the same population count were divided by an area of \(5.0\,\mathrm{km^2}\), the estimated density would be:

$$
\rho=\frac{18{,}000}{5.0}
=3{,}600\,\mathrm{residents\,km^{-2}}
$$

The output changes because the denominator changes. This does not tell us which area is correct. That depends on the study boundary and area calculation.

A useful model report should therefore preserve the population reference, boundary definition and area method, not only the final density value.

## 10. Model behaviour, plausibility and sensitivity

Dimensional consistency checks the structure of an equation. Other checks are needed to understand model behaviour.

### 10.1 Plausibility checks

Ask whether:

- the sign of the result is meaningful;
- the magnitude is plausible for the stated context;
- the result satisfies declared constraints;
- the output units match the target quantity;
- the model responds sensibly to changes in inputs;
- edge cases expose undefined or unrealistic behaviour.

For the density model, a positive population and positive area produce a non-negative density. A zero area makes the ratio undefined. A negative population or negative physical area indicates invalid inputs or a different mathematical interpretation.

### 10.2 Limiting cases

A limiting-case check asks what happens as an input approaches a meaningful boundary.

For:

$$
t=\frac{d}{v}
$$

if \(d=0\) and \(v>0\), the model gives \(t=0\). If \(v=0\), the expression is undefined. If speed approaches zero while distance remains positive, the calculated time grows without bound.

This behaviour is consistent with the simple model's interpretation, but it does not represent all real travel conditions. It also shows why a zero-speed case must be handled explicitly rather than passed blindly into software.

### 10.3 Sensitivity

Sensitivity describes how an output changes when an input changes.

For the density model:

$$
\rho=\frac{N}{A}
$$

holding \(N\) fixed, increasing \(A\) decreases \(\rho\). Holding \(A\) fixed, increasing \(N\) increases \(\rho\).

Sensitivity is not the same as uncertainty. Sensitivity describes model response to input changes. Uncertainty describes limited knowledge or variability in quantities and model results. A formal treatment of uncertainty propagation belongs in measurement science and probability/statistics.

## 11. Model types and when they are useful

Different questions require different model structures.

| Model type | Basic idea | Spatial example | Important caution |
|---|---|---|---|
| Deterministic | Same inputs and parameters produce the same output | Planar distance from coordinates | Deterministic does not mean accurate |
| Empirical | Relationship is estimated from observations | Predicting a measured environmental variable from predictors | Fit does not prove causality or validity outside the data domain |
| Mechanistic or process-based | Encodes a proposed process or physical relationship | Simplified flow or transport model | Requires suitable theory, parameters and boundary conditions |
| Statistical | Represents variation and estimates relationships from data | Spatial regression | Requires assumptions, diagnostics and an appropriate sampling design |
| Simulation | Repeatedly computes possible system states or scenarios | Land-use change scenarios | Scenario outputs are conditional on model structure and inputs |
| Optimisation | Searches for a solution that maximises or minimises an objective under constraints | Facility location or route allocation | The objective and constraints encode choices; a mathematical optimum is not automatically a socially preferred decision |

These categories can overlap. A process-based model may contain statistical parameters; a simulation may use optimisation; an empirical model may be deterministic once fitted.

## 12. Common modelling and dimensional-analysis errors

| Error | Why it matters | Better practice |
|---|---|---|
| Starting with software rather than a question | The workflow may calculate something unrelated to the decision | Define the target before choosing tools |
| Leaving the system boundary implicit | Readers cannot tell what is represented or omitted | State spatial, temporal and process boundaries |
| Mixing observations, parameters and assumptions | The evidence behind inputs becomes unclear | Label measured, estimated, stipulated and derived values |
| Omitting units | Calculations can silently mix incompatible quantities | Record units at input, intermediate and output stages |
| Adding unlike dimensions | The equation is structurally invalid | Check dimensions before numerical substitution |
| Treating dimensional consistency as proof | Many incorrect equations pass the dimensional check | Also inspect theory, data, boundary cases and independent evidence |
| Treating coordinate values as distances | Angular and projected coordinates have different meanings | Use the appropriate CRS and geodetic or planar method |
| Confusing cell size with accuracy | A finer grid may only resample or interpolate the same information | Describe source resolution, measurement support and uncertainty |
| Treating a scenario parameter as a measured fact | Outputs may appear more authoritative than their inputs justify | Record parameter origin and scenario status |
| Reporting an average as a local description | Aggregation hides within-area variation | State the aggregation level and inspect distribution |
| Assuming more complexity means better quality | Additional parameters can make a model harder to identify or validate | Add complexity only when the question and evidence justify it |
| Omitting model limitations | Users may apply results beyond their valid domain | State intended use, exclusions and failure conditions |

## 13. Exercises

Use the definitions and reasoning in this module. Show units and explain your interpretation.

### Exercise 1 — Define a model

A project wants to estimate the travel time from a set of residential origins to a health facility.

Write a concise model specification that identifies:
- the target output;
- the spatial and temporal scope;
- at least four required inputs;
- at least three assumptions or omitted processes;
- one way the result could be evaluated.

### Exercise 2 — Dimensional consistency

A proposed model states:

$$
A=lw+vt
$$

where \(A\) is area, \(l\) and \(w\) are lengths, \(v\) is speed and \(t\) is time.

Is the equation dimensionally consistent as written? Explain.

### Exercise 3 — Unit conversion

Convert \(54\,\mathrm{km/h}\) to metres per second. Show the conversion factors and unit cancellation.

### Exercise 4 — Spatial scaling

A raster cell width changes from 30 m to 10 m.

1. What is the ratio of new cell width to old cell width?
2. What is the ratio of new cell area to old cell area?
3. Approximately how does the number of cells change over a fixed region?
4. Does this prove the new raster is three times more accurate? Explain.

### Exercise 5 — Inspect a density model

A report states that a district has 2,400 residents per square kilometre.

List at least five additional pieces of information needed to interpret and assess this result.

### Exercise 6 — Limiting case

For \(t=d/v\), explain what happens when:
1. \(d=0\) and \(v>0\);
2. \(v=0\) and \(d>0\);
3. both \(d\) and \(v\) are multiplied by the same positive factor.

State what the model does not represent.

### Exercise 7 — Model critique

A team uses straight-line distance between each home and the nearest hospital to classify people as having “good access”.

Identify at least six assumptions, omissions or definitional issues that should be examined before interpreting the classification.

## 14. Answers and checks

### Exercise 1

A defensible specification might estimate network travel time from each defined residential origin to a selected facility, using a specified network snapshot, travel mode, access rules, speed assumptions and time period. Inputs could include origins, facility locations/status, routable network, segment lengths, travel speeds and access restrictions. Assumptions might exclude congestion, waiting, service availability and unrecorded barriers. Evaluation could compare selected routes or travel times with independent field observations. Other answers are possible if scope and assumptions are explicit.

### Exercise 2

No. The first term \(lw\) has dimension \(L^2\), while \(vt\) has dimension \(L\). Quantities of different dimensions cannot be added to produce area. A dimensionally consistent expression would require a different model term with area dimension, but dimensional consistency alone would not establish the correct relationship.

### Exercise 3

$$
54\,\frac{\mathrm{km}}{\mathrm{h}}
\times\frac{1000\,\mathrm{m}}{1\,\mathrm{km}}
\times\frac{1\,\mathrm{h}}{3600\,\mathrm{s}}
=15\,\mathrm{m/s}
$$

### Exercise 4

1. Width ratio: \(10/30=1/3\).
2. Area ratio: \((1/3)^2=1/9\).
3. Approximately nine times as many cells over the same region, ignoring edge and alignment effects.
4. No. Cell size describes the grid spacing, not the accuracy, source information content or validity of the represented values.

### Exercise 5

Possible requirements include the boundary used, population definition, population reference date, source and method of the count, area calculation method, area unit, treatment of water or uninhabited land, and whether the figure is an aggregate mean or a spatially varying estimate.

### Exercise 6

1. The model gives \(t=0\).
2. The expression is undefined; the model does not specify travel at zero speed.
3. The ratio \(d/v\) is unchanged because the same factor cancels.
   
The simple model omits acceleration, waiting, route changes, congestion, access and time-varying speed.

### Exercise 7

Consider whether straight-line distance is the intended access measure; whether roads, paths, rivers, barriers and terrain affect travel; whether the facility is open and provides the relevant service; whether travel mode matters; whether the origin represents a home or an area centroid; whether distance or travel time is the target; whether the threshold is justified; whether the data are current; and whether access constraints or population vulnerability are being ignored. “Good access” needs an explicit operational definition and should not be inferred from distance alone.

## 15. Connections across Spatial Methods

Mathematical modelling is a shared activity across the four pillars.

- **Spatial Algorithms:** the model defines the mathematical problem an algorithm is intended to solve. Algorithm design and correctness are developed further in computer science and numerical analysis.
- **Spatial Recipes:** a recipe should expose its inputs, parameters, transformations, assumptions, outputs and quality checks. The model should be understandable independently of a particular software interface.
- **Spatial Data Collection:** measurement design determines which quantities can be observed, at what resolution and with what limitations. The measurement-science foundation develops measurands, measurement models and uncertainty.
- **Theoretical Foundations:** physical, statistical, geometric and computational theories justify specialised model structures. This module provides common language rather than replacing those subjects.
- **Real-world applications:** every model has a purpose and context. A mathematically valid output can still be unsuitable for a planning, engineering, environmental or public decision.

## 16. Scope and limitations

This module introduces a general modelling workflow and elementary dimensional reasoning. It does not provide a complete treatment of:

- probability distributions, statistical estimation, model selection or spatial dependence;
- measurement uncertainty propagation and formal uncertainty budgets;
- calculus, differential equations or continuous physical modelling;
- matrix methods, least-squares estimation or optimisation;
- geodetic computation, map-projection theory or Earth-surface geometry;
- numerical conditioning, floating-point error or solver stability;
- advanced dimensional analysis, similarity theory or derivation of governing equations from physical principles.

Those topics have dedicated homes in the relevant Spatial Methods foundations. The examples here are hypothetical teaching illustrations. They are not field measurements, official population statistics, validated travel-time predictions or professional design recommendations.

Dimensional consistency can identify some invalid relationships, but it cannot prove a model is true, empirically supported or fit for a decision. Model validation requires evidence appropriate to the question and intended use.

## 17. Further development

The next planned mathematics module is **introductory discrete mathematics and logic**. It will develop sets, relations, propositions, Boolean operations and introductory graph language used in spatial queries and algorithms.

Trigonometry is also a required part of the mathematics domain. It will be developed as an explicit companion module rather than treated as an incidental subsection of modelling. Its foundations will include angle units, right-triangle relationships, the unit circle, trigonometric functions and planar spatial applications. Spherical and ellipsoidal trigonometry belong with geodesy.

## References and further reading

The explanations, model-building framework and worked examples in this module are original Spatial Methods teaching material. The following sources support unit and quantity conventions and introductory mathematical relationships.

1. **Bureau International des Poids et Mesures (BIPM).** (2026). *The International System of Units (SI Brochure)*, 9th edition, version 4.01. [Official publication](https://www.bipm.org/en/si-brochure-9). Used for quantities, dimensions, derived units, unit symbols and expression of quantity values. Source register: \`SM-SRC-000022\`.
2. **OpenStax.** *Algebra and Trigonometry 2e*. [Chapter 2: Equations and Inequalities](https://openstax.org/books/algebra-and-trigonometry-2e/pages/2-introduction-to-equations-and-inequalities), [Chapter 3: Functions](https://openstax.org/books/algebra-and-trigonometry-2e/pages/3-introduction-to-functions), and [Chapter 4: Linear Functions](https://openstax.org/books/algebra-and-trigonometry-2e/pages/4-introduction-to-linear-functions). Used as a further-learning reference for algebraic relationships and functions. Source register: \`SM-SRC-000021\`.

**Source-use boundary:** These references are linked for human study. Spatial Methods does not reproduce their text, figures or exercises. OpenStax's licence is noncommercial and its stated restrictions on generative-AI ingestion remain applicable.

**Review note:** The module's modelling workflow is an editorial teaching framework, not a published technical standard. Specialist applications require domain-specific theory, evidence and review.
