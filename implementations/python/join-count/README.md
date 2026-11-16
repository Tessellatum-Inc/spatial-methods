# Binary join-count test

Dependency-free reference implementation of the global binary join-count
statistics BB, WW and BW, with conditional randomisation inference.

## Run

~~~bash
python -m pip install -r requirements.txt
python -m pytest -q
~~~

## Contract

- Labels are binary (1 = black, 0 = white).
- The graph is undirected, represented by a symmetric binary weights matrix
  with zero diagonal. Every edge is counted once.
- Randomisation shuffles labels across vertices while preserving the observed
  number of each class.
- Expected counts are computed under the same fixed-composition null.
- p_upper and p_lower are separate one-sided plus-one Monte Carlo tail
  estimates. They are not multiple-testing adjusted.
- BB/WW joins describe same-class adjacency; BW joins describe cross-class
  adjacency. Interpret all three together with the graph and class prevalence.
- This is a small dense-matrix teaching implementation, not a sparse
  production spatial-weights engine.

See the [canonical algorithm note](../../../algorithms/statistics/join-count.md)
and [source verification record](../../../catalog/verification/join-count.md).
