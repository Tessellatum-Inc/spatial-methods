# HANTS time-series fitting

This package implements a bounded Harmonic Analysis of Time Series (HANTS)
baseline. A Fourier series is fitted by least squares, then the largest
residual exceeding the selected low/high rejection threshold is removed.
The process repeats until no eligible residual remains or the iteration
limit/minimum-observation guard is reached.

NaN observations are treated as missing. The result reports the fitted
series, residuals, retained/rejected/missing indices and convergence flag.

## Install and test

    python -m pip install -r requirements.txt
    python -m pytest -q

## Limits

This is a compact teaching baseline, not a complete reproduction of every
HANTS variant. It does not model heteroskedastic errors, irregular sampling
weights, sensor-specific quality flags, spatial interpolation or
uncertainty. Period and harmonic count must be selected deliberately.
