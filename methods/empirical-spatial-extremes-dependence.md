# Empirical F-madogram and pairwise extremal coefficients

For block maxima observed at spatial sites i and j, the F-madogram summarizes dependence between the two marginal distributions after probability-integral transformation:

    nu_F(i,j) = 1/2 E[ |F_i(X_i) - F_j(X_j)| ]

For a bivariate max-stable distribution, the pairwise extremal coefficient is related to the F-madogram by

    theta(i,j) = (1 + 2 nu_F(i,j)) / (1 - 2 nu_F(i,j))

The theoretical max-stable range is 1 ≤ theta ≤ 2: one denotes complete dependence and two denotes independence.

## Empirical estimator

The reference implementation estimates each marginal CDF using average ranks among pairwise-complete block maxima, divided by n+1. It then averages half the absolute difference of the two rank-based probability values. Pairwise deletion is explicit and the number of usable blocks is returned for every pair. Tied values receive average ranks.

## Spatial interpretation

When projected site coordinates are supplied, the implementation also returns pairwise Euclidean distances. It does not fit a parametric dependence-versus-distance curve. Coordinates must use a common planar coordinate system and linear unit.

## Scope and caveats

This is a small-data descriptive estimator. Finite-sample estimates are not clipped to the theoretical max-stable range; values outside [1,2] are retained as a diagnostic signal. The method does not estimate uncertainty, fit marginal GEV/Gumbel distributions, fit Brown–Resnick or other max-stable processes, fit spatial copulas, or produce spatial predictions. A shared and defensible block definition is required across sites.
