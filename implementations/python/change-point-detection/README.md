# Change-point detection: executable mean-shift baselines

This package implements three transparent univariate teaching algorithms:
- CUSUM: two-sided Page-style sequential monitoring against a known reference mean.
- Binary segmentation: greedy retrospective recursive splitting.
- PELT mean: pruned dynamic programming for a penalised piecewise-constant mean objective using segment SSE.

Run python -m pip install -r requirements.txt and python -m pytest -q.

Inputs are finite numeric observations in temporal order. The segmentation methods assume equally weighted observations and a piecewise-constant mean. Change points are zero-based indices of the first observation in the new segment. Minimum segment length is in observations.

CUSUM needs a known reference mean, allowance and threshold. It is not automatically calibrated for a target false-alarm rate. PELT is exact for the stated objective subject to numerical arithmetic; its worst-case runtime is quadratic. The package does not implement variance/distribution shifts, BOCPD, BEAST, irregular-time likelihoods or a general plug-in cost framework.


## Pettitt single-change-point test

`pettitt_test(values)` implements the rank-based single location-change statistic with average ranks for ties and returns the selected zero-based split, signed statistic, maximum absolute statistic K and the conventional large-sample approximate p-value. Its null calibration assumes independent observations; serial dependence, seasonality, trend and repeated testing across locations require separate treatment. The approximate p-value is not an exact permutation test.

## Bayesian online change-point detection

The bayesian_online.py module implements the Adams–MacKay run-length recursion for an explicit conjugate model: unknown segment mean with a Normal prior, known Gaussian observation variance and constant hazard. It returns the posterior over run length, change probability and MAP run length. This is not a generic BOCPD framework; changing the likelihood, parameter prior or hazard changes the model.

## Bayesian online change-point detection with known variance

The `online.py` module adds `bocpd_normal_mean`, a bounded Adams–MacKay run-length recursion for a Gaussian observation model with known observation variance, a Normal prior on each segment mean and constant hazard. It returns the per-observation change-point probability and MAP run length. This is a distinct, deliberately restricted model from the package's `bayesian_online.py` variant; do not treat either as a generic unknown-likelihood BOCPD engine. The companion `test_online.py` checks probability bounds, regime-change response, run-length truncation and invalid inputs.

## Restored detector module

The `detectors.py` module contains the dependency-free CUSUM, greedy binary-segmentation and penalised PELT implementations, with the corresponding `test_detectors.py` suite. PELT uses K=0 pruning for minimum segment length one and exact unpruned dynamic programming for larger minimum lengths, preserving the stated constraint. These methods target univariate piecewise-constant mean changes; they do not implement BEAST or automatically calibrate false-alarm rates.
