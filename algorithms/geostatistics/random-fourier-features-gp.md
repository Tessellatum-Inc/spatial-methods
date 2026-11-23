# Random Fourier feature Gaussian-process approximation

Random Fourier features replace a shift-invariant kernel with an explicit
finite-dimensional randomized feature map. For the Gaussian covariance used
in this repository,

\[
C(h)=\sigma^2\exp[-(\|h\|/a)^2],
\]

the spectral frequencies are sampled from
\(\mathcal N(0,2a^{-2}I)\). With independent uniform phases, cosine features
provide a Monte Carlo approximation to the covariance kernel.

The implementation fits Bayesian linear weights in this random feature
space. It returns approximate latent posterior means and variances using a
Gaussian prior on feature weights and supplied observation-noise variance.
The feature basis is fixed after training and must be reused at prediction.

This method reduces dependence on an \(n\times n\) kernel matrix when the
feature count is substantially smaller than the observation count. Its dense
posterior solve is still cubic in the feature count and quadratic in feature
storage. Approximation error depends on feature count and the random draw;
the reported variance is conditional on that finite basis and supplied
hyperparameters, not a complete uncertainty account.

## Runnable implementation

[Covariance-functions package, tests and walkthrough](../../implementations/python/covariance-functions/README.md).

## References

- Rahimi, A., & Recht, B. (2007). Random Features for Large-Scale Kernel
  Machines. *Advances in Neural Information Processing Systems*, 20,
  1177–1184. https://proceedings.neurips.cc/paper_files/paper/2007/file/013a006f03dbc5392effeb8f18fda755-Paper.pdf
