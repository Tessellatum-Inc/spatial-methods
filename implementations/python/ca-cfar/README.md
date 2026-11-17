# Cell-averaging CFAR

A NumPy 2D cell-averaging constant-false-alarm-rate detector for intensity
rasters. A square guard window excludes the cell under test and nearby
samples; the surrounding square ring estimates local background power.
The threshold multiplier uses the exact CA-CFAR expression for independent
exponential intensity samples.

Run:
    python -m pip install -r requirements.txt
    pytest -q

ca_cfar returns a boolean detection mask, threshold surface and local noise
estimate. Border cells and cells whose training ring contains NaN NoData are
not evaluated.

CA-CFAR is sensitive to clutter edges, multiple targets in the training ring,
correlated samples and heterogeneous backgrounds. This is not OS-CFAR,
GO-CFAR, SO-CFAR, clutter-map CFAR or a sensor-calibrated detection product.
