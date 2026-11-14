# Adaptive spatial sampling and active learning

Adaptive sampling chooses the next observations using what is already known, rather than selecting all locations in advance. The source inventory groups several distinct families under this heading; this lesson implements two reusable baselines and marks full Bayesian optimization as future work.

## Greedy uncertainty plus spatial diversity

Given candidate locations \(x_i\) and non-negative uncertainty scores \(u_i\), the selector greedily maximizes

\[
A(i)=\frac{u_i}{\max_j u_j}
+\lambda\frac{d(x_i,S)}{\max_{j\in R}d(x_j,S)},
\]

where \(S\) is the set of already selected locations, \(R\) is the remaining candidate set, and \(d(x_i,S)\) is distance to the nearest selected point. The first point is chosen by uncertainty alone. A minimum-distance exclusion can prevent clustered field visits; if no candidate meets it, the returned batch may be shorter than requested.

This is a heuristic acquisition score. It does not represent a posterior variance unless supplied by a model, and it is not Bayesian optimization or a global optimum. Coordinates must be measured in a meaningful metric space (typically an appropriate projected CRS for local work); Euclidean distance on raw longitude/latitude can distort rankings.

## UCB1 for survey/annotation allocation

For arm \(a\), with \(n_a\) pulls and cumulative reward \(R_a\), UCB1 selects the arm maximizing

\[
\bar R_a+\sqrt{\frac{2\ln t}{n_a}}.
\]

Untried arms are selected first. This is a basic stationary multi-armed bandit policy; it does not account for context, spatially varying rewards, unequal costs, delayed feedback or nonstationarity.

## Code

The [Python package](../implementations/python/adaptive-sampling/README.md) provides the greedy spatial selector, UCB1 and a finite-candidate Gaussian-process optimizer using an RBF kernel with UCB or expected-improvement acquisition. The GP implementation uses dense Cholesky factorization and has cubic training cost; it is intended for small teaching examples, not large spatial datasets.

## What remains outside this implementation

- Gaussian-process Bayesian optimization (posterior fitting and acquisition optimization such as expected improvement or GP-UCB);
- contextual and cost-aware bandits;
- adaptive cluster sampling with network/contagion-dependent inclusion probabilities;
- active learning for map validation with class-stratified sampling and design-based accuracy estimates;
- survey inclusion probabilities, stopping rules and uncertainty propagation.

For map validation, preserve the sampling design and inclusion probabilities. A model-driven sample is not automatically representative, and naïve accuracy estimates can be biased when selection probabilities vary.

## Sources

- Auer, P., Cesa-Bianchi, N., & Fischer, P. (2002). “Finite-time Analysis of the Multiarmed Bandit Problem.” *Machine Learning*, 47, 235–256. DOI: [10.1023/A:1013689704352](https://doi.org/10.1023/A:1013689704352).
- Settles, B. (2009). “Active Learning Literature Survey.” University of Wisconsin–Madison, Computer Sciences Technical Report 1648. [Report](https://minds.wisconsin.edu/handle/1793/60660).

No source text or figures are reproduced.
