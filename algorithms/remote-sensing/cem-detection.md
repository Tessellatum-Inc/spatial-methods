# Constrained Energy Minimisation (CEM)

CEM constructs a linear spectral filter with unit response to a specified target signature while minimising output energy under a spectral correlation matrix. The reference implementation estimates the uncentred second-moment matrix or accepts a supplied matrix, applies eigenvalue regularisation and returns pixel scores and filter weights.

CEM is distinct from a mean-centred adaptive matched filter and from ACE. Scores are not calibrated probabilities; background representativeness, target signature alignment and matrix conditioning require attention.
