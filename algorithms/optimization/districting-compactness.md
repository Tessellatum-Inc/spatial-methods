# Districting compactness metrics

For a planar polygon with area A and perimeter P:

- Polsby–Popper is 4πA/P²; larger is more compact.
- Reock is A divided by the area of the minimum enclosing circle; larger
  is more compact.
- Schwartzberg ratio is P divided by the circumference of an equal-area
  circle; values closer to 1 are more compact.

The linked implementation computes these metrics from one simple exterior
ring and uses a deterministic minimum enclosing circle. Coordinates must
be projected and planar. These metrics do not measure fairness, population
equality, community integrity or legal compliance; they are diagnostics
that should be interpreted alongside those requirements.
