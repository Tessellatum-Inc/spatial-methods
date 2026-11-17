# Lee speckle filter

NumPy reference implementation of adaptive Lee filtering for non-negative,
single-channel SAR intensity. Local moments use summed-area tables; image
edges use clipped neighbourhoods and NaNs are ignored as NoData.

Install and test:
    python -m pip install -r requirements.txt
    pytest -q

Call lee_filter(image, window_size=5, equivalent_looks=1.0). ENL must be
calibrated from sensor/product metadata or a homogeneous region; the default
is a teaching baseline only.

This is not refined Lee or polarimetric filtering. It does not perform
radiometric calibration, terrain correction, polarimetric decomposition,
CFAR, InSAR processing or SAR-to-optical translation. Filtering can blur
point targets and narrow edges.
