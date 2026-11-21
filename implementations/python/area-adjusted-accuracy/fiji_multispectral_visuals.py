#!/usr/bin/env python3
"""Create native-grid Sentinel-2 visual evidence panels without class predictions."""
from __future__ import annotations
import hashlib, json
from pathlib import Path
from typing import Any
import numpy as np
from PIL import Image
from multispectral_metrics import ndvi, ndre, scl_valid_mask

def _stretch(a: np.ndarray, low: float = 2, high: float = 98):
    x=np.asarray(a,dtype=np.float32); valid=np.isfinite(x)
    if not valid.any(): return np.zeros(x.shape,dtype=np.uint8), {"status":"no_valid_pixels","low":None,"high":None}
    lo,hi=np.percentile(x[valid],[low,high])
    if not np.isfinite(lo) or not np.isfinite(hi) or hi<=lo:
        lo,hi=float(np.nanmin(x)),float(np.nanmax(x))
        if hi<=lo: hi=lo+1.0
    scaled=np.clip((x-lo)/(hi-lo),0,1); scaled[~valid]=0
    return np.round(scaled*255).astype(np.uint8), {"status":"stretched","low":float(lo),"high":float(hi),"percentiles":[low,high],"gamma":1.0}

def _rgb(bands,keys):
    channels=[]; stretches={}
    for key in keys:
        if key not in bands: raise KeyError(key)
        ch,meta=_stretch(bands[key]); channels.append(ch); stretches[key]=meta
    return np.stack(channels,axis=-1),stretches

def _save(path,array):
    path.parent.mkdir(parents=True,exist_ok=True); Image.fromarray(array).save(path,format="PNG",optimize=True)
    return hashlib.sha256(path.read_bytes()).hexdigest()

def build_visual_evidence(sample_id,item_id,acquired,bands,metadata,output_dir):
    """Write native-grid panels; no cross-resolution band mixing or classification."""
    output_dir=Path(output_dir); records=[]
    def add(name,array,grid,description,stretches,mask="none"):
        safe="".join(c if c.isalnum() or c in "-_" else "_" for c in item_id)
        filename=f"{sample_id}__{safe}__{name}.png"; path=output_dir/filename; digest=_save(path,array)
        records.append({"sample_id":sample_id,"item_id":item_id,"datetime":acquired,"panel":name,"filename":filename,"native_grid":grid,"description":description,"mask":mask,"display_stretch":stretches,"sha256":digest,"source_bands":list(stretches)})
    if all(k in bands for k in ("B04","B03","B02")):
        img,st=_rgb(bands,("B04","B03","B02")); add("true_colour_10m",img,"10m","B04/B03/B02 true-colour; per-window percentile stretch.",st)
    if all(k in bands for k in ("B08","B04","B03")):
        img,st=_rgb(bands,("B08","B04","B03")); add("false_colour_10m",img,"10m","B08/B04/B03 false-colour; per-window percentile stretch.",st)
    if all(k in bands for k in ("B08","B04")) and bands["B08"].shape==bands["B04"].shape:
        x=ndvi(bands["B08"],bands["B04"]); img,st=_stretch(x,0,100); add("ndvi_10m",img,"10m","NDVI grayscale; display stretch only, not a class map.",{"NDVI":st})
    if all(k in bands for k in ("B8A","B05")) and bands["B8A"].shape==bands["B05"].shape:
        x=ndre(bands["B8A"],bands["B05"]); mask="none"
        if "SCL" in bands and bands["SCL"].shape==x.shape:
            x=np.where(scl_valid_mask(bands["SCL"]),x,np.nan); mask="SCL classes 2,4,5,6 retained on native 20m grid"
        img,st=_stretch(x,0,100); add("ndre_20m_scl_screened",img,"20m","NDRE grayscale from B8A/B05 on native 20m grid.",{"NDRE":st},mask)
    if all(k in bands for k in ("B12","B11","B05")) and len({bands[k].shape for k in ("B12","B11","B05")})==1:
        img,st=_rgb(bands,("B12","B11","B05")); add("swir_rededge_20m",img,"20m","B12/B11/B05 SWIR/red-edge context on native 20m grid.",st)
    if "SCL" in bands:
        scl=np.asarray(bands["SCL"]); valid=np.isfinite(scl); display=np.zeros(scl.shape,dtype=np.uint8); display[valid]=np.clip(scl[valid]*22,0,255).astype(np.uint8)
        add("scl_classes_20m",display,"20m","SCL category codes as grayscale intensity; use accompanying class counts.",{"SCL":{"mapping":"class_code × 22, clipped 0–255"}})
    return records

def write_visual_manifest(records,path):
    path=Path(path); path.parent.mkdir(parents=True,exist_ok=True); path.write_text(json.dumps(records,indent=2,sort_keys=True),encoding="utf-8")
