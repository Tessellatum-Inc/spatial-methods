# Gaussian-process mutual-information sensor selection

Let f_T be the latent Gaussian field at target locations and y_S be noisy
observations at a selected subset S of candidate sensor locations. The
implementation assumes a specified covariance kernel and independent
observation noise. The conditional target covariance is

```
K(T|y_S) = K(T,T) - K(T,S) [K(S,S) + R(S)]^-1 K(S,T)
```

The mutual information in nats is

```
I(f_T; y_S) = 0.5 * (log det K(T,T) - log det K(T|y_S))
```

The greedy algorithm repeatedly adds the candidate with the largest
conditional increase in mutual information. Ties are resolved by original
candidate order. The package supports Gaussian and exponential covariance
kernels with unit marginal variance and independent positive sensor noise.

## Scope

This is a dense greedy reference for small candidate sets. It is not an
exact combinatorial optimizer and does not claim a globally optimal subset.
It does not include spatial separation, budgeted costs, correlated noise,
hyperparameter fitting, anisotropy, non-Gaussian observation models or
network constraints. Coordinates must use meaningful planar units.
