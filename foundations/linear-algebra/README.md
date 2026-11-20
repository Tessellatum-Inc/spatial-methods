# Linear algebra and matrix methods

**Subject identity:** `SM-FND-002` — Linear algebra and matrix methods.

Linear algebra studies vector spaces, linear combinations, linear maps, systems of equations and the structure of matrices. Spatial science uses these ideas to transform coordinates, adjust measurement networks, estimate parameters, analyse multivariate observations, represent covariance, solve inverse problems and model networks.

This collection is developed from the demands of existing Spatial Methods resources. It is not a software-specific matrix cookbook. Each module should explain the mathematical structure, its spatial meaning, assumptions and computational implications.

## Scope and boundaries

The domain will cover:

- vectors, vector spaces, subspaces, linear combinations and span;
- matrices, dimensions, matrix operations and linear transformations;
- linear systems, elimination, rank, null spaces and solution structure;
- bases, dimension, coordinate representations and change of basis;
- inner products, norms, orthogonality and projections;
- least squares and constrained linear systems;
- symmetric matrices, quadratic forms and positive definiteness;
- eigenvalues, eigenvectors and spectral interpretation;
- matrix factorizations: LU, QR, Cholesky and singular-value decomposition;
- covariance matrices and their role in estimation and multivariate analysis.

Numerical analysis owns floating-point error, conditioning, stability, convergence and solver selection in depth. Probability and statistical inference own probability models and inferential interpretation. Geodesy owns the physical meaning of reference frames and coordinate operations. This domain supplies the algebraic structures those subjects use.

## Learning modules

| Module | Topic | Spatial connections | Status |
|---|---|---|---|
| 01 | [Vectors, matrices and linear transformations](vectors-matrices-and-linear-transformations.md) | Coordinate operations, design matrices, raster/vector data arrays and linear models | Initial public content |
| 02 | [Linear combinations, span, independence and subspaces](linear-combinations-span-independence-and-subspaces.md) | Network geometry, parameter identifiability and model structure | Initial public content |
| 03 | [Linear systems, elimination, rank and null spaces](linear-systems-elimination-rank-and-null-spaces.md) | Control networks, datum defects and coordinate estimation | Initial public content |
| 04 | [Bases, dimension, coordinates and change of basis](bases-dimension-coordinates-and-change-of-basis.md) | Local/global frames, basis choice and representation | Initial public content |
| 05 | [Inner products, norms, orthogonality and projections](inner-products-norms-orthogonality-and-projections.md) | Residuals, least squares and geometric distance | Initial public content |
| 06 | [Least squares and constrained systems](least-squares-and-constrained-systems.md) | Survey adjustment, regression and exact constraints | Initial public content |
| 07 | [Symmetric matrices, quadratic forms and definiteness](symmetric-matrices-quadratic-forms-and-definiteness.md) | Covariance, energy functions and optimisation | Initial public content |
| 08 | [Eigenvalues, eigenvectors and spectral structure](eigenvalues-eigenvectors-and-spectral-structure.md) | PCA, stability, spatial weights and network structure | Initial public content |
| 09 | Matrix factorizations | Cholesky GLS, QR least squares, SVD and rank diagnosis | Planned |
| 10 | Covariance matrices and multivariate structure | Correlated observations, PCA, kriging and uncertainty models | Planned |

The sequence is a suggested route, not a compulsory learning order. Readers may enter through a concrete application and follow its prerequisites.

## Application anchors already in the repository

- [Constrained and unconstrained covariance GLS](../../implementations/python/covariance-gls/README.md)
- [Measurement science and survey adjustment](../../learning-paths/measurement-science-and-survey-adjustment.md)
- [Coordinate transformation and CRS axis order](../../algorithms/geodesy/crs-transformation.md)
- [Principal component analysis](../../algorithms/statistics/pca.md)
- [Application dependency audit](../application-dependency-audit.md)

These are application anchors, not proof that every mathematical detail has been independently reviewed. The examples and links should be strengthened as the domain develops.

## Development standard

Every module should define its objects and notation, explain the geometric and algebraic interpretation, derive important identities, include worked spatial examples, identify assumptions and failure modes, provide exercises with worked guidance, and link to relevant algorithms, implementations, collection methods and recipes.

Do not conflate a mathematically valid model with a valid spatial interpretation. Units, coordinate reference, measurement design, data quality and physical meaning remain essential.

## Review status

Modules 01–08 are initial teaching resources. They have not received independent technical review or learner testing. The subject collection is incomplete; publication of a module does not constitute technical certification.
