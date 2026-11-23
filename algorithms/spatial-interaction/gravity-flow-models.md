# Constrained gravity and entropy-maximising spatial interaction

Spatial-interaction models estimate flows between origin zones i and destination zones j. Let O_i be origin production, D_j destination attraction and f(c_ij) a non-negative impedance function of generalized travel cost.

## Unconstrained model

[
T_{ij}=O_iD_jf(c_{ij})
]

Neither row nor column totals are enforced. This is a baseline interaction intensity, not a balanced trip table.

## Production-constrained model

[
T_{ij}=O_irac{D_jf(c_{ij})}{sum_kD_kf(c_{ik})}
]

Each origin's outflow is exactly O_i. Destination totals are predicted rather than fixed.

## Attraction-constrained model

[
T_{ij}=D_jrac{O_if(c_{ij})}{sum_kO_kf(c_{kj})}
]

Each destination's inflow is exactly D_j. Origin totals are predicted rather than fixed.

## Doubly constrained model

[
T_{ij}=A_iO_iB_jD_jf(c_{ij})
]

The balancing factors A_i and B_j are iteratively updated so that both row and column margins match. The implementation uses iterative proportional fitting (RAS) on the seed matrix O_i D_j f(c_ij). It preserves structural zeros and reports convergence, iteration count and normalized marginal errors. Origin and destination totals must agree; positive margins with no feasible support are rejected. Sparse support can make the constraints infeasible even when totals agree, in which case the routine may return a non-converged result with diagnostics.

## Wilson-style entropy-maximising variant

The implemented form uses exponential generalized-cost deterrence:

[
f(c_{ij})=exp(-eta c_{ij}),quad etageq0
]

and then applies the doubly constrained balancing procedure. This is a specified Wilson-style formulation, not a fitted estimate of beta. Cost units and beta units must be reciprocal; beta should be calibrated against observed flows before policy interpretation.

## Relation to PPML

The existing PPML gravity routine is a regression estimator for nonnegative observed flows and covariates. The methods here allocate aggregate margins across an OD matrix given an impedance surface. They solve different problems and should not be conflated. Negative-binomial gravity estimation and high-dimensional fixed effects are not included in this addition.

## Verification

Tests cover all four constraint forms, marginal balance, exponential cost deterrence, structural zeros, infeasible support, validation and explicit non-convergence reporting.

## References

- Wilson, A. G. (1970). *Entropy in Urban and Regional Modelling*. Pion.
- Wilson, A. G. (1971). A family of spatial interaction models, and associated developments. *Environment and Planning*, 3, 1–32.
- See also the [spatial interaction models primer](https://cran.ma.imperial.ac.uk/web/packages/simodels/vignettes/sims-first-principles.html) and the [Routledge edition of Wilson's book](https://www.routledge.com/Entropy-in-Urban-and-Regional-Modelling-Routledge-Revivals/Wilson/p/book/9780415696319).

See the [NumPy implementation and tests](../../implementations/python/regional-dynamics/README.md).
