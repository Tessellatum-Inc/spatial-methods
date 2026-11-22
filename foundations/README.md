# Theoretical foundations

The foundations collection explains the mathematical, statistical, physical and scientific principles that make spatial measurement, computation and reasoning possible.

It is one of the four permanent Spatial Methods pillars:

- **Theoretical Foundations** explain why methods work, what assumptions they require and where they fail.
- **Spatial Algorithms** turn mathematical and scientific ideas into computational procedures.
- **Spatial Data Collection** connects those ideas to observation, measurement, sampling and acquisition in the real world.
- **Spatial Recipes** combine knowledge, data, algorithms and tools to accomplish tasks.

These pillars are connected, not a prescribed learning sequence. A reader may enter through a practical problem, a measurement technology, an algorithm or a theoretical question.

## Follow the theory into practice

The [cross-pillar pathway index](../learning-paths/cross-pillar-pathways.md) connects foundational concepts to collection methods, computational algorithms and practical recipes, with evidence limits stated for each route.

## What belongs here

A foundation should explain the underlying concepts and reasoning, not merely document how to operate a software package. It should establish definitions, mathematical or physical models, assumptions, derivations where useful, examples, limitations and connections to other subjects.

Implementation details belong in the relevant algorithm, method or implementation records. Field procedures belong with collection methods and recipes. A foundation may link to all of them without duplicating their content.

## Subject map

The subject IDs below are stable identifiers from the [Geoinformatics master subject index](../catalog/master-subject-index.md). The status describes this foundations collection, not the maturity of the wider subject.

| Subject ID | Foundation domain | Collection status | Planned coverage |
|---|---|---|---|
| SM-FND-001 | Mathematics for spatial science | Initial collection; review required | Mathematical language, functions, vectors, coordinate geometry, proof and modelling |
| SM-FND-002 | Linear algebra and matrix methods | Initial ten-module sequence published; desk audit completed; independent review and learner testing pending | Vectors, matrices, linear systems, rank, eigenvalues, decompositions, covariance and multivariate structure |
| SM-FND-003 | Calculus and differential methods | Planned | Derivatives, gradients, integrals, multivariable calculus, differential equations and fields |
| SM-FND-004 | Probability and statistical inference | Initial eight-module sequence and applied pathway published; review and learner testing pending | Probability models, distributions, sampling, estimation, testing and Bayesian reasoning |
| SM-FND-005 | Spatial statistics and stochastic processes | Five initial teaching modules published; technical review and learner testing pending | Random fields, covariance, variograms, point processes, spatial sampling, Gaussian inference, anisotropy and spatiotemporal dynamics |
| SM-FND-006 | Geometry and computational geometry theory | Planned | Euclidean, affine and projective geometry; metric spaces; geometric constructions |
| SM-FND-007 | Topology and spatial relations | Planned | Topological spaces, continuity, connectedness, boundaries and spatial relations |
| SM-FND-008 | Geodesy and reference systems | Existing material; expansion required | Earth figure, datums, reference frames, coordinate systems, gravity and transformations |
| SM-FND-009 | Earth science, physical geography and geomorphology | Planned | Earth systems, landforms, processes, terrain and spatial environmental variation |
| SM-FND-010 | Cartographic theory and visual perception | Planned | Scale, visual variables, perception, symbolisation, generalisation and map communication |
| SM-FND-011 | Measurement science, accuracy and uncertainty | Initial collection; expansion and review required | Measurands, measurement models, uncertainty, covariance, traceability and verification |
| SM-FND-012 | Remote sensing physics and radiometry | Initial module published; technical review and learner testing pending | Electromagnetic radiation, spectra, radiometric quantities, interaction and observation models |
| SM-FND-013 | Optics, electromagnetism and wave physics | Planned | Geometric optics, wave behaviour, electromagnetic principles and sensor physics |
| SM-FND-014 | Signal processing and information theory | Planned | Sampling, filtering, transforms, spectral analysis, information and signal detection |
| SM-FND-015 | Computer science, algorithms and complexity | Planned | Computation models, data structures, algorithm analysis, logic and computability |
| SM-FND-016 | Numerical analysis and scientific computing | Initial domain roadmap and eight modules published; technical review and learner testing pending | Floating-point arithmetic, sensitivity, conditioning, stability, approximation and numerical solution |
| SM-FND-017 | Optimisation and operations research | Planned | Linear/nonlinear optimisation, constrained problems, graph optimisation and decision theory |
| SM-FND-018 | Geographic information science and spatial thinking | Planned | Geographic concepts, spatial cognition, representation, scale, ontology and GIScience theory |
| SM-FND-019 | Systems theory, complexity and emergence | Planned | Systems, feedback, networks, dynamical systems, complexity and emergence |
| SM-FND-020 | Physical, environmental and life-science foundations | Planned | Physical, chemical, ecological and biological processes underlying spatial phenomena |

