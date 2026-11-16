# Standard line Hough transform

Install dependencies and run `pytest -q`. The accumulator votes for line parameters in normal form, rho = x cos(theta) + y sin(theta), from nonzero edge pixels. Peak extraction applies rectangular non-maximum suppression.

The default theta grid spans [-pi/2, pi/2). Rho bins are quantized to the requested resolution. This is a standard straight-line detector, not a probabilistic or progressive probabilistic Hough transform; it does not estimate finite segment endpoints. The accumulator is dense and cost scales with edge-pixel count times theta-bin count.
