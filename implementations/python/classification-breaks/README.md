# Classification breaks for spatial attributes

Six one-dimensional thematic classification methods with explicit contracts:

- Geometric interval breaks for strictly positive, right-skewed measurements.
- Standard-deviation breaks around the mean, clipped to the observed range.
- Box-plot breaks using quartiles and Tukey fences.
- Head/tail breaks for heavy-tailed distributions.
- Dalenius–Hodges approximate optimal stratification using square-root frequencies.
- Exact 1D ckmeans breaks via dynamic programming that minimises within-class squared error.

All functions return sorted numeric class boundaries including observed minimum and maximum where applicable. They do not choose map colours, handle missing values implicitly or determine the correct number of classes for a study.

```bash
python -m pip install -r requirements.txt
python -m pytest -q
```

See the [algorithm note](../../../algorithms/cartography/classification-breaks.md).
