# Marxan-style marine reserve selection baseline

Install and test with `python -m pip install -r requirements.txt && python -m pytest -q`.

The package selects planning zones against feature representation targets. The objective is acquisition cost plus a caller-weighted selected/unselected boundary length plus a penalty on squared representation shortfalls. A seeded single-zone simulated-annealing search returns the best solution encountered, with explicit coverage and unmet targets.

This is an educational Marxan-style heuristic, not a reproduction of Marxan's full feature penalty, zone status, separation, connectivity and planning-unit options. It is not Zonation's iterative ranking algorithm and does not guarantee a global optimum. Spatial inputs, target values, costs and boundary lengths must be prepared and validated by the analyst.
