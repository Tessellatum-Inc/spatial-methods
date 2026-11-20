# Application coverage audit — mathematics for spatial science

**Subject:** SM-FND-001  
**Audit date:** 2026-11-20  
**Scope:** Modules 01–11, assessed against representative spatial workflows.  
**Status:** Desk-based curriculum audit; not a field trial, software benchmark, independent mathematical peer review or certification.

## 1. Why this audit exists

A mathematics foundation should be judged by whether it equips a learner to reason about real spatial tasks—not by the number of chapters or formulas.

This audit tests the eleven introductory modules against common work in surveying, GIS, raster analysis, terrain modelling, remote sensing, spatial networks, site screening and temporal analysis. It asks:

1. Can a learner identify the quantities, mathematical objects and assumptions in the task?
2. Does the mathematics foundation teach the relevant introductory concepts?
3. Which deeper methods belong in another specialist foundation?
4. What should be revised in this mathematics domain, rather than duplicated elsewhere?

The audit uses representative workflows and the current module contents. It does not claim that the examples have been executed against real datasets or that a learner has demonstrated competence.

## 2. Coverage matrix

Legend: **Core** = directly taught in Modules 01–11; **Intro** = introduced but not sufficient for a complete professional method; **Specialist** = prerequisite or advanced treatment belongs in another foundation; **Gap** = a targeted explanation or cross-link should be added.

| Spatial workflow | Core modules | Coverage assessment | Specialist knowledge still required |
|---|---|---|---|
| Local traverse, offsets and basic set-out calculations | 01, 02, 03, 04, 06, 07, 09, 10 | **Core / Intro.** Quantities, units, ratios, coordinates, displacement, vector components, angle conventions and planar calculations are represented. | Geodesy and reference systems (008); measurement science and uncertainty (011); linear algebra and adjustment (002); surveying observation procedures and instrument models. |
| Vector GIS selection and quality rules | 04, 05, 06, 11 | **Core / Intro.** Equations, thresholds, functions, coordinate geometry, sets, predicates, quantifiers and Boolean conditions are covered. | Computational geometry (006); topology (007); database theory and SQL dialect semantics (015); geometry validity and software-specific predicate behaviour. |
| Raster grids, area summaries and resampling | 01, 02, 03, 05, 08, 09, 11 | **Core / Intro.** Cell dimensions, scaling, numerical representation, functions, discretisation, set/class logic and model limitations are addressed. | Sampling theory, interpolation, spatial statistics (004/005), numerical analysis (016), image processing and remote-sensing physics (012/014). |
| Terrain, slope and surface interpretation | 05, 06, 07, 09, 10 | **Intro.** Coordinate surfaces, vectors, planar slope and modelling assumptions are introduced. | Differential calculus (003), interpolation and numerical methods (016), geodesy/vertical reference (008), terrain-specific algorithms and data quality. |
| Road and public-transport network accessibility | 04, 05, 07, 09, 11 | **Intro.** Graph vocabulary, conditions, functions, vector direction and modelling boundaries are introduced. | Graph algorithms and complexity (015), optimisation and operations research (017), network data semantics and GIScience (018), time-dependent and multimodal models. |
| Site suitability and constraint screening | 01, 03, 04, 05, 09, 11 | **Core / Intro.** Units, rates, functions, thresholds, Boolean combinations, model scope and limitations are taught. | Multi-criteria decision analysis, optimisation (017), statistical inference (004), uncertainty (011), spatial dependence (005), legal and domain-specific criteria. |
| GNSS, remote sensing and field data collection | 02, 03, 05, 06, 07, 09, 10 | **Intro.** Numerical values, ratios, transformations as mappings, coordinates, vectors, angles and model assumptions are introduced. | Geodesy (008), measurement science (011), sensor physics and radiometry (012/013), signal processing (014), estimation and numerical methods (002/016). |
| Temporal change, monitoring and simulation | 03, 05, 08, 09 | **Intro.** Rates, functions, sequences, approximation and model construction provide the elementary language. | Calculus and differential equations (003), probability/statistics and time series (004/005), numerical analysis (016), systems and complexity (019). |

