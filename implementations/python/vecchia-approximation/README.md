# Vecchia nearest-neighbour Gaussian-process approximation

A NumPy reference for the Vecchia factorisation of a zero-mean Gaussian
process. Each ordered observation is modelled conditionally on a small set of
nearest preceding observations. The example uses an isotropic
squared-exponential covariance with an optional nugget.

## Output

The function returns the approximate log-likelihood, conditional means and
variances indexed in original observation order, and the ordering used.
Selecting all predecessors recovers the exact dense Gaussian likelihood
(up to numerical jitter).

## Run

Install with python -m pip install -r requirements.txt, then run
python -m pytest -q.

## Limits

This is a compact likelihood baseline, not a complete scalable GP framework.
It uses dense covariance construction and local dense solves, so memory and
some setup costs remain quadratic. It does not implement parameter
optimisation, prediction at new locations, nonstationary kernels, covariance
tapering, fixed-rank methods, lattice kriging, multi-resolution approximation
or a general nearest-neighbour GP software stack. Ordering and neighbour count
affect approximation quality; compare likelihood and prediction diagnostics
against exact GP calculations on manageable subsets.


## Local prediction at new locations

`vecchia_predict` conditions each prediction site on its nearest observed training locations and returns a conditional mean, predictive variance and selected neighbour indexes. With all training observations selected, the result matches dense Gaussian-process conditioning. Prediction sites are treated independently conditional on the training data; the routine does not return their joint posterior covariance or implement the complete hierarchical NNGP inference framework.
