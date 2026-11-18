# Walkthrough: robust noise estimation from Haar diagonal detail

1. Split the image into non-overlapping 2x2 blocks. Drop an unmatched final row or column so no synthetic boundary values are introduced.
2. Compute the orthonormal diagonal-detail coefficient `(p00 - p01 - p10 + p11) / 2`. Its four weights have squared sum one, so independent equal-variance pixel noise retains variance sigma-squared in this coefficient band.
3. Estimate the centre by the median of the coefficients, then compute the median absolute deviation from that centre.
4. Divide by 0.67448975, the median absolute deviation of a standard normal variable, to obtain a robust sigma estimate.
5. For a band stack, repeat independently for each band; this does not model cross-band covariance.

The method is intentionally narrow. A smooth planar ramp has zero ideal HH detail, but textured surfaces and edges contribute real high-frequency energy and can inflate the estimate. Correlated, periodic, heteroscedastic and signal-dependent sensor noise require different models or preprocessing.
