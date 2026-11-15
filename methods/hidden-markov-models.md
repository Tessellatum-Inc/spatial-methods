# Discrete hidden Markov models: forward, Viterbi and Baum-Welch

A discrete HMM has an initial-state distribution pi, transition matrix A and
state-conditioned emission matrix B. The forward algorithm sums joint
probability over all hidden paths; Viterbi finds the single most likely path.

The scaled forward recursion normalises each time slice by its sum c_t. The
marginal log likelihood is sum_t log(c_t), avoiding underflow for long
sequences. The backward recursion uses the same scales. Posterior state
probabilities gamma_t(i) and transition probabilities xi_t(i,j) provide
expected sufficient statistics for expectation-maximisation.

Baum-Welch alternates an E-step (compute gamma and xi for every sequence) with
an M-step (update initial, transition and emission probabilities from expected
counts). It then recomputes marginal log likelihood and stops when its change
is small. Multiple independent sequences share the same parameters.

The companion [implementation](../implementations/python/hmm-viterbi/README.md)
supports multi-sequence discrete estimation and optional pseudocount
regularisation. EM can converge to local maxima and cannot identify semantic
state labels; initialisation and model selection remain substantive choices.
It is not a full continuous-observation HMM or map-matching implementation.

Tests compare forward likelihood with exhaustive hidden-path enumeration,
check EM likelihood improvement and probability normalisation, and cover
multiple sequences, empty sequences and invalid inputs.
