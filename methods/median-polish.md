# Tukey median polish for two-way tables

Median polish is a robust alternative to ordinary two-way additive decomposition. It fits

\[
y_{ij}=\mu+\alpha_i+\beta_j+e_{ij},
\]

where mu is an overall effect, alpha_i is a row effect, beta_j is a column effect and e_ij is the residual.

## Algorithm

Initialize mu to the median of observed cells and subtract it from the table. Then iterate:

1. Compute each row's median residual, add it to that row effect and subtract it from the row.
2. Compute each column's median residual, add it to that column effect and subtract it from the column.
3. Recenter row and column effects by their medians, adding those shifts to mu.
4. Compute the sum of absolute residuals. Stop when its proportional reduction is below eps or the iteration limit is reached.

This implementation follows the convergence criterion documented by R stats::medpolish. Missing values are rejected unless na_rm=True; when ignored, they remain missing in the residual output. All-missing rows and columns receive zero effects.

## Spatial use and limitations

Median polish is a robust two-way table decomposition, not a coordinate-based spatial smoother. It can be useful for exploratory row/column structures such as area-by-time tables, but it does not model adjacency, spatial covariance or interactions. It is unweighted and does not provide standard errors or hypothesis tests.

## References

- Tukey, J. W. (1977). *Exploratory Data Analysis*. Addison-Wesley.
- R stats package documentation, [medpolish](https://stat.ethz.ch/R-manual/R-devel/library/stats/html/medpolish.html).
