from __future__ import annotations
from math import isfinite, log
from typing import Hashable, Sequence

def _prob_vector(values, name):
 row=tuple(float(x) for x in values)
 if not row or any(not isfinite(x) or x<0 for x in row): raise ValueError(name+' must contain finite non-negative probabilities')
 if abs(sum(row)-1.0)>1e-9: raise ValueError(name+' must sum to one')
 return row

def _prob_matrix(values, name):
 rows=tuple(_prob_vector(row,name+' row') for row in values)
 if not rows or len({len(row) for row in rows})!=1: raise ValueError(name+' must be a non-empty rectangular matrix')
 return rows

def viterbi_decode(observations:Sequence[Hashable], states:Sequence[Hashable], symbols:Sequence[Hashable], start_probabilities, transition_probabilities, emission_probabilities):
 """Decode a discrete HMM; return (best_state_path, joint_log_probability).

    Matrix row/column order follows the supplied `states` and `symbols`.
    Ties are resolved by the first state in `states` order. Zero probabilities
    are valid and map to negative infinity in log space.
    """
 states=tuple(states); symbols=tuple(symbols); observations=tuple(observations)
 if not states or len(set(states))!=len(states): raise ValueError('states must be non-empty and unique')
 if not symbols or len(set(symbols))!=len(symbols): raise ValueError('symbols must be non-empty and unique')
 start=_prob_vector(start_probabilities,'start probabilities')
 trans=_prob_matrix(transition_probabilities,'transition probabilities')
 emit=_prob_matrix(emission_probabilities,'emission probabilities')
 n,m=len(states),len(symbols)
 if len(start)!=n or len(trans)!=n or any(len(row)!=n for row in trans): raise ValueError('transition dimensions must match states')
 if len(emit)!=n or any(len(row)!=m for row in emit): raise ValueError('emission dimensions must match states and symbols')
 index={symbol:i for i,symbol in enumerate(symbols)}
 try: obs=[index[x] for x in observations]
 except KeyError as exc: raise ValueError('observation is not in the declared symbol alphabet') from exc
 if not obs: return [],0.0
 neg_inf=float('-inf')
 def lp(p): return log(p) if p>0 else neg_inf
 log_start=[lp(p) for p in start]
 log_trans=[[lp(p) for p in row] for row in trans]
 log_emit=[[lp(p) for p in row] for row in emit]
 score=[log_start[i]+log_emit[i][obs[0]] for i in range(n)]
 back=[]
 for symbol in obs[1:]:
  next_score=[]; parents=[]
  for j in range(n):
   candidates=[score[i]+log_trans[i][j] for i in range(n)]
   parent=max(range(n),key=lambda i:candidates[i])
   parents.append(parent); next_score.append(candidates[parent]+log_emit[j][symbol])
  back.append(parents); score=next_score
 last=max(range(n),key=lambda i:score[i]); best=score[last]
 if best==neg_inf: raise ValueError('observation sequence has zero probability under this model')
 path=[last]
 for parents in reversed(back): path.append(parents[path[-1]])
 path.reverse()
 return [states[i] for i in path],best



def _forward_backward_indices(obs, start, trans, emit):
    """Scaled forward-backward; return gamma, xi and sequence log likelihood."""
    n = len(start)
    if not obs:
        return [], [], 0.0
    scales = []
    first = [start[i] * emit[i][obs[0]] for i in range(n)]
    scale = sum(first)
    if scale <= 0:
        raise ValueError("observation sequence has zero probability under this model")
    alpha = [[value / scale for value in first]]
    scales.append(scale)
    for symbol in obs[1:]:
        row = [emit[j][symbol] * sum(alpha[-1][i] * trans[i][j] for i in range(n)) for j in range(n)]
        scale = sum(row)
        if scale <= 0:
            raise ValueError("observation sequence has zero probability under this model")
        alpha.append([value / scale for value in row])
        scales.append(scale)
    beta = [[1.0] * n for _ in obs]
    for t in range(len(obs) - 2, -1, -1):
        beta[t] = [
            sum(trans[i][j] * emit[j][obs[t + 1]] * beta[t + 1][j] for j in range(n)) / scales[t + 1]
            for i in range(n)
        ]
    gamma = []
    for t in range(len(obs)):
        row = [alpha[t][i] * beta[t][i] for i in range(n)]
        total = sum(row)
        gamma.append([value / total for value in row])
    xis = []
    for t in range(len(obs) - 1):
        matrix = [[alpha[t][i] * trans[i][j] * emit[j][obs[t + 1]] * beta[t + 1][j]
                   for j in range(n)] for i in range(n)]
        total = sum(sum(row) for row in matrix)
        xis.append([[value / total for value in row] for row in matrix])
    return gamma, xis, sum(log(value) for value in scales)


