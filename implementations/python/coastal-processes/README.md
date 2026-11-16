# Coastal-process reference calculations

This package implements three transparent empirical/statistical building blocks from the coastal subsection of source page 7:

- **Stockdon wave runup**: the Stockdon et al. empirical R2 parameterization and simple proportional percentile summaries.
- **CERC longshore transport**: a signed immersed-weight energy-flux estimate using breaking wave height and angle relative to shore-normal.
- **Shoreline change rates**: end-point rate (EPR), ordinary least-squares linear rate, and optional inverse-variance weighted linear rate (WLR).

All distances and heights must use a consistent linear unit (normally metres); shoreline positions must be in a projected coordinate system and years must represent survey dates. These routines do not extract shorelines, generate transects, correct waterlines for tide, estimate positional uncertainty from imagery, calibrate site-specific coefficients, or replace DSAS workflows.

## Scope and cautions

Stockdon runup requires deep-water significant wave height, peak period and foreshore slope. The implementation reports the empirical R2 value; the R1/Rmean/Rlow outputs are simple scaled summaries, not independent fitted quantiles. Tide, surge and local morphology are not included.

CERC transport is highly sensitive to the empirical coefficient, breaking conditions, sediment density and porosity. The chosen shallow-water group-speed approximation is explicit; alternative CERC/Kamphuis formulations can differ materially. Treat output as a screening estimate, not a design discharge.

EPR uses only the first and last survey. OLS uses every observation equally; WLR uses supplied one-sigma positional errors as inverse-variance weights. The regression routines assume independent errors and do not account for shoreline autocorrelation, proxy-datum bias or uncertainty in survey dates.

Run tests with `python -m pytest -q`.


- **Bruun rule recession**: idealized shoreline retreat from sea-level rise and active-profile geometry using explicit berm height and closure depth.
- **Dean equilibrium beach profile**: the h(x)=A*x^(2/3) profile and its analytic cross-shore depth integral.

These are equation-level reference methods. Bruun-rule assumptions are restrictive and contested for many coasts; the implementation is not a predictive shoreline model. Dean's profile is not coupled to wave transformation, sediment continuity or morphodynamic evolution.
