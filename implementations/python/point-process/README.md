# Planar point-pattern summaries and areal cluster detection

Dependency-free functions for a bounded subset of spatial point-process analysis:

- Nearest-neighbour distances and empirical G function; Monte Carlo empty-space F function and combined J-function estimate.
- Cross-type G, rectangular translation-corrected cross-K, finite-difference cross pair correlation and Monte Carlo cross-J for two distinct marks.
- Homogeneous Poisson, stationary Thomas (Gaussian Neyman–Scott), stationary Matérn disc-cluster, grid-discretised log-Gaussian Cox and Strauss repulsive point-pattern simulation.
- Homogeneous Ripley's K with rectangular translation edge correction.
- Inhomogeneous K with externally supplied pointwise intensities and rectangular translation correction.
- Finite-difference pair-correlation estimates from K(r).
- Conditional multinomial Monte Carlo quadrat-count test for homogeneous complete spatial randomness (CSR).
- Circular Poisson spatial scan statistic for areal case counts with a population offset and conditional multinomial Monte Carlo p-value.
- Finite-grid elliptical Poisson scan over centroid-centred shapes and orientations, with global conditional Monte Carlo inference.
- Bounded exhaustive flexible Poisson scan over connected subsets of a supplied adjacency graph, with global conditional Monte Carlo inference (K <= 15).
- Tango's global distance-decay quadratic-form test with conditional multinomial Monte Carlo inference.
- Area-centred Besag–Newell cluster detection with exact conditional hypergeometric local tails and global Monte Carlo calibration.

## Run

~~~bash
python -m pip install -r requirements.txt
python -m pytest -q
~~~

## Point-process model simulators

The model simulators are intentionally separate from fitting and inference: [Poisson and Thomas process lesson](../../../algorithms/statistics/poisson-and-thomas-processes.md), [Matérn cluster process lesson](../../../algorithms/statistics/matern-cluster-process.md) and [log-Gaussian Cox process lesson](../../../algorithms/statistics/log-gaussian-cox-process.md). Thomas uses a finite Gaussian-tail buffer; Matérn uses an exact radius-sized buffer for its compact-support disc kernel; the LGCP is a small-grid piecewise-constant approximation with dense Cholesky.

## Strauss interaction process

The package includes a birth-death Metropolis–Hastings sampler for the finite-window Strauss model. Its density is proportional to βⁿγˢ, where s counts unordered pairs within the interaction radius. γ=1 is the Poisson limit; γ=0 is the hard-core limit. The finite MCMC run is approximate and depends on burn-in and chain length; it is not an exact sampler or fitted model. See the [canonical lesson](../../../algorithms/statistics/strauss-point-process.md) and walkthrough.

## Circular Poisson scan

The `spatial_scan.py` module implements a centroid-centred circular Poisson scan for areal case counts with population offsets. It enumerates candidate circles through tied centroid distances, applies a maximum population fraction and minimum case count, and reports the highest elevated-cluster log-likelihood ratio and relative risk. `monte_carlo_poisson_scan` conditions on the observed total cases and uses multinomial simulation with the plus-one p-value correction.

See the [canonical lesson](../../../algorithms/spatial-scan-statistic.md), [intern walkthrough](implementation-walkthrough.md), [test suite](test_spatial_scan.py) and [interactive lab](../../../notebooks/spatial-scan-statistic-lab.ipynb).

## Besag–Newell and Tango cluster tests

The same module implements an area-centred fixed-k Besag–Newell test with exact conditional hypergeometric local tails and global Monte Carlo calibration, plus Tango's global distance-decay quadratic-form statistic with conditional multinomial Monte Carlo inference. See the [Besag–Newell lesson](../../../algorithms/statistics/besag-newell.md) and [Tango lesson](../../../algorithms/statistics/tango-clustering-test.md). Both require projected centroids and population-at-risk data; the local Besag–Newell interface is area-centred, while Tango requires a prespecified distance scale.

## Inhomogeneous Poisson simulation

`simulate_inhomogeneous_poisson(intensity_grid, window, seed=...)` simulates a piecewise-constant intensity surface exactly under the supplied grid model. Each grid cell receives an independent Poisson event count with mean equal to its intensity times cell area; event locations are uniform within that cell. Grid values are in events per squared coordinate unit, rows increase from ymin, and the grid partitions the full rectangular window. This is not an intensity estimator or a continuous kernel-intensity simulator.

## Assumptions and limitations

Coordinates must be planar, in a consistent linear unit, and observed in a rectangular window. The homogeneous K estimator assumes stationarity/homogeneity and isotropy. The inhomogeneous estimator requires one strictly positive intensity estimate per observed point and assumes second-order intensity-reweighted stationarity; it does not fit an intensity surface or select its bandwidth. Pair correlation is obtained by numerical differentiation and is sensitive to radius spacing/noise. The G function uses observed nearest-neighbour distances; F uses seeded uniform Monte Carlo locations in the rectangular window; J=(1-G)/(1-F) is returned as NaN where F reaches one. The F/J estimators are teaching baselines without advanced boundary correction. The quadrat test conditions on the observed point count and uses equal-area cells under a uniform multinomial null; grid dimensions and origin are analyst choices, and the test is scale-dependent.

The scan is not a full SaTScan reproduction: it does not implement covariates, temporal scans, unrestricted arbitrary zones, secondary clusters, low-rate scans or polygon-boundary geometry. Ellipses are available through the separate finite-grid API described below. Coordinates for the scan must be projected planar centroids. Use a maintained point-process package for inferential analysis and complex observation windows.


## Network point-pattern distances and K

The companion `network_point_patterns.py` module handles events on a finite undirected weighted linear network. An event is represented by `(edge_index, offset_from_first_endpoint)`, and edge tuples are `(u, v, positive_length)`. It calculates shortest-path distances between events, considering direct travel along a shared edge and alternate routes through network nodes. The network K estimator counts ordered event pairs within each network-distance threshold and scales by total network length.

This is an uncorrected finite-network descriptive estimator. It does not correct for endpoint effects, network junction bias, varying network intensity or disconnected network components. See [network Ripley's K](../../../algorithms/statistics/network-ripley-k.md) and `test_network_point_patterns.py`.