def forward_log_likelihood(observations, states, symbols, start_probabilities,
                           transition_probabilities, emission_probabilities) -> float:
    """Return marginal log likelihood of a discrete observation sequence."""
    states, symbols = tuple(states), tuple(symbols)
    if not states or len(set(states)) != len(states):
        raise ValueError("states must be non-empty and unique")
    if not symbols or len(set(symbols)) != len(symbols):
        raise ValueError("symbols must be non-empty and unique")
    start = _prob_vector(start_probabilities, "start probabilities")
    trans = _prob_matrix(transition_probabilities, "transition probabilities")
    emit = _prob_matrix(emission_probabilities, "emission probabilities")
    n, m = len(states), len(symbols)
    if len(start) != n or len(trans) != n or any(len(row) != n for row in trans):
        raise ValueError("transition dimensions must match states")
    if len(emit) != n or any(len(row) != m for row in emit):
        raise ValueError("emission dimensions must match states and symbols")
    index = {symbol: i for i, symbol in enumerate(symbols)}
    try:
        obs = [index[value] for value in observations]
    except KeyError as exc:
        raise ValueError("observation is not in the declared symbol alphabet") from exc
    return _forward_backward_indices(obs, start, trans, emit)[2]


def baum_welch(observation_sequences, states, symbols, start_probabilities,
               transition_probabilities, emission_probabilities, *,
               max_iterations=100, tolerance=1e-6, pseudocount=1e-8):
    """Fit a discrete HMM with scaled multi-sequence Baum-Welch EM.

    Returns (start, transition, emission, log_likelihood_history). Parameters
    are tuples. EM is a local optimiser; pseudocounts regularise M-step rows.
    """
    states, symbols = tuple(states), tuple(symbols)
    if not states or len(set(states)) != len(states):
        raise ValueError("states must be non-empty and unique")
    if not symbols or len(set(symbols)) != len(symbols):
        raise ValueError("symbols must be non-empty and unique")
    start = list(_prob_vector(start_probabilities, "start probabilities"))
    trans = [list(row) for row in _prob_matrix(transition_probabilities, "transition probabilities")]
    emit = [list(row) for row in _prob_matrix(emission_probabilities, "emission probabilities")]
    n, m = len(states), len(symbols)
    if len(start) != n or len(trans) != n or any(len(row) != n for row in trans):
        raise ValueError("transition dimensions must match states")
    if len(emit) != n or any(len(row) != m for row in emit):
        raise ValueError("emission dimensions must match states and symbols")
    if isinstance(max_iterations, bool) or not isinstance(max_iterations, int) or max_iterations < 1:
        raise ValueError("max_iterations must be a positive integer")
    if not isfinite(float(tolerance)) or tolerance < 0:
        raise ValueError("tolerance must be finite and non-negative")
    if not isfinite(float(pseudocount)) or pseudocount < 0:
        raise ValueError("pseudocount must be finite and non-negative")
    symbol_index = {symbol: i for i, symbol in enumerate(symbols)}
    sequences = []
    for sequence in observation_sequences:
        try:
            encoded = [symbol_index[value] for value in sequence]
        except KeyError as exc:
            raise ValueError("observation is not in the declared symbol alphabet") from exc
        if encoded:
            sequences.append(encoded)
    if not sequences:
        raise ValueError("at least one non-empty observation sequence is required")

    def likelihood():
        return sum(_forward_backward_indices(obs, start, trans, emit)[2] for obs in sequences)

    history = [likelihood()]
    for _ in range(max_iterations):
        start_counts = [0.0] * n
        trans_counts = [[0.0] * n for _ in range(n)]
        emit_counts = [[0.0] * m for _ in range(n)]
        for obs in sequences:
            gamma, xis, _ = _forward_backward_indices(obs, start, trans, emit)
            for i in range(n):
                start_counts[i] += gamma[0][i]
            for t, symbol in enumerate(obs):
                for i in range(n):
                    emit_counts[i][symbol] += gamma[t][i]
            for matrix in xis:
                for i in range(n):
                    for j in range(n):
                        trans_counts[i][j] += matrix[i][j]

        def normalise(counts, fallback):
            values = [value + pseudocount for value in counts]
            total = sum(values)
            return [value / total for value in values] if total > 0 else list(fallback)

        start = normalise(start_counts, start)
        trans = [normalise(trans_counts[i], trans[i]) for i in range(n)]
        emit = [normalise(emit_counts[i], emit[i]) for i in range(n)]
        score = likelihood()
        history.append(score)
        if abs(score - history[-2]) <= tolerance * (1.0 + abs(history[-2])):
            break
    return tuple(start), tuple(tuple(row) for row in trans), tuple(tuple(row) for row in emit), history
