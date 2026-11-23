# Implementation verification — polynomial trend surface

The package implements global total-degree polynomial regression for planar
coordinates at degrees 0 through 3. It supports ordinary and positive
weighted least squares, internally normalized coordinates, and fitted-value
and residual diagnostics.

Synthetic checks recover known constant, linear and quadratic surfaces,
including predictions away from training coordinates. Additional tests
cover weighted fitting, coordinate translation/scaling, empty query batches,
rank-deficient geometries, invalid weights, invalid degree values and
non-finite inputs.

This is an algebraic teaching baseline. It does not include autocorrelation-
robust inference, spatial covariance modelling, automatic degree selection,
cross-validation, or external geospatial data validation. Bibliographic
references are orientation sources; source-entry identity and technical
claim verification remain separate catalogue tasks. Redistribution rights
for the source compendium remain unresolved.
