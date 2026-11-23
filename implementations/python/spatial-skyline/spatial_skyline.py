"""Location-aware multi-criteria skyline queries (block-nested-loop baseline)."""
from __future__ import annotations
import numpy as np

def spatial_skyline(query_point, locations, attributes, *, minimize=None):
    """Return original input indices in the spatial skyline.

    Squared Euclidean distance to query_point is always minimised. Attribute
    columns are minimised by default; set minimize[j] to False to maximise
    attribute j. Equal criterion vectors are retained as ties.
    """
    query=np.asarray(query_point,dtype=float)
    xy=np.asarray(locations,dtype=float)
    values=np.asarray(attributes,dtype=float)
    if query.shape!=(2,) or not np.isfinite(query).all():
        raise ValueError("query_point must be a finite 2D coordinate")
    if xy.ndim!=2 or xy.shape[1]!=2 or not np.isfinite(xy).all():
        raise ValueError("locations must be a finite N-by-2 array")
    if values.ndim!=2 or values.shape[0]!=len(xy) or values.shape[1]<1 or not np.isfinite(values).all():
        raise ValueError("attributes must be a finite N-by-K array with K >= 1")
    if minimize is None:
        directions=np.ones(values.shape[1],dtype=bool)
    else:
        directions=np.asarray(minimize)
        if directions.shape!=(values.shape[1],) or directions.dtype.kind!="b":
            raise ValueError("minimize must contain one boolean per attribute")
    criteria=np.column_stack((
        np.sum((xy-query)**2,axis=1),
        np.where(directions[None,:],values,-values),
    ))
    skyline=[]
    for index,candidate in enumerate(criteria):
        if any(np.all(criteria[j]<=candidate) and np.any(criteria[j]<candidate) for j in skyline):
            continue
        skyline=[j for j in skyline if not (
            np.all(candidate<=criteria[j]) and np.any(candidate<criteria[j])
        )]
        skyline.append(index)
    return tuple(sorted(skyline))
