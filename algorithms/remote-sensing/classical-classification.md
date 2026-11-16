# Classical multispectral classification baselines

## Gaussian maximum-likelihood classification

For each class k, training observations estimate a mean vector and covariance
matrix. For feature vector x, the Gaussian log posterior score is

\[
s_k(x)=-\frac12\left[p\ln(2\pi)+\ln|\Sigma_k|
+(x-\mu_k)^T\Sigma_k^{-1}(x-\mu_k)\right]+\ln\pi_k,
\]

where p is the feature count and pi-k is the class prior. Assign the class
with the largest score. The implementation estimates class-specific
maximum-likelihood covariance matrices, adds a small ridge term to stabilize
them, and supports supplied class priors.

This model assumes class-conditional multivariate Gaussian features. Training
data quality, covariance estimation, class imbalance and feature scaling
matter. The output scores are log posterior scores under the model, not
empirically calibrated probabilities.

## K-means clustering

K-means partitions observations into a chosen number K of groups by
minimizing the within-cluster squared Euclidean distance:

\[
\sum_{j=1}^{K}\sum_{x_i\in C_j}\|x_i-\mu_j\|^2.
\]

The implementation uses k-means++ initialization, multiple restarts,
deterministic random-state control and empty-cluster reseeding. Cluster IDs
have no inherent semantic meaning. K-means favors compact, approximately
spherical clusters and is sensitive to feature scaling, initialization and
the selected K. It is not ISODATA: automatic cluster splitting and merging
are not included.

## Implementation

The [reference package](../../implementations/python/remote-classification/README.md)
contains both methods and synthetic classification/clustering tests. Inputs
are finite sample-by-feature matrices; image tiling, spatial regularization,
segmentation, model selection, cross-validation and accuracy assessment are
outside this package.


## ISODATA split-and-merge clustering

ISODATA extends iterative centroid clustering by adapting the number of
clusters. This implementation removes clusters below a minimum sample count
when the configured minimum cluster count remains satisfied, splits the most
dispersed clusters along their highest-variance feature, and greedily merges
the closest centroid pair below a distance threshold. The user controls
minimum/maximum cluster counts, minimum cluster size, split spread and merge
distance.

These thresholds are expressed in feature units and are therefore sensitive
to scaling. This is a practical heuristic implementation, not every variant
of the original ISODATA family; it does not include supervised labels,
spatial contiguity, cluster validity selection or automatic threshold tuning.
