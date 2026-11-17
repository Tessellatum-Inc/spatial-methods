# Drought and vegetation-condition indicators

Drought monitoring combines meteorological anomalies, vegetation response and thermal stress. The indicators below are related but are not interchangeable: each uses a different reference distribution and answers a different question.

## Standardized Precipitation Index (SPI)

For an accumulation period, fit a probability distribution to precipitation totals and transform the fitted cumulative probability to a standard-normal score. The repository's teaching package fits a gamma distribution to positive precipitation and accounts for the probability mass at zero. SPI is scale-dependent: 1-, 3-, 6- and 12-month accumulation periods describe different persistence windows.

The package uses a single-population calibration. For strongly seasonal rainfall, fit equivalent calendar months or seasons separately. Report the calibration period, missing-data policy and accumulation scale.

## Vegetation and thermal condition

For a current vegetation index (V), historical minimum (V_{min}) and maximum (V_{max}), the vegetation condition index is

\[
VCI=100\frac{V-V_{min}}{V_{max}-V_{min}}.
\]

For land-surface temperature (T), historical minimum (T_{min}) and maximum (T_{max}), the thermal condition index reverses the direction so that hotter-than-normal conditions indicate stress:

\[
TCI=100\frac{T_{max}-T}{T_{max}-T_{min}}.
\]

A common vegetation health index combines them:

\[
VHI=\alpha VCI+(1-\alpha)TCI,
\]

where the weighting parameter must be stated and justified. The [drought-indices package](../../implementations/python/drought-indices/README.md) implements VCI, TCI, VHI and SPI. Constant historical ranges are undefined and represented as NaN rather than assigned an artificial score.

## Distinct methods that remain open

- **SPEI** standardizes climatic water balance (precipitation minus potential evapotranspiration); it is not just SPI with another label.
- **PDSI** is a recursive water-balance model with its own calibration and persistence assumptions.
- **Growing degree days** accumulate temperature above a crop- or species-specific base threshold.
- Crop-stress detection requires sensor, phenology, soil-water and field-validation context beyond the index formula.

## Interpretation and validation

These indices are indicators, not deterministic forecasts or insurance triggers. Sensor consistency, compositing, phenological phase, spatial support, calibration period, local climate and missing observations affect interpretation. Compare index anomalies with independent impacts or field observations and report uncertainty where possible.

## Tests and scope

The linked implementation includes tests for VCI/TCI/VHI bounds and degenerate ranges, gamma SPI with zero-rainfall probability, time-axis handling and missing values, plus threshold-run event extraction. It does not implement SPEI, PDSI or growing degree days in this package.
