# Fixed and adaptive kernel density estimation for point patterns

A planar Gaussian KDE estimates intensity at location x as

\[
\hat\lambda_h(x)=\sum_i w_i\frac{1}{2\pi h^2}
\exp\left(-\frac{\|x-x_i\|^2}{2h^2}\right).
\]

A global bandwidth h controls the bias-variance trade-off. For an isotropic
bivariate normal-reference rule, the package uses

\[ h_{S}=s\,n_{eff}^{-1/6}, \]

where s is the pooled root-mean-square sample standard deviation of the two
coordinate axes and n_eff is the Kish effective sample size (equal to n for
equal weights). This is a transparent starting value; it assumes a roughly
Gaussian reference distribution and is not an optimality guarantee. Small h preserves
local structure but can create noisy peaks; large h smooths local variation.
Leave-one-out (LOO) likelihood predicts each event from all other events and
selects the candidate bandwidth with the largest mean log predictive density.

Abramson-style adaptive KDE uses a pilot density f_i at each event and sets

\[
h_i=h\left(\frac{g}{f_i}\right)^\alpha,
\]

where g is the geometric mean of pilot densities and alpha is commonly 1/2.
Dense pilot regions receive smaller kernels; sparse regions receive larger
kernels. The sample-point estimator sums kernels using their event-specific
bandwidths. The implementation excludes each event from its own pilot estimate
and clips local bandwidth factors to a configurable positive interval.

The companion [implementation](../../implementations/python/point-pattern-kde/README.md)
provides fixed KDE, adaptive sample-point KDE and weighted LOO candidate
selection. It uses direct planar evaluation and applies no edge correction,
so kernels extending beyond the observation window can bias estimates down.
Adaptive evaluation costs O(n^2 + nm), and LOO selection O(n^2 c) for c
candidate bandwidths. These are transparent reference methods, not indexed
large-data estimators.

Tests compare adaptive surfaces and LOO scores with independent direct
calculations, including alpha=0 equivalence, event weights, one-event input,
chunking and invalid parameters.


## Bandwidth selection in practice

Use the normal-reference value to establish a reproducible scale, then inspect
a small candidate grid around it or use leave-one-out likelihood selection.
LOO scores predict each positive-weight event from the remaining events and
maximise the weighted mean log predictive density. Candidate selection is
conditional on the supplied grid and does not correct boundary bias.

The package also implements Abramson-style sample-point adaptation. Its
leave-one-out pilot estimates local intensity at each event and shrinks or
expands event-specific bandwidths relative to their geometric mean. Factor
clipping prevents extreme local bandwidths. Adaptive smoothing is a model
choice, not an automatic improvement.

The [test suite](../../implementations/python/point-pattern-kde/test_point_pattern_kde.py)
checks the normal-reference formula against an independent calculation,
translation/scale equivariance, weighted effective sample size, adaptive
surface calculations and LOO scores.
