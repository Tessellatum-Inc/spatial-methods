# Cross-module transfer assessment: selecting a temporary field hub

**Foundation domain:** Mathematics for spatial science  
**Subject ID:** `SM-FND-001`  
**Assessment type:** Integrated, open-response case study  
**Status:** Initial public learning resource; independent technical review and learner testing required  
**Prerequisites:** Modules 01–11. The assessment is designed to test selection and transfer, not mastery of every specialist subject.

## Purpose

This assessment asks you to solve an unfamiliar spatial planning problem by selecting and combining mathematical ideas from across the mathematics collection. It is not a formula-recall quiz. You must decide what to calculate, define the assumptions, check units, explain the meaning of your results and identify what the mathematics cannot establish.

The case is fictional. All locations, elevations, counts and criteria are invented for this exercise. Coordinates are in a local Cartesian grid in metres; they are not real-world coordinates and have no geographic reference system.

## Scenario

A field team needs a temporary hub from which to inspect three settlement clusters. Three candidate hub sites and three settlement centroids have been represented in a simplified local plane.

The planning team wants a first-pass candidate that:

- has verified access;
- is not flagged as flood-exposed in the supplied screening data;
- is no more than 375 m in straight-line plan distance from each settlement centroid.

For the first-pass comparison, use the arithmetic mean of the three straight-line distances as a descriptive measure of proximity. The maximum distance is the stated eligibility threshold. Do not replace these criteria with an invented weighted score.

### Candidate hub data

| Candidate | Easting x (m) | Northing y (m) | Elevation z (m) | Access verified? | Flood-exposure flag? |
|---|---:|---:|---:|---|---|
| A | 0 | 0 | 112 | Yes | No |
| B | 600 | 0 | 109 | Yes | Yes |
| C | 300 | 400 | 116 | Yes | No |

### Settlement centroid data

| Settlement | Easting x (m) | Northing y (m) |
|---|---:|---:|
| S1 | 100 | 100 |
| S2 | 500 | 100 |
| S3 | 300 | 350 |

### Additional terrain and raster information

For a separate access-gradient check, a mapped access-road point R has coordinates (500 m, 500 m) and elevation 108 m. Consider the line from candidate C to R. Assume the supplied elevations are compatible for this simplified local calculation; no vertical datum or measurement uncertainty information is provided.

A 1000 m by 1000 m square study area is also represented by a raster. Compare square grid cell widths of 20 m and 10 m. Assume the grid exactly covers the area without partial edge cells.

## Tasks

Show your reasoning. Keep unrounded values during calculations and report final distances to 0.1 m unless a task specifies otherwise.

### Task 1 — Define the model before calculating

1. State the decision question, the spatial domain, the unit of analysis and the intended use of the result.
2. Identify the inputs, decision variables or candidate alternatives, constraints and output.
3. List at least four assumptions or exclusions. Include the distinction between straight-line distance and actual travel distance.
4. Explain why this is a screening model rather than proof that a hub is safe, operationally suitable or officially approved.

*Concepts tested: Modules 01 and 09.*

### Task 2 — Check quantities, units and scale

1. Convert the study-area dimensions into kilometres and calculate its area in square kilometres.
2. Calculate the number of cells and the area of one cell for each raster resolution.
3. State the ratio of the two cell counts.
4. Explain why changing the output grid from 20 m to 10 m does not, by itself, create new observations or prove that the underlying information is twice as detailed.
5. Identify which quantities in the scenario are lengths, areas, coordinates, elevations, Boolean flags and counts.

*Concepts tested: Modules 02, 03, 08 and 09.*

### Task 3 — Build and evaluate the distance function

For candidate point $H_j=(x_j,y_j)$ and settlement centroid $S_k=(x_k,y_k)$, define a function for planar Euclidean distance.

1. Write the distance function with its variables and units.
2. Calculate all nine candidate-to-settlement distances.
3. For each candidate, calculate the arithmetic mean distance and the maximum distance.
4. Explain why the mean alone is insufficient for the stated eligibility rule.

*Concepts tested: Modules 05, 06 and 09.*

### Task 4 — Translate the decision rule into logic

