# Verification record: directional terrain travel time

## Implemented

Tobler's signed-slope hiking speed, Naismith travel-time rule, Langmuir descent correction and multi-source Dijkstra accumulation over an elevation raster. Edge costs are directed and accumulated in seconds.

## Tests

Tests verify reference rates, uphill/downhill asymmetry, descent correction bands, raster connectivity, NoData barriers, multiple sources and input validation.

## Limits

The Langmuir rule is applied per raster edge and is resolution-sensitive. No trail condition, load, weather, fitness, turn penalty, backlink raster, path geometry or continuous Eikonal solver is included.
