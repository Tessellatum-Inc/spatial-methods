# Staypoints, home/work inference and activity spaces

## Staypoint extraction

Given time-ordered fixes (p_i) and timestamps (t_i), a candidate dwell episode begins at (i) and continues while each subsequent fix remains within radius (r) of the first fix. It is retained when elapsed time reaches the minimum dwell duration. The representative location is the arithmetic centroid of its fixes.

## Candidate home and work

Staypoints are assigned to caller-specified night and day windows after applying a fixed UTC offset. DBSCAN clusters their centroids. The cluster with greatest accumulated dwell time is reported as a candidate home or work location using a dwell-weighted centroid. It is a ranking heuristic, not a validated inference model.

## Activity-space metrics

Radius of gyration is the root mean squared distance of fixes from their centroid. Convex-hull area summarizes the planar envelope of observed locations; it is zero for fewer than three non-collinear unique points.

## Limitations and verification

Sampling gaps, GPS noise, irregular schedules, seasonality, multiple residences and privacy constraints matter. The implementation does not extract co-location/contact networks, infer social ties, correct location error or validate roles longitudinally. Tests use synthetic dwell episodes, separated day/night clusters and a direct triangle-area oracle.

See the [implementation package](../../implementations/python/mobility-inference/README.md).
