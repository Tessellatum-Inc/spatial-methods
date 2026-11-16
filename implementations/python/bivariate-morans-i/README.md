# Bivariate Moran's I in Python

This package provides a small, dependency-free teaching implementation of global bivariate Moran's I. It relates one standardized variable at each location to the spatial lag of a second standardized variable.

## Run

```bash
python -m pip install -r requirements.txt
python -m pytest -q
```

## Example

```python
from bivariate_morans import bivariate_morans_i

weights = [
    [0, 1, 0, 0],
    [1, 0, 1, 0],
    [0, 1, 0, 1],
    [0, 0, 1, 0],
]
result = bivariate_morans_i(
    x=[1, 2, 3, 4],
    y=[2, 1, 4, 3],
    weights=weights,
    permutations=999,
    seed=2026,
)
print(result["I"], result["p_sim"])
```

## Contract and interpretation

The implementation uses sample-standardized variables, row-standardizes the supplied non-negative weights matrix, and calculates

```
I_xy = sum_i z(x)_i * sum_j w_ij z(y)_j / (n - 1)
```

This is asymmetric: exchanging x and y generally changes the result. It is not the ordinary univariate Moran's I applied to a single variable.

The optional conditional randomization holds x and W fixed and permutes y across locations. The reported two-sided pseudo-p-value compares absolute deviations from the simulated mean and applies the +1 correction. The random seed makes the simulation reproducible. This is an explicitly stated teaching convention; do not assume it matches every library's default tail convention.

## Input rules

- x and y must be finite numeric vectors of equal length, with at least two observations and non-zero sample variance.
- weights must be a finite, non-negative, square matrix aligned to the observations.
- diagonal weights must be zero; at least one positive link is required.
- rows with no outgoing links remain zero rows (islands).
- weights are row-standardized internally; the input is not modified.
- permutations must be a non-negative integer; zero disables inference.

The dense matrix implementation uses O(n²) time and memory per statistic. Permutation inference costs O(Mn²) for M permutations. It does not construct spatial neighbours, handle missing data, align geographic identifiers, fit a spatial model, or establish causal relationships. Validate the study design, spatial weights and null hypothesis before interpreting results.

For production spatial statistics and alternative inference conventions, consult [PySAL's Moran_BV reference](https://pysal.org/esda/stable/generated/esda.Moran_BV.html).
