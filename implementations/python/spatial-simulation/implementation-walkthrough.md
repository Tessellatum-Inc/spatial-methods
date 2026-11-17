# Spatial simulation implementation walkthrough

## 1. Choose the state representation

The binary automaton uses a two-dimensional integer array with 0 for dead and 1 for live. The Schelling model uses 0 for vacancy and positive integers for group labels. This makes vacancy distinct from every agent group.

## 2. Define the neighborhood

The implementation exposes Moore (eight offsets) and von Neumann (four offsets) neighborhoods. The boundary policy is explicit: fixed-dead boundaries omit off-grid cells, while periodic boundaries wrap coordinates.

## 3. Keep automaton updates synchronous

`live_neighbor_count` calculates the neighborhood sum from the unchanged input grid. `life_like_step` then evaluates birth and survival sets and returns a new array. The blinker test is a useful order-independence fixture: a horizontal three-cell line becomes vertical and then horizontal again.

## 4. Specify the Schelling rule

For each occupied cell, `same_group_share` measures the fraction of occupied neighbors carrying the same group label. Cells below the supplied tolerance are marked unhappy using the initial state. A seeded permutation chooses their processing order; each move selects a distinct cell that was empty at the start of the step.

## 5. Validate invariants

The tests check that group counts and the number of vacancies are conserved, seeded runs reproduce, invalid parameters fail early, and a stable configuration terminates with zero moves. These tests establish the documented teaching contract; they do not validate a real-world segregation theory.

## 6. Extend carefully

A more complete model should introduce explicit agent attributes, heterogeneous preferences, a defined search policy, sequential versus simultaneous move semantics, empirical calibration and sensitivity analysis. Named land-change systems such as SLEUTH and FLUS should be separate implementations with their own source and validation records.
