# Verification record: least-squares collocation

## Identity
- Canonical record: finite-dimensional linear least-squares collocation with fixed trend and correlated signal/noise.
- Implementation: implementations/python/geostatistics/least_squares_collocation.py.
- Classification: dense LSC predictor; mathematically equivalent to universal kriging under the stated covariance/trend assumptions.

## Bibliographic verification
- Moritz (1978), Reviews of Geophysics 16(3), 421–430, DOI 10.1029/RG016i003p00421, provides the foundational review of least-squares collocation.
- Moritz (1973), Publications on Geodesy, New Series 75, is the earlier monograph.
- The mixed model y=H beta+s+e and covariance-based predictor are consistent with the standard LSC formulation.

## Technical checks
- Combined observation covariance is C+R.
- Trend is estimated by generalized least squares.
- Target signal is predicted from cross-covariance with the observation residual.
- Prediction covariance includes both signal/noise uncertainty and fixed-trend estimation uncertainty.
- Covariance matrices are supplied by the user; the implementation does not estimate them.
- The package does not claim to implement the full physical-geodesy covariance-function machinery.

## Reproduction and rights
- Original NumPy implementation and tests.
- Tests cover constant trend, exact noiseless interpolation, correlated measurement noise, multiple trend terms, invalid dimensions and singular designs.
- No third-party code, figures or data are reproduced.
- Repository CI pending.
