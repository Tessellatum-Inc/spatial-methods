# Binary join-count statistics

Stable ID: \`SA-STAT-BINARY-JOIN-COUNT\` · Draft 0.1 · Source compendium section 2

## Question

For a binary attribute on a spatial graph, are neighbouring units more often
the same class or different classes than expected if the observed labels were
randomly assigned to the same graph?

The classic join-count family separates three undirected edge types:

- **BB** — both endpoints are black (label 1);
- **WW** — both endpoints are white (label 0);
- **BW** — one endpoint is black and the other white.

## Counting joins

Let \(w_{ij}\) be a symmetric binary adjacency matrix with a zero diagonal.
Count each undirected edge once:

\[
BB = \sum_{i<j} w_{ij} x_i x_j,
\qquad
WW = \sum_{i<j} w_{ij}(1-x_i)(1-x_j),
\]

\[
BW = \sum_{i<j} w_{ij}[x_i(1-x_j)+(1-x_i)x_j].
\]

Here \(x_i\in\{0,1\}\). If the graph has \(m\) edges, \(B\) black units and
\(W=n-B\) white units, the fixed-composition randomisation expectations are:

\[
E[BB]=m\frac{B(B-1)}{n(n-1)},\quad
E[WW]=m\frac{W(W-1)}{n(n-1)},
\]

\[
E[BW]=m\frac{2BW}{n(n-1)}.
\]

The expected counts sum to \(m\), as do the observed counts.

## Conditional randomisation

The reference implementation shuffles the binary labels among graph vertices
without replacement, preserving the number of black and white units. It
recalculates all three join counts for each permutation. It reports separate
one-sided plus-one Monte Carlo tail estimates:

- upper tail: unusually many joins of the given type;
- lower tail: unusually few joins of the given type.

High BB or WW counts indicate same-class adjacency relative to the null;
high BW indicates more cross-class mixing. These are not interchangeable
tests, and a small p-value does not establish a causal mechanism.

## Assumptions and limits

- The graph is undirected and represented by a symmetric binary matrix.
- The diagonal is zero and each edge is counted once.
- The null holds the graph and class totals fixed; it does not model
  uncertainty in the graph or spatially varying class probabilities.
- The implementation uses dense matrices and is intended for teaching and
  modest examples. Large spatial graphs should use sparse edge lists.
- Local join-count statistics, multicolour join counts, conditional
  autoregressive models and multiple-testing correction are not included.

## Implementation

The tested Python baseline is in
[implementations/python/join-count](../../implementations/python/join-count/README.md).
See the [source verification note](../../catalog/verification/join-count.md)
for the technical scope, tests and outstanding review dimensions.

## Reference

Cliff, A. D. and Ord, J. K. (1981). *Spatial Processes: Models & Applications*.
Pion.
