# Variogram model fitting and directional analysis

An empirical semivariogram is a noisy, binned estimate; kriging requires a
valid covariance/variogram model. This lesson implements spherical,
exponential, Gaussian and Matérn structures with nugget and partial sill, plus
pair-count weighted nonlinear least-squares fitting and dense Gaussian
restricted maximum-likelihood (REML) estimation with a constant unknown mean.

Directional analysis filters point pairs by an undirected azimuth and optional
cross-track bandwidth. The Cressie-Hawkins, Dowd and Genton estimators are included as robust alternatives
to Matheron's classical half mean squared increment. Genton's estimator uses
the Q_n robust scale of pairwise differences among the increments in each lag
class; it is computationally quadratic in the number of increments per class. Dowd's estimator uses 1.099 times the squared median absolute increment. Geometric anisotropy is supported with a fixed transform or joint REML estimation of major-axis azimuth and minor/major range ratio (bounded to [0.1, 1]); azimuth is clockwise from north.

Automatic anisotropy fitting is available in dense REML; nested structures, Matérn smoothness is supported as a fixed user-supplied parameter; estimating smoothness and parameter uncertainty remain open.

The Python implementation lives in implementations/python/variogram-models.
The fitted range and sill depend on the selected model and lag design. The
current baseline does not fit nested structures or parameter uncertainty; these remain separate extensions.
