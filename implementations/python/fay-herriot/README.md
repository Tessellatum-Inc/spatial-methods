# Fay-Herriot area-level small-area estimation

This package implements the normal-normal area-level model by restricted
maximum likelihood (REML). Direct area estimates are modelled as
y_i = x_i' beta + u_i + e_i, with u_i ~ N(0, A) and supplied sampling
variances D_i = Var(e_i).

The empirical BLUP combines the regression prediction with the direct
estimate using shrinkage factor A/(A + D_i). The package also returns a
plug-in prediction MSE approximation and standard error.

## Install and test

    python -m pip install -r requirements.txt
    python -m pytest -q

## Minimal example

    from fay_herriot import fay_herriot
    result = fay_herriot([10, 12, 8, 15, 9, 13], [0.5] * 6)
    print(result["predictions"])

## Scope and limitations

This is a teaching implementation of the area-level Fay-Herriot model, not
a unit-level model or a full small-area estimation suite. The MSE is a
plug-in approximation conditional on estimated A; it omits variance-
component estimation uncertainty. It assumes independent area random
effects and known positive sampling variances. It does not implement spatial
random effects, Horvitz-Thompson, model-assisted estimation, MRP or spatial
microsimulation.


## Horvitz-Thompson design-based estimator

The companion survey module provides a Horvitz-Thompson population total and
optional population mean when first- and second-order inclusion probabilities
are supplied. The pairwise inclusion matrix must be symmetric, have the
first-order probabilities on its diagonal, and contain positive values so
the design variance estimator is identifiable from the observed sample.

    from survey_estimators import horvitz_thompson
    result = horvitz_thompson(
        values=[10, 20],
        inclusion_probabilities=[0.5, 0.5],
        pairwise_inclusion=[[0.5, 1/6], [1/6, 0.5]],
        population_size=4,
    )

This is a design-based estimator; it is not a Fay-Herriot model or a
model-assisted estimator. The variance estimate can be negative for some
valid designs and samples; in that case the implementation reports the
signed variance and leaves the standard error undefined.
