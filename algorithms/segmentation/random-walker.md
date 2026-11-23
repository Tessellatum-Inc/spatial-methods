# Random-walker image segmentation

## Method

Represent each pixel as a graph node. Four-neighbour edges receive conductance w_ij = exp(-β ||I_i-I_j||²). The graph Laplacian is partitioned into unknown pixels U and fixed seed pixels S. For each class, solve L_UU x_U = -L_US y_S with seed values fixed to one for their class and zero for others. The resulting harmonic functions are normalized and interpreted as class probabilities.

## Assumptions

The input is a finite regular 2D grid, optionally with multiple feature channels. Seed labels are positive integers and zero denotes unknown. The implementation uses a sparse direct solver and four-neighbour connectivity.

## Limits

This is a small-grid teaching baseline. It does not implement GrabCut, seeded region growing, eight-neighbour graphs, physical pixel spacing, multiscale acceleration, large-scene iterative solvers or calibrated uncertainty.