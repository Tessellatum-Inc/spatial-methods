# Application dependency audit — foundations for Spatial Methods

**Status:** Initial repository-grounded curriculum and asset audit  
**Review date:** 2026-11-20  
**Scope:** Existing algorithm records, method records, implementations, experiments, learning paths and the survey-to-spatial-dataset recipe  
**Purpose:** Identify which theoretical foundations most directly support the work already present in Spatial Methods, where useful material already exists, and what should be developed next.

## 1. Why this audit exists

The foundations collection should grow in response to the intellectual and practical demands of the wider Spatial Methods ecosystem. A subject should not be prioritised merely because it appears in a conventional geoinformatics syllabus, nor should a new foundation duplicate explanations already maintained in algorithms, methods, implementations or recipes.

This audit asks:

1. Which mathematical, statistical, physical and computational ideas recur in the existing work?
2. Which foundations are already represented by substantive canonical resources?
3. Where do existing resources depend on a theory layer that is missing, thin or fragmented?
4. Which subject should be developed next to unlock the greatest amount of existing work?
5. Which topics should remain separate because their disciplinary assumptions differ?

The audit is based on a repository path inventory and targeted inspection of collection indexes, selected method and implementation READMEs, the geodesy learning path, the measurement-science resources and the survey-to-spatial-dataset recipe. It is a prioritisation aid, not a line-by-line technical review of every algorithm or implementation.

## 2. Evidence base and limits

The inspected repository contains substantial bodies of work in:

- geometric and computational geometry algorithms;
- coordinate transformations and geodetic computation;
- raster processing, terrain and hydrology;
- remote sensing and image processing;
- interpolation, geostatistics and spatial statistics;
- graph, routing, mobility and network analysis;
- spatial optimisation and decision methods;
- sampling, measurement, uncertainty and adjustment;
- Python implementations, notebooks, tests and synthetic experiments;
- an end-to-end survey-to-spatial-dataset recipe with a limited synthetic software rehearsal.

Representative inspected assets include:

