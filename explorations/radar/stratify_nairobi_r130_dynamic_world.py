#!/usr/bin/env python3
"""Stratify Nairobi R130 residuals by date-window Dynamic World class/confidence."""
from __future__ import annotations
import argparse,json,sys
from pathlib import Path
import numpy as np
import rasterio
from rasterio.enums import Resampling
from rasterio.warp import reproject

CLASS_NAMES=("water","trees","grass","flooded_vegetation","crops",
 "shrub_and_scrub","built","bare","snow_and_ice")
CONFIDENCE_THRESHOLDS=(0.0,0.5,0.7)

def summarize(values):
    v=np.asarray(values,dtype=float);v=v[np.isfinite(v)]
    if not v.size:return {"count":0}
    a=np.abs(v)
    return {"count":int(v.size),"bias_mean_db":float(v.mean()),
      "mae_db":float(a.mean()),"rmse_db":float(np.sqrt(np.mean(v*v))),
      "p95_absolute_db":float(np.percentile(a,95)),
      "fraction_abs_gt_0_5_db":float(np.mean(a>0.5)),
      "fraction_abs_gt_1_db":float(np.mean(a>1.0))}

def valid_landcover_support(residual_values,residual_nodata,klass,confidence):
    """Keep only residual pixels with an observed, nonzero-confidence DW label."""
    valid=np.isfinite(residual_values)
    if residual_nodata is not None:valid &= residual_values!=residual_nodata
    valid &= (klass<=8)&np.isfinite(confidence)&(confidence>0)&(confidence<=1)
    return valid

def align_dynamic_world(path,template):
    with rasterio.open(path) as src:
        if src.count!=2:raise ValueError(f"Expected class/confidence bands in {path.name}")
        klass=np.full((template.height,template.width),255,dtype=np.uint8)
        confidence=np.full((template.height,template.width),np.nan,dtype=np.float32)
        reproject(src.read(1),klass,src_transform=src.transform,src_crs=src.crs,
          src_nodata=src.nodata,dst_transform=template.transform,dst_crs=template.crs,
          dst_nodata=255,resampling=Resampling.nearest)
        reproject(src.read(2),confidence,src_transform=src.transform,src_crs=src.crs,
          src_nodata=src.nodata,dst_transform=template.transform,dst_crs=template.crs,
          dst_nodata=np.nan,resampling=Resampling.average)
        return klass,confidence

def run(residual_dir:Path,dynamic_dir:Path,output:Path):
    maps=sorted(residual_dir.glob("*_delta-residual-db.tif"))
    if len(maps)!=30:raise ValueError(f"Expected 30 residual maps, found {len(maps)}")
    cache={};records=[]
    for path in maps:
        date,burst,pol=path.name.split("_")[:3]
        dw_path=dynamic_dir/f"nairobi_r130_{date}_dynamic-world-30m.tif"
        if not dw_path.is_file():raise FileNotFoundError(f"Missing date-window Dynamic World raster: {dw_path}")
        with rasterio.open(path) as residual:
            # Each burst can have a slightly different raster grid/extent. Cache
            # by the complete target grid, not date alone, or a prior burst's
            # aligned arrays may have a different shape.
            grid_key=(date,residual.width,residual.height,str(residual.crs),tuple(residual.transform))
            if grid_key not in cache:cache[grid_key]=align_dynamic_world(dw_path,residual)
            klass,confidence=cache[grid_key]
            residual_values=residual.read(1).astype(np.float32)
            valid=valid_landcover_support(residual_values,residual.nodata,klass,confidence)
            total=int(valid.sum())
            thresholds=[]
            for threshold in CONFIDENCE_THRESHOLDS:
                threshold_mask=valid&(confidence>=threshold)
                classes=[]
                for code,name in enumerate(CLASS_NAMES):
                    m=threshold_mask&(klass==code)
                    classes.append({"class_code":code,"class_name":name,**summarize(residual_values[m])})
                thresholds.append({"minimum_top1_confidence":threshold,
                  "valid_pixels":int(threshold_mask.sum()),
                  "coverage_of_residual_valid_pixels":float(threshold_mask.sum()/total) if total else 0,
                  "classes":classes})
            records.append({"date":f"{date[:4]}-{date[4:6]}-{date[6:8]}",
              "burst_id":burst,"polarization":pol,"residual_pixels_with_landcover":total,
              "landcover_confidence_quantiles":{str(q):float(np.quantile(confidence[valid],q)) for q in (.1,.5,.9)} if total else {},
              "threshold_summaries":thresholds})
    report={"schema":"tessellatum.nairobi-r130-dynamic-world-residual-stratification.v1",
      "landcover_source":"Google/WRI Dynamic World V1",
      "temporal_method":"Median per-class probability composite over a 31-day window centred approximately on each Sentinel-1 date (15 days before through 15 days after).",
      "class_assignment":"Argmax of median class probabilities; top-1 confidence is maximum median probability.",
      "confidence_thresholds":list(CONFIDENCE_THRESHOLDS),
      "records":records,"checks":{"records":len(records),"all_30_maps_stratified":len(records)==30},
      "limitations":["Dynamic World classes are model predictions, not reference labels or ground truth.",
        "The temporal window may mix land-cover change and varying surface conditions.",
        "Confidence values are not assumed to be calibrated probabilities.",
        "Class-specific residual associations may be confounded by slope, aspect, ANF, incidence geometry and sample support.",
        "The primary cross-processor residual comparison is unchanged; land-cover stratification is limited to pixels with observed Dynamic World support (positive top-1 confidence)."]}
    output.parent.mkdir(parents=True,exist_ok=True);output.write_text(json.dumps(report,indent=2)+"\n")
    print("Land-cover stratification checks:",json.dumps(report["checks"],sort_keys=True),flush=True)
    for burst in sorted({r["burst_id"] for r in records}):
      for pol in ("VV","VH"):
        rows=[r for r in records if r["burst_id"]==burst and r["polarization"]==pol]
        summary=[]
        for code,name in enumerate(CLASS_NAMES):
          selected=[x for row in rows for x in row["threshold_summaries"][2]["classes"] if x["class_code"]==code and x["count"]>0]
          n=sum(x["count"] for x in selected)
          if n:
            mae=sum(x["count"]*x["mae_db"] for x in selected)/n
            summary.append({"class":name,"n":n,"mae_db":round(mae,4)})
        print(f"{burst} {pol} confidence>=0.7: {json.dumps(summary,separators=(',',':'))}",flush=True)
    return report

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--residual-dir",type=Path,default=Path("residual-maps"))
    p.add_argument("--dynamic-world-dir",type=Path,default=Path("dynamic-world-assets"))
    p.add_argument("--report",type=Path,default=Path("dynamic-world-residual-stratification.json"))
    a=p.parse_args()
    try:r=run(a.residual_dir,a.dynamic_world_dir,a.report)
    except Exception as exc:print(f"Dynamic World residual stratification failed: {type(exc).__name__}: {exc}",file=sys.stderr);return 2
    return 0 if r["checks"]["all_30_maps_stratified"] else 1
if __name__=="__main__":raise SystemExit(main())
