# Linear algebra foundation — sequence audit

**Subject identity:** `SM-FND-002` — Linear algebra and matrix methods  
**Audit record:** Initial editorial and mathematical consistency review, 20 November 2026  
**Coverage:** Modules 01–10, the subject README, their worked examples and exercise guidance, and their stated application links.  
**Status:** Desk audit completed; independent subject-matter review and learner testing remain outstanding.

## 1. Purpose and audit boundary

This review checks whether the ten published modules form a coherent introductory sequence and whether the mathematical statements, displayed derivations, numerical examples and worked exercise guidance are internally consistent at the level presented.

It is an editorial desk review, not:
- independent peer review by a qualified linear algebra or numerical-analysis specialist;
- a formal proof audit of every theorem and derivation;
- a learner usability study or assessment validation;
- a comprehensive claim-by-claim review of every cited source;
- software verification, benchmarking or numerical certification;
- validation of any field, geodetic, remote-sensing or other real-world dataset.

No module should be labelled technically certified on the basis of this audit.

## 2. Overall finding

The sequence is coherent as an introductory applied linear algebra pathway. It moves from matrix language and transformations through vector-space structure, systems and identifiability, coordinate representation, metric geometry, estimation, quadratic forms, spectral structure, computational factorizations and multivariate covariance.

The application thread is unusually consistent: local coordinate frames, relative-height networks, least-squares estimation, covariance-aware adjustment and PCA recur across the sequence without being treated as interchangeable problems.

The desk review found no confirmed mathematical error in the principal worked numerical examples sampled across the ten modules. The arithmetic in the matrix products, rotations, basis conversion, projections, least-squares line fit, constrained two-height example, covariance combinations, eigensystem, LU/Cholesky examples, QR line fit and covariance transformations is internally consistent.

That finding is deliberately narrow. It does not substitute for specialist review, independent recalculation of every derivation, or learner testing.

## 3. Sequence and prerequisite audit

| Module | Core role | Audit finding |
|---|---|---|
| 01 — Vectors, matrices and linear transformations | Notation, dimensions, operations, linear and affine maps | Appropriate entry point; spatial examples distinguish a planar matrix operation from a full CRS operation |
| 02 — Linear combinations, span, independence and subspaces | Direction, generation, redundancy and subspace structure | Correctly separates parameter-direction independence from observation redundancy and statistical usefulness |
| 03 — Linear systems, elimination, rank and null spaces | Consistency, solution structure and datum defects | Strong bridge from vector spaces to identifiable parameters; relative-height example is appropriately bounded |
| 04 — Bases, dimension, coordinates and change of basis | Representation versus underlying vector | Correctly distinguishes passive coordinate change from active vector rotation and origin translation |
| 05 — Inner products, norms, orthogonality and projections | Metric geometry and projection | Correct progression to residual geometry; finite segment is distinguished from its infinite supporting line |
| 06 — Least squares and constrained systems | Estimation, weighting, GLS and exact constraints | Important applied synthesis; distinguishes datum convention, exact control and stochastic control |
| 07 — Symmetric matrices, quadratic forms and definiteness | Curvature, covariance validity and positive definiteness | Appropriate prerequisite for covariance and Cholesky |
| 08 — Eigenvalues, eigenvectors and spectral structure | Principal directions, PCA and operator interpretation | Appropriate bridge to multivariate analysis; warns against transferring symmetric results to nonsymmetric operators |
| 09 — Matrix factorizations | LU, QR, Cholesky, SVD and pseudoinverse | Correctly connects matrix structure to computational strategy and rank diagnosis |
| 10 — Covariance matrices and multivariate structure | Covariance propagation, PCA, Mahalanobis distance and spatial covariance | Suitable synthesis and boundary to probability and spatial statistics |

The sequence is a useful route, not a strict dependency chain. Modules 01–05 support multiple entry points; readers approaching PCA can follow Modules 07–10, while readers approaching survey adjustment can enter through Modules 03, 05, 06 and 10 and backfill prerequisites.

## 4. Cross-module consistency checks

The following distinctions are used consistently and should remain explicit in future revisions:

1. **Vector versus coordinate column:** a vector is not the same thing as its representation in a selected basis.
2. **Active transformation versus passive basis change:** rotating an object and changing the coordinate description of the same object are inverse-direction operations in the stated convention.
3. **Linear independence versus observation redundancy:** an additional observation can contribute precision or quality-control evidence without adding a new parameter-space direction.
4. **Algebraic rank versus numerical rank:** exact rank is a mathematical property; numerical rank depends on tolerance, scaling and purpose.
5. **Identifiability versus precision:** more observations do not by themselves guarantee that all parameters are distinguishable or reliably estimated.
6. **Euclidean versus weighted geometry:** ordinary least-squares residual orthogonality is not the same as weighted GLS orthogonality.
7. **Exact datum constraint versus external control:** an inner constraint selects a representative; it does not create external reference information.
8. **Covariance PSD versus invertible covariance SPD:** singular covariance can be valid, although ordinary inverse-based GLS and standard Cholesky require stronger conditions.
9. **Eigenvalue interpretation versus matrix meaning:** a covariance eigenvalue is a variance; eigenvalues of other operators have operator-specific meaning.
10. **Mathematical solution versus physical validity:** factorization, estimation or a small residual does not establish correct CRS, measurement quality, model adequacy or field fitness.

## 5. Worked examples and exercise guidance

The desk check sampled the main numerical examples and worked guidance throughout the sequence. The following calculations were checked for internal consistency:

