# Drought condition indicators

Implements NDVI vegetation condition index (VCI), land-surface-temperature condition index (TCI), vegetation health index (VHI), gamma standardized precipitation index (SPI), and daily mean-method growing degree days (GDD) with a mixed zero-rainfall probability. VCI/TCI are clipped to [0,100]; constant historical ranges return NaN. SPI fits independently along a caller-selected time axis and preserves missing values. This is a single-population calibration: for strongly seasonal rainfall, group equivalent calendar months/seasons before fitting. These are indicators, not forecasts or insurance triggers; calibration period, sensor consistency, phenology and local validation remain essential.


The companion `run_theory.py` module extracts threshold-run events from one-dimensional indices such as SPI, reporting duration, exceedance days and cumulative/peak/mean severity. Optional short gaps can be bridged; missing values always break runs.


The `growing_degree_days` function returns daily mean-method increments above a caller-supplied base temperature, with an optional upper cap. Sum the daily values over the declared crop-development period; the base/cap temperatures are crop- and region-specific and are not inferred by the package.
