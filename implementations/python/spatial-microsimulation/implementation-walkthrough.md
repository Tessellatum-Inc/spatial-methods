# Iterative proportional fitting walkthrough

1. Start with a nonnegative seed table whose cells encode initial joint
   weights or counts.
2. Scale each row to its target row total.
3. Scale each column to its target column total.
4. Repeat the two projections until the largest absolute marginal error
   is below the tolerance times the grand total, or the iteration limit
   is reached.
5. Structural zeros remain zero because multiplicative scaling cannot
   create support where the seed contains none.

The algorithm cannot meet a positive target margin if its corresponding
seed support is entirely zero. Even when every margin has support, the
combination of structural zeros can make the full set of margins
infeasible. Inspect the convergence flag and the resulting marginal error.
