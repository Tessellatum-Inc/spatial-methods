# Verification dossier: descriptive mobility metrics

## Implemented
- Weighted/unweighted radius of gyration.
- Step lengths and signed turning angles.
- Shannon visit entropy and effective state count.
- Numerical Fano upper-bound solution for maximum predictability.

## Independent tests
Tests cover a closed-form two-point radius, weighted radius, known step/turn sequence, uniform visit entropy, predictability endpoints, monotonicity, invalid coordinates, duplicate steps, unhashable/empty visits and invalid entropy.

## Exclusions
Exploration/preferential-return models, Lévy flights, CTRW, Brownian bridge, step-selection and resource-selection functions remain open.
