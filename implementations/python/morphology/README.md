# Binary mathematical morphology

Implements dilation, erosion, opening, closing and the dilation-minus-erosion boundary (morphological gradient) for 2-D binary arrays. The structuring element is an explicit nonempty boolean matrix, defaulting to a 3×3 square. Outside-image cells are treated as background for both dilation and erosion; this boundary convention is important and differs from some libraries' defaults.

This is a binary morphology baseline, not grayscale morphology, reconstruction, skeletonization, hit-or-miss or geodesic morphology.

```python
from morphology import opening, closing
clean = opening(binary_mask, structure=my_footprint)
filled = closing(clean, structure=my_footprint)
```

Run `pytest -q` in this directory.
