# Classification and segmentation accuracy assessment

Dependency-free reference functions for a reference-row/prediction-column
confusion matrix; overall, producer and user accuracy; Cohen's kappa;
quantity and allocation disagreement; per-class F1, intersection-over-union
(IoU) and Dice; macro-F1 and mean IoU; binary change-detection Figure of Merit
(FoM); and tolerance-aware binary boundary F1 for 2D masks.

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
