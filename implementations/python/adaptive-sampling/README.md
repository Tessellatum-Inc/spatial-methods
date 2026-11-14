# Spatial active-sampling and UCB1 baselines

Two dependency-free building blocks:

- **Greedy spatial active sampling:** selects candidates using normalized predictive uncertainty plus distance from the already-selected set. It supports a minimum-distance exclusion and returns fewer than the requested batch size when no remaining candidate satisfies that constraint.
- **UCB1:** chooses a survey/annotation arm using empirical mean reward plus an exploration bonus; untried arms are selected first.

These are transparent heuristics, not a complete Bayesian-optimization system. The spatial selector does not fit a Gaussian process, model observation noise, optimize expected improvement, or guarantee global optimality. Coordinates must be in a meaningful projected metric or otherwise appropriate distance space; raw longitude/latitude Euclidean distance is not generally valid. UCB1 assumes a stationary reward model for its classical interpretation; nonstationary survey costs, delayed rewards and contextual covariates require other policies.

Run from this directory:

```bash
python -m pytest -q
```
