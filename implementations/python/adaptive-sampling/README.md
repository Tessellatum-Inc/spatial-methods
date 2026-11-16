# Adaptive and Bayesian spatial sampling algorithms

This package includes:
- network-based adaptive cluster sampling expansion from an initial sample;
- Gaussian-process upper-confidence-bound (GP-UCB) selection over candidate spatial survey sites.

The GP-UCB baseline assumes an isotropic stationary RBF kernel, known hyperparameters, a constant prior mean and independent Gaussian observation noise. It selects from a supplied finite candidate set. It is not a spatially nonstationary or constrained Bayesian optimiser; hyperparameter fitting, anisotropy, barriers, costs, batch selection and design-based survey inference remain outside scope.

The adaptive cluster sampler returns the realised sample set, not a population estimator. Valid inclusion probabilities and estimators depend on the initial probability-sampling design and adaptive network structure.

Run python -m pip install -r requirements.txt and python -m pytest -q.


The package also includes generic UCB1 for independent stationary reward arms. This is a bandit baseline for comparing survey-site reward strategies; it does not model spatial correlation between candidate locations.


The package also provides a one-round spatially constrained uncertainty sampler for map validation. It greedily ranks candidate sites by uncertainty (or uncertainty per unit cost) while enforcing a minimum distance between selected sites. This is a batch selection heuristic, not a complete active-learning loop or a design-based accuracy estimator.


Learning labs:
- [Adaptive cluster sampling](../../../notebooks/adaptive-cluster-sampling-lab.ipynb)
- [GP-UCB spatial survey selection](../../../notebooks/gp-ucb-spatial-survey-lab.ipynb)
- [UCB1 survey bandit](../../../notebooks/ucb1-survey-bandit-lab.ipynb)
- [Spatial active learning](../../../notebooks/spatial-active-learning-lab.ipynb)

## Explicit sampling and acquisition baselines

The `sampling.py` module exposes three additional teaching baselines: `select_spatial_batch` greedily combines normalized uncertainty with distance-based diversity and an optional minimum separation; `ucb1_arm` selects among stationary independent reward arms using the UCB1 exploration bonus; and `gp_select_next` performs dense exact-GP candidate selection with an RBF kernel using either UCB or expected improvement. The GP implementation is intentionally small and cubic in the number of observations; it assumes known kernel hyperparameters and independent Gaussian noise. These are selection heuristics, not substitutes for design-based survey estimators or a complete active-learning evaluation protocol. The companion `test_sampling.py` covers spatial separation, UCB1, GP posterior behaviour, expected improvement and duplicate-observation jitter.
