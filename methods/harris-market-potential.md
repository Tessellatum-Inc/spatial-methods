# Harris-style market potential

## Core idea

Market potential at origin i is an accessibility index that sums the size of destination markets weighted by a declining function of generalized travel impedance:

\[ MP_i=\sum_j M_j c_{ij}^{-\alpha}. \]

Here M_j is a market-mass proxy (for example, purchasing power or output), c_ij is a positive generalized cost, and alpha is a positive impedance-decay exponent. The inverse-distance form with alpha=1 is the classic Harris-style index. The code optionally excludes self-potential; if included, diagonal impedance must be supplied explicitly and positive.

## Implementation

The NumPy routine validates nonnegative market mass and positive off-diagonal costs, supports a configurable power-decay exponent, and returns an index for each origin. Costs can represent distance, travel time or another consistently measured generalized impedance.

## Interpretation limits

This is a descriptive potential/accessibility index, not a calibrated gravity model, spatial equilibrium, consumer-choice model or causal estimate. Results depend on market-mass definition, impedance matrix, decay exponent, self-potential convention and spatial scale. It does not estimate the decay parameter or correct for endogenous market size. Use network travel costs when straight-line distance is not a defensible proxy.

## Primary source

Harris, C. D. (1954). The Market as a Factor in the Localization of Industry in the United States. Annals of the Association of American Geographers, 44(4), 315–348. https://doi.org/10.1080/00045605409352140.