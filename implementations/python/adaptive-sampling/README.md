# Spatial active-sampling and UCB1 baselines

Three dependency-free building blocks:

- **Greedy spatial active sampling:** selects candidates using normalized predictive uncertainty plus distance from the already-selected set. It supports a minimum-distance exclusion and returns fewer than the requested batch size when no remaining candidate satisfies that constraint.
- **UCB1:** chooses a survey/annotation arm using empirical mean reward plus an exploration bonus; untried arms are selected first.\n- **Finite-candidate Gaussian-process optimization:** exact dense RBF-kernel regression with Cholesky solves and either upper-confidence-bound (UCB) or expected-improvement (EI) acquisition. Duplicate observations are stabilized with numerical jitter.

The GP selector is a small dense Bayesian-optimization baseline over a finite candidate set; it is not scalable to large observation sets and does not optimize over a continuous domain. The separate spatial selector remains a transparent uncertainty/diversity heuristic. Hyperparameter selection and model diagnostics remain the user's responsibility. Coordinates must be in a meaningful projected metric or otherwise appropriate distance space; raw longitude/latitude Euclidean distance is not generally valid. UCB1 assumes a stationary reward model for its classical interpretation; nonstationary survey costs, delayed rewards and contextual covariates require other policies.

Run from this directory:

```bash
python -m pytest -q
```
