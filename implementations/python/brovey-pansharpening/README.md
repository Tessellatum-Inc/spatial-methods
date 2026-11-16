# Brovey pan-sharpening

A dependency-free component-substitution baseline for co-registered,
same-sized multispectral and panchromatic rasters.

For N multispectral bands, each pixel is transformed as

    output_i = input_i * PAN * N / sum(input bands)

The operation scales all bands by the same per-pixel factor, so their
relative proportions are preserved. If any input band or the panchromatic
pixel is missing, or the multispectral sum is zero, all output bands at that
pixel are marked None. Negative valid inputs are rejected. Values are not
clipped or rescaled to a display range.

## Assumptions and limitations

The caller must align and resample the multispectral bands and PAN image to
the same grid and radiometric units first. Brovey is a simple spectral
component-substitution method; it can distort spectral signatures, especially
for vegetation and water, and does not model sensor modulation transfer
functions, point-spread functions, registration error, noise or spectral
response. It is not a substitute for Gram-Schmidt, IHS, wavelet or Bayesian
fusion. Validate spectral and spatial fidelity for the sensor/application.

## Tests

    python -m pytest -q
