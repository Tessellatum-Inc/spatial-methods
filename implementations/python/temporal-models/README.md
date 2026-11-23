# Robust trend, temporal decomposition and HMM decoding baselines

This dependency-free package contains:

- **Theil–Sen:** median of all pairwise slopes, with median intercept; resistant to some outliers but quadratic in sample count in this direct implementation.
- **Pettitt:** rank-based single change-point statistic with average ranks for ties and an approximate p-value. It tests one dominant distributional change; it is not a multiple-change segmentation method.
- **Viterbi:** log-space decoding for a discrete-emission hidden Markov model with explicit start, transition and emission probabilities.
- **Kalman / RTS:** scalar local-level Kalman filtering and Rauch–Tung–Striebel smoothing, with prediction-only handling of missing observations; see the [methods lesson](../../../methods/kalman-temporal-filtering.md).
- **STL-style decomposition:** local-linear LOESS seasonal-subseries filtering, low-pass adjustment, iterative trend extraction and optional robust weights; see the [STL lesson](../../../methods/stl-seasonal-trend-decomposition.md).

Run from this directory:

```bash
python -m pytest -q --import-mode=importlib
```

Theil–Sen requires numeric paired observations and at least two distinct x-values. Pettitt assumes an ordered independent sequence under its usual null calibration; serial dependence and ties affect inference. Viterbi does not estimate HMM parameters, handle continuous emissions or replace model validation. The Kalman package is scalar/local-level only; it does not provide general matrix-state models or estimate noise parameters.

The STL implementation is a compact educational approximation, not an exact port of Cleveland et al. (1990) or a replacement for a mature implementation. It requires finite equally spaced observations and at least two complete cycles; missing values, irregular timestamps, multiplicative decomposition, calendar effects and the original algorithm's full tuning controls are not implemented. These are teaching baselines, not turnkey EO time-series workflows.