## 3. Workflow tests

### 3.1 Local traverse and field set-out

**Test question:** Given a local starting coordinate, a horizontal distance and a direction recorded as a clockwise-from-north azimuth, can a learner calculate the east and north components, update the coordinate, and explain the assumptions?

Modules 06, 07 and 10 provide the necessary planar coordinate, vector and angle concepts. Modules 01–03 and 09 support units, scale, quantities and dimensional checks. The learner must still distinguish a mathematical angle from a survey azimuth and must not silently substitute grid, true or magnetic north.

**Result:** introductory planar calculation is supported. A real survey requires reference-system definition, geodetic treatment where applicable, instrument/observation procedures, control, corrections, uncertainty and independent checks. These are not supplied by elementary trigonometry.

**Curriculum decision:** retain the boundary and cross-links to SM-FND-008 and SM-FND-011. Do not turn the mathematics module into a surveying procedures manual.

### 3.2 Vector GIS query and quality control

**Test question:** Can a learner express “inside the project boundary, flagged for inspection, not retired, and either missing a photograph or failing positional QA” as a precise logical condition?

Module 11 introduces sets, predicates, quantifiers, Boolean connectives and parentheses. Module 04 introduces inequalities and constraints. The learner is warned that a mathematical predicate does not define the geometry semantics of spatial predicates such as within, intersects or touches, and that SQL NULL introduces UNKNOWN.

**Result:** the logical structure is supported. Implementing a reliable production query still requires geometry/topology semantics, database-specific three-valued logic, data validation and software documentation.

**Curriculum decision:** keep the conceptual distinction in Module 11. Detailed SQL, spatial predicates and topology belong in computing, GIScience and topology foundations.

### 3.3 Raster analysis and resampling

**Test question:** Can a learner calculate planar cell area, reason about the change in cell count when cell width changes, distinguish stored digital numbers from physical quantities, and explain why resampling to a finer grid does not create new observations?

Modules 01–03, 08 and 09 cover cell dimensions, ratios, units, quantisation, discretisation, scaling and the limits of finer resolution. Module 05 establishes the distinction between raster samples and an inferred continuous surface.

**Result:** elementary numerical and representational reasoning is supported. The mathematics does not yet teach sampling theory, aliasing, interpolation error, spatial autocorrelation, convolution, resampling kernels or radiometric calibration.

**Curriculum decision:** route those topics to signal processing, spatial statistics, numerical analysis and remote-sensing physics. Add a targeted cross-link if the specialist resources are created; do not add an unbounded raster mathematics chapter here.

### 3.4 Terrain and slope

**Test question:** Can a learner interpret slope as rise over horizontal run, distinguish percent grade from an angle, and understand that a terrain surface is a model built from samples?

Modules 05, 06, 07, 09 and 10 cover surfaces as functions, coordinate geometry, vectors, model assumptions and planar trigonometry. The material does not derive a terrain gradient from partial derivatives or quantify interpolation uncertainty.

**Result:** elementary slope interpretation is supported; surface analysis is not complete.

**Curriculum decision:** calculus (003), numerical analysis (016), geodesy (008) and relevant measurement science should provide the deeper treatment. Keep percent grade, vertical angle and coordinate/reference distinctions explicit in the introductory module.

### 3.5 Spatial network accessibility

**Test question:** Can a learner distinguish a geometric crossing from a traversable connection, represent stops and road segments as a graph, and express a basic eligibility condition?

Module 11 introduces vertices, edges, directed graphs, paths and connectivity. Modules 04, 05, 07 and 09 support constraints, costs as functions, displacement and model boundaries.

**Result:** vocabulary and modelling caution are supported. No shortest-path algorithm, turn model, edge-weight design, route choice, network flow, centrality or time-dependent accessibility method is taught in this mathematics domain.

