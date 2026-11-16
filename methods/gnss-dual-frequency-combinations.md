# Dual-frequency GNSS combinations

For two carrier frequencies \(f_1\) and \(f_2\), let \(L_1,L_2\) be carrier-phase observables expressed as range in metres. The geometry-free combination is
\[
L_{GF}=L_1-L_2,
\]
which removes common geometric range and clocks but retains frequency-dependent terms, including much of the ionospheric signature. A discontinuity can help flag a cycle slip, but practical detection needs noise and ionosphere modelling and robust thresholds.

The first-order ionosphere-free combination is
\[
L_{IF}=\frac{f_1^2L_1-f_2^2L_2}{f_1^2-f_2^2}.
\]
It cancels the first-order ionospheric term under the standard dispersive model, while amplifying measurement noise and not removing higher-order effects, multipath or hardware biases. The wide-lane phase combination in cycles is \(N_W=L_1^{(cycles)}-L_2^{(cycles)}\), with wavelength \(c/(f_1-f_2)\).

The [Python package](../implementations/python/gnss-ambiguity/README.md) implements these combinations and a separate low-dimensional integer least-squares search. It does not implement cycle-slip detection or a complete PPP/RTK pipeline.

## Sources

- Hofmann-Wellenhof, B., Lichtenegger, H., & Wasle, E. (2008). *GNSS — Global Navigation Satellite Systems: GPS, GLONASS, Galileo, and More*. Springer. Dual-frequency observation combinations and ionospheric effects.
- Teunissen, P. J. G. (1995). “The least-squares ambiguity decorrelation adjustment: a method for fast GPS integer ambiguity estimation.” *Journal of Geodesy*, 70, 65–82. [DOI](https://doi.org/10.1007/BF00863419).

No source text or figures are reproduced.