- Module 01: matrix products, 90-degree rotation, affine point transformation and dimensions.
- Module 02: span, dependence, column-space membership and the distinction between redundant direction and useful observation.
- Module 03: elimination, rank/nullity, consistency and the common-translation datum defect.
- Module 04: non-standard basis coordinates, basis conversion and rotated-frame coordinate signs.
- Module 05: inner products, projection coefficients, orthogonal residuals and segment endpoint handling.
- Module 06: line-fit residuals, inverse-variance weights, GLS/WLS distinction and the two-height KKT constraint example.
- Module 07: two-by-two definiteness, covariance of sums/differences and curvature conditions.
- Module 08: symmetric eigensystem, covariance PCA example and graph-matrix caveats.
- Module 09: pivoted-LU framing, triangular solves, QR least-squares line fit, Cholesky product and rank-deficient SVD example.
- Module 10: correlated difference uncertainty, sum/difference covariance transformation, correlation conversion and illustrative coordinate covariance.

The exercises currently provide worked guidance rather than full formal answer keys in every case. That is acceptable for the initial publication, but the next teaching-quality pass should standardise the expected level of solution: final result, intermediate reasoning, units where relevant, and a short interpretation.

## 6. Editorial corrections made during this audit

Two stale forward references were updated:
- Module 07 now links directly to Module 08 instead of referring generically to “the next module”.
- Module 09 now links directly to the completed Module 10 instead of describing it as future work.

The ten-module index and review status remain aligned: all ten are initial teaching resources, not independently reviewed or learner-tested material.

## 7. Improvements still required

These are improvements, not confirmed mathematical defects.

### Priority 1 — source-to-claim evidence

The modules cite MIT OpenCourseWare, Strang's notes and, in Module 10, the metrology guidance. The source register records source identity and broad topic coverage, but the linear algebra modules do not yet have a detailed claim-evidence map linking individual mathematical claims to exact lecture, section or page locations.

Next action: add claim-level evidence for definitions, theorems, formulae and specialist statements, distinguishing direct support from contextual references. Do not upgrade source status merely because a source is reputable.

### Priority 2 — independent technical review

Commission a review by someone competent in linear algebra and numerical linear algebra. Module 06 and Module 09 deserve particular attention because constraints, covariance weighting, KKT systems, rank-deficient problems and solver choice are easy to oversimplify.

The review should record reviewer scope, date, findings, corrections and unresolved disagreements. It must not be presented as certification of applications outside the reviewer's scope.

### Priority 3 — learner testing and assessment quality

Test with readers at different levels: introductory geospatial students, advanced students/researchers and practitioners returning to the mathematics. Record where notation, prerequisite knowledge, worked examples or spatial interpretation cause difficulty.

Add complete answer keys or instructor guidance as appropriate, without turning every page into an oversized textbook chapter.

### Priority 4 — computational companions

An initial [linear algebra computational companion lab](../../notebooks/linear-algebra-computational-companion-lab.ipynb) is now published. It compares normal equations and QR, performs covariance-aware GLS through Cholesky whitening, inspects SVD rank diagnostics and propagates covariance through a linear transformation using synthetic data. It uses NumPy and includes assertions and explicit interpretation limits.

Remaining work: add a carefully bounded LU comparison; extend the SVD example to a minimum-norm solution; add a more realistic spatial design example; and independently review the mathematics and numerical claims. Notebook execution is necessary but does not establish technical correctness or application fitness.

### Priority 5 — broaden spatial examples

The sequence is strongest in surveying, coordinate geometry, least squares, covariance and PCA. Future editions should add carefully scoped examples from:
- raster and image processing;
- network analysis and graph operators;
- spatial optimisation and allocation;
- remote sensing and multiband data;
- point clouds and three-dimensional geometry;
- spatiotemporal and environmental modelling.

These examples should be selected to illuminate a mathematical idea, not added merely to increase the number of domains named.

## 8. Boundary and gap register

| Topic | Current treatment | Where deeper treatment belongs |
|---|---|---|
| Floating-point error, conditioning and stable algorithms | Introduced as cautions | SM-FND-016 — Numerical analysis and scientific computing |
| Probability distributions and covariance estimation | Matrix structure and interpretation introduced | SM-FND-004 — Probability and statistical inference |
| Spatial covariance functions, variograms and kriging | Finite-matrix connection introduced | SM-FND-005 — Spatial statistics and stochastic processes |
| CRS, reference frames and geodetic transformations | Matrix language and local frames introduced | SM-FND-008 — Geodesy and reference systems |
| Robust estimation and variance components | Referred to in applications | Measurement science and statistical foundations |
| Sparse matrices and large-scale solvers | Not developed | SM-FND-016 — Numerical analysis and scientific computing |
| Constrained optimisation beyond linear equality constraints | Limited KKT introduction | SM-FND-017 — Optimisation and operations research |
| Tensors and higher-order data structures | Not included | Specialist domain selection based on application need |

These are deliberate scope boundaries, not missing prerequisites for the introductory ten-module sequence.

## 9. Recommended next work

Do not open another foundation domain immediately. The highest-value next step is a focused evidence and teaching-quality pass:

1. Build a claim-evidence map for the ten modules.
2. Add full answer keys for the most important cumulative exercises.
3. Create one computational companion comparing LU, QR, Cholesky and SVD on the same small spatial problems.
4. Obtain independent technical review.
5. Conduct learner testing and revise from observed difficulties.

Only after those steps should the collection be described as a reviewed learning resource. Until then, use the accurate status: **initial ten-module foundation published; desk audit completed; independent technical review and learner testing pending.**
