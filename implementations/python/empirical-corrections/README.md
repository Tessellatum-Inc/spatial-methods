# Empirical optical and terrain corrections

This package provides three scoped reference methods: percentile-based dark-object subtraction, per-band C-correction from a fitted reflectance–illumination relation, and Minnaert correction with caller-supplied exponent.

Inputs must be co-registered. Terrain methods expect illumination cosine arrays in [0, 1]. Invalid or unilluminated cells are returned as NaN. Dark-object subtraction is an empirical haze correction, not 6S/MODTRAN radiative transfer. C-correction assumes a linear reflectance-illumination relation; Minnaert k is supplied rather than silently estimated.

Install NumPy and pytest, then run pytest -q.
