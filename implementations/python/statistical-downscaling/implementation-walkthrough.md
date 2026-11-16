# Statistical downscaling walkthrough

## Empirical quantile mapping

1. Build equally spaced probability levels between zero and one.
2. Evaluate model calibration and observed calibration distributions at
   those levels.
3. Collapse repeated model quantile knots and average their paired observed
   quantiles so interpolation abscissae are strictly increasing.
4. Interpolate simulated values through the mapping. Values outside the
   calibration range use constant endpoint values.

This is a univariate empirical mapping. It does not guarantee preservation
of climate-change trends or cross-variable dependence.

## Delta change

The additive form adds the modelled future-minus-historical mean change to
the observed historical mean. The multiplicative form applies the modelled
future-to-historical mean ratio. The correction is applied to each future
value, preserving the future array shape.
