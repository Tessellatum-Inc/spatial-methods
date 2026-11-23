# Floating catchment area accessibility

Reference implementations of two-step floating catchment area (2SFCA) and enhanced 2SFCA (E2SFCA) using a caller-supplied demand-to-supply distance matrix.

## Model

For supply location j, the first step computes its supply-to-demand ratio over demand locations i inside the catchment:

\(R_j=S_j / \sum_i P_i w_{ij}\).

The second step sums accessible facility ratios for each demand location:

\(A_i=\sum_j R_j w_{ij}\).

2SFCA uses a uniform binary weight inside a closed catchment radius. E2SFCA accepts explicit increasing distance-zone upper bounds and non-negative zone weights.

## Important assumptions

- Distance units and catchment thresholds must be compatible.
- Demand and supply quantities must be measured in compatible service units.
- Zero denominators produce a zero ratio, not infinity.
- Distances exactly on a zone upper bound are included in that zone.
- This is a deterministic accessibility measure, not a causal estimate or an uncertainty interval.
- Network travel times, competition choice models, capacity constraints, multimodal transfers and equity inference must be modelled separately.

## Reproduce

~~~bash
python -m pip install -r requirements.txt
python -m pytest -q
~~~

## Reusable distance-decay kernels

The package also exposes Gaussian, regularised power-law and Epanechnikov compact-support weights. They return dimensionless weights in [0, 1] and can be supplied to downstream catchment or accessibility models. These functions do not select a scientifically appropriate bandwidth or calibrate a behavioural impedance function.
