# Gaussian-process mutual-information sensor selection

This package greedily chooses candidate sensor locations to maximize the
mutual information between a latent Gaussian field at target locations and
noisy observations at selected candidates. It supports Gaussian and
exponential covariance kernels, unit marginal variance, a positive length
scale, and independent positive observation-noise variances.

The objective is computed from the determinant of the target covariance
before and after conditioning on selected observations. At each step, the
candidate with the largest conditional information gain is selected;
ties retain the lowest original candidate index. Information is reported
in nats.

## Use

```python
from mutual_information_sensor_selection import gaussian_sensor_mutual_information

result = gaussian_sensor_mutual_information(
    target_points=[(0, 0), (1, 0), (0, 1)],
    candidate_points=[(0, 0), (1, 1), (3, 0)],
    max_sensors=2,
    length_scale=1.5,
    noise_variance=0.1,
)
print(result["selected_indices"], result["mutual_information"])
```

## Limits

This is a dense, small-problem greedy baseline. It does not optimize sensor
costs, enforce spatial separation or network constraints, model correlated
measurement noise, estimate covariance hyperparameters, or use non-Gaussian
likelihoods. It requires a positive-definite target covariance and uses
planar Euclidean distance. The greedy solution is not claimed to be the
global optimum for a fixed sensor budget.

## Greedy kriging-variance design

The module also provides `greedy_kriging_variance_design`, an A-optimal
criterion that greedily reduces the trace of the posterior covariance over
the supplied target locations. This is distinct from the mutual-information
(log-determinant) objective and shares its fixed covariance and independent
noise assumptions.
