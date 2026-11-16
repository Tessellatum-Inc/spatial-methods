# Flow-capturing location model

## Problem

A flow-capturing location model (FCLM) chooses a limited number of facilities
from candidate sites to maximize the weight of origin-destination paths that
pass at least one selected facility. It is useful for locating services such
as charging points, retail facilities, information kiosks or inspection
stations when demand follows known network paths.

## Mathematical formulation

Let P be the set of paths, J the candidate sites, w_p >= 0 the demand weight
on path p, and a_pj = 1 when candidate j lies on path p. With binary decision
variable x_j and budget b, the objective is

    maximize sum_p w_p * min(1, sum_j a_pj x_j)
    subject to sum_j x_j <= b
               x_j in {0,1}

Each path's weight is counted once even if it encounters multiple selected
sites. The objective is monotone submodular for non-negative weights.

## Algorithms

The exact reference solver enumerates all b-site subsets and is exponential
in the number of candidates. It is suitable for small instances, validation
and benchmark oracles.

The greedy solver repeatedly chooses the site with the greatest marginal
newly captured flow. For a monotone submodular objective under a cardinality
constraint, this achieves at least (1 - 1/e) of the optimum.

## Interpretation and limitations

The input paths and their candidate-site incidence are supplied by the
caller. The implementation does not infer paths from trajectories, perform
map matching, construct a network, model congestion, enforce detours, or
include facility costs and capacities. It assumes a single global cardinality
budget and non-negative fixed path weights.

FCLM must not be confused with the flow-refueling location model (FRLM).
FRLM requires feasible refueling sequences under a vehicle's driving range;
merely encountering one selected facility is insufficient. That remains a
separate algorithmic work package.

## Implementation and tests

See the Python package at
../../implementations/python/flow-capturing-location/README.md for exact and
greedy solvers and independent subset-enumeration tests.

## References

- Hodgson, M. J. (1990). A Flow-Capturing Location-Allocation Model.
  Geographical Analysis, 22(3), 270–279.
  https://doi.org/10.1111/j.1538-4632.1990.tb00210.x
- Church, R. L. (2002). Geographical Information Systems and Location Science.
  Computers & Operations Research, 29(6), 541–562.
  https://doi.org/10.1016/S0305-0548(99)00104-5
