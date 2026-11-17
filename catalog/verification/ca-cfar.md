# CA-CFAR verification

- Scope: square-window 2D cell-averaging CFAR for intensity data.
- Implementation: implementations/python/ca-cfar/ca_cfar.py.
- Tests: implementations/python/ca-cfar/test_ca_cfar.py.
- Checks: constant background, point-target detection, guard-cell exclusion, border and NoData handling, incomplete training ring, and parameter validation.
- Assumptions: independent exponential intensity samples; square training/guard geometry.
- Not covered: OS-CFAR, GO-CFAR, SO-CFAR, clutter maps, correlated-clutter calibration or sensor-specific detection validation.
- Status: scoped implementation and authored tests; CI execution pending.
