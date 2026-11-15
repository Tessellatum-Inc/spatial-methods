# Discrete hidden Markov models: decoding and estimation

This package implements Viterbi maximum-a-posteriori decoding, scaled forward
marginal likelihood and Baum-Welch expectation-maximisation for discrete
emissions. Multiple independent observation sequences can be fitted jointly.

Run `python -m pytest -q` from this directory. Runtime code uses only the
Python standard library.

State and symbol ordering follows supplied sequences. Probability vectors and
matrix rows must be finite, non-negative and sum to one. Viterbi ties use the
first declared state; zero probabilities are supported. Baum-Welch returns
updated start, transition and emission probabilities plus the marginal
log-likelihood history. A small pseudocount (default 1e-8) regularises rows.
EM is a local optimiser: results depend on initialisation, state labels are
permutation-invariant, and convergence does not imply a global maximum.

This is a discrete-observation HMM, not a continuous emission model or a
complete map-matching system. Spatial map matching additionally needs
candidate generation, network-aware transition probabilities, measurement-
error assumptions and treatment of sampling intervals.