Let:

- A_j mean that candidate j has verified access;
- D_j mean that candidate j is not flagged as flood-exposed;
- M_j mean that its maximum settlement distance is no greater than 375 m.

1. Express the eligibility rule as a logical proposition.
2. Evaluate each candidate against the three conditions.
3. Identify the eligible candidate or candidates.
4. Explain how your answer would change if the flood-exposure flag were missing rather than explicitly false. Do not silently treat missing information as evidence of safety.
5. Explain why the Boolean rule does not establish the geometric meaning of the supplied access or flood-screening attributes.

*Concepts tested: Modules 04 and 11.*

### Task 5 — Use vectors and trigonometry to check the access line

For the line from candidate C to access-road point R:

1. Calculate the east and north displacement components.
2. Calculate the horizontal plan distance.
3. Calculate the azimuth clockwise from north, stating your convention.
4. Calculate the vertical difference, signed grade and percentage grade.
5. Calculate the elevation angle relative to the horizontal.
6. Explain why the grade is based on horizontal distance rather than the 3D slope distance.
7. State what additional information would be needed before treating this as an engineering or surveyed access assessment.

*Concepts tested: Modules 06, 07, 09 and 10.*

### Task 6 — Approximation and numerical judgement

1. Explain why reporting a distance as 360.6 m does not mean the underlying location is known to the nearest 0.1 m.
2. Distinguish numerical rounding from measurement uncertainty.
3. Identify at least three sources of uncertainty or model error that the supplied data do not quantify.
4. Explain why a raster with smaller cells may still contain less reliable elevation information than a coarser but better-supported dataset.

*Concepts tested: Modules 02, 08 and 09; connects to measurement science (SM-FND-011) and numerical analysis (SM-FND-016).*

### Task 7 — Challenge the decision

Write a short recommendation to the planning team. It must:

- state the result of the mathematical screening;
- distinguish what the result supports from what it does not support;
- identify at least five checks needed before selecting or using a real hub;
- identify the specialist foundations or methods that should be consulted next.

Do not invent a road network, travel times, flood probabilities, population weights, safety guarantees or field verification results.

*Concepts tested: Modules 01–11 as an integrated set.*

## Worked guidance and answer key

The worked guidance is provided so that the assessment can be used for self-study. In a taught setting, instructors may withhold this section until learners submit their own reasoning.

### Task 1 — Model definition

A defensible decision question is: which of the three supplied candidate points satisfies the stated access, flood-screening and maximum straight-line-distance criteria, and how do the candidates compare on mean straight-line distance?

The domain is the supplied 1000 m by 1000 m local plane. The unit of analysis is one candidate hub, evaluated against the three settlement centroids. Inputs are candidate and settlement coordinates, candidate elevations, access flags, flood-screening flags and the stated distance threshold. The alternatives are A, B and C. The outputs are the nine distances, candidate mean and maximum distances, condition checks and eligibility result.

Possible assumptions and exclusions include:

- The coordinates share one consistent local Cartesian reference and use metres.
- Straight-line Euclidean distance is the intended proximity measure; no road or pedestrian network is supplied.
- Each settlement centroid represents its settlement for this screening exercise.
- The Boolean flags are accepted as supplied, but their evidence and definitions have not been independently checked.
- The threshold is a planning rule supplied by the scenario, not a universal safety or service standard.
- Elevations are treated as compatible for the simple line-gradient calculation, although their vertical datum and uncertainty are unknown.
- No capacity, land ownership, access rights, utilities, safety, operating costs or community preferences are modelled.

This is a screening calculation using simplified inputs. It cannot establish field conditions, legal status, safety, flood probability, operational feasibility or approval.

### Task 2 — Units and raster grid

The study-area width and height are each 1000 m = 1 km. Its area is:

$$
A=1000\ \mathrm{m}\times1000\ \mathrm{m}
=1{,}000{,}000\ \mathrm{m}^2
=1\ \mathrm{km}^2
$$

For 20 m cells:

$$
n_x=n_y=\frac{1000}{20}=50
$$

$$
N=50\times50=2500\ \mathrm{cells}
$$

