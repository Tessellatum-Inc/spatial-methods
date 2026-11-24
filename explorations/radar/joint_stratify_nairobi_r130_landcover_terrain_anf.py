#!/usr/bin/env python3
"""Compare Dynamic World classes within matched burst/date/polarization, slope and ANF strata."""
from __future__ import annotations
import argparse,json,sys
from datetime import date as calendar_date
from pathlib import Path
import numpy as np
import rasterio
from rasterio.enums import Resampling
from rasterio.warp import reproject

CLASSES=("water","trees","grass","flooded_vegetation","crops","shrub_and_scrub","built","bare","snow_and_ice")
SLOPE_EDGES=np.array([0,1,3,5,10,15,30,90],dtype=float)
CONFIDENCE=(0.0,0.5,0.7)
def report_date(token):
    if not isinstance(token,str) or len(token)!=10 or token[4]!="-" or token[7]!="-":
        raise ValueError(f"Expected YYYY-MM-DD date token, got {token!r}")
    return calendar_date.fromisoformat(token).isoformat()
def summarize(v):
    x=np.asarray(v,dtype=np.float64);x=x[np.isfinite(x)]
    if not x.size:return {"count":0}
    a=np.abs(x)
    return {"count":int(x.size),"mae_db":float(a.mean()),"rmse_db":float(np.sqrt(np.mean(x*x))),
            "bias_mean_db":float(x.mean())}
def one(folder,pattern,label):
    hits=sorted(folder.glob(pattern))
    if len(hits)!=1:raise ValueError(f"Expected one {label}; found {[p.name for p in hits]}")
    return hits[0]
def static_file(folder,burst,suffix):
    hits=[p for p in folder.glob("*.tif") if burst in p.name and p.name.endswith(suffix)
          and not(suffix=="_incidence_angle.tif" and p.name.endswith("_local_incidence_angle.tif"))]
    if len(hits)!=1:raise ValueError(f"Expected one {suffix} for {burst}; found {[p.name for p in hits]}")
    return hits[0]
def align(src_path,template,band,resampling,dtype,nodata):
    out=np.full((template.height,template.width),nodata,dtype=dtype)
    with rasterio.open(src_path) as src:
        reproject(src.read(band),out,src_transform=src.transform,src_crs=src.crs,src_nodata=src.nodata,
          dst_transform=template.transform,dst_crs=template.crs,dst_nodata=nodata,resampling=resampling)
    return out
def terrain(elev,valid,pixel_size):
    z=np.asarray(elev,dtype=np.float64);ok=np.asarray(valid,bool)&np.isfinite(z)
    dx=np.full(z.shape,np.nan);dy=np.full(z.shape,np.nan)
    core=ok[1:-1,1:-1]&ok[1:-1,:-2]&ok[1:-1,2:]&ok[:-2,1:-1]&ok[2:,1:-1]
    east=(z[1:-1,2:]-z[1:-1,:-2])/(2*pixel_size)
    north=(z[:-2,1:-1]-z[2:,1:-1])/(2*pixel_size)
    dx[1:-1,1:-1][core]=east[core];dy[1:-1,1:-1][core]=north[core]
    slope=np.degrees(np.arctan(np.hypot(dx,dy)))
    slope[~np.isfinite(dx)|~np.isfinite(dy)]=np.nan
    return slope
def reproject_dem(path,template):
    with rasterio.open(path) as src:
        src_e=np.where(src.read(2)>0.5,src.read(1),np.nan).astype(np.float32)
        elev=np.full((template.height,template.width),np.nan,dtype=np.float32)
        mask=np.zeros((template.height,template.width),dtype=np.uint8)
        reproject(src_e,elev,src_transform=src.transform,src_crs=src.crs,src_nodata=np.nan,
          dst_transform=template.transform,dst_crs=template.crs,dst_nodata=np.nan,resampling=Resampling.bilinear)
        reproject(src.read(2),mask,src_transform=src.transform,src_crs=src.crs,
          dst_transform=template.transform,dst_crs=template.crs,dst_nodata=0,resampling=Resampling.nearest)
    return elev,(mask>0)&np.isfinite(elev)
