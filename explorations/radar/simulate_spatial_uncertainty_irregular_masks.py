"""Coverage diagnostic under irregular spatial eligibility masks."""
from __future__ import annotations
import json
import numpy as np

from explorations.radar.simulate_moving_spatial_block_bootstrap import separable_ar1_field
from explorations.radar.spatial_moving_block_bootstrap import moving_spatial_block_bootstrap_interval
from explorations.radar.spatial_hac import spatial_hac_mean_interval
from explorations.radar.spatial_subsampling import spatial_subsampling_mean_interval


def make_mask(size, scenario, rng):
    mask=np.ones((size,size),dtype=bool)
    if scenario=="random_20pct_holes":
        mask=rng.random((size,size))>=0.20
    elif scenario=="single_clustered_hole":
        r=int(rng.integers(4,size-10)); c=int(rng.integers(4,size-10))
        mask[r:r+8,c:c+8]=False
    elif scenario=="edge_truncated_plus_holes":
        mask[int(size*0.18):,:]=True
        mask[:int(size*0.18),:]=False
        mask &= rng.random((size,size))>=0.08
    elif scenario=="multiple_clustered_holes":
        for _ in range(3):
            r=int(rng.integers(0,size-5)); c=int(rng.integers(0,size-5))
            mask[r:r+5,c:c+5]=False
    else:
        raise ValueError(scenario)
    return mask


def wilson(successes,trials,z=1.959963984540054):
    p=successes/trials; den=1+z*z/trials
    centre=(p+z*z/(2*trials))/den
    half=z*np.sqrt(p*(1-p)/trials+z*z/(4*trials*trials))/den
    return [float(centre-half),float(centre+half)]


def run(simulations=100,grid_size=30,correlations=(0.3,0.6,0.8),
        masks=("random_20pct_holes","single_clustered_hole",
               "edge_truncated_plus_holes","multiple_clustered_holes"),
        widths=(4,8,12),bootstrap_replicates=250,seed=20261202):
    rng=np.random.default_rng(seed); output=[]
    all_ids=np.arange(grid_size*grid_size,dtype=np.int64)
    for rho in correlations:
        for scenario in masks:
            stats={(method,w):{"covered":0,"widths":[]} for method in
                   ("moving_window","spatial_hac","subsampling") for w in widths}
            eligible_counts=[]
            for trial in range(simulations):
                y=separable_ar1_field(grid_size,rho,rng).ravel()
                mask=make_mask(grid_size,scenario,rng).ravel()
                ids=all_ids[mask]; values=y[mask]
                eligible_counts.append(int(ids.size))
                for w in widths:
                    results={
                        "moving_window":moving_spatial_block_bootstrap_interval(
                            ids,values,grid_columns=grid_size,window_width_blocks=w,
                            replicates=bootstrap_replicates,seed=seed+trial*100+w,
                            min_windows=20,min_blocks=20),
                        "spatial_hac":spatial_hac_mean_interval(
                            ids,values,grid_columns=grid_size,bandwidth_rows=w,
                            bandwidth_columns=w,min_blocks=20),
                        "subsampling":spatial_subsampling_mean_interval(
                            ids,values,grid_rows=grid_size,grid_columns=grid_size,
                            subsample_width_blocks=w,min_subwindows=20),
                    }
                    for method,res in results.items():
                        if method=="subsampling" and res["interval_status"]=="irregular_mask_unsupported":
                            continue
                        lo=res["lower_95_db"] if method=="moving_window" else res["lower"]
                        hi=res["upper_95_db"] if method=="moving_window" else res["upper"]
                        stats[(method,w)]["covered"]+=int(lo<=0<=hi)
                        stats[(method,w)]["widths"].append(hi-lo)
            for (method,w),v in stats.items():
                valid=len(v["widths"])
                output.append({"rho":float(rho),"mask_scenario":scenario,
                    "method":method,"width_blocks":int(w),
                    "simulations":int(simulations),"valid_intervals":valid,
                    "unsupported_intervals":int(simulations-valid),
                    "coverage":v["covered"]/valid if valid else None,
                    "coverage_wilson_95":wilson(v["covered"],valid) if valid else None,
                    "mean_interval_width":float(np.mean(v["widths"])) if valid else None,
                    "mean_eligible_blocks":float(np.mean(eligible_counts))})
    return {"schema":"tessellatum.spatial-uncertainty-irregular-mask.v1",
        "design":"Same generated field and eligibility mask passed to supported methods.",
        "data_generating_process":"mean-zero separable Gaussian AR(1) field",
        "grid_size":[grid_size,grid_size],"seed":seed,
        "results":output,
        "limitations":["Stationary isotropic Gaussian fields only.",
            "Masks are independent of field values but include random and clustered geometry.",
            "Spatial subsampling deliberately reports unsupported for irregular masks.",
            "No matched-strata/block-contrast or nonstationarity evaluation."]}


if __name__=="__main__":
    print(json.dumps(run(),indent=2))
