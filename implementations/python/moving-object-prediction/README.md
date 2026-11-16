# Moving-object dead reckoning

A compact NumPy reference implementation for constant-velocity prediction, uncertainty ellipses and threshold-triggered position reporting.

## Install and test

```bash
python -m pip install -r requirements.txt
python -m pytest -q
```

## Prediction

`predict_constant_velocity` propagates a planar state `[x, y, vx, vy]` and its covariance through a constant-velocity transition. Optional white-acceleration process noise accounts for increasing uncertainty over time.

## Uncertainty and reporting

`position_confidence_ellipse` returns the major/minor radii and orientation of a Gaussian 2D position confidence ellipse. `dead_reckoning_update_decision` requests a report when predicted displacement from the last reported position, the major uncertainty radius or elapsed time reaches its configured threshold.

## Scope

This is a state-prediction and communication-policy kernel. It does not implement a Kalman measurement update, trajectory database, indexing, predictive range-query engine, map matching, road-network constraints, turn dynamics or multi-object association. The constant-velocity assumption can be poor under abrupt manoeuvres; tune process noise and thresholds to the tracked domain.

See `algorithms/moving-objects/dead-reckoning-prediction.md`.


## Predictive range filtering

`predictive_range_candidates` computes confidence-ellipse axis-aligned bounding boxes and returns objects whose boxes intersect a query rectangle. It is a conservative filter: false positives are possible and should be refined with an exact ellipse/region predicate when required.
