# Area-level inequality, entropy and two-group segregation

## Weighted Gini

For nonnegative area values x_i, weights w_i and weighted mean μ, the weighted Gini coefficient is

\[
G_w=\frac{\sum_i\sum_j w_iw_j|x_i-x_j|}
{2\mu(\sum_iw_i)^2}.
\]

It summarizes inequality in area values. It does not include spatial distances or adjacency.

## Theil T and Theil L

Let p_i = w_i / sum(w) and μ = sum(w_i x_i)/sum(w_i). Theil T is

\[
T=\sum_i p_i\frac{x_i}{\mu}\log\left(\frac{x_i}{\mu}\right),
\]

with zero-valued x_i terms defined by continuity as zero. Theil L (mean log deviation) is

\[
L=\sum_i p_i\log\left(\frac{\mu}{x_i}\right).
\]

Theil L is infinite when a positive-weight observation is zero; this implementation raises an explicit error rather than returning a misleading finite value. Both indices are zero under equality and are decomposable under suitable group partitions.

## Shannon entropy of areal population shares

For area population shares p_i = n_i / sum(n),

\[
H=-\sum_i p_i\log(p_i).
\]

The normalized entropy H/log(m) lies between zero and one for m supplied areas. It reaches one when population is equally distributed and zero when all population lies in one area. This summary ignores the geometric arrangement of areas.

## Two-group dissimilarity

For counts a_i and b_i in each area,

\[
D=\frac{1}{2}\sum_i\left|\frac{a_i}{A}-\frac{b_i}{B}\right|,
\qquad A=\sum_i a_i,\ B=\sum_i b_i.
\]

D is bounded by zero and one. It measures evenness, not spatial clustering or proximity.

## Isolation and interaction

For a group-A resident selected at random, the isolation index is

\[
P_{AA}=\sum_i\frac{a_i}{A}\frac{a_i}{a_i+b_i},
\]

and the interaction index is

\[
P_{AB}=\sum_i\frac{a_i}{A}\frac{b_i}{a_i+b_i}.
\]

For exactly two exhaustive groups, P_AA + P_AB = 1. These are exposure measures and depend on the relative sizes and definitions of the groups.

## Scope

The implementation does not calculate distance-weighted spatial Gini, Moran-based inequality, multi-group entropy decomposition, spatial clustering/proximity indices, concentration, centralization or distance-decay exposure. These measures are descriptive and sensitive to area definitions and population denominators.

## References

- Duncan, O. D. and Duncan, B. (1955). “A Methodological Analysis of Segregation Indexes.” *American Sociological Review*, 20(2), 210–217. DOI [10.2307/2088328](https://doi.org/10.2307/2088328).
- Massey, D. S. and Denton, N. A. (1988). “The Dimensions of Residential Segregation.” *Social Forces*, 67(2), 281–315. DOI [10.1093/sf/67.2.281](https://doi.org/10.1093/sf/67.2.281).
- Shannon, C. E. (1948). “A Mathematical Theory of Communication.” *Bell System Technical Journal*, 27(3), 379–423. DOI [10.1002/j.1538-7305.1948.tb01338.x](https://doi.org/10.1002/j.1538-7305.1948.tb01338.x).
- Theil, H. (1967). *Economics and Information Theory*. North-Holland.
