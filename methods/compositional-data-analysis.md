# Compositional data analysis and log-ratio geometry

## 1. Compositions live on a simplex

A D-part composition is a positive vector whose information is carried by relative magnitudes, not its arbitrary total. Closure maps a nonnegative vector with positive total to unit sum:

\[
C(x)=\frac{x}{\sum_{j=1}^{D}x_j}.
\]

Scaling every part by the same positive constant leaves the closed composition unchanged.

## 2. Centered log-ratio transform

Let g(x) be the geometric mean of the positive parts. The centered log-ratio transform is

\[
\operatorname{clr}(x)_i=\log\frac{x_i}{g(x)}
=\log x_i-\frac{1}{D}\sum_j\log x_j.
\]

The coordinates sum to zero, so the D-dimensional CLR covariance matrix is singular. CLR is useful for expressing log-ratio geometry but its coordinates are not unconstrained independent Euclidean variables.

## 3. Isometric log-ratio transform

Let H be a D-by-(D−1) orthonormal contrast matrix with HᵀH=I and 1ᵀH=0. The ILR transform is

\[
\operatorname{ilr}(x)=\log(C(x))^T H.
\]

This implementation uses a Helmert basis. The inverse maps coordinates back by multiplying by Hᵀ, exponentiating and closing. ILR coordinates are Euclidean and preserve Aitchison distance. Individual balance coordinates depend on the selected orthonormal basis.

## 4. Additive log-ratio transform

For a selected denominator part d,

\[
\operatorname{alr}(x)_i=\log(x_i/x_d),\qquad i\ne d.
\]

ALR is simple to interpret but depends on the denominator and is not an isometric coordinate system.

## 5. Aitchison distance

The Aitchison distance is the Euclidean distance between ILR coordinates, equivalently the norm of the difference between CLR coordinates. It compares relative composition rather than absolute totals.

## 6. Zero values and scope

Log-ratio methods require positive parts. Structural zeros, rounded zeros and values below detection limits are not interchangeable. This implementation rejects zeros in CLR, ALR and ILR rather than silently applying a pseudocount. Zero replacement and imputation require an explicit measurement model.

The companion [NumPy implementation](../implementations/python/compositional-data/README.md) includes closure, CLR, ALR, ILR, inverse transforms and Aitchison distance. It does not implement compositional kriging, spatial dependence, regression, Bayesian inference or zero replacement.

## References

- Aitchison, J. (1982). “The statistical analysis of compositional data.” *Journal of the Royal Statistical Society: Series B*, 44(2), 139–160. https://doi.org/10.1111/j.2517-6161.1982.tb01195.x.
- Egozcue, J. J., Pawlowsky-Glahn, V., Mateu-Figueras, G., & Barceló-Vidal, C. (2003). “Isometric logratio transformations for compositional data analysis.” *Mathematical Geology*, 35(3), 279–300. https://doi.org/10.1023/A:1023818214614.
