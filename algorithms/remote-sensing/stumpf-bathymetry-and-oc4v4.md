# Stumpf satellite-derived bathymetry and SeaWiFS OC4v4 chlorophyll

## Stumpf log-band-ratio bathymetry

The empirical ratio method uses two water-leaving reflectance bands:

    q = ln(n Rrs(blue)) / ln(n Rrs(green))
    depth = m1 q + m0

The scale factor n (commonly 1000) keeps logarithm arguments positive for
typical reflectance magnitudes. The slope and intercept must be calibrated
against local known depths; no universal coefficients are assumed. Positive
reflectance, suitable shallow-water conditions, atmospheric correction and
vertical datum consistency are prerequisites. The implementation fits a
simple least-squares calibration and applies it to paired bands.

## SeaWiFS OC4v4 chlorophyll-a

OC4v4 uses the maximum blue-to-green reflectance ratio:

    X = log10(max(Rrs443, Rrs490, Rrs510) / Rrs555)

    log10(Chl-a) = 0.366 - 3.067 X + 1.930 X^2 + 0.649 X^3 - 1.532 X^4

The output is chlorophyll-a in mg m-3. These coefficients are for SeaWiFS
OC4v4 specifically. Do not silently reuse them for MODIS, OLCI or other
sensor/version combinations. Atmospheric correction, cloud masking and
quality control are upstream responsibilities.

The reference package contains a Stumpf calibration/application workflow,
OC4v4 computation and independent numerical tests.

## References

- Stumpf, R. P., Holderied, K., & Sinclair, M. (2003). Determination of water
  depth with high-resolution satellite imagery over variable bottom types.
  *Limnology and Oceanography*, 48(1, part 2), 547–556.
  https://doi.org/10.4319/lo.2003.48.1_part_2.0547
- O'Reilly, J. E., et al. (2000). Ocean color chlorophyll a algorithms for
  SeaWiFS, OC2, and OC4: Version 4. *NASA Technical Memorandum 2000-206892*.
