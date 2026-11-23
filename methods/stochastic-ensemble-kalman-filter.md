# Stochastic ensemble Kalman filter (EnKF)

The stochastic EnKF represents a forecast distribution with an ensemble.
For a linear observation operator H, the forecast ensemble supplies
sample state covariance P^f, state/observation cross-covariance P_xy,
and predicted-observation covariance P_yy. The gain is

\[
K=P_{xy}(P_{yy}+R)^{-1}.
\]

Each ensemble member receives an independent observation perturbation
epsilon_j ~ N(0,R), and the analysis update is

\[
x_j^a=x_j^f+K[y+\epsilon_j-Hx_j^f].
\]

The perturbations restore the observation-error contribution to the analysis
ensemble covariance in expectation. Updating every member with the same
unperturbed observation generally produces an ensemble that is too narrow.

## Implemented scope

The NumPy reference implementation performs one batch analysis for a linear
observation operator and a full positive-definite observation covariance.
It returns the analysis ensemble, sample moments, gain, innovation and
generated observation perturbations. It does not advance a forecast model.

This is distinct from the deterministic ETKF implementation, which applies a
symmetric square-root transform in ensemble space and does not perturb
observations. Both are valid algorithmic approaches with different numerical
properties.

## Limits

No forecast propagation, nonlinear observation operator, localization,
inflation, adaptive inflation, serial processing, model-error treatment,
cycling or adaptive observation targeting. The stochastic analysis has
finite-ensemble Monte Carlo error and requires a sufficiently large ensemble.
It is not a complete operational data-assimilation system.

## Reproduction

Run from implementations/python/state-estimation:

~~~bash
python -m pytest -q --import-mode=importlib
~~~

## Reference

Burgers, G., van Leeuwen, P. J., & Evensen, G. (1998). Analysis Scheme in the
Ensemble Kalman Filter. *Monthly Weather Review*, 126(6), 1719–1724.
https://doi.org/10.1175/1520-0493(1998)126<1719:ASITEK>2.0.CO;2.
