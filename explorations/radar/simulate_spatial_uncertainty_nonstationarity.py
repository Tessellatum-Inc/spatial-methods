"""Coverage diagnostics under nonstationarity and informative missingness.

The target is the finite full-grid mean (constructed to be zero in expectation).
Methods receive only eligible cells. Value-dependent masks intentionally violate
the independent-mask assumption and expose selection bias; no missingness
correction is attempted. This is a stress test, not a calibration exercise.
"""
from __future__ import annotations
import json
import numpy as np

from explorations.radar.spatial_moving_block_bootstrap import moving_spatial_block_bootstrap_interval
from explorations.radar.spatial_hac import spatial_hac_mean_interval
from explorations.radar.spatial_subsampling import spatial_subsampling_mean_interval


def make_field(size, scenario, rng):
    noise = rng.normal(size=(size, size))
    rows, cols = np.indices((size, size))
    if scenario == "smooth_gradient":
        trend = 1.2 * (cols / (size - 1) - 0.5)
        return trend + noise * 0.65
    if scenario == "variance_gradient":
        scale = 0.35 + 1.3 * cols / (size - 1)
        field = noise * scale
        return field - field.mean()
    if scenario == "abrupt_mean_boundary":
        trend = np.where(cols < size // 2, -0.9, 0.9)
        return trend + noise * 0.65
    raise ValueError(scenario)


def wilson(successes, trials, z=1.959963984540054):
    p=successes/trials; den=1+z*z/trials
    centre=(p+z*z/(2*trials))/den
    half=z*np.sqrt(p*(1-p)/trials+z*z/(4*trials*trials))/den
    return [float(centre-half),float(centre+half)]


def run(simulations=80, grid_size=24, seed=20261203,
        hac_bandwidths=(3,6), widths=(4,6), bootstrap_replicates=200):
    rng=np.random.default_rng(seed)
    ids_all=np.arange(grid_size*grid_size,dtype=np.int64)
    scenarios=("smooth_gradient","variance_gradient","abrupt_mean_boundary",
               "informative_high_value_missingness")
    methods=[("spatial_hac",w) for w in hac_bandwidths]
    methods += [(m,w) for m in ("moving_window","subsampling") for w in widths]
    output=[]
    for scenario in scenarios:
        stats={(m,w):{"covered":0,"widths":[],"valid":0,"unsupported":0,
                      "biases":[]} for m,w in methods}
        eligible=[]
        for trial in range(simulations):
            if scenario=="informative_high_value_missingness":
                # Stationary correlated noise; high values are preferentially absent.
                white=rng.normal(size=(grid_size,grid_size))
                field=white.copy()
                for rr in range(1,grid_size):
                    field[rr,:]=0.55*field[rr-1,:]+np.sqrt(1-0.55**2)*field[rr,:]
                for cc in range(1,grid_size):
                    field[:,cc]=0.55*field[:,cc-1]+np.sqrt(1-0.55**2)*field[:,cc]
                # Selection is explicitly a function of the observed value.
                threshold=np.quantile(field,0.22)
                mask=field<=threshold
            else:
                field=make_field(grid_size,scenario,rng)
                mask=np.ones((grid_size,grid_size),dtype=bool)
            y=field.ravel()
            ids=ids_all[mask.ravel()]
            values=y[mask.ravel()]
            truth=float(y.mean())
            eligible.append(int(ids.size))
            for method,w in methods:
                if method=="spatial_hac":
                    res=spatial_hac_mean_interval(ids,values,grid_columns=grid_size,
                        bandwidth_rows=w,bandwidth_columns=w,min_blocks=20)
                    lo,hi=res["lower"],res["upper"]
                    status=res["interval_status"]
                elif method=="moving_window":
                    res=moving_spatial_block_bootstrap_interval(ids,values,
                        grid_columns=grid_size,window_width_blocks=w,
                        replicates=bootstrap_replicates,seed=seed+trial*31+w,
                        min_windows=20,min_blocks=20)
                    lo,hi=res["lower_95_db"],res["upper_95_db"]
                    status=res["interval_status"]
                else:
                    res=spatial_subsampling_mean_interval(ids,values,
                        grid_rows=grid_size,grid_columns=grid_size,
                        subsample_width_blocks=w,min_subwindows=20)
                    lo,hi=res["lower"],res["upper"]
                    status=res["interval_status"]
                s=stats[(method,w)]
                if lo is None or hi is None:
                    s["unsupported"]+=1
                    continue
                s["valid"]+=1
                s["covered"]+=int(lo<=truth<=hi)
                s["widths"].append(float(hi-lo))
                s["biases"].append(float(res["estimate"]-truth if method=="spatial_hac"
                    else res["estimate_db"]-truth if method=="moving_window"
                    else res["estimate"]-truth))
        for (method,w),s in stats.items():
            n=s["valid"]
            output.append({"scenario":scenario,"method":method,"bandwidth_or_width":w,
                "simulations":simulations,"valid_intervals":n,
                "unsupported_intervals":s["unsupported"],
                "coverage":s["covered"]/n if n else None,
                "coverage_wilson_95":wilson(s["covered"],n) if n else None,
                "mean_interval_width":float(np.mean(s["widths"])) if n else None,
                "mean_estimate_bias":float(np.mean(s["biases"])) if n else None,
                "mean_eligible_cells":float(np.mean(eligible))})
    return {"schema":"tessellatum.spatial-uncertainty-nonstationarity.v1",
        "design":"Same field realizations passed to all available methods; coverage target is the finite full-grid mean.",
        "grid_size":[grid_size,grid_size],"seed":seed,"results":output,
        "scenarios":{
          "smooth_gradient":"Deterministic spatial mean gradient plus independent noise.",
          "variance_gradient":"Column-varying noise scale, field recentered to zero.",
          "abrupt_mean_boundary":"Two-region mean discontinuity plus independent noise.",
          "informative_high_value_missingness":"Correlated field; upper 22% removed by a value-dependent eligibility rule."},
        "limitations":["Small simulation and tuning grid; exploratory only.",
          "Informative missingness is not corrected; intervals target the full-grid mean despite value-dependent selection.",
          "No matched-strata/block-contrast estimand, heteroskedastic spatial dependence model, or calibration claim.",
          "Spatial subsampling is expected to refuse the irregular informative-missingness mask."]}


if __name__=="__main__":
    print(json.dumps(run(),indent=2))
