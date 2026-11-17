# Classical remote-sensing classification walkthrough

## Gaussian maximum likelihood

Fit a class-specific mean and covariance for each supplied label, stabilize
covariances with a small ridge term, and assign the class with the largest
Gaussian log-posterior score.

## K-means and ISODATA

K-means uses k-means++ starts and multiple restarts to minimize within-cluster
squared distance. ISODATA adds heuristic cluster deletion, splitting and
merging. Cluster IDs are not semantic classes.

## Support-vector machine

The SVM baseline uses scikit-learn SVC with linear, polynomial, RBF or
sigmoid kernels. Tune C, kernel and gamma using training-only preprocessing
and spatially appropriate cross-validation. Decision margins are not
probabilities unless a separate calibration step is fitted without leakage.

## Random forest

The random-forest baseline fits an ensemble of decision trees and can return
class vote fractions and feature importances. Vote fractions are not
automatically calibrated probabilities. Check spatial autocorrelation and
sampling bias when splitting training and validation pixels.

The package does not include XGBoost, LightGBM, stacked generalization,
spatial regularization or area-adjusted accuracy assessment.
