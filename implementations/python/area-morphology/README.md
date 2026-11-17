# Grayscale area morphology

NumPy reference implementation of grayscale area opening and closing using thresholded connected components.

For each distinct gray level, the algorithm labels connected components in the upper-level set. Bright components smaller than the requested pixel area are removed by taking the highest threshold at which each pixel belongs to a sufficiently large component. Area closing is implemented by duality on the negated raster. Four- and eight-neighbour connectivity are supported.

## Run

```bash
python -m pip install -r requirements.txt
python -m pytest -q
```

## Complexity and limits

This transparent threshold-stack implementation costs O(U*N) time and O(N) auxiliary memory per threshold, where U is the number of unique raster values and N is the number of cells. It is intended for small rasters and reproducibility, not large-scale image processing. It does not expose a canonical max-tree/min-tree, alpha-tree, shape attributes or general attribute filters. Pixel area is measured in cells; use an equal-area or otherwise appropriate raster grid when interpreting physical area.