Each cell covers $20\times20=400\ \mathrm{m}^2$.

For 10 m cells:

$$
n_x=n_y=\frac{1000}{10}=100
$$

$$
N=100\times100=10{,}000\ \mathrm{cells}
$$

Each cell covers $10\times10=100\ \mathrm{m}^2$.

The finer grid has four times as many cells. Its cell width is half as large and its cell area is one quarter as large. Resampling or changing grid spacing does not automatically add independent observations, recover detail absent from the source, or improve positional accuracy.

### Task 3 — Distance calculations

The distance from candidate $H_j$ to settlement $S_k$ is:

$$
d_{jk}=\sqrt{(x_j-x_k)^2+(y_j-y_k)^2}
$$

Coordinate differences are in metres, so the result is in metres.

| Candidate | To S1 (m) | To S2 (m) | To S3 (m) | Mean (m) | Maximum (m) |
|---|---:|---:|---:|---:|---:|
| A | 141.4 | 509.9 | 461.0 | 370.8 | 509.9 |
| B | 509.9 | 141.4 | 461.0 | 370.8 | 509.9 |
| C | 360.6 | 360.6 | 50.0 | 257.0 | 360.6 |

For example, candidate C to S1 is:

$$
d_{C1}=\sqrt{(300-100)^2+(400-100)^2}
=\sqrt{130000}
\approx360.6\ \mathrm{m}
$$

Candidate C's mean is:

$$
\bar d_C=\frac{360.555+360.555+50}{3}
\approx257.0\ \mathrm{m}
$$

The mean describes average proximity but can conceal a settlement that is much farther away. The maximum is needed because the eligibility condition applies to every settlement.

### Task 4 — Logical eligibility

The eligibility proposition is:

$$
E_j=A_j\land D_j\land M_j
$$

where:

$$
M_j=(\max_k d_{jk}\leq375\ \mathrm{m})
$$

The candidate checks are:

| Candidate | Access verified A_j | Not flood-flagged D_j | Maximum distance ≤ 375 m | Eligible E_j |
|---|---|---|---|---|
| A | TRUE | TRUE | FALSE | FALSE |
| B | TRUE | FALSE | FALSE | FALSE |
| C | TRUE | TRUE | TRUE | TRUE |

Candidate C is the only candidate that satisfies all three supplied conditions.

If a flood flag were missing, the corresponding condition would be unknown, not automatically true. A conservative decision process should mark the candidate as requiring verification or ineligible pending evidence, according to a rule declared before evaluation. Missing data are not equivalent to a confirmed absence of flood exposure.

The logical expression only combines supplied attributes. It does not define how access was verified, what flood exposure means, how the geometry was constructed or whether the data are current.

### Task 5 — Vector, azimuth and grade

From C (300, 400, 116) to R (500, 500, 108):

$$
\Delta E=500-300=200\ \mathrm{m}
$$

$$
\Delta N=500-400=100\ \mathrm{m}
$$

The horizontal distance is:

$$
d_h=\sqrt{200^2+100^2}
=\sqrt{50000}
\approx223.6\ \mathrm{m}
$$

With azimuth measured clockwise from north:

$$
\alpha=\operatorname{atan2}(\Delta E,\Delta N)
=\operatorname{atan2}(200,100)
\approx63.4^\circ
$$

The line points northeast, which agrees with the positive east and north components.

The vertical difference is:

$$
\Delta z=108-116=-8\ \mathrm{m}
$$

The signed grade from C toward R is:

$$
g=\frac{-8}{223.6068}\approx-0.0358
$$

Therefore the signed percentage grade is approximately −3.58%. The negative sign indicates descent in the direction from C to R.

The elevation angle is:

$$
\theta=\tan^{-1}(-0.0358)\approx-2.05^\circ
$$

Grade uses horizontal plan distance. Slope distance is the 3D line length and is not the horizontal run used in the rise-over-run definition. An engineering or surveyed assessment would need, among other things, a verified horizontal and vertical reference, field observations, measurement uncertainty, alignment and surface profile, drainage and ground conditions, design criteria, rights of access and competent professional review.

