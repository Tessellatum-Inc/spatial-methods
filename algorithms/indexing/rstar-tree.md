# Mutable R*-tree insertion and splitting

R*-trees reduce sibling-envelope overlap to limit unnecessary range-query traversal. During descent, choose the child with the smallest overlap enlargement, breaking ties by area enlargement and current area.

On overflow, the R*-style split has two stages. First choose the axis with the smallest sum of margins across all legal distributions, considering both lower- and upper-coordinate orderings. Then choose the distribution on that axis with minimum overlap, using combined area as a tie-break.

This implementation deliberately omits forced reinsertion, a defining part of the full R*-tree algorithm. It is therefore labelled R*-style, not a complete production implementation. It also omits deletion, condensation, disk pages and persistence.

The index stores axis-aligned boxes and returns closed-envelope intersections. For arbitrary geometries, follow envelope filtering with exact predicates. Query worst-case complexity remains linear when envelopes overlap heavily.
