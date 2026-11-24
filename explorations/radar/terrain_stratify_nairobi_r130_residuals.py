#!/usr/bin/env python3
"""Stratify Nairobi R130 residuals by Copernicus DEM slope and aspect."""
from __future__ import annotations
import argparse,json,sys
from pathlib import Path
import numpy as np
import rasterio
from rasterio.enums import Resampling
from rasterio.warp import reproject

SLOPE_EDGES=np.array([0,1,3,5,10,15,30,90],dtype=float)
ASPECT_NAMES=("N","NE","E","SE","S","SW","W","NW")

def terrain_derivatives(elevation,valid,pixel_size=30.0):
    z=np.asarray(elevation,dtype=np.float64); ok=np.asarray(valid,dtype=bool)&np.isfinite(z)
    h,w=z.shape
    dzdx=np.full(z.shape,np.nan); dzdy=np.full(z.shape,np.nan)
    core=ok[1:-1,1:-1]&ok[1:-1,:-2]&ok[1:-1,2:]&ok[:-2,1:-1]&ok[2:,1:-1]
    east=(z[1:-1,2:]-z[1:-1,:-2])/(2*pixel_size)
    north=(z[:-2,1:-1]-z[2:,1:-1])/(2*pixel_size)
    dzdx[1:-1,1:-1][core]=east[core]
    dzdy[1:-1,1:-1][core]=north[core]
    slope=np.degrees(np.arctan(np.hypot(dzdx,dzdy)))
    aspect=np.mod(np.degrees(np.arctan2(-dzdx,-dzdy)),360.0)
    slope[~np.isfinite(dzdx)|~np.isfinite(dzdy)]=np.nan
    aspect[(~np.isfinite(slope))|(slope<1.0)]=np.nan
    return slope,aspect,np.isfinite(slope)

def summarize(values):
    v=np.asarray(values,dtype=float);v=v[np.isfinite(v)]
    if not v.size:return {"count":0}
    a=np.abs(v)
    return {"count":int(v.size),"bias_mean_db":float(v.mean()),"mae_db":float(a.mean()),
      "rmse_db":float(np.sqrt(np.mean(v*v))),"p95_absolute_db":float(np.percentile(a,95)),
      "fraction_abs_gt_0_5_db":float(np.mean(a>0.5)),"fraction_abs_gt_1_db":float(np.mean(a>1.0))}

def strata(values,covariate,edges,labels):
    v=np.asarray(values);c=np.asarray(covariate);finite=np.isfinite(v)&np.isfinite(c);out=[]
    for i,label in enumerate(labels):
        m=finite&(c>=edges[i])&(c<edges[i+1])
        out.append({"bin":label,"lower":float(edges[i]),"upper_exclusive":float(edges[i+1]),**summarize(v[m])})
    return out

def reproject_dem(dem,template):
    with rasterio.open(dem) as src:
        elev=np.full((template.height,template.width),np.nan,dtype=np.float32)
        mask=np.full((template.height,template.width),0,dtype=np.uint8)
        source=np.where(src.read(2)>0.5,src.read(1),np.nan).astype(np.float32)
        reproject(source,elev,src_transform=src.transform,src_crs=src.crs,
          src_nodata=np.nan,dst_transform=template.transform,dst_crs=template.crs,
          dst_nodata=np.nan,resampling=Resampling.bilinear)
        reproject(src.read(2),mask,src_transform=src.transform,src_crs=src.crs,
          dst_transform=template.transform,dst_crs=template.crs,dst_nodata=0,
          resampling=Resampling.nearest)
        return elev,(mask>0)&np.isfinite(elev)

