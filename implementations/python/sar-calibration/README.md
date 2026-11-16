# SAR radiometric calibration and multilooking

Install and test with `python -m pip install -r requirements.txt && python -m pytest -q`.

`radiometric_calibrate` maps complex or detected digital numbers to calibrated sigma-nought using a caller-supplied factor, optionally subtracting noise power. It can convert sigma0 to beta0 or gamma0 using a caller-supplied incidence-angle image in radians. Calibration factors and their sensor-specific interpretation are external inputs.

`multilook_intensity` averages non-overlapping azimuth/range blocks and crops incomplete trailing blocks. The NoData policy is explicit: omit invalid samples or propagate them to the output block.

This package does not estimate calibration LUTs, noise floors, orbit state, DEM-based radiometric terrain correction, geocoding, speckle filtering, TOPS ESD coregistration or full Sentinel-1/other sensor processing chains.
