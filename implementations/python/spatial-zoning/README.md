# Spatially constrained zoning and scale effects

Install and test with `python -m pip install -r requirements.txt && python -m pytest -q`.

`spatially_constrained_ward` starts with one zone per unit and repeatedly merges only adjacent zones, choosing the pair with the smallest Ward increase in within-zone sum of squares. It returns unit labels, zone sizes and the cumulative within-zone SSE. `zoning_scale_effect` evaluates the result over requested zone counts.

The graph must be connected enough to reach the requested number of zones. The method does not implement AMOEBA, simulated annealing, regional boundary constraints, minimum population thresholds, attribute standardization, or full MAUP inference. Results depend on the input attributes, contiguity definition and scale.
