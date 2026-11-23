# Getis-Ord G and Gi* reference implementations

This package contains two deliberately separate statistics:

- Global Getis-Ord G with a fixed-weights permutation reference distribution.
- Local Getis-Ord Gi* with binary self-inclusive weights and the analytical
  randomisation z-score.

## Run

~~~bash
python -m pip install -r requirements.txt
python -m pytest -q
~~~

## Important contracts

- Both methods require strictly positive values with a meaningful zero.
- Global G excludes diagonal pairs, reports E[G] = S0/(n(n-1)), and does
  not silently row-standardise weights.
- Global G permutation inference shuffles values among locations, holding
  weights fixed. Its p_sim is a centred, two-sided plus-one Monte Carlo
  estimate; this is not PySAL's one-sided p_sim convention.
- Gi* requires binary weights with the focal observation included on the
  diagonal. It returns a randomisation z-score and two-sided normal-tail
  approximation; it does not return permutation p-values.
- Neither statistic identifies causation. Local Gi* results require
  multiple-testing consideration before hotspot/coldspot mapping.

See the [Global G dossier](../../../algorithms/statistics/global-getis-ord-g.md)
and [Gi* dossier](../../../algorithms/statistics/getis-ord-gi-star.md).
