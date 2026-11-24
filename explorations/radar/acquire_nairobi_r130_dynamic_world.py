#!/usr/bin/env python3
"""Acquire date-window Dynamic World probability composites for Nairobi R130 scenes."""
from __future__ import annotations
import argparse,hashlib,json,os,sys
from datetime import date,timedelta,datetime,timezone
from pathlib import Path
from tempfile import TemporaryDirectory
from urllib.request import urlopen
from urllib.error import HTTPError
import numpy as np
import rasterio
from rasterio.merge import merge

BBOX=[36.65,-1.45,37.05,-1.15]
DATES=("2026-10-06","2026-10-18","2026-10-30","2026-11-11","2026-11-23")
PROBABILITY_BANDS=("water","trees","grass","flooded_vegetation","crops",
                   "shrub_and_scrub","built","bare","snow_and_ice")
COLLECTION="GOOGLE/DYNAMICWORLD/V1"
WINDOW_DAYS=15
OUTPUT_SCALE_M=30
DOWNLOAD_TILES_X=4
DOWNLOAD_TILES_Y=4

def date_window(day:str,half_window:int=WINDOW_DAYS):
    d=date.fromisoformat(day)
    return (d-timedelta(days=half_window)).isoformat(),(d+timedelta(days=half_window+1)).isoformat()

def make_download_tiles(bbox=BBOX,nx=DOWNLOAD_TILES_X,ny=DOWNLOAD_TILES_Y):
    """Partition a CRS84 bounding box into deterministic, gap-free tiles."""
    if nx<1 or ny<1:raise ValueError("Tile counts must be positive")
    west,south,east,north=map(float,bbox)
    if not west<east or not south<north:raise ValueError("Invalid bounding box")
    dx=(east-west)/nx;dy=(north-south)/ny
    return [[west+i*dx,south+j*dy,west+(i+1)*dx,south+(j+1)*dy]
      for j in range(ny) for i in range(nx)]

def build_composite(ee,day:str):
    start,end=date_window(day)
    region=ee.Geometry.Rectangle(BBOX,proj="EPSG:4326",geodesic=False)
    collection=(ee.ImageCollection(COLLECTION).filterBounds(region)
      .filterDate(start,end).select(list(PROBABILITY_BANDS)))
    count=collection.size().getInfo()
    if not count:raise ValueError(f"No Dynamic World scenes in {start} to {end} for Nairobi")
    first_ms=collection.aggregate_min("system:time_start").getInfo()
    last_ms=collection.aggregate_max("system:time_start").getInfo()
    first_date=datetime.fromtimestamp(first_ms/1000,timezone.utc).date().isoformat()
    last_date=datetime.fromtimestamp(last_ms/1000,timezone.utc).date().isoformat()
    # ImageCollection reductions can lose a meaningful default projection.
    # Restore the native 10 m projection from an actual Dynamic World scene
    # before calling reduceResolution; otherwise Earth Engine may attempt to
    # aggregate from its generic WGS84 one-degree default.
    native_projection=ee.Image(collection.first()).select("water").projection()
    probabilities=collection.median().setDefaultProjection(native_projection)
    predicted=(probabilities.toArray().arrayArgmax().arrayGet([0])
      .rename("dw_class").toByte().setDefaultProjection(native_projection))
    confidence=(probabilities.reduce(ee.Reducer.max())
      .rename("dw_confidence").toFloat().setDefaultProjection(native_projection))
    # Reduce the 10m predictions to a nominal 30m grid. Keep confidence rather
    # than hard-filtering it so uncertainty thresholds remain explicit downstream.
    class30=predicted.reduceResolution(reducer=ee.Reducer.mode(),maxPixels=64)
    conf30=confidence.reduceResolution(reducer=ee.Reducer.mean(),maxPixels=64)
    output=ee.Image.cat([class30,conf30]).rename(["dw_class","dw_confidence"])
    return output,{"window_start":start,"window_end_exclusive":end,"source_scene_count":int(count),
      "first_source_scene_date":first_date,"last_source_scene_date":last_date}

