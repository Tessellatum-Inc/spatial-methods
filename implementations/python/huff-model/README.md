# Huff competitive facility-choice model

Implements the Huff gravity model: each origin allocates demand probabilistically across facilities in proportion to facility attractiveness raised to alpha and generalized travel impedance raised to negative beta. The implementation returns origin-facility probabilities and aggregate expected visits, with explicit zero-cost regularization. It does not estimate attractiveness/beta, model capacity constraints, strategic Stackelberg/Nash competition or endogenous facility entry.
