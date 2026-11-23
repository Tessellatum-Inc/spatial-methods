# Local Geary reference implementation

Small dense-matrix implementation of local Geary c_i and conditional
randomisation inference.

## Run

~~~bash
python -m pip install -r requirements.txt
python -m pytest -q
~~~

## Contract

- Computes the raw local statistic c_i = sum_j w_ij (x_i - x_j)^2.
- Does not silently row-standardise or otherwise rescale supplied weights.
- Conditional permutations hold the focal value fixed and reassign the
  remaining values without replacement; each focal row's weights are retained.
- p_sim is a two-sided, centred, plus-one Monte Carlo estimate. It is an
  explicit inference convention and is not claimed to duplicate all software
  package defaults.
- Islands receive local c=0 and p=1. Apply multiple-testing correction before
  interpreting a large set of local tests.
- Dense matrices suit small teaching cases; use sparse graph representations
  for larger datasets.

See the [canonical dossier](../../../algorithms/statistics/local-geary.md).
