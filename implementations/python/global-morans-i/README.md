# Global Moran's I in Python

This small reference implementation shows how the global Moran's I statistic is calculated from a numeric attribute and a spatial weights matrix.

It is deliberately dependency-free so the calculation is easy to read. It now includes random-labelling permutation inference with seeded reproducibility, one- and two-sided alternatives, and a plus-one pseudo-p-value correction.

## What the example includes

- a direct implementation of the global Moran's I formula;
- a row-standardisation helper;
- random-labelling permutation inference with a reported null expectation and simulation summary;
- validation for misaligned inputs, non-finite values, negative weights, self-weights, constant data and zero-weight matrices;
- tests for positive and negative spatial association, weight transformations and mathematical invariance properties.

## Run it

From this directory:

```bash
python -m pip install -r requirements.txt
python - <<'PY'
from moran_i import morans_i, row_standardize

weights = [
    [0, 1, 0, 0],
    [1, 0, 1, 0],
    [0, 1, 0, 1],
    [0, 0, 1, 0],
]

print(morans_i([1, 2, 3, 4], weights))
print(morans_i([1, 4, 1, 4], weights))
print(morans_i([1, 2, 3, 4], row_standardize(weights)))
PY
```

Expected output:

```text
0.3333333333333333
-1.0
0.4
```

The first sequence has similar values next to one another. The second alternates high and low values. The third repeats the first sequence after row-standardising the weights; its value changes because the weights changed.

## Run the tests

```bash
python -m pytest -q
```

## Step-by-step walkthrough

Follow the [implementation walkthrough](implementation-walkthrough.md) to trace the weights validation, centring, numerator, denominator and final formula.

## Important limitations

- The implementation uses a dense matrix, so its time and memory requirements grow quadratically with the number of spatial units.
- It assumes non-negative weights and a zero diagonal.
- It does not check that the weights are symmetric or that they represent a defensible spatial relationship.
- It does not handle missing data, construct neighbours from geometry or align geographic IDs.
- It does not implement analytical significance, spatially constrained permutations, or multiple-testing correction.

For spatial weights construction and statistical inference, use a maintained library such as [PySAL](https://pysal.org/). The [official global Moran's I guide](https://pysal.org/esda/stable/user-guide/global_morans_i.html) demonstrates contiguity weights, spatial lags, analytical inference and permutation tests.

## Reproduce

The tests use a four-unit chain and check the hand-calculated examples in the [canonical lesson](../../../algorithms/statistics/global-morans-i.md).



## Distance-band Moran correlogram

`morans_i_correlogram(points, values, distance_edges)` builds a symmetric
binary neighbour graph independently for each non-overlapping Euclidean
distance band and returns Moran's I, link count and randomisation expectation.
The final band includes its upper edge; earlier bands are half-open. Empty
bands return a null statistic. Optional row standardisation leaves isolates
as zero rows. This is descriptive, not a multiple-testing procedure or a
formal correlogram significance envelope.
