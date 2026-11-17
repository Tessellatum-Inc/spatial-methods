# Implementation verification — Gaussian-process sensor selection

The package implements greedy mutual-information selection for a finite set
of planar candidate sensors and a finite target set. It computes the
Gaussian conditional target covariance using dense linear solves and
positive-definite log determinants. Observation noise is independent and
may be supplied as a scalar or per-candidate vector.

Tests include a closed-form one-target case, an independently calculated
conditional-covariance marginal-gain oracle, deterministic selection,
non-negative gains, zero-budget behaviour and invalid/singular inputs.
The package is a small-instance numerical reference; no large-scale
performance or field-data validation is claimed.

The source entry groups model-based and adaptive designs. This record covers
only the Gaussian-process mutual-information greedy component; kriging
variance minimization, Bayesian optimal design and robotic path planning
remain separate methods.

## Additional variance-design objective

A greedy A-optimal design minimizes the trace of the target posterior
covariance. Tests compare each selection step with an independently
calculated covariance-trace oracle and a closed-form single-target case.
This is not a general Bayesian optimal-design engine.