### Mathematics for spatial science

The mathematics domain begins with [Mathematical language, quantities and spatial models](mathematics/mathematical-language-quantities-and-spatial-models.md). Its [domain roadmap](mathematics/README.md) tracks the sequence and status of the modules developed so far, including [functions and relationships](mathematics/functions-and-relationships.md), [coordinate geometry and reference frames](mathematics/coordinate-geometry-and-reference-frames.md) [vectors and vector operations](mathematics/vectors-and-vector-operations.md) and [sequences, series and approximation](mathematics/sequences-series-and-approximation.md), with further coverage planned for modelling and discrete mathematics.

### Linear algebra and matrix methods

[Linear algebra and matrix methods](linear-algebra/README.md) now contains an initial ten-module sequence, selected because matrix operations, linear systems, covariance structures and transformations recur throughout the repository's survey adjustment, CRS, PCA, regression, geostatistics and optimisation work. The sequence runs from [vectors, matrices and linear transformations](linear-algebra/vectors-matrices-and-linear-transformations.md) through [covariance matrices and multivariate structure](linear-algebra/covariance-matrices-and-multivariate-structure.md). Its [sequence audit](linear-algebra/sequence-audit.md) records the desk review and the remaining work. Independent technical review and learner testing are still required.

### Spatial statistics and stochastic processes

[Spatial statistics and stochastic processes](spatial-statistics-and-stochastic-processes/README.md) now has five initial modules: [random fields, covariance functions and variograms](spatial-statistics-and-stochastic-processes/random-fields-covariance-and-variograms.md), [spatial point processes and sampling design](spatial-statistics-and-stochastic-processes/spatial-point-processes-and-sampling-design.md), [anisotropic and nonstationary spatial fields](spatial-statistics-and-stochastic-processes/anisotropic-and-nonstationary-spatial-fields.md), [Gaussian random-field inference and conditional simulation](spatial-statistics-and-stochastic-processes/gaussian-random-field-inference-and-conditional-simulation.md), and [spatiotemporal random fields, advection and dynamic prediction](spatial-statistics-and-stochastic-processes/spatiotemporal-random-fields-advection-and-dynamic-prediction.md). Together they establish spatial and temporal dependence, sampling design, covariance validity, conditional inference, simulation and dynamic prediction. Advanced Bayesian inference, covariance-parameter uncertainty, preferential sampling, scalable dynamic models, independent technical review and learner testing remain open.

### Probability and statistical inference

[Probability and statistical inference](probability-and-statistics/README.md) is now in development. Its first module, [Probability models, events and conditioning](probability-and-statistics/probability-models-events-and-conditioning.md), establishes event rules, conditional probability, independence and Bayes' theorem through an explicitly synthetic spatial-screening example. The domain roadmap distinguishes general probability from spatial stochastic processes and measurement science; independent technical review and learner testing remain outstanding.

### Numerical analysis and scientific computing

[Numerical analysis and scientific computing](numerical-analysis/README.md) has an initial domain roadmap and eight teaching modules: [floating-point numbers, rounding and computational error](numerical-analysis/floating-point-numbers-rounding-and-computational-error.md), [sensitivity and perturbation analysis](numerical-analysis/sensitivity-and-perturbation-analysis.md), [numerical stability and backward error](numerical-analysis/numerical-stability-and-backward-error.md), [convergence, iterative methods and stopping criteria](numerical-analysis/convergence-iterative-methods-and-stopping-criteria.md), [root finding and nonlinear equation solving](numerical-analysis/root-finding-and-nonlinear-equation-solving.md), [numerical differentiation](numerical-analysis/numerical-differentiation.md), [numerical integration and quadrature](numerical-analysis/numerical-integration-and-quadrature.md), and [interpolation and approximation](numerical-analysis/interpolation-and-approximation.md). Together, they introduce finite-precision representation, sensitivity and conditioning, algorithmic stability, iterative convergence, nonlinear root solving, derivative estimation, quadrature, and interpolation and approximation of spatial fields. The modules use spatial computation examples and distinguish computational error from measurement uncertainty. The subject remains incomplete; independent numerical-analysis review and learner testing are pending.

### Remote sensing physics and radiometry