**Curriculum decision:** develop graph algorithms in SM-FND-015 and optimisation in SM-FND-017. The mathematics domain should retain only enough graph language to make those later resources accessible.

### 3.6 Site suitability and constraint screening

**Test question:** Can a learner express minimum area, minimum separation and maximum slope as constraints, combine them with explicit logic, and explain why a pass/fail screen is not a complete suitability decision?

Modules 01, 03, 04, 05, 09 and 11 cover quantities, rates, functions, inequalities, model construction, predicates and Boolean combinations. The modules already caution that thresholds need justification and that screening does not establish legal approval or suitability.

**Result:** basic deterministic screening is supported. Weighted criteria, trade-offs, uncertainty, spatial dependence and optimisation are outside the introductory mathematics sequence.

**Curriculum decision:** retain the basic worked screening pattern; route decision analysis and optimisation to SM-FND-017, probability/statistics to SM-FND-004/005, and measurement uncertainty to SM-FND-011.

### 3.7 GNSS, remote sensing and field observations

**Test question:** Can a learner explain why coordinate tuples need reference metadata, why angle conventions matter, why digital numbers may need scale/offset interpretation, and why recorded values are not automatically true values?

Modules 01, 02, 05, 06, 07, 09 and 10 establish these elementary distinctions. The sequence does not derive GNSS observation equations, sensor radiometry, atmospheric effects, calibration models or full uncertainty budgets.

**Result:** the mathematical language and cautions are present; domain-specific measurement and sensor models are not.

**Curriculum decision:** maintain clear links to geodesy, measurement science, remote-sensing physics, optics and signal processing. Do not duplicate those disciplines in the general mathematics folder.

### 3.8 Temporal change and simulation

**Test question:** Can a learner distinguish a rate over an interval from an instantaneous rate, describe an iterative sequence, and recognise that a simulation time step is a discretisation choice?

Modules 03, 05, 08 and 09 provide introductory rates, functions, sequences, approximation and model construction. They do not teach differential equations, stochastic processes, numerical stability or time-series inference.

**Result:** introductory representation is supported, but quantitative temporal modelling depends on specialist mathematics.

**Curriculum decision:** link to calculus (003), probability/statistics (004/005), numerical analysis (016) and systems theory (019).

## 4. Cross-cutting findings

### Strengths demonstrated by the current sequence

1. **Quantities and units:** learners are repeatedly reminded that numbers need meanings, units, reference systems and context.
2. **Planar geometry and direction:** coordinate geometry, vectors and trigonometry provide a coherent elementary toolkit.
3. **Model discipline:** Module 09 separates the real-world question, data, conceptual model, mathematical model, algorithm, implementation and evaluation.
4. **Discrete reasoning:** Module 11 provides the language for selections, conditions, relations and basic networks.
5. **Limitations:** examples generally state when they are planar, hypothetical, simplified or insufficient for a professional decision.

### Remaining risks

1. **Conceptual transfer is not yet demonstrated.** A worked example in one module does not prove that learners can select the right mathematics in an unfamiliar workflow.
2. **Some specialist prerequisites are only signposted.** The mathematics folder is not a substitute for the still-to-be-developed linear algebra, calculus, statistics, geodesy, numerical analysis and optimisation foundations.
3. **Angle and coordinate conventions are high-risk.** East/north axis order, grid/true/magnetic north, degrees/radians, projected/geographic coordinates and vertical references must be explicit in every applied workflow.
4. **Spatial semantics cannot be reduced to algebra.** A mathematically valid expression can still be applied to invalid geometries, inappropriate coordinate systems or mismatched datasets.
5. **A complete mathematical explanation is not a validated spatial method.** Data quality, algorithm implementation, parameter selection and empirical evaluation remain separate tasks.

## 5. Targeted revision register

The audit does not justify adding another broad mathematics module. It identifies a small number of high-value revisions and cross-links.

