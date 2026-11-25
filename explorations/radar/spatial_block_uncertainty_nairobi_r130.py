#!/usr/bin/env python3
"""Spatial-block uncertainty for matched Nairobi R130 trees-vs-built residual contrasts."""
from __future__ import annotations
import argparse,json
from pathlib import Path
import sys
# Executing this file directly places explorations/radar on sys.path; add repository root for package-style imports.
_REPO_ROOT=Path(__file__).resolve().parents[2]
if str(_REPO_ROOT) not in sys.path:sys.path.insert(0,str(_REPO_ROOT))
import numpy as np
import rasterio
from rasterio.enums import Resampling
from pyproj import Transformer
from explorations.radar.joint_stratify_nairobi_r130_landcover_terrain_anf import (
 align,static_file,reproject_dem,pixel_spacing_metres,terrain,SLOPE_EDGES,report_date)
from explorations.radar.spatial_block_bootstrap import matched_block_contrasts,bootstrap_interval

BLOCK_SIZES=(500,1000,2000);THRESHOLDS=(0.0,0.5,0.7);TREE_CODE=1;BUILT_CODE=6

def metric_block_ids(template,block_size_m):
    """Fixed-origin square grid in EPSG:32737, assigned by pixel-centre coordinates."""
    if template.crs is None:raise ValueError("Raster CRS is missing")
    transformer=Transformer.from_crs(template.crs,"EPSG:32737",always_xy=True)
    rows,cols=np.indices((template.height,template.width));x,y=template.transform*(cols+.5,rows+.5)
    east,north=transformer.transform(x,y)
    bx=np.floor(east/block_size_m).astype(np.int64);by=np.floor(north/block_size_m).astype(np.int64)
    # Unique deterministic signed integer key for 2-D block coordinates.
    key=(bx-bx.min())*(by.max()-by.min()+1)+(by-by.min())
    return key.astype(np.int64),{"metric_crs":"EPSG:32737","grid_origin":"metric coordinate 0,0","block_size_m":int(block_size_m)}

def analyze_scene(residual_path,opera_dir,dw_dir,dem_path,block_sizes,thresholds):
 date,burst,pol=residual_path.name.split("_")[:3];report_date(date);dw=dw_dir/f"nairobi_r130_{date}_dynamic-world-30m.tif"
 if not dw.exists():raise FileNotFoundError(dw)
 with rasterio.open(residual_path) as r:
  val=r.read(1).astype(np.float32);rv=np.isfinite(val)
  if r.nodata is not None:rv &= val!=r.nodata
  anf=align(static_file(opera_dir/"static",burst,"_rtc_anf_gamma0_to_beta0.tif"),r,1,Resampling.nearest,np.float32,np.nan)
  elev,demvalid=reproject_dem(dem_path,r);px,py=pixel_spacing_metres(r);sl=terrain(elev,demvalid,px,py)
  klass=align(dw,r,1,Resampling.nearest,np.uint8,255);conf=align(dw,r,2,Resampling.average,np.float32,np.nan)
  joint=rv&np.isfinite(anf)&(anf>0)&np.isfinite(sl)&(klass<=8)&np.isfinite(conf)&(conf>0)&(conf<=1)
  if joint.sum()<1000:raise ValueError(f"Insufficient valid support in {residual_path.name}")
  q=np.unique(np.quantile(anf[joint],[0,.25,.5,.75,1]));ab=np.digitize(anf,q[1:-1]);sb=np.digitize(sl,SLOPE_EDGES[1:-1]);strata=sb*4+ab
  flatvalid=joint.ravel();v=val.ravel();c=klass.ravel();f=conf.ravel();st=strata.ravel()
  results=[]
  for threshold in thresholds:
   select=flatvalid&(f>=threshold)&((c==TREE_CODE)|(c==BUILT_CODE))
   for size in block_sizes:
    block,meta=metric_block_ids(r,size);b=block.ravel()
    contrasts=matched_block_contrasts(b[select],c[select],st[select],v[select],built_code=BUILT_CODE,target_code=TREE_CODE)
    ci=bootstrap_interval([x["contrast_db"] for x in contrasts],replicates=2000,seed=20261125,min_blocks=20)
    results.append({"minimum_dw_confidence":threshold,**meta,"trees_vs_built_mae_contrast":ci,
      "tree_pixels_in_eligible_blocks":sum(x["target_pixels"] for x in contrasts),"built_pixels_in_eligible_blocks":sum(x["built_pixels"] for x in contrasts),
      "matched_strata_total":sum(x["matched_strata"] for x in contrasts),"block_details":contrasts})
  return {"date":date,"burst_id":burst,"polarization":pol,"valid_joint_pixels":int(joint.sum()),"results":results}
def run(residual_dir,opera_dir,dw_dir,dem,out):
 maps=sorted(residual_dir.glob("*_delta-residual-db.tif"));
 if len(maps)!=30:raise ValueError(f"Expected 30 maps; found {len(maps)}")
 records=[analyze_scene(p,opera_dir,dw_dir,dem,BLOCK_SIZES,THRESHOLDS) for p in maps]
 report={"schema":"tessellatum.nairobi-r130-spatial-block-bootstrap.v1","estimand":"Within scene, trees-minus-built MAE difference, matched by slope bins and scene ANF quartile; equal weighting of matched strata within blocks and equal weighting of eligible blocks.","bootstrap":{"method":"percentile resampling of spatial blocks within each scene","replicates":2000,"seed":20261125,"minimum_eligible_blocks":20},"block_sizes_m":list(BLOCK_SIZES),"confidence_thresholds":list(THRESHOLDS),"metric_crs":"EPSG:32737","records":records,"limitations":["Spatial blocks may remain dependent; intervals are exploratory and block-size sensitivity is essential.","Dynamic World predictions are not reference labels; confidence is uncalibrated and date composites can mix surface conditions.","Slope is DSM-derived; matching is only on coarse slope and scene ANF strata.","Results are descriptive processor residual contrasts, not absolute calibration, causal land-cover effects, or universal processor interchangeability.","Only blocks containing both target and built classes in shared strata are eligible; small eligible-block counts suppress intervals."]}
 out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(report,indent=2)+"\\n")
 print("Processed",len(records),"scene records; block sizes",BLOCK_SIZES,"confidence thresholds",THRESHOLDS,flush=True)
 return report
if __name__=="__main__":
 p=argparse.ArgumentParser();p.add_argument("--residual-dir",type=Path,default=Path("residual-maps"));p.add_argument("--opera-dir",type=Path,default=Path("opera-assets"));p.add_argument("--dynamic-world-dir",type=Path,default=Path("dynamic-world-assets"));p.add_argument("--dem",type=Path,default=Path("dem-assets/nairobi_copernicus_dem_glo30.tif"));p.add_argument("--output",type=Path,default=Path("spatial-block-uncertainty.json"));a=p.parse_args();run(a.residual_dir,a.opera_dir,a.dynamic_world_dir,a.dem,a.output)
