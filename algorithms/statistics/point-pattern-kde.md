# Fixed and adaptive kernel density estimation for point patterns

A planar Gaussian KDE estimates intensity at location x as

\[
\hat\lambda_h(x)=\sum_i w_i\frac{1}{2\pi h^2}
\exp\left(-\frac{\|x-x_i\|^2}{2h^2}\right).
\]

A global bandwidth h controls the bias-variance trade-off. Small h preserves
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
