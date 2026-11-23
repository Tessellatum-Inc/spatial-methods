# Verification dossier: classification and segmentation metrics

## Implemented scope

Reference-row/prediction-column confusion matrix; overall, producer and user accuracy; Cohen's kappa; quantity/allocation disagreement; class F1, IoU and Dice; macro-F1 and mean IoU; binary change Figure of Merit; and tolerance-aware binary boundary F1.

## Independent test coverage

Tests cover label ordering and validation, confusion-matrix orientation, known accuracy and kappa values, degenerate class margins, disagreement decomposition, hand-calculated F1/IoU/Dice, macro averaging with undefined classes, exact and shifted mask boundaries, tolerance matching, empty masks and invalid inputs.

## Exclusions

Area-adjusted sampling estimators, uncertainty intervals, fuzzy kappa, detection mAP, rotated boxes, panoptic quality, regression/forecast scores and probabilistic calibration remain outside the implementation. The source entry remains Partial.