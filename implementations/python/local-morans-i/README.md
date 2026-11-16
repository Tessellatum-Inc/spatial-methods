# Local Moran's I reference implementation

A dependency-light implementation of the local Moran statistic and conditional
randomisation inference for a dense spatial-weights matrix.

## Run

~~~bash
python -m pip install -r requirements.txt
python -m pytest -q
~~~

## Example

~~~python
from local_morans_i import local_morans_i

weights = [[0, 1, 0], [1, 0, 1], [0, 1, 0]]
result = local_morans_i([1.0, 2.0, 5.0], weights, permutations=999, seed=7)
print(result.local_i, result.quadrant, result.p_sim)
~~~

## Contract and interpretation

- Values are standardised with the population standard deviation.
- Local I uses the documented factor (n-1)/n and the supplied weights without
  silently changing their transformation.
- Conditional randomisation fixes the focal value and permutes the remaining
  values among locations; the focal row's weights stay fixed.
- p_sim is a two-sided, centred plus-one Monte Carlo estimate. This is an
  explicit convention, not a claim of byte-for-byte equivalence with PySAL,
  GeoDa or other software's tail conventions.
- Quadrants are coded 1=HH, 2=LH, 3=LL, 4=HL. Quadrants describe sign patterns,
  not significance. Apply a documented multiple-testing procedure before
  interpreting many local tests.
- Islands receive zero lag and p=1. Weights may be asymmetric and need not be
  row-standardised; self-weights must be zero.
- Dense matrices are intended for small teaching examples. Large spatial
  graphs should use sparse adjacency structures and specialised permutation
  implementations.

See the [canonical algorithm dossier](../../../algorithms/statistics/local-morans-i.md).
