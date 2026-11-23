# Districting polygon compactness metrics

This package computes three planar compactness metrics from one simple
polygon exterior ring:

- **Polsby–Popper:** 4πA/P²; higher values indicate more compact shapes.
- **Reock:** polygon area divided by the area of its minimum enclosing circle.
- **Schwartzberg ratio:** perimeter divided by the circumference of an
  equal-area circle; values closer to 1 indicate more compact shapes.

A deterministic incremental minimum-enclosing-circle routine is included.

## Install and test

    python -m pip install -r requirements.txt
    python -m pytest -q

## Scope and limitations

Coordinates must be planar in a suitable projected CRS. The input is one
simple exterior ring; holes, multipart polygons, self-intersection repair,
geodesic area/perimeter and legal districting constraints are not handled.
Compactness scores are diagnostics, not fairness or representativeness
measures. Metric choice and policy thresholds require context.
