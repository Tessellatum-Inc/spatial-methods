# Compositional data geometry

A composition represents relative parts of a whole. Its information is in
ratios, not absolute magnitude. Multiplying every component by the same
positive constant must therefore leave the represented composition unchanged.

## Closure

For non-negative components with positive total, closure maps x to
C(x) = x / sum(x), placing the composition on the unit simplex.

## Centred log-ratio transform

For positive parts x_i and geometric mean g(x), the CLR coordinates are

    clr(x)_i = log(x_i / g(x))

The coordinates sum to zero and are invariant to common scaling. Their
Euclidean distance is the Aitchison distance.

## Zero replacement

The logarithm is undefined at zero. The reference implementation requires
an explicit replacement mass delta. It assigns delta to every zero and
multiplies all nonzero parts by a common factor so the total remains one and
their ratios are preserved. The total mass assigned to zeros must be below
one. This simple treatment does not distinguish structural zeros from
rounded or below-detection values.

See the Python package for closure, CLR, multiplicative zero replacement,
Aitchison distance and reference tests. Compositional kriging and probabilistic
models remain open.

Reference: Aitchison, J. (1986). The Statistical Analysis of Compositional
Data. Chapman & Hall.
