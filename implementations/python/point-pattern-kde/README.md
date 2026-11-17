# Planar Gaussian kernel density estimation for point patterns

This package provides fixed-bandwidth and sample-point adaptive Gaussian KDE,
plus leave-one-out likelihood bandwidth selection for modest planar samples.

## Run
~~~bash
python -m pip install -r requirements.txt
python -m pytest -q
~~~

## Fixed KDE
~~~python
from point_pattern_kde import gaussian_kde
density, xs, ys = gaussian_kde(
    [(2, 3), (2.2, 3.1), (7, 8)], bounds=(0, 10, 0, 10),
    grid_shape=(100, 100), bandwidth=0.8,
)
~~~

## Adaptive KDE and bandwidth selection
~~~python
from point_pattern_kde import adaptive_gaussian_kde, select_bandwidth_loo, silverman_bandwidth
surface, xs, ys, local_h = adaptive_gaussian_kde(
    points, bounds=(0, 10, 0, 10), bandwidth=0.8,
)
rule_of_thumb_h = silverman_bandwidth(points)\nbest_h, candidate_scores = select_bandwidth_loo(points, [0.3, 0.5, 0.8, 1.2])
~~~

Adaptive KDE estimates a leave-one-out pilot density at each event and applies
Abramson's square-root rule h_i = h * (g / f_i)^alpha. Dense pilot regions
receive smaller kernels; sparse regions receive larger kernels. Factors are
clipped by default to [0.25, 4]. Returned local bandwidths follow input order.
With one event, or alpha=0, every event uses the global bandwidth.

Silverman's isotropic bivariate normal-reference rule uses the pooled RMS\nsample standard deviation s and Kish effective sample size n_eff:\n\n    h = s * n_eff**(-1/6)\n\nIt is a reproducible starting value, not a guarantee of optimal smoothing.\nLOO selection predicts each event from all other events and maximises weighted
mean log predictive density over the supplied candidates. It evaluates the
candidate grid as given; it does not run a continuous optimiser.

Coordinates must be planar and use consistent linear units. Bounds are
(xmin, xmax, ymin, ymax), grid shape is (rows, columns), and all events must
lie inside the bounds. Optional weights are finite and non-negative. Output
is intensity per square map unit, not counts per cell. No edge correction is
applied. Fixed KDE costs O(nm), adaptive KDE O(n^2 + nm), and LOO selection
O(n^2 c) for c candidates; these are transparent reference methods, not
large-data indexed estimators.
