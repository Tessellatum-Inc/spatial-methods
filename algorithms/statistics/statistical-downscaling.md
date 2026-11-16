# Statistical downscaling: quantile mapping and delta change

Empirical quantile mapping corrects a simulated value by locating its
quantile in the model calibration distribution and mapping that probability
to the observed calibration distribution. The linked baseline uses
piecewise-linear interpolation and constant tails outside the calibration
range. It is univariate and assumes the calibration-period bias relationship
remains relevant.

Delta change applies a modelled future change to the observed historical
mean. The additive form applies an absolute change; the multiplicative form
applies a ratio. It adjusts a mean-level change and does not correct the
future distribution's shape.

Neither method is a complete spatial downscaling workflow. BCSD, analog
methods, multivariate correction, physical disaggregation and validation
against independent periods remain distinct work.
