# Spatial skyline queries

A dependency-light exact block-nested-loop baseline for location-aware multi-criteria skyline queries.

Each object has a planar location and numeric attributes. Squared Euclidean distance to the query point is always minimised. Attribute columns are minimised by default; pass `minimize=[True, False, ...]` to maximise selected columns.

Object A dominates B when A is no worse on every criterion and strictly better on at least one. Identical criterion vectors are retained as ties.

```python
from spatial_skyline import spatial_skyline
locations = [(1, 0), (2, 0), (3, 0), (4, 0)]
attributes = [[8], [5], [9], [2]]
print(spatial_skyline((0, 0), locations, attributes))
# (0, 1, 3)
```

The block-nested-loop implementation takes O(n²k) worst-case time and O(sk) working memory, where n is object count, k criteria and s current skyline size. It is a transparent reference implementation, not an indexed large-scale query engine. Coordinates must use a common planar Cartesian CRS; Euclidean distance in longitude/latitude degrees is not appropriate. Network distance, textual relevance, uncertain dominance and approximate skyline semantics are not included.

```bash
python -m pip install -r requirements.txt
python -m pytest -q
```

See the [algorithm note](../../../algorithms/query-processing/spatial-skyline.md) and [tests](test_spatial_skyline.py).
