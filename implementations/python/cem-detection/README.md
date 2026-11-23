# Constrained Energy Minimisation (CEM)

Run `pytest -q`. CEM constructs a linear filter that has unit response to the supplied target signature while minimising output energy under a global spectral correlation matrix. The reference implementation estimates the uncentred second-moment matrix from selected background pixels or accepts one directly, applies eigenvalue regularisation and returns scores and weights.

CEM differs from the adaptive matched filter: it uses an uncentred correlation matrix and the unit target-response constraint, rather than centring on a background mean and maximizing target-to-background contrast. It is not ACE or a subspace detector. Output scores are not calibrated probabilities.
