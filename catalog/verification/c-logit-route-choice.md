# Source verification — C-logit route choice

## Identity and bibliography

Cascetta, E., Nuzzolo, A., Russo, F., and Vitetta, A. (1996), “A modified
logit route choice model overcoming path overlapping problems: specification
and some calibration results for interurban networks,” *Transportation and
Traffic Theory*, 13th International Symposium, 697–711.

The 1996 paper identity and conference pagination were checked against the
Transport Research International Documentation record. A later technical
review reproduces the length-based commonality factor and utility penalty.

## Implemented scope

This package implements the first commonality-factor definition:
the logarithm of the sum of powered shared-length ratios
L_kj / sqrt(L_k L_j), including the route's self-term. The factor is
subtracted from utility with a non-negative scale parameter, followed by
a numerically stable multinomial-logit normalization.

Tests cover single-route and disjoint-route limits, identical routes,
a hand-calculated partial overlap, probability normalization, the zero-
penalty multinomial-logit limit and invalid inputs.

## Boundaries

The source describes four commonality-factor definitions. This package
implements only the length-overlap form. Parameter estimation, alternative
definitions, route-set generation, stochastic user equilibrium and empirical
calibration remain open. No behavioural performance claim is made.
