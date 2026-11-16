# Knox space-time interaction test

Install and test with python -m pip install -r requirements.txt && python -m pytest -q.

The Knox test counts unordered event pairs whose planar separation is at most the spatial threshold and whose absolute time separation is at most the temporal threshold. A Monte Carlo permutation test holds locations fixed and permutes event times. The one-sided p-value tests for excess close pairs and uses the plus-one correction.

The null requires exchangeability of event times over the fixed locations. It is not a causal test and does not correct for inhomogeneous intensity, population at risk, repeated events from the same source, spatial edge effects or threshold selection. Coordinates and times must use consistent units. The implementation is quadratic in event count and intended for small-to-medium event sets.
