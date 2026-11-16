# Climate analogs and velocity

A compact NumPy package for two climate-space calculations from source section 16.

## Install and test

```bash
python -m pip install -r requirements.txt
python -m pytest -q
```

## Mahalanobis climate analogs

`mahalanobis_climate_analogs` ranks historical multivariate climate samples for each future climate vector. By default it estimates a sample covariance from the historical reference matrix; a caller-supplied covariance is also supported. A scale-relative ridge makes singular or collinear variable sets numerically usable. It returns stable nearest-analog indices and Mahalanobis distances.

The method uses one global covariance model. It does not construct a local analog surface, estimate novelty thresholds, account for spatial dependence, select climate variables, or model species dispersal and refugia. A high distance indicates dissimilarity under the chosen variables and covariance, not a universal novelty probability.

## Climate velocity

`climate_velocity` computes isocline displacement from temporal climate change and the spatial gradient. The vector solves `grad(T) dot v + dT/dt = 0`; the speed is absolute temporal change divided by gradient magnitude. Results use distance/time units implied by the gradient and temporal trend. Flat gradients return infinite speed and undefined direction.

The caller supplies derivatives; the package does not estimate them from climate rasters or handle coastlines, barriers, topography, climate-model ensembles, uncertainty or refugia optimisation.

See `algorithms/remote-sensing/climate-analogs-velocity.md`.
