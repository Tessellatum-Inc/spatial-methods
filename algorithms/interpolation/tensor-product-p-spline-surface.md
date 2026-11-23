# Tensor-product B-spline P-surface

A scalar spatial response is represented by a tensor product of marginal B-spline bases:

\[
f(x,y)=\sum_{i=1}^{n_x}\sum_{j=1}^{n_y}c_{ij}B_i(x)B_j(y).
\]

The coefficient array is regularized by second divided differences in each coordinate direction:

\[
\min_C\|y-\mathcal BC\|_2^2+
\lambda_x\|D_xC\|_F^2+
\lambda_y\|CD_y^T\|_F^2.
\]

This is a tensor-product P-spline regression surface, not a thin-plate radial-basis spline or a classical minimum-curvature smoothing spline. The NumPy baseline uses open-uniform knots, Cox–de Boor basis evaluation, a dense tensor-product design matrix and separate x/y coefficient penalties. Penalty operators are defined on Greville abscissae, preserving linear marginal trends and their bilinear tensor-product null space.

The implementation is a small-data teaching baseline. Dense matrices are unsuitable for large rasters or streaming workloads. Knot counts and smoothing strengths are analyst supplied; automatic smoothing selection, uncertainty, missing-data models, sparse/array solvers, boundary conditions, barrier-aware bases and extrapolation are not implemented. Use projected planar coordinates with a meaningful metric.

## Sources
- Eilers, P. H. C., & Marx, B. D. (1996). Flexible smoothing with B-splines and penalties. *Statistical Science*, 11(2), 89–102. https://doi.org/10.1214/ss/1038425655.
- Wood, S. N. (2017). P-splines with derivative based penalties and tensor product smoothing of unevenly distributed data. *Statistics and Computing*, 27, 985–989. https://doi.org/10.1007/s11222-016-9666-x.

No source figures, code or datasets are reproduced.
