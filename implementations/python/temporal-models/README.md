# Robust trend, Pettitt and HMM decoding baselines

This dependency-free package contains:

- **Theil–Sen:** median of all pairwise slopes, with median intercept; robust to some outliers but quadratic in sample count in this direct implementation.
- **Pettitt:** rank-based single change-point statistic with average ranks for ties and an approximate p-value. It tests one dominant distributional change; it is not a multiple-change segmentation method.
- **Viterbi:** log-space decoding for a discrete-emission hidden Markov model with explicit start, transition and emission probabilities.

Run from this directory:

```bash
python -m pytest -q
```

Theil–Sen requires numeric paired observations and at least two distinct x-values. Pettitt assumes an ordered independent sequence under its usual null calibration; serial dependence and ties affect inference. Viterbi does not estimate HMM parameters, handle continuous emissions or replace model validation. These are teaching baselines, not turnkey EO change-detection workflows.
