# Weighted head-banging spatial smoothing

Head-banging is a robust median-based spatial smoother designed to suppress isolated spikes while retaining broader edges and regional patterns.

For target location i, select its k nearest neighbours. Among all neighbour pairs (j,l), retain pairs for which the angle at i is within phi degrees of 180 degrees. These nearly collinear triples define a local axis through the target. Keep up to J triples, ordered by closeness to 180 degrees.

For each retained triple, identify the lower and higher endpoint values. The low screen L_i is the weighted median of the lower endpoint values; the high screen H_i is the weighted median of the higher endpoint values. The weights are those attached to the selected endpoints.

The target is updated by the weighted median

\[
\tilde y_i=\operatorname{wmed}(L_i,y_i,H_i;W_{L_i},Jw_i,W_{H_i}),
\]

where W_L and W_H are the sums of the weights of selected low and high endpoints, J is the number of retained triples and w_i is the target's weight. This leaves a target unchanged when its weighted evidence dominates, but moves it to a screen when endpoint evidence dominates. With equal weights it reduces to the ordinary median of the low screen, current value and high screen.

Repeat across all locations until convergence or an iteration cap. This implementation uses synchronous updates; all new values in an iteration are computed from the previous iteration's values.

## Parameters and interpretation

The NCI Head-Bang software describes a default neighbourhood size of 30, angular tolerance of 45 degrees, a triple cap around two-thirds of the neighbourhood size and 10 iterations. These are starting points, not universal optimal values. The smoother is robust to isolated spikes but can remove genuine local extremes and introduces bias. Weight definition, neighbourhood size and triple selection materially affect results.

## Scope

The implementation uses Euclidean k-nearest neighbours in a projected plane. It leaves locations with no qualifying triples unchanged and does not implement the full software's corner-point rules, automatic parameter selection, age adjustment, risk estimation or uncertainty quantification. It is a descriptive smoother, not an empirical-Bayes or hierarchical model.

## References

- Hansen, K. M. (1991). “Head-banging: Robust smoothing in the plane.” *IEEE Transactions on Geoscience and Remote Sensing*, 29(3), 369–378.
- Mungiole, M., Pickle, L. W. and Simonson, K. H. (1999). “Application of a weighted head-banging algorithm to mortality data maps.” *Statistics in Medicine*, 18(23), 3201–3209. DOI [10.1002/(SICI)1097-0258(19991215)18:23<3201::AID-SIM310>3.0.CO;2-U](https://doi.org/10.1002/(SICI)1097-0258(19991215)18:23%3CAID-SIM310%3E3.0.CO;2-U).
