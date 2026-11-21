# SAR constant-false-alarm-rate detection

**Physical and data context:** The [radar scattering and SAR signal-formation foundation](../../foundations/remote-sensing-physics/radar-scattering-and-sar-signal-formation.md) introduces coherent radar returns, intensity and speckle. Before applying CFAR, use the [SAR acquisition and observation design method](../../collection/sar-acquisition-and-observation-design.md) to establish product type, calibration, value scale, polarisation, geometry and provenance.

CA-CFAR estimates local clutter with the mean of a guard-excluded training ring. OS-CFAR uses a selected ascending order statistic, reducing sensitivity to a limited number of bright interfering targets in the reference window.

For N independent exponential intensity training samples, CA-CFAR uses alpha = N(Pfa^(-1/N) - 1). For OS-CFAR with one-based rank k, alpha is solved from Pfa = product((N-i)/(N-i+alpha)) for i from 0 to k-1. The reference implementation uses monotone bisection.

The implementation uses square Chebyshev windows, omits incomplete border windows, skips non-finite training samples and exposes a validity mask. Analytic false-alarm rates are not guaranteed for correlated or heterogeneous clutter. In particular, the exponential clutter model is an idealised assumption; calibration, preprocessing, multilooking, spatial correlation and target heterogeneity can change the false-alarm behaviour.

See [implementation](../../implementations/python/sar-cfar/README.md) and [verification record](../../catalog/verification/sar-cfar.md).
