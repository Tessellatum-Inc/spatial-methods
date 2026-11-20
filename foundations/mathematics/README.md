# Mathematics for spatial science

Mathematics is the language used to describe quantities, relationships, change, structure and uncertainty. Spatial science uses it to represent locations, measure distances and areas, describe surfaces and networks, transform coordinates, analyse patterns, model processes and make decisions.

This collection builds the mathematical ideas needed across geoinformatics. It is not intended to be a generic school-mathematics textbook: each topic is connected to spatial questions, data and methods.

**Subject identity:** `SM-FND-001` — Mathematics for spatial science.

## Learning architecture

The sequence below moves from mathematical language toward structures and methods used repeatedly in spatial work. It is a suggested progression; readers may enter through a relevant application and follow its prerequisites.

| Module | Topic | Main spatial connections |
|---|---|---|
| 01 | [Mathematical language, quantities and spatial models](mathematical-language-quantities-and-spatial-models.md) | Variables, units, functions, coordinate pairs, scale, area, density and modelling |
| 02 | [Number systems, arithmetic and numerical representation](number-systems-arithmetic-and-numerical-representation.md) | Measurement values, precision, rounding, significant figures and numerical data |
| 03 | [Ratios, proportions, rates and logarithms](ratios-proportions-rates-and-logarithms.md) | Map scale, resolution, density, rates of change, decibels and spectral transforms |
| 04 | [Equations, inequalities and mathematical reasoning](equations-inequalities-and-mathematical-reasoning.md) | Thresholds, constraints, classification rules and solving spatial problems |
| 05 | [Functions and relationships](functions-and-relationships.md) | Transformations, distance functions, terrain surfaces and spatial models |
| 06 | [Coordinate geometry and reference frames](coordinate-geometry-and-reference-frames.md) | Cartesian coordinates, lines, planes, coordinate transformations and geometric interpretation |
| 07 | [Vectors and vector operations](vectors-and-vector-operations.md) | Displacement, direction, velocity, gradients and 3D geometry |
| 08 | [Sequences, series and approximation](sequences-series-and-approximation.md) | Iterative algorithms, discretisation and convergence |
| 09 | [Mathematical modelling and dimensional analysis](mathematical-modelling-and-dimensional-analysis.md) | Model construction, assumptions, units, scaling, sensitivity and plausibility checks |
| 10 | [Trigonometry for spatial science](trigonometry-for-spatial-science.md) | Angles, radians, trigonometric functions, bearings, azimuths, slopes and planar geometry |
| 11 | [Introductory discrete mathematics and logic](discrete-mathematics-and-logic-for-spatial-science.md) | Sets, relations, functions, propositions, Boolean logic, proofs and introductory graphs |

## Coverage audit

Modules 01–11 have received an initial editorial coverage review. The [application coverage audit](application-coverage-audit.md) tests the sequence against eight representative spatial workflows, identifies where introductory mathematics is sufficient, and routes deeper requirements to specialist foundations. The [mathematics gap register](gap-register.md) tracks individual content gaps and revisions. Neither audit is independent technical certification or evidence of learner competence.

## Which foundation should I study next?

Use this guide when a spatial task crosses beyond introductory mathematics. It is a **routing guide, not a compulsory sequence**: start from the problem you need to solve, follow the relevant mathematical foothold, then study the specialist theory that explains the method. A workflow may require several foundations at once.

