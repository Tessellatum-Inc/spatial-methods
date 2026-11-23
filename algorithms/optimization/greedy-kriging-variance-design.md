# Greedy kriging-variance sensor design

Given a Gaussian-process covariance over target locations and candidate
sensor locations, observing a selected set S with independent noise yields
the conditional target covariance

```
K(T|y_S) = K(T,T) - K(T,S) [K(S,S) + R(S)]^-1 K(S,T)
```

This A-optimal criterion minimizes the trace of the posterior covariance,
equivalently the sum of posterior variances at the supplied target points.
At each step, the greedy algorithm adds the candidate that produces the
largest trace reduction. Ties are resolved by original candidate order.

The implementation uses Gaussian or exponential covariance kernels with
unit marginal variance and a fixed positive length scale. It reports the
selected indices, posterior covariance and per-step variance reductions.

## Scope

This is a dense greedy baseline for finite target and candidate sets. It is
not a global combinatorial optimizer, does not account for sensor costs or
correlated noise, and does not estimate covariance hyperparameters. The
objective is defined over supplied target points, not a continuous domain.