def _project_fingerprint(value:str)->str:
    """Return a non-reversible identifier for comparing project IDs in CI logs."""
    return hashlib.sha256(value.encode("utf-8")).hexdigest()[:12]

def diagnose_project_identity(info:dict,raw_project:str)->str:
    """Validate and safely compare the configured and service-account project IDs."""
    configured=(raw_project or "").strip()
    if not configured:
        raise ValueError("GEE_PROJECT_ID secret is required")
    # Earth Engine expects the project ID, not the Resource Manager projects/<id> path.
    project=configured.removeprefix("projects/").strip()
    if not project:
        raise ValueError("GEE_PROJECT_ID must contain a project ID")
    service_project=str(info.get("project_id","")).strip()
    print("Earth Engine project identity diagnostics:",flush=True)
    print(f"  configured project fingerprint: {_project_fingerprint(project)}",flush=True)
    print(f"  configured project suffix: ...{project[-6:]}",flush=True)
    if configured != project:
        print("  note: removed a leading 'projects/' prefix from GEE_PROJECT_ID",flush=True)
    if service_project:
        print(f"  service-account project fingerprint: {_project_fingerprint(service_project)}",flush=True)
        print(f"  service-account project suffix: ...{service_project[-6:]}",flush=True)
        print(f"  configured/service-account project IDs match: {project == service_project}",flush=True)
    else:
        print("  service-account JSON has no project_id field",flush=True)
    print("  project passed to ee.Initialize(): configured GEE_PROJECT_ID",flush=True)
    return project

def format_download_http_error(exc:HTTPError,day:str,params:dict,tile_bbox=None)->str:
    """Expose a bounded, non-secret Earth Engine error and request summary."""
    try:
        raw=exc.read(4096)
        detail=raw.decode("utf-8","replace").strip()
    except Exception as read_exc:
        detail=f"<could not read response body: {type(read_exc).__name__}>"
    if len(detail)>3000:
        detail=detail[:3000]+"… [truncated]"
    headers=exc.headers or {}
    content_type=headers.get("Content-Type","unknown")
    content_length=headers.get("Content-Length","unknown")
    return (
        f"Earth Engine download HTTP {exc.code} for {day}; "
        f"content_type={content_type}; content_length={content_length}; "
        f"request_name={params.get('name')}; scale_m={params.get('scale')}; "
        f"crs={params.get('crs')}; format={params.get('format')}; "
        f"region_bbox_crs84={tile_bbox if tile_bbox is not None else BBOX}; response={detail or '<empty>'}"
    )

