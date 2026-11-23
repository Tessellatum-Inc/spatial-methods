# SAR CFAR verification record

- Scope: square-window 2-D CA-CFAR and OS-CFAR on non-negative intensity arrays.
- Tests: homogeneous background, injected target, guard exclusion, NaN training/CUT, border validity, invalid parameters and OS threshold monotonicity.
- Statistical model: independent exponential intensity; requested false-alarm rate is nominal under this model only.
- Not covered: real-sensor empirical calibration, correlated/compound-Gaussian clutter, GO/SO-CFAR, polarimetric detection, clustering or full SAR preprocessing.
- Status: tested reference implementation, not a validated operational detector.
