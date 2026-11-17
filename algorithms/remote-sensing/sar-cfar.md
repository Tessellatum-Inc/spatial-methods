# SAR constant-false-alarm-rate detection

CA-CFAR estimates local clutter with the mean of a guard-excluded training ring. OS-CFAR uses a selected ascending order statistic, reducing sensitivity to a limited number of bright interfering targets in the reference window.

For N independent exponential intensity training samples, CA-CFAR uses alpha = N(Pfa^(-1/N) - 1). For OS-CFAR with one-based rank k, alpha is solved from Pfa = product((N-i)/(N-i+alpha)) for i from 0 to k-1. The reference implementation uses monotone bisection.

The implementation uses square Chebyshev windows, omits incomplete border windows, skips non-finite training samples and exposes a validity mask. Analytic false-alarm rates are not guaranteed for correlated or heterogeneous clutter.

See [implementation](../../implementations/python/sar-cfar/README.md) and [verification record](../../catalog/verification/sar-cfar.md).
