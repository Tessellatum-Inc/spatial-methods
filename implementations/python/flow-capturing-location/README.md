# Flow-capturing location model (FCLM)

This package selects a fixed number of candidate facilities to maximize the
weight of paths that encounter at least one selected facility.

## Model

Let P be a set of paths, J a set of candidate sites, w_p >= 0 the flow on
path p, and a_pj indicate whether site j lies on path p. For a selected set
S with |S| <= b, captured flow is

    sum_p w_p * 1[sum_{j in S} a_pj >= 1]

A path contributes its weight once even if it encounters multiple selected
sites. The implementation returns exactly b sites; with non-negative weights
and unused sites allowed, this is equivalent to an at-most-b budget.

## Algorithms

- flow_capturing_exact: exhaustive subset enumeration, useful for small
  instances and as a correctness oracle. Complexity is
  O(binomial(|J|, b) * total_path_site_incidence).
- flow_capturing_greedy: repeatedly selects the site with greatest marginal
  newly captured flow. The objective is monotone submodular for non-negative
  path weights, so cardinality-constrained greedy has a (1 - 1/e) guarantee.

Input path-site incidence and flow weights are supplied by the caller. The
package does not perform map matching, infer routes from GPS trajectories,
construct a road network, model congestion or enforce route detours.

## Deliberate exclusions

This is FCLM, not the flow-refueling location model (FRLM). FCLM only asks
whether a path encounters a selected site. FRLM additionally requires
feasible refueling sequences under vehicle range and station placement;
that distinct constraint is not approximated by this package.

## Run

    python -m pytest -q

The runtime uses only the Python standard library; pytest is the test runner.
