# Vecchia approximation for Gaussian processes

For an ordered Gaussian vector, the exact joint density factors into
conditionals:

    p(y) = product_i p(y_i | y_1, ..., y_(i-1)).

Vecchia approximations replace the full predecessor set with a small
neighbourhood N_i:

    p(y) approximately product_i p(y_i | y_Ni).

For a zero-mean Gaussian process with covariance K, the local conditional
mean and variance are

    mu_i = K_iN K_NN^(-1) y_N
    F_i  = K_ii - K_iN K_NN^(-1) K_Ni.

The reference implementation selects the nearest preceding locations and
uses a squared-exponential covariance. Selecting every predecessor recovers
the exact dense Gaussian likelihood up to numerical jitter.

See [the Python implementation](../../implementations/python/vecchia-approximation/README.md).
This is a likelihood baseline, not a production scalable GP framework;
ordering, neighbour count, kernel assumptions and numerical conditioning
matter.
