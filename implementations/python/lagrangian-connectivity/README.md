# Lagrangian particle advection and regional connectivity

This package contains a steady-field two-dimensional particle integrator and a weighted source-to-destination connectivity aggregator.

## Install and test

```bash
python -m pip install -r requirements.txt
python -m pytest -q
```

## Particle advection

`advect_particles_rk4` integrates particle positions through a steady eastward/northward velocity field using fourth-order Runge–Kutta. The velocity field is bilinearly interpolated on caller-supplied ascending rectilinear coordinates. The trajectory includes the initial positions; particles that leave the interpolation domain become inactive and have NaN positions thereafter. Coordinate, velocity and timestep units must be consistent.

## Connectivity

`connectivity_matrix` aggregates source and destination region IDs into weighted counts and probabilities. Destination ID -1 represents an unassigned or lost particle. Probabilities are divided by all released weight in each source region, so assigned probabilities plus the unassigned fraction sum to one for nonempty sources.

## Scope

This is a deterministic steady-current baseline. It does not include time-varying currents, diffusion, stochastic turbulence, vertical motion, beaching, mortality/decay, land masks beyond interpolation-domain exit, boundary reflection, uncertainty ensembles, hydrodynamic coupling or marine protected area optimisation.

See `algorithms/marine/lagrangian-particle-tracking.md`.
