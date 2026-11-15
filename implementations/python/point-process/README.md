# Planar point-pattern summaries and circular Poisson scan

Dependency-free functions for a bounded subset of spatial point-process analysis:

- Nearest-neighbour distances and empirical G function; Monte Carlo empty-space F function and combined J-function estimate.
- Cross-type G, rectangular translation-corrected cross-K, finite-difference cross pair correlation and Monte Carlo cross-J for two distinct marks.
- Homogeneous Poisson, stationary Thomas (Gaussian Neyman–Scott), stationary Matérn disc-cluster and grid-discretised log-Gaussian Cox point-pattern simulation.
- Homogeneous Ripley's K with rectangular translation edge correction.
- Inhomogeneous K with externally supplied pointwise intensities and rectangular translation correction.
- Finite-difference pair-correlation estimates from K(r).
- Conditional multinomial Monte Carlo quadrat-count test for homogeneous complete spatial randomness (CSR).
- Circular Poisson spatial scan statistic for areal case counts with a population offset and conditional multinomial Monte Carlo p-value.

## Run

~~~bash
python -m pip install -r requirements.txt
python -m pytest -q
~~~

## Circular Poisson scan

The `spatial_scan.py` module implements a centroid-centred circular Poisson scan for areal case counts with population offsets. It enumerates candidate circles through tied centroid distances, applies a maximum population fraction and minimum case count, and reports the highest elevated-cluster log-likelihood ratio and relative risk. `monte_carlo_poisson_scan` conditions on the observed total cases and uses multinomial simulation with the plus-one p-value correction.

See the [canonical lesson](../../../algorithms/spatial-scan-statistic.md), [intern walkthrough](implementation-walkthrough.md), [test suite](test_spatial_scan.py) and [interactive lab](../../../notebooks/spatial-scan-statistic-lab.ipynb).

## Assumptions and limitations

Coordinates must be planar, in a consistent linear unit, and observed in a rectangular window. The homogeneous K estimator assumes stationarity/homogeneity and isotropy. The inhomogeneous estimator requires one strictly positive intensity estimate per observed point and assumes second-order intensity-reweighted stationarity; it does not fit an intensity surface or select its bandwidth. Pair correlation is obtained by numerical differentiation and is sensitive to radius spacing/noise. The G function uses observed nearest-neighbour distances; F uses seeded uniform Monte Carlo locations in the rectangular window; J=(1-G)/(1-F) is returned as NaN where F reaches one. The F/J estimators are teaching baselines without advanced boundary correction. The quadrat test conditions on the observed point count and uses equal-area cells under a uniform multinomial null; grid dimensions and origin are analyst choices, and the test is scale-dependent.

The scan is not a full SaTScan reproduction: it does not implement covariates, temporal scans, elliptical or arbitrary zones, secondary clusters, low-rate scans or polygon-boundary geometry. Coordinates for the scan must be projected planar centroids. Use a maintained point-process package for inferential analysis and complex observation windows.
