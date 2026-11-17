# Adaptive Lee speckle filtering

The Lee filter is a local adaptive estimator for speckled intensity imagery.
This implementation uses the multiplicative-noise approximation in which
local noise variance is the squared local mean divided by equivalent number
of looks (ENL). It subtracts modeled noise variance from observed local
variance to estimate signal variance, then blends each centre pixel toward
the local mean according to the signal-to-observed-variance ratio.

Neighbourhoods are clipped at image edges and NaN NoData cells are excluded
from local moments. ENL is an explicit assumption and must be calibrated to
the image product. This is a teaching baseline, not refined Lee filtering or
a complete SAR preprocessing chain.

See the [implementation](../../implementations/python/lee-speckle-filter/README.md)
and [tests](../../implementations/python/lee-speckle-filter/test_lee_filter.py).

It does not cover polarimetric decomposition, CFAR, InSAR, SAR-to-optical
translation or sensor-specific radiometric calibration. Filtering can
suppress speckle while blurring point targets and narrow linear features.
