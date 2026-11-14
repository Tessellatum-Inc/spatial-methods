# Spatial distribution shift

This package implements a small block-level MMD two-sample test. It uses whole spatial blocks as the permutation unit and makes the exchangeability assumption explicit. See the [method lesson](../../../methods/spatial-distribution-shift.md) and [lab notebook](../../../notebooks/spatial-block-permutation-mmd-lab.ipynb).

Run from this directory:

```bash
python -m pip install -r requirements.txt
python -m pytest -q --import-mode=importlib
```

This is a dense educational baseline, not a universal spatial permutation test. See the method record for assumptions and limitations.
