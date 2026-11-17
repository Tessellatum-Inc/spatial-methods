# Classification and segmentation evaluation metrics

## Scope

This record covers count-based thematic classification measures and binary-mask overlap/boundary measures: overall accuracy, producer and user accuracy, Cohen's kappa, quantity and allocation disagreement, per-class F1, intersection-over-union (IoU), Dice, macro-F1, mean IoU, change Figure of Merit, and tolerance-aware binary boundary F1.

## Conventions

The confusion matrix uses reference classes as rows and predicted classes as columns. Producer accuracy is recall; user accuracy is precision. Per-class F1 and Dice coincide under the one-vs-rest formulation. Per-class IoU is TP/(TP+FP+FN). Undefined class denominators return None and are omitted from macro averages. Boundary F1 uses 4-neighbour foreground boundaries and Euclidean distance in pixel coordinates.

## Important limitations

These count-based metrics are not design-based area-adjusted estimates. The reference boundary metric is deliberately simple and has quadratic boundary-set matching cost. Detection mAP, rotated-box IoU, panoptic quality, probabilistic calibration, regression and forecast metrics, uncertainty intervals, and sampling-design variance are not implemented by this record.