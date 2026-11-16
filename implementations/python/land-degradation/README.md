# RESTREND land-degradation screening

Install and test with `python -m pip install -r requirements.txt && python -m pytest -q`.

`resttrend` fits a separate linear NDVI-on-precipitation relationship for each pixel, calculates residuals and estimates their linear temporal trend. It returns rainfall sensitivity, residual trend, R-squared, p-value, valid observation count and the residual cube. Missing pairs are omitted per pixel.

A negative residual trend can be consistent with declining vegetation productivity beyond the fitted rainfall response, but it is not proof of land degradation. Model form, precipitation quality, land-cover transitions, irrigation, fire, sensor harmonization and temporal sampling all matter. This baseline is not a full RESTREND study, NPP residual workflow or soil-salinity retrieval.
