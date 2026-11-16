# Monte Carlo uncertainty propagation and Sobol sensitivity

Install and test with python -m pip install -r requirements.txt && python -m pytest -q.

monte_carlo_propagation samples independent uniform inputs over declared bounds and reports output mean, sample standard deviation and requested quantiles. Set return_samples=True to retain inputs and outputs.

sobol_sensitivity estimates first-order and total-order variance-based indices with the Saltelli pick-freeze design. It currently accepts scalar-valued vectorized models and independent uniform inputs.

Dependent inputs, arbitrary probability distributions, spatially correlated errors, Latin-hypercube sampling, polynomial chaos and bootstrap confidence intervals are not implemented. Increase sample count and compare estimates to assess convergence.