def acquire(output_dir:Path):
    import ee
    from google.oauth2 import service_account
    info=json.loads(os.environ.get("GEE_SERVICE_ACCOUNT_JSON",""))
    project=diagnose_project_identity(info,os.environ.get("GEE_PROJECT_ID",""))
    credentials=service_account.Credentials.from_service_account_info(
      info,scopes=["https://www.googleapis.com/auth/earthengine"])
    ee.Initialize(credentials=credentials,project=project)
    output_dir.mkdir(parents=True,exist_ok=True)
    records=[]
    tiles=make_download_tiles()
    for day in DATES:
        image,window=build_composite(ee,day)
        path=output_dir/f"nairobi_r130_{day}_dynamic-world-30m.tif"
        with TemporaryDirectory(prefix=f"dw-{day}-") as tmp:
            tile_paths=[]
            for tile_index,tile_bbox in enumerate(tiles):
                tile_region=ee.Geometry.Rectangle(tile_bbox,proj="EPSG:4326",geodesic=False)
                params={"name":f"dynamic-world-nairobi-r130-{day}-tile-{tile_index:02d}",
                  "scale":OUTPUT_SCALE_M,"region":tile_region,"crs":"EPSG:4326",
                  "format":"GEO_TIFF"}
                try:
                    url=image.getDownloadURL(params)
                    body=urlopen(url,timeout=300).read()
                except HTTPError as exc:
                    raise RuntimeError(format_download_http_error(exc,day,params,tile_bbox)) from exc
                tile_path=Path(tmp)/f"tile-{tile_index:02d}.tif"
                tile_path.write_bytes(body)
                tile_paths.append(tile_path)
            # Earth Engine may round tile edges to its output grid. Merge the
            # georeferenced pieces locally; downstream QA reprojects the mosaic
            # to the residual-map grid, so no exact source-grid match is needed.
            with rasterio.open(tile_paths[0]) as first:
                mosaic,transform=merge([rasterio.open(p) for p in tile_paths])
                profile=first.profile.copy()
                profile.update(driver="GTiff",height=mosaic.shape[1],width=mosaic.shape[2],
                  transform=transform,count=2,compress="deflate")
            with rasterio.open(path,"w",**profile) as dst:
                dst.write(mosaic)
        with rasterio.open(path) as ds:
            if ds.count!=2 or ds.crs is None:raise ValueError(f"Unexpected Dynamic World raster schema for {day}")
            klass=ds.read(1);conf=ds.read(2)
            valid=np.isfinite(klass)&np.isfinite(conf)&(klass>=0)&(klass<=8)&(conf>=0)&(conf<=1)
            if valid.mean()<0.70:raise ValueError(f"Low valid Dynamic World coverage for {day}: {valid.mean():.3%}")
            q={"crs":ds.crs.to_string(),"width":ds.width,"height":ds.height,
              "transform":list(ds.transform)[:6],"valid_fraction":float(valid.mean()),
              "class_counts":{str(k):int(np.sum(valid&(klass==k))) for k in range(9)},
              "confidence_quantiles":{str(q):float(np.quantile(conf[valid],q)) for q in (.1,.25,.5,.75,.9)},
              "fraction_confidence_ge_0_5":float(np.mean(conf[valid]>=.5)),
              "fraction_confidence_ge_0_7":float(np.mean(conf[valid]>=.7))}
        records.append({"sentinel1_date":day,**window,"file":path.name,
          "sha256":hashlib.sha256(body).hexdigest(),"qa":q})
        print(f"{day}: scenes={window['source_scene_count']}; valid={q['valid_fraction']:.3%}; conf>=0.7={q['fraction_confidence_ge_0_7']:.3%}",flush=True)
    report={"schema":"tessellatum.nairobi-r130-dynamic-world.v1",
      "provider":"Google / World Resources Institute Dynamic World",
      "collection":COLLECTION,"bbox_crs84":BBOX,"window_half_width_days":WINDOW_DAYS,"download_tiling":{"nx":DOWNLOAD_TILES_X,"ny":DOWNLOAD_TILES_Y,"tile_count":len(tiles)},
      "probability_bands":list(PROBABILITY_BANDS),
      "class_codes":{"0":"water","1":"trees","2":"grass","3":"flooded_vegetation",
        "4":"crops","5":"shrub_and_scrub","6":"built","7":"bare","8":"snow_and_ice"},
      "composite":"Median of per-scene class probabilities over the date window; class is argmax of median probabilities; confidence is max median class probability. 10m predictions are reduced to nominal 30m with mode class and mean confidence.",
      "records":records,
      "limitations":["The 15-day window is a temporal neighbourhood, not an exact-date observation.",
        "Dynamic World is a Sentinel-2-derived prediction and its quality varies with cloud masking, season and surface type.",
        "Confidence is preserved, not treated as calibrated probability or ground truth.",
        "The 30m output is an aggregation of 10m predictions and does not create new source information.",
        "Class associations are descriptive; no residual pixels are excluded."]}
    (output_dir/"dynamic-world-qa.json").write_text(json.dumps(report,indent=2)+"\n")
    return report

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--output-dir",type=Path,default=Path("dynamic-world-assets"))
    a=p.parse_args()
    try:acquire(a.output_dir)
    except Exception as exc:print(f"Dynamic World acquisition failed: {type(exc).__name__}: {exc}",file=sys.stderr);return 2
    return 0
if __name__=="__main__":raise SystemExit(main())
