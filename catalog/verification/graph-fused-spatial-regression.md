# Verification record: graph-fused spatial regression

## Identity and scope
- Implementation: implementations/python/spatial-regression/graph_fused_lasso.py
- Classification: original ADMM solver for location-specific linear coefficients with elementwise sparsity and graph total-variation penalties.

## Bibliographic checks
- Tibshirani et al. (2005), Sparsity and smoothness via the fused lasso, JRSS B 67(1), 91–108, DOI 10.1111/j.1467-9868.2005.00490.x. Supports the fused-lasso sparsity/smoothness penalty family.
- Kim et al. (2009), l1 trend filtering, SIAM Review 51(2), 339–360, DOI 10.1137/070690274. Related total-variation penalization context; not claimed as the exact spatial model implemented.

## Technical checks
- Each observation is assigned to one location and shares a common predictor dimension.
- Graph differences are formed from an incidence matrix; the L1 norm is invariant to edge orientation.
- ADMM uses soft thresholding for coefficient sparsity and graph differences.
- Reports primal/dual residual histories and convergence status.
- Dense direct linear solve; no scalability guarantee.
- This is not geographically weighted LASSO, spatial lag/error regression, CAR/BYM, or a full spatially varying coefficient inference model.

## Reproduction and rights
- Original code and tests; no source text, figures or code copied.
- Tests cover convergence on a smooth coefficient chain, sparsity shrinkage, no-edge/disconnected graphs and invalid inputs.
- Full repository pytest and CI have not been run in this authoring session.