### Task 6 — Approximation and uncertainty

A value displayed to 0.1 m is a rounded numerical result. The display precision does not establish that either coordinate or distance is known within 0.1 m. Measurement uncertainty concerns the quality of the inputs and measurement model, not merely the number of decimal places printed.

Unquantified sources include coordinate measurement error, centroid generalisation, reference-system distortion, source-data age, elevation error, terrain variability, and uncertainty in the supplied access or flood-screening attributes.

A finer raster grid can simply subdivide or interpolate existing information. Effective spatial resolution and reliability depend on the source sensor or survey, sampling, georeferencing, processing, noise, interpolation and validation—not cell size alone.

### Task 7 — Example recommendation

Under the supplied screening rules, candidate C is the only eligible candidate. Its maximum straight-line distance to the three settlement centroids is approximately 360.6 m, below the stated 375 m threshold. Its mean straight-line distance is approximately 257.0 m. Candidates A and B exceed the maximum-distance threshold; B also carries the supplied flood-exposure flag.

This result supports only a first-pass comparison of the fictional candidate points under the stated assumptions. It does not demonstrate safe access, flood safety, legal availability, actual travel time, suitability for operations or the quality of the source data.

Before any real selection, verify the coordinate and vertical reference systems; inspect and independently validate the locations; confirm access rights and physical access; obtain appropriate flood and drainage evidence; assess route-network travel and barriers; check land use, utilities, capacity and safety; consult affected communities and relevant authorities; and obtain competent professional review.

Relevant next foundations include geodesy (SM-FND-008), measurement science (SM-FND-011), geometry and topology (SM-FND-006/007), geographic information science (SM-FND-018), probability and spatial statistics (SM-FND-004/005), numerical analysis (SM-FND-016), and the relevant environmental or physical science.

## Assessment rubric

Use the rubric to assess the quality of reasoning, not only whether the final candidate is correct.

| Criterion | Strong evidence | Partial evidence | Weak evidence |
|---|---|---|---|
| Model definition | Clearly states purpose, domain, unit of analysis, inputs, criteria, assumptions and exclusions | Identifies most elements but leaves assumptions or scope unclear | Starts calculating without defining the problem |
| Units and numerical reasoning | Converts units consistently, checks dimensions and distinguishes precision from information | Mostly correct but has minor omissions or weak interpretation | Mixes units, cell size, area or numerical precision |
| Geometry and vectors | Uses the correct distance function, component signs, quadrant and angle convention | Correct method with limited explanation or a minor arithmetic error | Uses an unsuitable formula or confuses direction conventions |
| Logic and decision | Translates all conditions correctly and treats missing information explicitly | Correct outcome but incomplete logical explanation | Ignores a condition or treats unknown as false/true without justification |
| Model critique | Identifies meaningful limitations and further evidence required | Lists generic caveats without linking them to the case | Treats the computed answer as proof of real-world suitability |
| Communication | Reports units, rounding, assumptions and a clear qualified recommendation | Understandable but missing some units or qualifications | Results cannot be interpreted or reproduced |

## Module map

| Assessment element | Main modules |
|---|---|
| Model, quantities and assumptions | 01, 09 |
| Number representation, units, ratios and rates | 02, 03 |
| Constraints and inequalities | 04 |
| Distance as a function | 05 |
| Coordinates and Euclidean geometry | 06 |
| Displacements and vectors | 07 |
| Raster discretisation and approximation | 08 |
| Modelling and dimensional consistency | 09 |
| Azimuth, trigonometry and grade | 10 |
| Sets, predicates and Boolean decisions | 11 |

## Limitations and review status

This is an original synthetic teaching assessment. It is not a field study, engineering design, flood assessment, route analysis, cadastral determination or professional site-selection recommendation. The worked answers demonstrate one defensible solution under the stated assumptions; they do not imply that the assumptions are appropriate for a real project.

The assessment has not yet been independently technically reviewed or tested with learners. A correct worked answer is not evidence that the assessment reliably measures learner competence. Instructors should review the mathematics, adapt the context to the learning objectives and assess reasoning as well as numerical output.