def process(residual_path,opera_dir,dw_dir,dem_path):
    date,burst,pol=residual_path.name.split("_")[:3]
    report_date(date)
    dw_path=dw_dir/f"nairobi_r130_{date}_dynamic-world-30m.tif"
    if not dw_path.is_file():raise FileNotFoundError(dw_path)
    rtc=opera_dir/"rtc";static=opera_dir/"static"
    anf_path=static_file(static,burst,"_rtc_anf_gamma0_to_beta0.tif")
    with rasterio.open(residual_path) as residual:
      shape=(residual.height,residual.width);grid=(residual.crs,residual.transform,residual.width,residual.height)
      values=residual.read(1).astype(np.float32)
      rv=np.isfinite(values)
      if residual.nodata is not None:rv &= values!=residual.nodata
      anf=align(anf_path,residual,1,Resampling.nearest,np.float32,np.nan)
      # DEM-derived slope is calculated on the target native OPERA burst grid.
      elev,dem_valid=reproject_dem(dem_path,residual)
      slope=terrain(elev,dem_valid,abs(residual.res[0]))
      klass=align(dw_path,residual,1,Resampling.nearest,np.uint8,255)
      conf=align(dw_path,residual,2,Resampling.average,np.float32,np.nan)
      valid=rv&np.isfinite(anf)&(anf>0)&np.isfinite(slope)&(klass<=8)&np.isfinite(conf)&(conf>0)&(conf<=1)
      if int(valid.sum())<1000:raise ValueError(f"{residual_path.name}: only {valid.sum()} joint valid pixels")
      # ANF quartile edges are scene-specific; strata only compare within this scene.
      anf_edges=np.unique(np.quantile(anf[valid],[0,.25,.5,.75,1]))
      if len(anf_edges)<2:raise ValueError(f"{residual_path.name}: ANF has no usable spread")
      slope_bin=np.digitize(slope,SLOPE_EDGES[1:-1],right=False)
      anf_bin=np.digitize(anf,anf_edges[1:-1],right=False)
      rows=[]
      for threshold in CONFIDENCE:
        selected=valid&(conf>=threshold)
        cells={}
        for s in range(len(SLOPE_EDGES)-1):
          for a in range(len(anf_edges)-1):
            base=selected&(slope_bin==s)&(anf_bin==a)
            if not base.any():continue
            for code,name in enumerate(CLASSES):
              m=base&(klass==code)
              if m.any():
                met=summarize(values[m])
                cells[(s,a,code)]={"count":met["count"],"mae_db":met["mae_db"],"rmse_db":met["rmse_db"],"bias_mean_db":met["bias_mean_db"]}
        totals={}
        for code,name in enumerate(CLASSES):
          items=[v for (s,a,c),v in cells.items() if c==code]
          n=sum(x["count"] for x in items)
          if n:
            totals[name]={"count":n,"mae_db":sum(x["count"]*x["mae_db"] for x in items)/n,
                          "rmse_db":float(np.sqrt(sum(x["count"]*x["rmse_db"]**2 for x in items)/n))}
        matched=[]
        # Built is the reference class. Contrast is computed only in identical
        # scene/slope/ANF cells containing both built and the comparison class.
        for code,name in enumerate(CLASSES):
          if name=="built":continue
          pairs=[]
          for s in range(len(SLOPE_EDGES)-1):
            for a in range(len(anf_edges)-1):
              b=cells.get((s,a,6));other=cells.get((s,a,code))
              if b and other:
                pairs.append({"slope_bin":int(s),"anf_quartile":int(a),
                  "built_n":b["count"],"class_n":other["count"],
                  "built_mae_db":b["mae_db"],"class_mae_db":other["mae_db"],
                  "class_minus_built_mae_db":other["mae_db"]-b["mae_db"]})
          n_class=sum(x["class_n"] for x in pairs);n_built=sum(x["built_n"] for x in pairs)
          if pairs:
            # Equal weight per matched cell prevents the largest pixel stratum
            # from entirely defining the contrast. This is descriptive, not inferential.
            matched.append({"class_name":name,"matched_cells":len(pairs),
              "class_pixels_in_matched_cells":n_class,"built_pixels_in_matched_cells":n_built,
              "mean_within_cell_mae_difference_db":float(np.mean([x["class_minus_built_mae_db"] for x in pairs])),
              "cell_details":pairs})
        rows.append({"minimum_confidence":threshold,"observed_pixels":int(selected.sum()),
          "coverage_of_residual_valid_pixels":float(selected.sum()/rv.sum()) if rv.sum() else 0,
          "class_totals":totals,"matched_to_built":matched})
      return {"date":report_date(date),"burst_id":burst,"polarization":pol,
        "residual_valid_pixels":int(rv.sum()),"joint_valid_pixels":int(valid.sum()),
        "slope_bins_degrees":SLOPE_EDGES.tolist(),"anf_quartile_edges_scene_specific":[float(x) for x in anf_edges],
        "confidence_sensitivity":rows}
