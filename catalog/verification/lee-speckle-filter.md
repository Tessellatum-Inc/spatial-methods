# Lee speckle-filter verification

- Scope: single-channel non-negative SAR intensity with an adaptive local Lee estimator.
- Implementation: implementations/python/lee-speckle-filter/lee_filter.py.
- Tests: implementations/python/lee-speckle-filter/test_lee_filter.py.
- Checks: constant-field preservation, impulse smoothing, NaN NoData isolation, all-NoData input, window and ENL validation, non-square arrays and clipped edges.
- Limits: caller-supplied ENL; local finite-neighbourhood moment approximation; no refined/polarimetric variant or sensor calibration.
- Not covered: polarimetric decomposition, CFAR, InSAR or SAR-to-optical translation.
- Status: scoped implementation and authored tests; CI execution pending.
