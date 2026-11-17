# Classification and segmentation accuracy assessment

Dependency-free reference functions for a reference-row/prediction-column
confusion matrix; overall, producer and user accuracy; Cohen's kappa;
quantity and allocation disagreement; per-class F1, intersection-over-union
(IoU) and Dice; macro-F1 and mean IoU; binary change-detection Figure of Merit
(FoM); tolerance-aware binary boundary F1 for 2D masks; regression MAE, RMSE and weighted R-squared; and top-label expected calibration error (ECE) with equal-width bins and optional sample weights.

Run python -m pip install -r requirements.txt && python -m pytest -q.

The confusion-matrix metrics assume a fixed class label order and count-based
evaluation. Classes with no reference or predicted support have undefined
per-class F1/IoU (None) and are excluded from macro means. Dice and F1 are
equal for the one-vs-rest binary class formulation. Boundary F1 uses 4-neighbour
foreground boundaries and Euclidean pixel tolerance; the transparent reference
implementation is O(B_ref * B_pred).

Not implemented here: design-based area-adjusted accuracy, sampling variance,
confidence intervals, fuzzy kappa, detection mAP, rotated-box IoU, panoptic
quality, multi-date error propagation, probabilistic calibration metrics,
regression/forecast metrics (including CRPS, NSE and KGE), or full sampling
design. Do not interpret these pixel-count metrics as area-adjusted estimates
when the validation sample design requires area weighting.
\n\nRegression metrics use finite paired observations and optional non-negative sample weights. R-squared returns 1 for a perfect constant target and 0 for an imperfect constant target. ECE is top-label confidence calibration with equal-width bins; it is sensitive to bin count and sample size and is not a classwise or adaptive calibration estimator.\n
Retrieval/evaluation helpers include macro query-level recall@k (queries without relevant items are skipped; all-empty relevance returns None) and arithmetic-normalised mutual information (NMI) for arbitrary cluster labels. These are descriptive metrics; geographic stratification and benchmark-specific relevance protocols remain caller responsibilities.
