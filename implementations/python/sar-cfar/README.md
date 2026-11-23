# SAR CFAR detectors

NumPy reference implementations of square-window 2-D cell-averaging CFAR (CA-CFAR) and ordered-statistics CFAR (OS-CFAR).

Both functions return a CFARResult with detections, threshold, background estimate and validity mask. The outer square radius is training_cells; the inner square radius guard_cells is excluded. Border cells are not evaluated. Non-finite training cells are omitted.

OS-CFAR uses a one-based ascending rank, defaulting to the 75th percentile of the nominal training ring. CA and OS multipliers assume independent, identically distributed exponential intensity. Real SAR clutter may be correlated, textured, heterogeneous or multi-look; the requested Pfa is therefore nominal, not guaranteed. Calibrate against representative data before operational use.

Not included: GO/SO-CFAR, edge-adaptive windows, polarimetric detectors, CFAR clustering or sensor-specific preprocessing.

Run: python -m pip install -r requirements.txt pytest && python -m pytest -q
