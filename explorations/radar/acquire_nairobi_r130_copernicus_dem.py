#!/usr/bin/env python3
"""Acquire Copernicus GLO-30 public COG tiles for Nairobi without credentials."""
from __future__ import annotations
import argparse,hashlib,json,re,sys
from datetime import datetime,timezone
from pathlib import Path
from urllib.request import Request,urlopen
import numpy as np
import rasterio
from rasterio.merge import merge
from rasterio.transform import from_bounds
from rasterio.warp import reproject,Resampling

BBOX=[36.65,-1.45,37.05,-1.15]
WIDTH=2500;HEIGHT=2200
BUCKET="https://copernicus-dem-30m.s3.eu-central-1.amazonaws.com"
TILE_RE=re.compile(r"(Copernicus_DSM_COG_10_[NS]\\d{2}_00_[EW]\\d{3}_00_DEM)",re.I)

def tile_bounds(name):
    m=re.search(r"_([NS])(\\d{2})_00_([EW])(\\d{3})_00_DEM$",name,re.I)
    if not m:raise ValueError(f"Unrecognized Copernicus tile name: {name}")
    lat=int(m.group(2))*(1 if m.group(1).upper()=="N" else -1)
    lon=int(m.group(4))*(1 if m.group(3).upper()=="E" else -1)
    return (lon,lat,lon+1,lat+1)

def intersect(a,b):
    return a[0]<b[2] and a[2]>b[0] and a[1]<b[3] and a[3]>b[1]

def fetch(url,timeout=300):
    req=Request(url,headers={"User-Agent":"Tessellatum-Spatial-Methods/1.0"})
    with urlopen(req,timeout=timeout) as response:return response.read()

def select_tiles():
    listing=fetch(f"{BUCKET}/tileList.txt").decode("utf-8")
    names=sorted(set(TILE_RE.findall(listing)))
    selected=[n for n in names if intersect(tile_bounds(n),BBOX)]
    if not selected:raise RuntimeError("No public GLO-30 tiles intersect the Nairobi study extent")
    return selected

def run(output_dir:Path,timeout:int):
    output_dir.mkdir(parents=True,exist_ok=True)
    tiles=select_tiles();tile_paths=[]
    for name in tiles:
        path=output_dir/f"{name}.tif"
        if not path.exists():
            path.write_bytes(fetch(f"{BUCKET}/{name}/{name}.tif",timeout))
        if path.stat().st_size<1024:raise ValueError(f"Downloaded tile is unexpectedly small: {name}")
        with rasterio.open(path) as ds:
            if ds.crs is None or ds.count!=1:raise ValueError(f"Unexpected tile schema: {name}")
        tile_paths.append(path)
        print(f"Verified {name}: {path.stat().st_size:,} bytes",flush=True)
    with rasterio.open(tile_paths[0]) as first:
        mosaic,transform=merge([rasterio.open(p) for p in tile_paths],bounds=BBOX)
        crs=first.crs;nodata=first.nodata
    source=mosaic[0].astype(np.float32)
    if nodata is not None:source[source==nodata]=np.nan
    destination=np.full((HEIGHT,WIDTH),np.nan,dtype=np.float32)
    dst_transform=from_bounds(*BBOX,WIDTH,HEIGHT)
    reproject(source,destination,src_transform=transform,src_crs=crs,src_nodata=np.nan,
      dst_transform=dst_transform,dst_crs="EPSG:4326",dst_nodata=np.nan,
      resampling=Resampling.bilinear)
    valid=np.isfinite(destination)
    if valid.mean()<0.80:raise ValueError(f"DEM coverage too low: {valid.mean():.3%}")
    output=output_dir/"nairobi_copernicus_dem_glo30.tif"
    profile={"driver":"GTiff","width":WIDTH,"height":HEIGHT,"count":2,"dtype":"float32",
      "crs":"EPSG:4326","transform":dst_transform,"nodata":-9999.0,
      "compress":"deflate","predictor":3,"tiled":True}
    with rasterio.open(output,"w",**profile) as dst:
        dst.write(np.where(valid,destination,-9999).astype(np.float32),1)
        dst.write(valid.astype(np.float32),2)
        dst.set_band_description(1,"elevation_m")
        dst.set_band_description(2,"dataMask")
    with rasterio.open(output) as ds:
        qa={"crs":ds.crs.to_string(),"width":ds.width,"height":ds.height,
          "transform":list(ds.transform)[:6],"valid_pixels":int(valid.sum()),
          "valid_fraction":float(valid.mean()),"elevation_min_m":float(np.nanmin(destination)),
          "elevation_median_m":float(np.nanmedian(destination)),
          "elevation_max_m":float(np.nanmax(destination))}
    digest=hashlib.sha256(output.read_bytes()).hexdigest()
    metadata={"schema":"tessellatum.nairobi-r130-copernicus-dem.v1",
      "provider":"Copernicus DEM GLO-30 Public via AWS Open Data",
      "bucket":BUCKET,"tiles":tiles,"bbox_crs84":BBOX,
      "source_release":"Public AWS registry copy described as Copernicus DEM 2021 release",
      "output_grid":{"width":WIDTH,"height":HEIGHT,"crs":"EPSG:4326"},
      "retrieved_at_utc":datetime.now(timezone.utc).isoformat(),"sha256":digest,
      "raster":output.name,"qa":qa,
      "limitations":["The source is a digital surface model (DSM), not a bare-earth terrain model.",
        "The public GLO-30 bucket has limited global coverage; only listed tiles are selected.",
        "The output grid oversamples the nominal 1 arc-second DEM and does not increase source resolution.",
        "The source DEM represents TanDEM-X acquisitions from 2011-2015 and is static."]}
    (output_dir/"dem-qa.json").write_text(json.dumps(metadata,indent=2)+"\\n")
    print(json.dumps({"tiles":tiles,"sha256":digest,"qa":qa},sort_keys=True),flush=True)
    return metadata

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--output-dir",type=Path,default=Path("dem-assets"))
    p.add_argument("--timeout",type=int,default=300)
    a=p.parse_args()
    try:run(a.output_dir,a.timeout)
    except Exception as exc:
        print(f"DEM acquisition failed: {type(exc).__name__}: {exc}",file=sys.stderr);return 2
    return 0
if __name__=="__main__":raise SystemExit(main())
