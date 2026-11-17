# Source verification — ETAS-style branching simulator

## Identity and bibliography
- Ogata (1988), “Statistical models for earthquake occurrences and residual analysis for point processes,” *Journal of the American Statistical Association*, 83(401), 9–27, DOI 10.1080/01621459.1988.10478560.
- Hawkes & Oakes (1974), “A cluster process representation of a self-exciting process,” *Journal of Applied Probability*, 11(3), 493–503, DOI 10.2307/3212693.

## Technical claims
- The implementation is a marked immigration-birth/branching simulator.
- Magnitudes are exponentially distributed above a threshold; productivity is calibrated so expected offspring under this mark distribution equals the supplied branching ratio.
- Temporal delays use a normalized Omori density; spatial displacements use an isotropic power-law radial kernel.
- Toroidal wrapping and no pre-window history are explicit simplifying assumptions.

## Implementation and tests
Seeded event simulation, magnitude marks, parent/generation metadata, subcritical branching, toroidal coordinates, finite horizon and maximum-event guard. Tests cover reproducibility, event ordering, parent genealogy, magnitude threshold, zero branching, invalid parameters and event-cap enforcement.

## Limits and rights
No likelihood, estimation, background-intensity fitting, catalogue-completeness correction or operational seismicity diagnostics. Original code and explanatory text; bibliographic metadata only.
