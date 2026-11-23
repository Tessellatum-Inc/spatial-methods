# Time-series DTW verification

- Scope: dynamic time warping and an explicitly specified logistic time-weighted DTW variant.
- Implementation: implementations/python/time-series-dtw/dtw.py.
- Tests: implementations/python/time-series-dtw/test_dtw.py.
- Checks: identical-sequence zero cost, repeated-observation warping, path endpoints, window validation, multivariate dimensions, temporal penalty monotonicity, timestamp shape/order/finiteness and parameter validation.
- Limits: accumulated rather than normalized cost; Euclidean local metric; quadratic dynamic program; caller-calibrated temporal units and penalty parameters.
- Not covered: TempCNN, Transformer, InceptionTime, TimeMatch, training, classification, missing-data handling or published benchmark reproduction.
- Status: scoped implementation and authored tests; CI execution pending.
