# Moran eigenvector spatial filtering

Extract orthogonal spatial patterns from the centered symmetric weights matrix HWH and add a selected subset of positive-eigenvalue eigenvectors to a regression as synthetic covariates.

The [implementation](../../implementations/python/moran-eigenvector-filtering/README.md) includes the eigenvector basis and a fixed-size OLS filter. The number of eigenvectors is caller-specified.

This is not the complete semiparametric eigenvector filtering procedure: automatic subset selection, the general covariate projection, Spatial+, restricted spatial regression and GLM variants remain open.

## References

Griffith (2003); Griffith and Peres-Neto (2006); Tiefelsdorf and Griffith (2007).
