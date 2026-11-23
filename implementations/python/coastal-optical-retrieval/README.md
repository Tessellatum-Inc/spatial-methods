# Coastal optical retrieval baselines

This package implements two empirical optical algorithms with deliberately
narrow contracts.

## Stumpf log-band-ratio bathymetry

The predictor is

    q = ln(n Rrs_blue) / ln(n Rrs_green)
    depth = slope * q + intercept

The default n is 1000, but it is explicit and caller-configurable. Fit the
slope and intercept by ordinary least squares against paired in-situ depths,
then apply the fitted model to new reflectance pairs. Calibration is local:
coefficients are not transferable universal constants. The model assumes
positive water-leaving reflectances and does not correct water-column,
bottom-type, atmospheric, sun-glint, tide or water-level effects.

## SeaWiFS OC4v4 chlorophyll-a

The implementation uses

    X = log10(max(Rrs443, Rrs490, Rrs510) / Rrs555)
    log10(Chl-a) = 0.366 - 3.067 X + 1.930 X^2 + 0.649 X^3 - 1.532 X^4

and returns chlorophyll-a in mg m-3. These coefficients are specifically
SeaWiFS OC4v4, not a universal ocean-colour model. Other sensors and algorithm
versions require their own validated coefficient sets and band responses.
Atmospheric correction and quality masking are upstream responsibilities.

## Tests

    python -m pytest -q

Tests cover the formula, calibration recovery, coefficient use, monotonicity
in a bounded test case, and invalid inputs. These are numerical reference
tests, not validation against an independent in-situ dataset.
