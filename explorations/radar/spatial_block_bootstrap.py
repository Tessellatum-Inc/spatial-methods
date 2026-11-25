"""Spatial-block bootstrap helpers for matched spatial class contrasts."""
from __future__ import annotations
import numpy as np


def block_mean_contrast(block_contrasts):
    """Return equal-block mean of finite contrasts; each block is one replicate."""
    x=np.asarray(block_contrasts,dtype=float);x=x[np.isfinite(x)]
    if x.size==0:return None
    return float(x.mean())


def matched_block_contrasts(block_ids, class_codes, stratum_ids, residual_db, *, built_code=6, target_code=1):
    """Compute per-block target-minus-built MAE using only shared strata.

    Uses grouped bincount aggregation rather than rescanning all pixels for every
    block/stratum. Within each block, shared strata contribute equally.
    """
    b=np.asarray(block_ids,dtype=np.int64);c=np.asarray(class_codes);s=np.asarray(stratum_ids,dtype=np.int64);r=np.asarray(residual_db,dtype=float)
    if not (b.shape==c.shape==s.shape==r.shape):raise ValueError("Inputs must have matching shapes")
    valid=np.isfinite(r)&(b>=0)&(s>=0)&((c==built_code)|(c==target_code))
    b,c,s,r=b[valid],c[valid],s[valid],r[valid]
    if b.size==0:return []
    nstrata=int(s.max())+1
    nblocks=int(b.max())+1
    # Last key dimension is class: 0=built, 1=target.
    key=((b*nstrata+s)*2)+(c==target_code).astype(np.int64)
    total=nblocks*nstrata*2
    sums=np.bincount(key,weights=np.abs(r),minlength=total).reshape(nblocks,nstrata,2)
    counts=np.bincount(key,minlength=total).reshape(nblocks,nstrata,2)
    shared=(counts[:,:,0]>0)&(counts[:,:,1]>0)
    block_rows=[]
    for block in np.flatnonzero(shared.any(axis=1)):
        strata=np.flatnonzero(shared[block]);built_n=counts[block,strata,0];target_n=counts[block,strata,1]
        built_mae=sums[block,strata,0]/built_n;target_mae=sums[block,strata,1]/target_n
        diffs=target_mae-built_mae
        details=[{"stratum_id":int(st),"built_n":int(bn),"target_n":int(tn),
                  "built_mae_db":float(bm),"target_mae_db":float(tm),"difference_db":float(df)}
                 for st,bn,tn,bm,tm,df in zip(strata,built_n,target_n,built_mae,target_mae,diffs)]
        block_rows.append({"block_id":int(block),"matched_strata":len(details),
            "built_pixels":int(built_n.sum()),"target_pixels":int(target_n.sum()),
            "contrast_db":float(diffs.mean()),"strata":details})
    return block_rows


def bootstrap_interval(block_contrasts, *, replicates=2000, seed=20261125, min_blocks=20):
    """Percentile bootstrap resampling blocks, never individual pixels."""
    x=np.asarray(block_contrasts,dtype=float);x=x[np.isfinite(x)];n=int(x.size)
    if n<min_blocks:
        return {"estimate_db":block_mean_contrast(x),"lower_95_db":None,"upper_95_db":None,
                "eligible_blocks":n,"interval_status":"insufficient_blocks","minimum_blocks":int(min_blocks),
                "replicates":0,"seed":int(seed)}
    rng=np.random.default_rng(seed);draws=rng.choice(x,size=(replicates,n),replace=True).mean(axis=1)
    lo,hi=np.quantile(draws,[.025,.975])
    return {"estimate_db":float(x.mean()),"lower_95_db":float(lo),"upper_95_db":float(hi),
            "eligible_blocks":n,"interval_status":"percentile_block_bootstrap","minimum_blocks":int(min_blocks),
            "replicates":int(replicates),"seed":int(seed)}



def rook_morans_i(block_ids, block_values, *, grid_columns, min_blocks=20):
    """Descriptive rook-neighbour Moran's I for a regular block grid.

    Block IDs use the deterministic key row * grid_columns + column.
    Only immediately adjacent north/south/east/west eligible blocks are linked.
    No p-value is returned: this diagnostic describes remaining local spatial
    structure and does not establish independence or bootstrap validity.
    """
    ids = np.asarray(block_ids, dtype=np.int64)
    values = np.asarray(block_values, dtype=float)
    if ids.shape != values.shape:
        raise ValueError("Block IDs and values must have matching shapes")
    if grid_columns < 1:
        raise ValueError("grid_columns must be positive")
    valid = np.isfinite(values) & (ids >= 0)
    ids, values = ids[valid], values[valid]
    if np.unique(ids).size != ids.size:
        raise ValueError("Each eligible block ID must occur once")
    n = int(values.size)
    base = {"eligible_blocks": n, "neighbor_pairs": 0, "moran_i": None}
    if n < min_blocks:
        return {**base, "status": "insufficient_blocks"}
    if n < 2:
        return {**base, "status": "no_neighbour_pairs"}

    rows = ids // int(grid_columns)
    cols = ids % int(grid_columns)
    index = {(int(row), int(col)): i for i, (row, col) in enumerate(zip(rows, cols))}
    pairs = []
    for i, (row, col) in enumerate(zip(rows, cols)):
        for neighbour in ((int(row) + 1, int(col)), (int(row), int(col) + 1)):
            j = index.get(neighbour)
            if j is not None:
                pairs.append((i, j))
    pair_count = len(pairs)
    if pair_count == 0:
        return {**base, "status": "no_neighbour_pairs"}
    centred = values - values.mean()
    denominator = float(np.dot(centred, centred))
    if denominator <= 0:
        return {**base, "neighbor_pairs": pair_count, "status": "no_variation"}
    cross_product = sum(float(centred[i] * centred[j]) for i, j in pairs)
    # Symmetric binary weights: each undirected pair contributes twice to W
    # and twice to the cross-product numerator.
    moran = (n / pair_count) * (cross_product / denominator)
    return {
        "eligible_blocks": n,
        "neighbor_pairs": pair_count,
        "moran_i": float(moran),
        "status": "computed",
    }