def run(dem_path:Path,residual_dir:Path,output:Path):
    maps=sorted(residual_dir.glob("*_delta-residual-db.tif"))
    if len(maps)!=30:raise ValueError(f"Expected 30 residual maps, found {len(maps)}")
    cache={};records=[]
    for path in maps:
        parts=path.name.split("_")
        date=parts[0];burst=parts[1];pol=parts[2]
        with rasterio.open(path) as residual:
            key=burst
            if key not in cache:
                elev,valid=reproject_dem(dem_path,residual)
                slope,aspect,terrain_valid=terrain_derivatives(elev,valid,pixel_size=abs(residual.res[0]))
                cache[key]=(slope,aspect,terrain_valid,elev)
            slope,aspect,terrain_valid,_=cache[key]
            values=residual.read(1).astype(np.float32)
            valid=(values!=residual.nodata)&np.isfinite(values)&terrain_valid
            v=values[valid];sl=slope[valid];asp=aspect[valid]
            slope_bins=strata(v,sl,SLOPE_EDGES,
              [f"{SLOPE_EDGES[i]:g}-{SLOPE_EDGES[i+1]:g}°" for i in range(len(SLOPE_EDGES)-1)])
            # Aspect is a circular variable; flat pixels are reported separately.
            aspect_bins=[]
            for i,name in enumerate(ASPECT_NAMES):
                m=valid&(slope>=1)&(aspect>=i*45)&(aspect<(i+1)*45)
                aspect_bins.append({"bin":name,"azimuth_from_deg":i*45,"azimuth_to_deg":(i+1)*45,**summarize(values[m])})
            flat=valid&(slope<1)
            records.append({"date":f"{date[:4]}-{date[4:6]}-{date[6:8]}","burst_id":burst,
              "polarization":pol,"overall":summarize(v),"slope_strata":slope_bins,
              "aspect_strata":aspect_bins,"flat_or_low_slope":summarize(values[flat]),
              "valid_terrain_pixels":int(valid.sum()),"slope_median_deg":float(np.median(sl)),
              "slope_p95_deg":float(np.percentile(sl,95))})
    report={"schema":"tessellatum.nairobi-r130-terrain-residual-stratification.v1",
      "terrain_source":"Copernicus DEM GLO-30 Public 2021 release via public AWS Open Data COG tiles.",
      "terrain_derivatives":"Central differences on each native OPERA grid at 30m pixel spacing; aspect is downslope azimuth clockwise from north; aspect omitted for slope below 1 degree.",
      "slope_edges_degrees":SLOPE_EDGES.tolist(),"aspect_bins_degrees":45,
      "records":records,"checks":{"records":len(records),"all_30_maps_stratified":len(records)==30},
      "limitations":["Copernicus DEM is a DSM containing buildings and vegetation, not bare-earth terrain.",
        "Nominal DEM source acquisition period is 2011-2015 and the output is oversampled to the requested grid; it does not provide 30m independent detail everywhere.",
        "Slope/aspect are descriptive covariates and may be correlated with ANF, land cover, local incidence angle, and spatial sampling.",
        "This stage does not establish causality or validate absolute backscatter."]}
    output.parent.mkdir(parents=True,exist_ok=True);output.write_text(json.dumps(report,indent=2)+"\n")
    print("Terrain diagnostic checks:",json.dumps(report["checks"],sort_keys=True),flush=True)
    for b in sorted({r["burst_id"] for r in records}):
      for pol in ("VV","VH"):
        rows=[r for r in records if r["burst_id"]==b and r["polarization"]==pol]
        n=sum(x["overall"]["count"] for x in rows)
        mae=sum(x["overall"]["count"]*x["overall"]["mae_db"] for x in rows)/n
        print(f"{b} {pol}: terrain-valid={n:,}; pixel-weighted MAE={mae:.4f} dB",flush=True)
        for field in ("slope_strata","aspect_strata"):
          agg={}
          for row in rows:
            for item in row[field]:
              if item["count"]:
                acc=agg.setdefault(item["bin"],[0,0.0,0.0])
                acc[0]+=item["count"];acc[1]+=item["count"]*item["mae_db"]
                acc[2]+=item["count"]*item["rmse_db"]
          summary=[{"bin":k,"count":v[0],"mae_db":round(v[1]/v[0],4),
                    "rmse_db":round(v[2]/v[0],4)} for k,v in agg.items()]
          print(f"{b} {pol} {field}: {json.dumps(summary,separators=(',',':'))}",flush=True)
    return report

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--dem",type=Path,default=Path("dem-assets/nairobi_copernicus_dem_glo30.tif"))
    p.add_argument("--residual-dir",type=Path,default=Path("residual-maps"))
    p.add_argument("--report",type=Path,default=Path("terrain-stratification.json"))
    a=p.parse_args()
    try:r=run(a.dem,a.residual_dir,a.report)
    except Exception as exc:print(f"Terrain stratification failed: {type(exc).__name__}: {exc}",file=sys.stderr);return 2
    return 0 if r["checks"]["all_30_maps_stratified"] else 1
if __name__=="__main__":raise SystemExit(main())
