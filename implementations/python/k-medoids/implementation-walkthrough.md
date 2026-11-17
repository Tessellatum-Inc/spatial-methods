# PAM k-medoids and CLARA walkthrough

1. Represent the observations with a symmetric, non-negative dissimilarity
   matrix whose diagonal is zero. Euclidean distances are one option, not a
   requirement.
2. BUILD chooses the first medoid by minimum total dissimilarity, then greedily
   adds the object that most reduces the current nearest-medoid cost.
3. SWAP examines each medoid/non-medoid exchange and applies the best strict
   improvement. It stops when no improving exchange remains or the iteration
   limit is reached.
4. Assign each observation to its nearest medoid. Ties follow medoid order.
5. CLARA draws repeated samples without replacement, runs PAM on each sample,
   maps medoids back to original row indices and scores the candidates against
   all observations.
6. Return the medoid indices, labels, objective value and convergence/sample
   metadata so callers can inspect the result rather than infer it from a plot.

This is a bounded reference implementation. It does not impose geographic
contiguity, balance, capacities or equal cluster sizes.