The subject IDs are stable identifiers in the [theoretical foundations subject map](../README.md#subject-map). A subject marked *planned* is a destination in the curriculum, not a claim that a complete module is already available. The existing [measurement-science collection](../README.md#existing-measurement-science-resources) and [survey-adjustment learning path](../../learning-paths/measurement-science-and-survey-adjustment.md) are available now.

| Workflow family | Mathematical foothold in this collection | Follow into these foundations | Why the next foundation matters |
|---|---|---|---|
| **1. Surveying, traverses and set-out** | Modules 01–07, 09–10: quantities, coordinates, vectors, planar geometry, azimuths and components | **SM-FND-008** Geodesy and reference systems; **SM-FND-011** Measurement science; **SM-FND-002** Linear algebra; **SM-FND-006** Geometry | Establish the reference frame and Earth model; understand observations, corrections and uncertainty; then study coordinate transformations and network adjustment. A planar traverse calculation is not a geodetic survey solution. |
| **2. Vector GIS, spatial queries and data QA** | Modules 04–07 and 11: equations, functions, coordinate geometry, vectors, sets and logic | **SM-FND-006** Geometry and computational geometry; **SM-FND-007** Topology and spatial relations; **SM-FND-015** Computer science; **SM-FND-018** Geographic information science; **SM-FND-016** Numerical analysis | Learn the exact meaning and computational behaviour of geometric predicates, topology, data structures, spatial representation and finite-precision operations. Boolean logic alone does not define spatial predicate semantics or geometry validity. |
| **3. Raster analysis, resampling and image-derived surfaces** | Modules 01–05, 08–09: quantities, ratios, functions, discretisation, approximation and modelling | **SM-FND-012** Remote sensing physics and radiometry; **SM-FND-014** Signal processing and information theory; **SM-FND-016** Numerical analysis; **SM-FND-004/005** Probability and spatial statistics; **SM-FND-009** Earth science and geomorphology | Understand what the sensor measures, sampling and spatial resolution, interpolation and numerical error, uncertainty and spatial variation, and the physical meaning of the mapped phenomenon. |
| **4. Terrain, slope, hydrology and surface modelling** | Modules 05–07, 09–10: functions, coordinate geometry, vectors, modelling, grade and introductory gradient | **SM-FND-003** Calculus and differential methods; **SM-FND-016** Numerical analysis; **SM-FND-009** Earth science and geomorphology; **SM-FND-008** Geodesy; **SM-FND-011** Measurement science | Calculus defines continuous surface derivatives and fields; numerical analysis explains how DEM algorithms estimate them; geomorphology supplies process interpretation; vertical reference and measurement quality constrain elevation results. |
| **5. Road, transport and network accessibility** | Modules 04–05, 07, 09 and 11: constraints, functions, vectors, modelling, sets and graph vocabulary | **SM-FND-015** Computer science and algorithms; **SM-FND-017** Optimisation and operations research; **SM-FND-018** Geographic information science; **SM-FND-004/005** Probability and spatial statistics; **SM-FND-019** Systems and complexity | Move from graph vocabulary to path-finding and algorithm complexity, constrained routing and allocation, geographic network representation, uncertain travel conditions and dynamic system behaviour. |
| **6. Site suitability and spatial decision support** | Modules 01, 03–05, 09 and 11: units, ratios, functions, inequalities, model design and logical conditions | **SM-FND-017** Optimisation and operations research; **SM-FND-004** Probability and statistical inference; **SM-FND-005** Spatial statistics; **SM-FND-018** Geographic information science; **SM-FND-011** Measurement science; relevant domain science such as **SM-FND-020** | Learn decision objectives and constraints, uncertainty and evidence, spatial dependence, representation and scale, measurement quality, and the substantive science behind each criterion. A weighted overlay is not automatically a defensible decision model. |
| **7. GNSS, remote sensing and field/sensor data collection** | Modules 01–03, 06–10: quantities, numerical representation, coordinates, vectors, models and angles | **SM-FND-008** Geodesy and reference systems; **SM-FND-011** Measurement science; **SM-FND-012** Remote sensing physics; **SM-FND-013** Optics and electromagnetism; **SM-FND-014** Signal processing; **SM-FND-002/016** Linear algebra and numerical analysis | Connect measurements to reference frames and sensor physics; understand calibration, uncertainty and observation models; then study signal formation, processing, transformations and estimation. |
| **8. Temporal monitoring, change detection and simulation** | Modules 03, 05, 08–09: rates, functions, sequences, approximation and model construction | **SM-FND-003** Calculus and differential methods; **SM-FND-004** Probability and statistical inference; **SM-FND-005** Spatial statistics and stochastic processes; **SM-FND-016** Numerical analysis; **SM-FND-019** Systems and complexity; relevant **SM-FND-020** domain science | Distinguish interval rates from continuous change, quantify variability and spatial dependence, model time-evolving systems, assess numerical stability and interpret the physical or social process being monitored. |

### How to use the routes

1. **Define the actual task.** “Map slope” could mean average grade between two points, local gradient from a DEM, or geomorphological interpretation. Those are different problems.
2. **Identify the data and reference.** Check units, coordinate and vertical reference systems, sampling, time period, provenance and known limitations before choosing equations.
3. **Use the mathematics modules as a prerequisite check.** Revisit only the concepts needed for the task; the module numbers are not mandatory gates.
4. **Follow the specialist foundations.** Study the theory that governs the observations, data structures, algorithms or decisions in question.
5. **Move into implementation and recipes.** A foundation explains why a method works; the algorithm explains how it is computed; a recipe combines it with data, tools, checks and outputs.
6. **Return to evidence and validation.** A mathematically coherent result is not proof that the data, assumptions, implementation or real-world interpretation is correct.

## What this domain covers—and what it does not

This domain establishes the common mathematical language. More specialised theory has its own home:

- Matrix algebra, vector spaces, eigenvalues and decompositions belong in [Linear algebra and matrix methods](../README.md#subject-map) under `SM-FND-002`.
- Derivatives, integrals, gradients, differential equations and continuous change belong in `SM-FND-003`.
- Probability and statistical inference belong in `SM-FND-004`; spatial stochastic processes belong in `SM-FND-005`.
- Geometric structures and topology receive deeper treatment under `SM-FND-006` and `SM-FND-007`.
- Floating-point error, conditioning and numerical stability belong in `SM-FND-016`.

A module may introduce a concept needed to understand a later subject, but it should link to the canonical deeper treatment rather than reproduce it.

## Competency goals

A learner completing this domain should be able to:

1. Translate a spatial question into defined quantities, variables and relationships.
2. Distinguish a number from the quantity, unit, reference and measurement process it represents.
3. Use ratios, rates, functions and coordinate relationships correctly.
4. Check equations and results using dimensions, units, limiting cases and physical interpretation.
5. Recognise when a mathematical representation is an approximation and state its assumptions.
6. Identify the mathematical prerequisites of a spatial algorithm or measurement method.

## Development and review standard

Each module should include, where relevant:

- clear definitions and consistent mathematical notation;
- inline mathematics using single dollar delimiters, for example `$x^2+y^2=r^2$`;
- display mathematics using double dollar delimiters on their own lines, for example `$$` on a line before and after the expression;
- units typeset upright with `\mathrm{}` and symbols defined;
- intuitive explanation followed by formal treatment;
- derivations or justification of important relationships;
- worked spatial examples with units;
- common errors and boundary cases;
- exercises that require interpretation, not only calculation;
- connections to algorithms, data collection, recipes and applications;
- relevant references for technical claims, linked to stable records in the source register;
- an explicit evidence/review state and scope limitations.

Do not mistake a long list of formulas for a foundation. The aim is to teach how to select, interpret and question a mathematical model.

## Current status

Modules 01–11 now have initial public content and have received notation, source and initial coverage audits. Independent technical review and targeted expansion remain necessary; publication does not imply technical certification. The gap register guides the next work; coverage will expand only when each module has meaningful explanatory content.