def empirical_block_semivariogram(block_ids, block_values, *, grid_columns, block_size_m,
                                  lag_edges_blocks=(0.0, 1.5, 2.5, 4.5, 8.5, 16.5, float("inf")),
                                  min_pairs=10):
    """Descriptive empirical semivariogram of block contrasts on a regular grid.

    Distances are between block centroids, expressed in block-width units.
    Lag bins are left-closed/right-open. No model fitting or inferential
    uncertainty is implied; sparse bins are retained with an explicit status.

    Finite-distance pairs are enumerated through grid-neighbour lookups rather
    than all-pairs arrays. If the final lag edge is infinite, its count and
    semivariance are obtained by subtracting enumerated near pairs from the
    closed-form totals, avoiding quadratic work for the far-distance bin.
    """
    ids = np.asarray(block_ids, dtype=np.int64)
    values = np.asarray(block_values, dtype=float)
    edges = np.asarray(lag_edges_blocks, dtype=float)
    if ids.shape != values.shape:
        raise ValueError("Block IDs and values must have matching shapes")
    if grid_columns < 1 or block_size_m <= 0:
        raise ValueError("grid_columns and block_size_m must be positive")
    if edges.ndim != 1 or edges.size < 2 or edges[0] < 0 or np.any(np.diff(edges) <= 0):
        raise ValueError("lag_edges_blocks must be strictly increasing and non-negative")
    valid = np.isfinite(values) & (ids >= 0)
    ids, values = ids[valid], values[valid]
    if np.unique(ids).size != ids.size:
        raise ValueError("Each eligible block ID must occur once")

    rows = ids // int(grid_columns)
    cols = ids % int(grid_columns)
    n_bins = edges.size - 1
    pair_counts = np.zeros(n_bins, dtype=np.int64)
    semivariance_sums = np.zeros(n_bins, dtype=float)
    positions = {(int(row), int(col)): float(value)
                 for row, col, value in zip(rows, cols, values)}

    # The last bin is handled analytically when unbounded. Enumerate only
    # pairs strictly below its lower edge; otherwise enumerate to its upper edge.
    unbounded_tail = bool(np.isinf(edges[-1]))
    search_radius = float(edges[-2] if unbounded_tail else edges[-1])
    max_offset = int(np.ceil(search_radius))
    offsets = []
    for dr in range(-max_offset, max_offset + 1):
        for dc in range(-max_offset, max_offset + 1):
            distance = float(np.hypot(dr, dc))
            if distance <= 0 or distance >= search_radius:
                continue
            if dr > 0 or (dr == 0 and dc > 0):
                offsets.append((dr, dc, distance))

    for (row, col), value in positions.items():
        for dr, dc, distance in offsets:
            other = positions.get((row + dr, col + dc))
            if other is None:
                continue
            bin_index = int(np.searchsorted(edges, distance, side="right") - 1)
            if 0 <= bin_index < n_bins:
                pair_counts[bin_index] += 1
                semivariance_sums[bin_index] += 0.5 * (value - other) ** 2

    if unbounded_tail:
        n = int(values.size)
        total_pairs = n * (n - 1) // 2
        total_semivariance = 0.5 * (
            n * float(np.dot(values, values)) - float(values.sum()) ** 2
        )
        pair_counts[-1] = total_pairs - int(pair_counts[:-1].sum())
        semivariance_sums[-1] = total_semivariance - float(semivariance_sums[:-1].sum())

    result = []
    for i in range(n_bins):
        count = int(pair_counts[i])
        result.append({
            "lag_min_blocks": float(edges[i]),
            "lag_max_blocks": None if np.isinf(edges[i + 1]) else float(edges[i + 1]),
            "pair_count": count,
            "semivariance": float(semivariance_sums[i] / count) if count else None,
            "status": "computed" if count >= min_pairs else "insufficient_pairs",
        })
    return {
        "eligible_blocks": int(len(ids)),
        "block_size_m": int(block_size_m),
        "distance_unit": "block widths",
        "bins": result,
    }