The initial module, [Electromagnetic observations and radiometric quantities](remote-sensing-physics/electromagnetic-observations-and-radiometric-quantities.md), establishes shared electromagnetic vocabulary and radiometric distinctions. The new [Radar scattering and SAR signal formation](remote-sensing-physics/radar-scattering-and-sar-signal-formation.md) module develops wave geometry, range and azimuth formation, complex signal representation, scattering mechanisms, polarisation, speckle, terrain distortion, phase and coherence. Both are initial modules; technical review, numerical verification and learner testing remain pending. Detailed optical radiative transfer and advanced radar signal processing remain open.

### Existing measurement-science resources

The first developed foundation domain is measurement science:

1. [Measurement principles and field verification](measurement-science/measurement-principles-and-field-verification.md)
2. [Measurement models and measurand definition](measurement-science/measurement-models-and-measurand-definition.md)
3. [Standard uncertainty: Type A and Type B evaluation](measurement-science/standard-uncertainty-type-a-type-b.md)
4. [Covariance, correlated observations and generalized least squares](measurement-science/covariance-correlated-observations-and-gls.md)
5. [Hydrographic sounding uncertainty: measurement model and covariance budget](measurement-science/hydrographic-sounding-uncertainty-model.md)

These resources are connected to the [measurement science and survey adjustment learning path](../learning-paths/measurement-science-and-survey-adjustment.md), synthetic [measurement experiments](../experiments/measurement/) and the [covariance/GLS Python implementation](../implementations/python/covariance-gls/README.md).

## Application-grounded development priorities

The [application dependency audit](application-dependency-audit.md) maps existing algorithm, method, implementation and recipe work to the foundations it depends on. It records current starting points, distinguishes existing applied assets from a complete theory collection, and sets a working development order.

Linear algebra and matrix methods (SM-FND-002) now has an initial ten-module sequence and a desk audit. The next domain selected is **SM-FND-004 — Probability and statistical inference**, because it supports existing work in sampling, classification, geostatistics, prediction, model validation and measurement uncertainty. Numerical analysis (SM-FND-016) remains a close parallel priority. This is a practical development order, not a compulsory learning sequence.

## How each foundation will be developed

A topic is not complete because it has a page. Each substantial foundation should be developed against an explicit content standard.

1. **Scope and vocabulary** — define the subject, its boundaries and important terminology.
2. **First principles** — explain the underlying mathematical, physical or scientific ideas.
3. **Models and derivations** — establish equations, assumptions, units and conditions of use.
4. **Interpretation** — explain what the quantities and results mean in spatial contexts.
5. **Worked examples** — use transparent examples, with synthetic inputs labelled as such.
6. **Limitations and failure modes** — identify simplifications, edge cases and common misconceptions.
7. **Connections** — link relevant algorithms, collection technologies, recipes, applications and neighbouring foundations.
8. **Evidence and references** — cite authoritative and primary sources, recording edition, scope and claim-level support where appropriate.
9. **Review and maintenance** — record technical review status, version-sensitive details and unresolved questions.

Not every topic needs the same mathematical depth or the same type of example. The standard is consistent intellectual care, not a rigid page template.

## Recommended internal organisation

As subject coverage grows, organise material into durable domain folders rather than one large flat directory:

- \`mathematics/\`
- \`linear-algebra/\`
- \`calculus-and-differential-methods/\`
- \`probability-and-statistics/\`
- \`spatial-statistics/\`
- \`geometry-and-topology/\`
- \`geodesy-and-reference-systems/\`
- \`earth-science-and-physical-geography/\`
- \`cartography-and-visual-perception/\`
- \`measurement-science/\`
- \`remote-sensing-physics/\`
- \`optics-and-electromagnetism/\`
- \`signal-processing-and-information-theory/\`
- \`computer-science/\`
- \`numerical-analysis/\`
- \`optimisation-and-operations-research/\`
- \`geographic-information-science/\`
- \`systems-and-complexity/\`
- \`environmental-and-life-sciences/\`

Create a folder when substantive canonical material is ready to live there; avoid filling the repository with empty placeholders.

## Development principles

- **Build a connected knowledge base, not twenty isolated textbooks.** Cross-link concepts and explain dependencies.
- **Teach from first principles without assuming every reader is a mathematician.** Introduce prerequisites and build depth progressively.
- **Do not flatten differences between disciplines.** Geodesy, cartography, remote sensing physics, statistics and computer science have distinct intellectual foundations.
- **Separate established theory from modelling choices.** Make assumptions and conventions visible.
- **Keep examples reproducible.** Publish data, code and computational assumptions when they materially support the explanation.
- **Distinguish synthetic demonstrations from real-world evidence.**
- **Use authoritative sources critically.** A citation supports specific claims within its scope; it does not validate an entire page.
- **Avoid duplicate content.** Explain the theory here and link to canonical algorithms, implementations, collection methods and recipes.
