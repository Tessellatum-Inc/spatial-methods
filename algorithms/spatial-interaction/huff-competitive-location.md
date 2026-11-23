# Huff competitive facility location

For origin i and facility j, Huff choice probability is proportional to A_j^alpha * c_ij^(-beta), where A_j is attractiveness and c_ij is generalized travel impedance. The implementation regularizes zero costs with a caller-specified minimum, normalizes probabilities by origin, and aggregates expected visits using origin demand. Attractiveness and impedance must be consistently scaled and beta should be calibrated to observed choice data before forecasting.

This is a probabilistic market-area model, not a strategic game: it does not model facility capacity, competitor reaction, Stackelberg/Nash equilibrium, endogenous entry or location optimization.
