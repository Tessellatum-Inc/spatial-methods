# Graph-fused spatially varying coefficient regression

## Model

Suppose observation j has response y_j, predictor vector x_j and spatial-unit label s_j. Each unit has its own coefficient vector beta_s. The implementation minimizes

1/2 sum_j (y_j - x_j^T beta_{s_j})^2
+ lambda_1 ||B||_1
+ lambda_f ||D B||_1,

where B stacks the unit-specific coefficient vectors and D is an oriented incidence matrix for a supplied undirected adjacency graph. The first penalty encourages sparse coefficients; the graph total-variation penalty encourages neighboring units to have similar coefficients while allowing discontinuities.

## Implemented solver

The reference implementation uses ADMM. It splits B and DB into thresholded auxiliary variables, solves a dense linear system for the coefficient update, applies elementwise soft-thresholding, and records primal/dual residuals and tolerances. The graph orientation does not affect the L1 total-variation objective.

Each observation contributes to one local design block. A location with no observations is still represented and can be informed by graph coupling, although its estimate may be weakly identified. Disconnected graph components are not fused together.

## Interpretation and limitations

This is graph-fused LASSO with location-specific coefficients. It is not geographically weighted regression, geographically weighted LASSO, spatial error/lag regression, a CAR/BYM model, or a general spatially varying coefficient model with kernel weighting. The user supplies the graph; topology and edge weights are not learned. The current objective uses an unweighted L1 penalty on every coefficient, including any intercept column supplied by the caller.

The solver uses dense matrices and a dense direct solve on every ADMM iteration. It is intended for small/medium teaching problems, not large networks. ADMM convergence is checked using primal and dual residual tolerances; non-convergence at max_iter is reported rather than hidden. Penalty selection, uncertainty quantification, robust losses, weighted edges and inferential calibration are not included.

## Learning workflow

1. Construct an explicit location adjacency graph and document how it was derived.
2. Build a common predictor design matrix and a location index for each observation.
3. Fit several lambda_1 and lambda_f combinations; inspect sparsity and neighboring coefficient differences.
4. Compare with a pooled regression (lambda_f large) and independent local regressions (lambda_f zero).
5. Tune penalties with spatially structured validation rather than random row splits when spatial leakage is a concern.

## References

- Tibshirani, R., Saunders, M., Rosset, S., Zhu, J., & Knight, K. (2005). Sparsity and smoothness via the fused lasso. Journal of the Royal Statistical Society: Series B, 67(1), 91–108. DOI: 10.1111/j.1467-9868.2005.00490.x.
- Kim, S., Koh, K., Boyd, S., & Gorinevsky, D. (2009). l1 trend filtering. SIAM Review, 51(2), 339–360. DOI: 10.1137/070690274.

The implementation is original and does not reproduce source code or figures.
