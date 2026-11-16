# Universal kriging with polynomial drift

Install and test with `python -m pip install -r requirements.txt && python -m pytest -q`.

The dense solver supports unknown constant, linear or quadratic polynomial drift and caller-supplied spherical, exponential or Gaussian variogram parameters. It returns target predictions and conditional kriging variance. Coordinates are planar and range uses the same units.

This is a small-data reference solver. It does not fit variograms, select local neighbourhoods, handle anisotropy, or implement co-kriging, regression kriging, external drift, indicator/disjunctive, block, area-to-point/area-to-area or spatiotemporal kriging. The model's variance is conditional on the supplied covariance structure and drift specification.
