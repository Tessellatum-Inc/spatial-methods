# Mantel and partial Mantel tests

Stable IDs: SA-STAT-MANTEL, SA-STAT-PARTIAL-MANTEL · Draft 0.1 · Source compendium section 2, page 2

## The question

A Mantel test asks whether two distance or dissimilarity matrices, computed for the same observations, are associated. A partial Mantel test asks whether two such matrices remain linearly associated after controlling for a third distance matrix.

## Simple Mantel statistic

Let D^X and D^Y be symmetric n by n distance matrices. Extract their unique upper-triangle entries into vectors x and y, each of length n(n-1)/2. The statistic is their Pearson correlation:

r_M = cor(x, y)

The test permutes observation labels, applying the same permutation to rows and columns of one matrix, then recomputes the statistic. It does not shuffle individual matrix cells: that would destroy the distance structure and shared-observation dependence.

For B random permutations, a common Monte Carlo estimate is p = (1 + number of at-least-as-extreme permuted statistics)/(B + 1). The plus-one correction prevents a Monte Carlo p-value of zero. State one-sided alternatives before inspecting results.

## Partial Mantel statistic

Let z be the upper triangle of a third distance matrix. Regress x and y separately on z, including intercepts, and correlate the residual vectors. This is the partial Pearson correlation of the distance entries. The conventional permutation procedure relabels one tested matrix and recomputes the partial statistic.

## Assumptions and interpretation

- Matrix rows and columns must refer to the same observations in the same order.
- Matrices must represent meaningful distances/dissimilarities; symmetry and a zero diagonal are expected here.
- The ordinary permutation reference relies on exchangeability of observation labels under the null.
- Distance entries are not independent: pairs share observations. Do not treat the upper triangle as an ordinary independent sample for a textbook correlation p-value.
- Association between distances does not establish causation or a spatial mechanism.

## The spatial-autocorrelation warning

Partial Mantel is often presented as a way to control geographic distance. Guillot and Rousset (2013) showed that simple and partial Mantel tests can have inflated Type I error when both tested variables are spatially autocorrelated; adding geographic distance as a third matrix does not generally remove the problem. Spatially constrained randomisation methods have been proposed, but validity depends on the null model and represented spatial structure.

A 2024 benchmark further distinguishes hypotheses genuinely formulated in terms of distances from hypotheses about raw variables converted into distances. Conversion can discard information and change the hypothesis. Choose a method based on the scientific question, not convenience. If the question concerns raw response and predictors, begin with a model for those variables (for example, regression, spatial regression or constrained ordination). If the hypothesis is inherently about pairwise dissimilarities, a Mantel-family statistic may be relevant, but justify exchangeability and permutation design. Do not use partial Mantel as a generic spatial-autocorrelation fix.

## Implementation scope

The companion package implements simple Mantel and partial Mantel statistics, one control matrix, two-sided/greater/less alternatives, seeded label permutations and plus-one Monte Carlo p-values. It does not implement spatially constrained permutations, multiple control matrices, exact enumeration, confidence intervals, or calibrated inference under spatial autocorrelation. Complexity is O(B n^2) time and O(n^2) input storage.

## References

- Mantel, N. (1967). The detection of disease clustering and a generalized regression approach. Cancer Research, 27(2), 209–220.
- Smouse, P. E., Long, J. C., & Sokal, R. R. (1986). Multiple regression and correlation extensions of the Mantel test of matrix correspondence. Systematic Zoology, 35(4), 627–632.
- Guillot, G., & Rousset, F. (2013). Dismantling the Mantel tests. Methods in Ecology and Evolution, 4, 336–344. https://doi.org/10.1111/2041-210X.12018
- Legendre, P., & Fortin, M.-J. (2010). Comparison of the Mantel test and alternative approaches for detecting complex multivariate relationships in the spatial analysis of genetic data. Molecular Ecology Resources, 10, 831–844.
- Debastiani, V. J., & da Silva Duarte, L. (2024). Benchmarking the Mantel test and derived methods for testing association between distance matrices. https://pmc.ncbi.nlm.nih.gov/articles/PMC11696488/
