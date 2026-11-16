# Classical remote-sensing classification

Two interpretable baselines for finite multispectral feature matrices:

- Gaussian maximum-likelihood classification with class-specific covariance
  matrices, log-priors and ridge stabilization.
- Lloyd k-means clustering with k-means++ initialization, multiple restarts,
  deterministic random-state control and empty-cluster reseeding.
- ISODATA clustering with minimum-size deletion, spread-based splitting and
  nearest-centroid merging under explicit cluster-count limits.

Samples have shape (n_samples, n_features); each row is a pixel or object
feature vector. Inputs are numeric and finite. The Gaussian classifier learns
from supplied labels; k-means is unsupervised and returns cluster IDs without
semantic class meaning.

## Run

```bash
python -m pip install -r requirements.txt
python -m pytest -q
```

## Scope and limitations

Gaussian maximum likelihood assumes class-conditional multivariate Gaussian
features and independent training observations. It is sensitive to training
sample quality, class imbalance, feature scaling and covariance estimation.
Priors can be supplied explicitly. Ridge regularization stabilizes covariance
matrices but does not compensate for unrepresentative training samples.

K-means minimizes within-cluster squared Euclidean distance. It assumes a
chosen cluster count, favors compact approximately spherical groups, and is
sensitive to feature scaling and initialization. It is not ISODATA: automatic
cluster splitting/merging and class-count adaptation are not implemented.
Neither method performs image segmentation, spatial regularization,
cross-validation, probability calibration or accuracy assessment.
