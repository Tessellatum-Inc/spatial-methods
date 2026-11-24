#!/usr/bin/env python3
"""Test whether Nairobi R130 residual outliers concentrate near common-support edges."""
from __future__ import annotations
import argparse,json,sys
from pathlib import Path
import numpy as np
import rasterio

RADII=(1,2,5,10,20)

def dilate8(mask):
    m=np.asarray(mask,dtype=bool);h,w=m.shape
    p=np.pad(m,1,constant_values=False)
    out=np.zeros_like(m)
    for dr in range(3):
        for dc in range(3):
            out |= p[dr:dr+h,dc:dc+w]
    return out

def support_edge_distance(valid,max_radius=max(RADII)):
    valid=np.asarray(valid,dtype=bool)
    invalid=~valid
    padded=np.pad(invalid,1,constant_values=True)
    touches=np.zeros_like(valid)
    h,w=valid.shape
    for dr in range(3):
        for dc in range(3):
            if dr==1 and dc==1:continue
            touches |= padded[dr:dr+h,dc:dc+w]
    frontier=valid&touches
    distance=np.zeros(valid.shape,dtype=np.uint8)
    distance[frontier]=1
    reached=frontier.copy()
    for radius in range(2,max_radius+1):
        expanded=dilate8(frontier)&valid&~reached
        distance[expanded]=radius
        reached |= expanded
        frontier=expanded
        if not frontier.any():break
    return distance

def metrics(values):
    v=np.asarray(values,dtype=float);v=v[np.isfinite(v)]
    if not v.size:return {"count":0}
    a=np.abs(v)
    return {"count":int(v.size),"mae_db":float(a.mean()),
      "rmse_db":float(np.sqrt(np.mean(v*v))),
      "fraction_abs_gt_0_5_db":float(np.mean(a>0.5)),
      "fraction_abs_gt_1_db":float(np.mean(a>1.0)),
      "fraction_abs_gt_2_db":float(np.mean(a>2.0))}

def analyze_map(path:Path):
    with rasterio.open(path) as ds:
        a=ds.read(1).astype(np.float32)
        valid=(a!=ds.nodata)&np.isfinite(a)
        distance=support_edge_distance(valid)
        values=a[valid]
        overall=metrics(values)
        buffers=[]
        for radius in RADII:
            selected=valid&(distance>0)&(distance<=radius)
            buffers.append({"within_pixels":radius,"within_meters_approx":radius*abs(ds.res[0]),
              **metrics(a[selected])})
        interior=valid&(distance==0)
        return {"file":path.name,"overall":overall,"edge_buffers":buffers,
          "interior_beyond_20_pixels":metrics(a[interior]),
          "edge_pixel_count":int(np.sum(valid&(distance==1))),
          "interior_pixel_count":int(interior.sum()),
          "grid_resolution":list(ds.res),"crs":ds.crs.to_string()}

def run(residual_dir:Path,report_path:Path):
    paths=sorted(residual_dir.glob("*_delta-residual-db.tif"))
    if len(paths)!=30:raise ValueError(f"Expected 30 residual maps, found {len(paths)}")
    records=[analyze_map(p) for p in paths]
    report={"schema":"tessellatum.nairobi-r130-support-edge-residual-diagnostics.v1",
      "definition":"Support edge is a valid residual pixel with at least one invalid 8-neighbour; distance is 8-connected pixel distance inward from that edge.",
      "radii_pixels":list(RADII),"approximate_pixel_size_m":30,
      "records":records,
      "checks":{"all_30_maps_processed":len(records)==30,
        "all_maps_have_valid_pixels":all(x["overall"]["count"]>0 for x in records)},
      "limitations":["Residual nodata combines OPERA and Sentinel Hub mask/support failures; this test cannot identify which provider's mask caused an edge.",
        "A 30m pixel-distance buffer is a grid-space approximation, not a terrain-following or exact Euclidean distance.",
        "Edge association is descriptive and does not establish why residuals are elevated.",
        "No pixels are excluded from the primary comparison."]}
    report_path.parent.mkdir(parents=True,exist_ok=True)
    report_path.write_text(json.dumps(report,indent=2)+"\n")
    print("Edge diagnostic checks:",json.dumps(report["checks"],sort_keys=True),flush=True)
    for burst in sorted({x["file"].split("_")[1] for x in records}):
      for pol in ("VV","VH"):
        rows=[x for x in records if burst in x["file"] and f"_{pol}_" in x["file"]]
        n=sum(x["overall"]["count"] for x in rows)
        for radius in (1,5,10,20):
          buf=[x["edge_buffers"][RADII.index(radius)] for x in rows]
          count=sum(x["count"] for x in buf)
          exceed=sum(x["count"]*x["fraction_abs_gt_1_db"] for x in buf if x["count"])
          frac=exceed/count if count else 0
          print(f"{burst} {pol} edge<= {radius}px: n={count:,}; >1dB={frac:.4%}",flush=True)
        inside=[x["interior_beyond_20_pixels"] for x in rows]
        ni=sum(x["count"] for x in inside)
        ei=sum(x["count"]*x["fraction_abs_gt_1_db"] for x in inside if x["count"])
        print(f"{burst} {pol} interior>20px: n={ni:,}; >1dB={ei/ni if ni else 0:.4%}",flush=True)
    return report

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--residual-dir",type=Path,default=Path("residual-maps"))
    p.add_argument("--report",type=Path,default=Path("support-edge-diagnostics.json"))
    a=p.parse_args()
    try:r=run(a.residual_dir,a.report)
    except Exception as exc:print(f"Support-edge diagnostics failed: {type(exc).__name__}: {exc}",file=sys.stderr);return 2
    return 0 if all(r["checks"].values()) else 1
if __name__=="__main__":raise SystemExit(main())
