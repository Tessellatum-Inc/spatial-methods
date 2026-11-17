# Numeric map classification

Pure-Python reference implementations of equal-interval, linearly interpolated
quantile and exact Fisher-Jenks natural-break classification, plus deterministic
assignment of observations to the resulting intervals.

Run `python -m pip install -r requirements.txt && python -m pytest -q`.

Jenks minimizes one-dimensional within-class sum of squared deviations by
dynamic programming and costs O(k n²) time and memory O(k n). The package
expects finite numeric values and at most as many classes as distinct values.
Quantile breaks may repeat when the sample has ties. Class boundaries are
inclusive on the lower side of each class interval: an interior boundary value
belongs to the lower class. This is a numeric classification baseline, not a
cartographic color-scale or bivariate-map design system.
