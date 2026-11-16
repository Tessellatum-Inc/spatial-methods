# Inhomogeneous Ripley's K

The inhomogeneous K-function adjusts pair contributions for a spatially varying first-order intensity surface. Given event locations x_i and positive intensity estimates lambda_i, the ordered-pair estimator is

\[
\widehat K_{inhom}(r)=\frac{1}{|W|}\sum_{i\ne j}\frac{\mathbf 1(d_{ij}\le r)}{\hat\lambda(x_i)\hat\lambda(x_j)}.
\]

The implementation accepts event-specific intensities from the caller and optionally applies rectangular-window translation correction. Intensities are in events per unit area. If all intensities equal n/|W|, the uncorrected inhomogeneous estimator reduces to the ordinary uncorrected K estimator.

The intensity surface is not estimated internally. Kernel bandwidth selection, edge correction for irregular windows, parameter-estimation effects and simulation-based global inference remain separate tasks. Inhomogeneous K is not a substitute for a defensible first-order model; estimating intensity from the same point pattern can introduce bias and must be accounted for in inference.

Code and regression tests: implementations/python/ripley-k.