def run(residual_dir,opera_dir,dw_dir,dem_path,out):
    maps=sorted(residual_dir.glob("*_delta-residual-db.tif"))
    if len(maps)!=30:raise ValueError(f"Expected 30 residual maps, found {len(maps)}")
    records=[process(p,opera_dir,dw_dir,dem_path) for p in maps]
    report={"schema":"tessellatum.nairobi-r130-joint-landcover-terrain-anf.v1",
      "estimand":"Descriptive within-scene, within-slope-band and within-scene-ANF-quartile class MAE contrasts against built surfaces, on common observed Dynamic World support.",
      "records":records,"checks":{"records":len(records),"all_30_maps_processed":len(records)==30},
      "limitations":["Dynamic World predictions are model outputs, not reference land-cover truth; confidence is not calibrated.",
        "The 31-day composite can mix land-cover change and varying surface conditions.",
        "ANF quartiles are scene-specific and must not be compared as common absolute thresholds.",
        "Slope is derived from a DSM and can reflect buildings and vegetation as well as terrain.",
        "Within-cell contrasts control only coarse slope and ANF bins; residual confounding, spatial dependence and burst geography remain.",
        "Cells are descriptive summaries, not independent statistical replicates; no pixel-level p-values or causal claims are made.",
        "Confidence filtering changes class composition and spatial coverage; inspect counts and coverage before interpreting contrasts.",
        "Residuals represent cross-processor terrain-to-ellipsoid delta differences, not absolute calibration error."]}
    out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(report,indent=2)+"\n")
    print("Joint stratification checks:",json.dumps(report["checks"]),flush=True)
    for threshold in CONFIDENCE:
      print(f"\nConfidence >= {threshold:.1f}",flush=True)
      for name in ("built","trees","shrub_and_scrub","crops"):
        pairs=[m for r in records for q in r["confidence_sensitivity"] if q["minimum_confidence"]==threshold
               for m in q["matched_to_built"] if m["class_name"]==name]
        n=sum(x["class_pixels_in_matched_cells"] for x in pairs)
        if pairs:
          weighted=sum(x["class_pixels_in_matched_cells"]*x["mean_within_cell_mae_difference_db"] for x in pairs)/n if n else float("nan")
          print(f"{name}: matched scene-class records={len(pairs)}; class pixels={n:,}; weighted within-cell MAE difference vs built={weighted:+.4f} dB",flush=True)
    return report
def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--residual-dir",type=Path,default=Path("residual-maps"))
    p.add_argument("--opera-dir",type=Path,default=Path("opera-assets"))
    p.add_argument("--dynamic-world-dir",type=Path,default=Path("dynamic-world-assets"))
    p.add_argument("--dem",type=Path,default=Path("dem-assets/nairobi_copernicus_dem_glo30.tif"))
    p.add_argument("--output",type=Path,default=Path("joint-stratification.json"))
    a=p.parse_args()
    try:r=run(a.residual_dir,a.opera_dir,a.dynamic_world_dir,a.dem,a.output)
    except Exception as e:print(f"Joint stratification failed: {type(e).__name__}: {e}",file=sys.stderr);return 2
    return 0 if r["checks"]["all_30_maps_processed"] else 1
if __name__=="__main__":raise SystemExit(main())
