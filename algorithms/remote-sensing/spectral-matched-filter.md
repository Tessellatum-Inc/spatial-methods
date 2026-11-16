# Spectral matched filter

## Purpose

The spectral matched filter detects a known target signature against a statistical background model, enhancing target contrast while accounting for background covariance.

## Implemented scope

The reference implementation estimates or accepts a global background covariance, applies covariance regularisation and returns normalized matched-filter scores and weights. See [implementation](../../implementations/python/spectral-matched-filter/README.md).

## Distinctions

This is not RX anomaly detection: RX scores general spectral deviation, whereas matched filtering tests contrast against a specified target signature. It is also distinct from CEM, ACE and matched-subspace detection.
