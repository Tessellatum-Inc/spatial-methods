# Source verification — discrete centroidal Voronoi / Lloyd iteration

## Identity and bibliography
- Du, Faber & Gunzburger (1999), *SIAM Review* 41(4), 637–676, DOI 10.1137/S0036144599352836.
- Du, Emelianenko & Ju (2006), *SIAM Journal on Numerical Analysis* 44(1), 102–119, DOI 10.1137/040617364.

The first paper defines CVTs through generators that are centroids of their Voronoi regions and surveys algorithms and applications. The second analyzes convergence properties of Lloyd iteration; it does not imply that every initialization reaches a global optimum.

## Technical and implementation scope
The implementation is weighted Lloyd iteration over finite sample points with Euclidean distance. It is a discrete approximation, not an exact continuous-domain CVT implementation.

Not implemented: exact polygon clipping/integration, power diagrams, capacity constraints, semi-discrete optimal transport, constrained surface CVT, geodesic distance, or global optimization.

## Reproduction
Tests are authored for centroid updates, weighted centroids, deterministic behavior, empty clusters and invalid inputs. Repository CI/test status must be checked separately.

## Rights
Bibliographic metadata and original explanatory text only; no article figures, source text or datasets are reproduced.
