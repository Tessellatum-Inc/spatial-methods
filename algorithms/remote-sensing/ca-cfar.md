# Two-dimensional cell-averaging CFAR

Cell-averaging constant-false-alarm-rate (CA-CFAR) detection estimates local
background intensity from a training ring around a cell under test (CUT).
Guard cells prevent a target and its immediate response from contaminating
that estimate. For N independent exponentially distributed intensity
samples and desired false-alarm probability Pfa, the multiplier is
\[
\alpha=N(P_{fa}^{-1/N}-1), \qquad T=\alpha\bar{x}.
\]
The included implementation uses square outer and guard windows. It marks
border cells and CUTs with NoData in the training ring as unevaluated.

See the [implementation](../../implementations/python/ca-cfar/README.md) and
[tests](../../implementations/python/ca-cfar/test_ca_cfar.py).

The statistical model assumes independent exponential intensity samples.
Correlated speckle, clutter edges and multiple targets in the training ring
can invalidate the nominal false-alarm rate. This is not OS-CFAR, GO-CFAR,
SO-CFAR or a sensor-calibrated detection workflow.