- [Algorithm collection](../algorithms/README.md), including geometry, raster, remote sensing, networks, interpolation, geostatistics and optimisation.
- [Methods collection](../methods/README.md), including spatial sampling, transformations, spatial weights, covariance models, decision methods and spatial validation.
- [Working implementations](../implementations/README.md), including covariance GLS, PCA, shortest paths, raster resampling, kriging and uncertainty propagation.
- [Geodesy foundations learning path](../learning-paths/geodesy-foundations.md).
- [Measurement-science foundations](README.md#existing-measurement-science-resources), synthetic measurement experiments and the covariance/GLS implementation.
- [Survey-to-spatial-dataset recipe](../recipes/survey-to-spatial-dataset/README.md).

A file's existence does not prove its technical quality, completeness, reproducibility or validation. This audit does not re-run every package, inspect every source claim, certify any method or establish that every listed algorithm is currently usable. It identifies where the repository's own work creates a clear demand for deeper theory.

## 3. Application-to-foundation dependency map

| Existing work family | Representative repository assets | Foundations required | Current position and main gap |
|---|---|---|---|
| **Surveying, positioning and reference** | CRS transformation, ECEF–ENU, ellipsoidal geodesics, Helmert transformation, GNSS ambiguity and RAIM methods, measurement experiments A–O, covariance GLS, survey-to-spatial-dataset recipe | SM-FND-008 Geodesy; SM-FND-011 Measurement science; SM-FND-002 Linear algebra; SM-FND-016 Numerical analysis; SM-FND-015 Computer science | Geodesy and measurement science have useful partial collections. Linear algebra, numerical solution theory, reference-frame realisation, observation models and field-measurement theory need connected treatment. |
| **Vector geometry, topology and spatial queries** | Point-in-polygon, segment intersection, overlay, polygon validity, Voronoi/Delaunay, alpha shapes, mesh methods, exact orientation predicates, spatial joins and indexes | SM-FND-006 Geometry and computational geometry; SM-FND-007 Topology and spatial relations; SM-FND-016 Numerical analysis; SM-FND-015 Computer science | Many algorithms and reference implementations exist. The missing layer is a coherent explanation of geometric objects, invariants, topology, degeneracy, robustness, precision models and computational complexity. |
| **Raster, terrain and hydrology** | Resampling, map algebra, terrain derivatives, flow direction/accumulation, watershed delineation, viewshed, cost distance, interpolation and hydrological routing | SM-FND-003 Calculus; SM-FND-009 Earth science and geomorphology; SM-FND-014 Signal processing; SM-FND-016 Numerical analysis; SM-FND-011 Measurement science | Introductory mathematics and many algorithm records exist. Continuous surfaces, sampling, derivatives, discretisation error, physical process assumptions and uncertainty require specialist foundations. |
| **Remote sensing and photogrammetry** | Spectral indices, atmospheric/empirical corrections, PCA/MNF, endmember extraction, image registration, SAR CFAR, photogrammetric flight design, point-cloud processing | SM-FND-012 Remote sensing physics and radiometry; SM-FND-013 Optics and electromagnetism; SM-FND-014 Signal processing and information theory; SM-FND-002 Linear algebra; SM-FND-004 Probability and statistics | Extensive algorithm and implementation activity exists, but sensor physics, radiometric quantities, sampling/noise, image formation and spectral measurement theory are not yet a coherent foundation collection. |
| **Spatial statistics, interpolation and prediction** | Moran's I and local statistics, point processes, variograms, kriging, Gaussian processes, spatial regression, spatial cross-validation and uncertainty propagation | SM-FND-004 Probability and statistical inference; SM-FND-005 Spatial statistics and stochastic processes; SM-FND-002 Linear algebra; SM-FND-016 Numerical analysis | Several advanced methods and implementations exist. Probability, inference, stochastic processes, spatial dependence, model assumptions and validation theory need a substantive foundation layer. |
| **Networks, mobility and accessibility** | Dijkstra/A*, RAPTOR, isochrones, time-dependent routing, map matching, centrality, network resilience, accessibility and location models | SM-FND-015 Computer science and algorithms; SM-FND-017 Optimisation and operations research; SM-FND-018 GIScience and spatial thinking; SM-FND-004 Probability for uncertain demand and travel | Discrete mathematics provides introductory vocabulary. Graph theory, algorithm complexity, operations research, behavioural assumptions, time dependence and accessibility concepts need deeper treatments. |
| **Spatial decision and optimisation** | p-median, p-center, maximal covering, set covering, facility location, TOPSIS, AHP, ELECTRE, fuzzy/Boolean overlay and weighted criteria | SM-FND-017 Optimisation and operations research; SM-FND-004 Probability and statistics; SM-FND-002 Linear algebra; SM-FND-018 GIScience | Many methods are documented. A connected theory of decision variables, feasible regions, objective functions, constraints, duality, uncertainty, multi-criteria preference and sensitivity is needed. |
| **Environmental, physical and social processes** | Drought indices, coastal processes, hydrology, heat, emissions, land change, cellular automata, agent-based models and spatial interaction | SM-FND-009 Earth science and geomorphology; SM-FND-020 Physical, environmental and life sciences; SM-FND-019 Systems and complexity; SM-FND-003 Calculus; SM-FND-004/005 Probability and spatial statistics | Models and algorithms are present across several domains. Their physical meaning, governing processes, scales, causal assumptions and validation evidence must be taught in the relevant scientific foundations rather than inferred from code. |

## 4. What the audit says about current foundation status

### Substantive starting points

- **SM-FND-001 Mathematics:** Modules 01–11 now form an initial public introductory collection. The application audit and transfer assessment improve its application orientation. Independent technical review and learner testing remain outstanding.
- **SM-FND-008 Geodesy:** A partial learning path and several geodetic algorithms/methods exist. It is not yet a complete geodesy foundation.
- **SM-FND-011 Measurement science:** Four foundation resources, a survey-adjustment learning path, synthetic experiments and a GLS implementation provide a substantial initial base. It remains in progress and is not a complete metrology or professional surveying curriculum.
- **SM-FND-015 Computer science:** The repository contains many implementations, tests and algorithm records, but these do not yet constitute a coherent theoretical foundation.
- **Other domains:** There are useful methods and algorithm records, but no basis in this audit for describing their foundation collections as established.

### Important distinction

An algorithm record explains a method. An implementation demonstrates a computational realisation. A recipe connects methods and tools to a task. A foundation explains the underlying concepts, conditions, assumptions and limitations. One artefact may link to another, but these roles should not be collapsed.

## 5. Development priorities

The next sequence is a practical development order, not a universal prerequisite chain. Readers and projects may enter through any relevant domain.

### Priority 1 — Linear algebra and matrix methods (SM-FND-002)

**Why now:** Matrix and vector operations are already central to network adjustment, coordinate transformations, PCA, least-squares estimation, covariance models, regression, Kalman methods, kriging and many optimisation procedures. Existing mathematics modules introduce vectors but do not teach matrix algebra, linear systems, rank, eigensystems or matrix decompositions at the level these resources require.

**Initial scope:**
- vectors, matrices, dimensions and matrix operations;
- linear systems and geometric interpretation;
- rank, linear independence, null spaces and datum defects;
- orthogonality, projections and least squares;
- symmetric matrices, positive definiteness and quadratic forms;
- eigenvalues, eigenvectors and spectral interpretation;
- QR, Cholesky and singular-value decompositions;
- covariance matrices and their interpretation;
- connections to numerical stability without duplicating the numerical-analysis foundation.

**Anchor applications:** constrained and unconstrained GLS; control-network adjustment; Helmert and coordinate transformations; PCA; kriging; spatial regression.

### Priority 2 — Probability and statistical inference (SM-FND-004)

**Why next:** Spatial Methods contains statistical tests, estimation, sampling, uncertainty, prediction, classification, model comparison and validation. Learners need a coherent account of random variables, probability models, sampling distributions, estimation, intervals, hypothesis tests and Bayesian reasoning before advanced spatial statistics can be interpreted responsibly.

**Initial scope:** probability rules; random variables and distributions; expectation and variance; joint distributions and dependence; sampling; likelihood; estimation; confidence and credible intervals; hypothesis testing; multiple comparisons; Bayesian updating; practical interpretation and limitations.

### Priority 3 — Numerical analysis and scientific computing (SM-FND-016)

**Why early:** Many methods are mathematically correct in exact arithmetic but can fail through floating-point representation, poor conditioning, unstable algorithms, inappropriate tolerances or solver misuse. The repository already contains geometry predicates, iterative methods, matrix solvers, raster algorithms and numerical optimisation that depend on these ideas.

**Initial scope:** floating-point arithmetic; error and conditioning; stability and convergence; root finding; linear-system solution; interpolation and approximation error; numerical differentiation/integration; iterative methods; tolerances and reproducibility.

Develop this alongside linear algebra where the topics naturally meet, while retaining a separate subject identity.

### Numerical analysis and scientific computing

SM-FND-016 now has an initial domain roadmap and a first module on floating-point representation, rounding, cancellation, error measures, conditioning and algorithmic stability. This is a starting point, not completion of the numerical-analysis domain. Further development should cover stable numerical solution, convergence, approximation and tolerance selection, using repository applications as anchors. Independent specialist review and learner testing remain outstanding.

### Priority 4 — Geometry and computational geometry (SM-FND-006), then topology and spatial relations (SM-FND-007)

**Why:** The algorithm catalogue has deep coverage of intersections, predicates, triangulations, overlays, meshes, Voronoi structures and spatial relations. A formal theory layer can connect these algorithms and explain invariants, degeneracy, boundary conventions, precision and topological correctness.

Geometry and topology are related but not interchangeable. Preserve their distinct scopes and connect them explicitly.

### Priority 5 — Calculus and differential methods (SM-FND-003)

**Why:** Terrain derivatives, continuous surfaces, fields, optimisation, physical models and dynamic processes require a stronger account of change, gradients, integrals and differential equations than the introductory mathematics collection provides.

### Parallel domain-specific development

- **SM-FND-008 Geodesy:** continue targeted expansion because coordinate-reference decisions affect nearly every spatial measurement and many existing algorithms.
- **SM-FND-011 Measurement science:** consolidate the existing resources and close gaps in traceability, calibration, uncertainty budgets, covariance, verification and quality decisions.
- **SM-FND-012/013/014:** develop as a connected remote-sensing physics, optics/electromagnetism and signal-processing sequence, preserving separate subject identities.
- **SM-FND-015:** build computer science foundations around data structures, graph algorithms, computational complexity, databases and software correctness.
- **SM-FND-017:** develop optimisation and operations research around models, constraints, duality, graph optimisation, multi-objective decisions and uncertainty.
- **SM-FND-009/019/020:** develop scientific process foundations with discipline-specific evidence and clear model boundaries.
- **SM-FND-018:** develop GIScience and spatial thinking around representation, scale, geographic concepts, ontology, spatial cognition and the meaning of spatial information.

## 6. Recommended next development: SM-FND-002

The immediate next foundation should be **Linear algebra and matrix methods**.

It is the strongest bridge between the completed introductory mathematics collection and several mature areas of existing repository work. It also provides a common mathematical language for measurement adjustment, coordinate transformations, multivariate remote sensing, spatial statistics, covariance modelling and optimisation.

Do not begin by creating a large sequence of disconnected pages. First create a domain-level scope and dependency map. Then develop a small coherent core around linear systems, least squares, matrix structure and decompositions, using examples from existing Spatial Methods assets. Avoid reproducing the full GLS implementation or PCA algorithm: the foundation should explain the mathematics and link to those canonical implementations.

## 7. Development quality gates

A new foundation domain should not be marked mature until it has:

1. A clearly bounded scope and stable subject identity.
2. A dependency map showing what it needs and what uses it.
3. A coherent progression from first principles to specialist concepts.
4. Worked examples drawn from at least two relevant spatial application families where appropriate.
5. Clear definitions, units, notation, assumptions and boundary cases.
6. Links to existing algorithms, methods, implementations, collection technologies and recipes.
7. References with recorded editions, provenance, licensing and review scope.
8. An explicit distinction between original explanation, source-supported claims and illustrative examples.
9. Independent technical review appropriate to the subject.
10. Learner testing or other evidence before claiming demonstrated educational effectiveness.

## 8. Conclusion

Spatial Methods already contains a large amount of applied computational work. The next constraint is not a shortage of algorithm names. It is the need for a connected theory layer that explains why the methods work, how their assumptions differ and how to judge their outputs.

Develop linear algebra next, with numerical analysis close beside it. Then strengthen probability and statistical inference, geometry and topology, and calculus, while expanding geodesy and measurement science where actual application work exposes gaps.

This sequence is a working decision based on the repository's current assets. It should be revised as new recipes, implementations, data-collection methods and real-world applications reveal different dependencies.
