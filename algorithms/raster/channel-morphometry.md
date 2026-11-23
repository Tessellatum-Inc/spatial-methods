# Channel chi, slope-area and knickpoint analysis

## Chi coordinate

For a channel profile with drainage area A(x), reference area A0 and concavity exponent θ, the chi coordinate is the along-channel integral of (A0/A)^θ. The implementation uses trapezoidal integration over strictly increasing distance samples and sets the first value to zero. Distance and drainage area must be in consistent declared units; A0 uses the same area unit.

## Slope-area relationship

The slope-area helper estimates local segment slope from adjacent elevation-distance samples, associates it with mean segment drainage area, and fits log10(S)=intercept+b log10(A) by ordinary least squares. It returns b, 10^intercept, R² and segment arrays. The fit is descriptive and sensitive to DEM resolution, channel segmentation, smoothing and area errors; it is not a direct uplift or erosion-rate inversion.

## Knickpoint screening

The knickpoint helper compares each centre profile elevation with the chord joining the endpoints of a complete odd-sized moving window. A signed residual threshold screens candidate convex-up and concave-up departures. This is a transparent profile-shape detector, not a geological attribution or a robust automated knickzone segmentation method.

## Scope

The routines require a single ordered channel profile and supplied drainage areas. They do not extract channel networks, select concavity from data, account for tributary junctions, propagate elevation/area uncertainty, correct DEM artifacts, or infer tectonic history. Record profile direction, map units, DEM resolution, window size and thresholds.
