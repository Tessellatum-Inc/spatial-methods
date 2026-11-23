# Flood-frequency analysis: Gumbel and GEV

## Purpose

Estimate annual-maximum event quantiles associated with selected return periods. This module provides empirical Weibull plotting positions and two L-moment fitted extreme-value distributions: Gumbel and the generalized extreme-value (GEV) family.

## Methods

For descending annual maxima, the Weibull plotting position uses exceedance probability m/(n+1) and return period (n+1)/m. Gumbel parameters are estimated from sample L-location and L-scale. GEV location, scale and shape are estimated from the first three sample L-moments, using a standard polynomial approximation for shape; shape zero is the Gumbel limit.

For a T-year return period, the target non-exceedance probability is 1-1/T. The return level is the corresponding fitted distribution quantile.

## Implementation and assumptions

See [flood_frequency.py](../../implementations/python/terrain-derivatives/flood_frequency.py). Input values must be a one-dimensional sample of independent, identically distributed annual maxima in consistent units. At least three observations are required for Gumbel fitting and four for GEV fitting. The L-moment estimators are transparent teaching/reference estimators; the shape approximation and short-record uncertainty warrant caution.

A T-year return period is an annual exceedance probability of 1/T under stationarity. It does not mean an event occurs regularly every T years. The implementation does not perform trend/nonstationarity analysis, regional pooling, censoring, historical-information weighting, uncertainty intervals, goodness-of-fit selection, peak-over-threshold modelling or hydraulic design checks. Extrapolated design quantiles should not be used without diagnostics and uncertainty analysis.