| ID | Priority | Revision | Destination | Completion test |
|---|---|---|---|---|
| APP-MATH-01 | P1 | Add a compact end-to-end local traverse example connecting azimuth convention, components, coordinate update, units and a planar limitation. | Module 10, linked to Modules 06–07 | A learner can solve and direction-check a complete two-leg example without mixing angle conventions. |
| APP-MATH-02 | P1 | Add a cross-module worked GIS predicate example showing mathematical logic, explicit parentheses, boundary semantics and a NULL/UNKNOWN caution. | Module 11, linked to Module 04 | A learner can translate a verbal rule into logic and identify what must be defined by the spatial database. |
| APP-MATH-03 | P1 | Add a compact raster resolution comparison linking cell width, cell area, approximate cell count, scale/offset and the non-creation of information by resampling. | Modules 02, 03 and 08 (cross-links; avoid duplication) | A learner can distinguish grid size, stored value, physical quantity and information content. |
| APP-MATH-04 | P2 | Add a short concept map for slope, percent grade, vertical angle and terrain gradient, explicitly separating elementary trigonometry from calculus. | Modules 07 and 10, linked to SM-FND-003 | A learner can state which quantity is being calculated and when derivatives are required. |
| APP-MATH-05 | P2 | Add a concise “which foundation next?” routing table for eight workflow families. | Mathematics README | Each workflow points to the appropriate specialist foundations without duplicating their content. |
| APP-MATH-06 | P2 | Review module exercises for transfer: include at least one unfamiliar scenario requiring learners to choose concepts from multiple modules. | Modules 01–11 | Exercises assess interpretation, assumption selection and method choice, not just formula substitution. |

### Implementation status — 2026-11-20

- **APP-MATH-01 implemented:** Module 10 now includes a complete two-leg local planar traverse from azimuths and distances through coordinate updates, direction checks, path length versus displacement, and explicit limitations. Independent technical review and learner testing remain outstanding.
- **APP-MATH-02 implemented:** Module 11 now evaluates a spatial QA predicate across TRUE, FALSE and UNKNOWN cases, explains why UNKNOWN is not selected by a typical SQL WHERE clause, and distinguishes attribute logic from geometry predicate semantics. Database-specific implementation and learner testing remain outstanding.
- **APP-MATH-03 implemented:** Module 08 now combines a fixed-extent 20 m / 10 m / 5 m grid comparison, cell areas and counts, a scale/offset conversion, and an explicit explanation of why upsampling does not create independent observations or new sensor detail. Modules 02 and 03 cross-link to the worked example. Technical review and learner testing remain outstanding.
- **APP-MATH-04 to APP-MATH-06 remain open.**

## 6. What this audit does not justify

The audit does **not** justify:
- adding a general-purpose “advanced mathematics” module;
- moving matrix algebra, calculus, probability, geodesy, numerical analysis or optimisation into SM-FND-001;
- claiming the 11 modules are complete, peer reviewed or professionally sufficient;
- treating a correct calculation as evidence that source data, coordinate reference, sensor, model or implementation is valid;
- treating a desk-based coverage review as learner assessment or field validation.

## 7. Recommended execution order

1. Implement APP-MATH-01 and APP-MATH-02 first: angle conventions and spatial query logic are high-consequence sources of avoidable error.
2. Implement APP-MATH-03 next: raster resolution and value semantics connect several modules and recur across remote sensing and GIS.
3. Add APP-MATH-04 and APP-MATH-05 as concise cross-links, not new chapters.
4. Design a small transfer assessment from APP-MATH-06 after the three worked examples are in place.
5. Then use real recipes and implementation work to test whether any additional mathematics is genuinely missing.

## 8. Audit conclusion

The eleven modules form a credible **introductory mathematical language layer** for common spatial workflows. They support first-pass reasoning about quantities, units, scale, coordinates, planar geometry, vectors, angles, models, raster discretisation, sets and logical conditions.

They do not form a complete mathematical education for professional geospatial practice. Their purpose is to make the prerequisites visible, teach a useful common core and route deeper methods to the correct specialist foundations.

The next step should be targeted applied revision and learner-transfer testing—not adding more generic chapters.
