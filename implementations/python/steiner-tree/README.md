# Exact Steiner tree for small terminal sets

A Dreyfus–Wagner subset dynamic program with shortest-path closure. Given an undirected weighted graph and a set of terminals, it returns an exact minimum-weight connected subgraph spanning all terminals. Non-terminal vertices may be included when they reduce total weight.

## Run

~~~bash
python -m pip install -r requirements.txt
python -m pytest -q
~~~

## Complexity and limitations

The dynamic program is exponential in the number of terminals (roughly O(3^k V + 2^k E log V)); the implementation defaults to a hard limit of 12 terminals to prevent accidental runaway work. Edge weights must be finite and strictly positive. Parallel edges are reduced to their minimum weight and self-loops ignored. The input is an undirected graph. This is an exact small-terminal reference method, not a scalable approximation or a Euclidean geometric Steiner solver.
