"""Directional-dependence coverage experiment for spatial uncertainty methods."""
from __future__ import annotations
import json
import numpy as np

from explorations.radar.spatial_moving_block_bootstrap import moving_spatial_block_bootstrap_interval
from explorations.radar.spatial_hac import spatial_hac_mean_interval
from explorations.radar.spatial_subsampling import spatial_subsampling_mean_interval


def anisotropic_field(size, rho_rows, rho_columns, rng):
    field=rng.normal(size=(size,size))
    sr=np.sqrt(1-rho_rows*rho_rows)
    sc=np.sqrt(1-rho_columns*rho_columns)
    for row in range(1,size):
        field[row,:]=rho_rows*field[row-1,:]+sr*field[row,:]
    for col in range(1,size):
        field[:,col]=rho_columns*field[:,col-1]+sc*field[:,col]
    return field


def wilson(successes,trials,z=1.959963984540054):
    p=successes/trials; den=1+z*z/trials
    centre=(p+z*z/(2*trials))/den
    half=z*np.sqrt(p*(1-p)/trials+z*z/(4*trials*trials))/den
    return [float(centre-half),float(centre+half)]


def run(simulations=100,grid_size=30,orientations=((0.8,0.3),(0.3,0.8)),
        hac_bandwidths=((4,4),(8,4),(12,4),(4,8),(4,12),(8,8),(12,12)),
        square_widths=(8,12),bootstrap_replicates=250,seed=20261201):
    rng=np.random.default_rng(seed); ids=np.arange(grid_size*grid_size,dtype=np.int64)
    configs=[("spatial_hac",a,b) for a,b in hac_bandwidths]
    configs += [("moving_window",w,w) for w in square_widths]
    configs += [("subsampling",w,w) for w in square_widths]
    output=[]
    for rho_r,rho_c in orientations:
        stats={(m,a,b):{"covered":0,"widths":[]} for m,a,b in configs}
        for trial in range(simulations):
            y=anisotropic_field(grid_size,rho_r,rho_c,rng).ravel()
            for method,a,b in configs:
                if method=="spatial_hac":
                    res=spatial_hac_mean_interval(ids,y,grid_columns=grid_size,
                        bandwidth_rows=a,bandwidth_columns=b,min_blocks=20)
                    lo,hi=res["lower"],res["upper"]
                elif method=="moving_window":
                    res=moving_spatial_block_bootstrap_interval(ids,y,grid_columns=grid_size,
                        window_width_blocks=a,replicates=bootstrap_replicates,
                        seed=seed+trial*100+a,min_windows=20,min_blocks=20)
                    lo,hi=res["lower_95_db"],res["upper_95_db"]
                else:
                    res=spatial_subsampling_mean_interval(ids,y,grid_rows=grid_size,
                        grid_columns=grid_size,subsample_width_blocks=a,min_subwindows=20)
                    lo,hi=res["lower"],res["upper"]
                stats[(method,a,b)]["covered"]+=int(lo<=0<=hi)
                stats[(method,a,b)]["widths"].append(hi-lo)
        for (method,a,b),v in stats.items():
            output.append({"rho_rows":rho_r,"rho_columns":rho_c,"method":method,
                "bandwidth_or_width_rows":a,"bandwidth_or_width_columns":b,
                "simulations":simulations,"coverage":v["covered"]/simulations,
                "covered_simulations":v["covered"],
                "coverage_wilson_95":wilson(v["covered"],simulations),
                "mean_interval_width":float(np.mean(v["widths"]))})
    return {"schema":"tessellatum.spatial-uncertainty-anisotropy.v1",
        "design":"Same anisotropic field realizations evaluated by all candidate configurations.",
        "data_generating_process":"separable Gaussian AR(1) with distinct row and column correlations",
        "grid_size":[grid_size,grid_size],"seed":seed,"results":output,
        "limitations":["Complete regular grids only.",
            "Two anisotropy orientations and finite bandwidth grids only.",
            "No nominal coverage claim or automatic bandwidth selection.",
            "Matched-strata block contrasts and irregular masks remain untested."]}


if __name__=="__main__":
    print(json.dumps(run(),indent=2))
