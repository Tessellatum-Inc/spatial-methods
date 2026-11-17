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


## Local prediction

The companion `vecchia_predict` function applies the same local Gaussian conditioning to new prediction sites. For each prediction location it selects the nearest observed training locations and evaluates the conditional Gaussian mean and variance. Selecting all training sites reproduces the exact dense GP conditional predictor (up to numerical jitter). Prediction sites are handled independently conditional on the training data, so this is not a joint predictive covariance construction or full Bayesian NNGP model.
