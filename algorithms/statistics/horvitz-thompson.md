# Horvitz-Thompson estimator

For sample values y_i with first-order inclusion probabilities pi_i, the
Horvitz-Thompson estimator of the population total is:

    Y_hat = sum_i y_i / pi_i

When second-order inclusion probabilities pi_ij are available, a design-
unbiased variance estimator is:

    Var_hat(Y_hat) = sum_i sum_j (pi_ij - pi_i*pi_j)
                     (y_i/pi_i) (y_j/pi_j)

The implementation requires a symmetric pairwise inclusion matrix whose
diagonal equals the first-order probabilities. Positive pairwise
probabilities are required to estimate the variance from the observed
sample. A population mean is returned when population size is supplied.
This estimator is design-based and distinct from Fay-Herriot model-based
shrinkage and model-assisted estimators.


## Source
- Horvitz, D. G., & Thompson, D. J. (1952). A generalization of sampling without replacement from a finite universe. *Journal of the American Statistical Association*, 47(260), 663–685. https://doi.org/10.1080/01621459.1952.10483446.
