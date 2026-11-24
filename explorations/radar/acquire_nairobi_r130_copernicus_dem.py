#!/usr/bin/env python3
"""Acquire the Copernicus DEM used by the Nairobi R130 terrain-correction workflow."""
from __future__ import annotations
import argparse, hashlib, importlib.util, json, os, sys
from datetime import datetime, timezone
from pathlib import Path

RADAR=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location("process_sentinelhub_sentinel1",RADAR/"process_sentinelhub_sentinel1.py")
if spec is None or spec.loader is None: raise RuntimeError("Cannot load Sentinel Hub Process API client")
PROCESS=importlib.util.module_from_spec(spec);spec.loader.exec_module(PROCESS)

BBOX=[36.65,-1.45,37.05,-1.15]
WIDTH=2500;HEIGHT=2200;DEM_INSTANCE="COPERNICUS_30"
EVALSCRIPT="""//VERSION=3
function setup() {
  return { input: [{ bands: ["DEM", "dataMask"] }],
    output: { bands: 2, sampleType: SampleType.FLOAT32 } };
}
function evaluatePixel(sample) { return [sample.DEM, sample.dataMask]; }
"""

def build_payload():
    return {
      "input":{"bounds":{"bbox":BBOX,"properties":{"crs":"http://www.opengis.net/def/crs/OGC/1.3/CRS84"}},
        "data":[{"type":"dem","dataFilter":{"demInstance":DEM_INSTANCE},
          "processing":{"upsampling":"BILINEAR","downsampling":"BILINEAR"}}]},
      "output":{"width":WIDTH,"height":HEIGHT,
        "responses":[{"identifier":"default","format":{"type":"image/tiff"}}]},
      "evalscript":EVALSCRIPT}

def run(output_dir:Path,timeout:int):
    client=os.environ.get("SENTINEL_HUB_CLIENT_ID","")
    secret=os.environ.get("SENTINEL_HUB_CLIENT_SECRET","")
    token=PROCESS._CATALOG.request_access_token(client,secret,timeout=min(timeout,30))
    payload=build_payload()
    body=PROCESS.request_geotiff(token,payload,timeout=timeout)
    output_dir.mkdir(parents=True,exist_ok=True)
    raster=output_dir/"nairobi_copernicus_dem_glo30.tif"
    raster.write_bytes(body)
    import rasterio
    with rasterio.open(raster) as ds:
        if ds.count!=2 or ds.width!=WIDTH or ds.height!=HEIGHT:
            raise ValueError(f"Unexpected DEM output schema/grid: {ds.count} bands, {ds.width}x{ds.height}")
        mask=ds.read(2)>0.5
        elevation=ds.read(1)
        valid=mask & (elevation!=ds.nodata if ds.nodata is not None else True)
        if valid.mean()<0.80: raise ValueError(f"DEM valid coverage too low: {valid.mean():.3%}")
        qa={"crs":ds.crs.to_string(),"width":ds.width,"height":ds.height,
          "transform":list(ds.transform)[:6],"bands":["elevation_m","dataMask"],
          "valid_pixels":int(valid.sum()),"valid_fraction":float(valid.mean()),
          "elevation_min_m":float(elevation[valid].min()),
          "elevation_median_m":float(__import__("numpy").median(elevation[valid])),
          "elevation_max_m":float(elevation[valid].max())}
    digest=hashlib.sha256(body).hexdigest()
    metadata={"schema":"tessellatum.nairobi-r130-copernicus-dem.v1",
      "provider":"Copernicus DEM via Sentinel Hub Process API",
      "dem_instance":DEM_INSTANCE,"nominal_source":"Copernicus DEM GLO-30 Public, with GLO-90 infill where GLO-30 is unavailable",
      "bbox_crs84":BBOX,"output_grid":{"width":WIDTH,"height":HEIGHT,"crs":"EPSG:4326"},
      "retrieved_at_utc":datetime.now(timezone.utc).isoformat(),"sha256":digest,
      "raster":raster.name,"qa":qa,
      "limitations":["The source is a digital surface model (DSM), not a bare-earth terrain model.",
        "The output grid oversamples the nominal DEM and does not increase source resolution.",
        "The provider documents GLO-30 with GLO-90 infill where 30m public tiles are unavailable.",
        "The elevation product is static and represents source acquisitions primarily from 2011-2015."]}
    (output_dir/"dem-qa.json").write_text(json.dumps(metadata,indent=2)+"\n")
    print(json.dumps({"raster":raster.name,"sha256":digest,"qa":qa},sort_keys=True),flush=True)
    return metadata

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--output-dir",type=Path,default=Path("dem-assets"))
    p.add_argument("--timeout",type=int,default=300)
    a=p.parse_args()
    try: run(a.output_dir,a.timeout)
    except Exception as exc:
        print(f"DEM acquisition failed: {type(exc).__name__}: {exc}",file=sys.stderr);return 2
    return 0
if __name__=="__main__": raise SystemExit(main())
