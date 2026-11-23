# Source verification — spatial Hawkes process simulator

## Identity and bibliography
- Hawkes (1971), “Spectra of some self-exciting and mutually exciting point processes,” *Biometrika*, 58(1), 83–90, DOI 10.1093/biomet/58.1.83.
- Hawkes & Oakes (1974), “A cluster process representation of a self-exciting process,” *Journal of Applied Probability*, 11(3), 493–503, DOI 10.2307/3212693.

## Technical claims
- The branching/immigration-birth representation is the basis of the simulator.
- The direct offspring count is Poisson with mean branching ratio n; n is constrained to [0,1).
- Exponential temporal delays and wrapped Gaussian spatial offsets are explicit model choices, not universal Hawkes kernels.

## Implementation and tests
- Seeded finite-horizon simulation with toroidal spatial wrapping, parent/generation metadata and event cap.
- Tests cover deterministic reproducibility, chronological ordering, parent-before-child genealogy, window containment, zero-baseline/zero-branching cases, invalid parameters and event-cap enforcement.

## Limits and rights
No pre-window history, so a temporal startup transient remains. Toroidal boundaries, exponential triggering and Gaussian spatial displacement are scoped assumptions. No ETAS, likelihood, parameter fitting or inference is implemented. Original code and explanatory text; bibliographic metadata only.
