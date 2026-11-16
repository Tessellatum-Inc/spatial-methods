# Two-market food price transmission

Install and test with `python -m pip install -r requirements.txt && python -m pytest -q`.

The two-stage model first estimates a long-run linear relation between source- and target-market prices. It then fits a short-run error-correction equation using lagged long-run disequilibrium and the source-market price change. The adjustment coefficient is expected to be negative when the target market corrects deviations from equilibrium.

This is a pairwise linear econometric baseline. It does not implement multi-market spatial equilibrium, asymmetric threshold adjustment, structural breaks, cointegration pretesting, transport costs, market networks, IPC/FEWS NET food-security classification or livelihood-zone delineation. Price series should be deflated, aligned in frequency and assessed for stationarity and structural breaks before substantive interpretation.
