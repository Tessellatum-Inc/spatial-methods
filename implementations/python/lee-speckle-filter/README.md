# Lee local-statistics speckle filter

A NumPy-only scalar-intensity Lee-style filter. Each pixel is blended with its
local mean according to an estimated signal-to-observed-variance ratio.
Noise variance is explicit, windows are odd square footprints, borders use
edge replication, and NaN cells are ignored and preserved.

## Run

```bash
python -m pip install -r requirements.txt
python -m pytest -q
```

```python
import numpy as np
from lee_filter import lee_filter

image = np.array([[10., 11., 9.], [10., 80., 11.], [9., 10., 10.]])
result = lee_filter(image, noise_variance=25.0, window_size=3)
```

## Scope and limitations

This is a transparent teaching baseline for a scalar image with an additive,
locally stationary noise-variance model. SAR intensity speckle is commonly
multiplicative; transform-domain or distribution-aware noise estimation may
be required before applying this model. It does not implement directional
Refined Lee filtering, multi-looking, polarimetric covariance filtering,
sensor calibration, or a production SAR processing chain. The supplied
noise variance is a modelling input, not estimated automatically.
