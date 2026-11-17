# Classification accuracy assessment

Dependency-free reference functions for a reference-row/prediction-column
confusion matrix, overall accuracy, producer/user accuracy, Cohen's kappa,
quantity and allocation disagreement, and binary change-detection Figure of
Merit (FoM).

Run `python -m pip install -r requirements.txt && python -m pytest -q`.

This package does not implement design-based area-adjusted accuracy, fuzzy
kappa, confidence intervals, sampling variance, multi-date error propagation
or a full accuracy-assessment sampling design. Kappa is undefined (None) when
expected chance agreement is one; class-specific accuracy is None when its
denominator is zero. Quantity/allocation disagreement follows the stated
reference/prediction marginal convention.
