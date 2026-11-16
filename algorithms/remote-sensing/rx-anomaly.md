# Reed–Xiaoli (RX) anomaly detection

## Purpose

RX detects spectrally unusual pixels by measuring squared Mahalanobis distance from an estimated background distribution. It is a classic hyperspectral anomaly-detection baseline.

## Implemented scope

The NumPy reference implements global RX with empirical or supplied covariance, a background mask and eigenvalue regularisation. Invalid output positions are NaN. See [implementation](../../implementations/python/rx-anomaly/README.md).

## Assumptions and limitations

The global detector assumes one background mean/covariance adequately describes the scene. Background contamination and spatially heterogeneous backgrounds can reduce detection quality. Scores are not calibrated probabilities. Local RX, kernel RX, subspace methods and operational false-alarm control are not implemented.
