#!/usr/bin/env python3
"""Interpolate source GRD incidenceAngle tie points onto the Nairobi analysis grid."""
from __future__ import annotations
import argparse, importlib.util, json, os, sys
from pathlib import Path
import numpy as np
import rasterio
from rasterio.transform import from_origin
from scipy.interpolate import LinearNDInterpolator
from scipy.spatial import Delaunay, QhullError

RADAR=Path(__file__).resolve().parent
SPEC=importlib.util.spec_from_file_location("extract_sentinel1_grd_incidence_grids",RADAR/"extract_sentinel1_grd_incidence_grids.py")
if SPEC is None or SPEC.loader is None: raise RuntimeError("Cannot load GRD geolocation-grid extractor")
EXTRACT=importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(EXTRACT)
BBOX=(36.65,-1.45,37.05,-1.15)
WIDTH=2048; HEIGHT=1536

def points_arrays(points):
    lon=np.asarray([p["longitude"] for p in points],dtype=np.float64)
    lat=np.asarray([p["latitude"] for p in points],dtype=np.float64)
    angle=np.asarray([p["incidenceAngle"] for p in points],dtype=np.float64)
    valid=np.isfinite(lon)&np.isfinite(lat)&np.isfinite(angle)
    xy=np.column_stack((lon[valid],lat[valid]))
    values=angle[valid]
    if len(values)<20: raise ValueError("Too few finite geolocation tie points")
    if len(np.unique(xy,axis=0))!=len(xy): raise ValueError("Duplicate geolocation coordinates in tie-point grid")
    return xy,values

def cross_validate(points,folds=5):
    xy,values=points_arrays(points)
    line_values=sorted({p["line"] for p in points})
    pixel_values=sorted({p["pixel"] for p in points})
    line_index={v:i for i,v in enumerate(line_values)}
    pixel_index={v:i for i,v in enumerate(pixel_values)}
    fold_ids=np.asarray([(line_index[p["line"]]*3+pixel_index[p["pixel"]]*2)%folds for p in points])
    predictions=np.full(len(points),np.nan,dtype=np.float64)
    for fold in range(folds):
        train=fold_ids!=fold; test=fold_ids==fold
        try:
            tri=Delaunay(xy[train])
            interp=LinearNDInterpolator(tri,values[train],fill_value=np.nan)
            predictions[test]=np.asarray(interp(xy[test]),dtype=np.float64)
        except QhullError as exc:
            raise ValueError(f"Could not triangulate training tie points in fold {fold}: {exc}") from exc
    valid=np.isfinite(predictions)
    if not valid.any(): raise ValueError("Cross-validation produced no in-hull predictions")
    error=predictions[valid]-values[valid]
    return {"method":"five-fold spatially interleaved holdout; linear interpolation; no extrapolation",
        "fold_count":folds,"total_tie_points":int(len(values)),"held_out_points_predicted":int(valid.sum()),
        "held_out_prediction_coverage_fraction":float(valid.mean()),
        "mae_degrees":float(np.mean(np.abs(error))),"rmse_degrees":float(np.sqrt(np.mean(error**2))),
        "p95_absolute_error_degrees":float(np.percentile(np.abs(error),95)),
        "max_absolute_error_degrees":float(np.max(np.abs(error)))}

def interpolate_to_grid(points,width=WIDTH,height=HEIGHT,bbox=BBOX):
    xy,values=points_arrays(points)
    west,south,east,north=bbox
    if width<2 or height<2 or not west<east or not south<north: raise ValueError("Invalid target grid")
    xres=(east-west)/width; yres=(north-south)/height
    xs=west+(np.arange(width,dtype=np.float64)+0.5)*xres
    ys=north-(np.arange(height,dtype=np.float64)+0.5)*yres
    xx,yy=np.meshgrid(xs,ys)
    try:
        tri=Delaunay(xy)
        interp=LinearNDInterpolator(tri,values,fill_value=np.nan)
        result=np.asarray(interp(np.column_stack((xx.ravel(),yy.ravel()))),dtype=np.float32).reshape(height,width)
    except QhullError as exc:
        raise ValueError(f"Could not triangulate source geolocation grid: {exc}") from exc
    coverage=float(np.isfinite(result).mean())
    if coverage<0.95: raise ValueError(f"Only {coverage:.3%} of target grid is inside source tie-point hull; refusing extrapolation")
    return result,{"width":width,"height":height,"bbox_crs84":[west,south,east,north],
        "crs":"EPSG:4326","pixel_size_degrees":[xres,yres],"coverage_fraction":coverage,
        "interpolation":"linear Delaunay interpolation in longitude/latitude; no extrapolation",
        "valid_pixel_count":int(np.isfinite(result).sum())}

def write_geotiff(array,path,bbox=BBOX):
    west,south,east,north=bbox
    transform=from_origin(west,north,(east-west)/array.shape[1],(north-south)/array.shape[0])
    data=np.where(np.isfinite(array),array,-9999.0).astype(np.float32)
    path.parent.mkdir(parents=True,exist_ok=True)
    with rasterio.open(path,"w",driver="GTiff",width=array.shape[1],height=array.shape[0],count=1,
        dtype="float32",crs="EPSG:4326",transform=transform,nodata=-9999.0,
        compress="deflate",predictor=3,tiled=True) as dst:
        dst.write(data,1)
        dst.set_band_description(1,"source_grd_ellipsoid_incidence_angle_degrees")

def build_report(products,output_dir):
    results=[]
    for product in products:
        points=product["geolocation_grid"]["points"]
        cv=cross_validate(points)
        raster,grid=interpolate_to_grid(points)
        out=output_dir/f"sentinel1_{product['relative_orbit']:03d}_{product['datetime_utc'][:10]}_ellipsoid_incidence_angle.tif"
        write_geotiff(raster,out)
        valid=raster[np.isfinite(raster)]
        results.append({"product_id":product["product_id"],"datetime_utc":product["datetime_utc"],
            "relative_orbit":product["relative_orbit"],"source_annotation":product["annotation_key"],
            "source_tie_points":product["geolocation_grid"]["point_count"],
            "source_incidence_angle_degrees":product["geolocation_grid"]["incidence_angle_degrees"],
            "cross_validation":cv,"target_grid":grid,
            "interpolated_angle_degrees":{"min":float(valid.min()),"median":float(np.median(valid)),"max":float(valid.max())},
            "output_file":str(out)})
        print(f"R{product['relative_orbit']:03d} {product['datetime_utc']}: coverage={grid['coverage_fraction']:.4f}; CV MAE/RMSE/P95={cv['mae_degrees']:.5f}/{cv['rmse_degrees']:.5f}/{cv['p95_absolute_error_degrees']:.5f} degrees; {out.name}")
    return {"schema":"tessellatum.sentinel1.grd-ellipsoid-incidence-angle-grid.v1",
        "products":results,"product_count":len(results),"analysis_ready":False,
        "interpretation":"Source annotation incidenceAngle tie points were linearly interpolated in geographic coordinates to the fixed Nairobi output grid. No extrapolation was permitted.",
        "limitations":["Interpolation is an approximation between sparse annotation tie points.",
            "Cross-validation is internal to each product's tie-point grid, not an independent geodetic validation.",
            "The raster has not yet been compared with RTC/ellipsoid backscatter residuals.",
            "No radiometric normalization or change detection is performed."]}

def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--output-dir",type=Path,default=Path("data/sentinelhub/nairobi/ellipsoid_incidence"))
    p.add_argument("--report",type=Path,default=Path("data/sentinelhub/nairobi/sentinel1_ellipsoid_incidence_grid_qa.json"))
    a=p.parse_args(argv)
    access=os.environ.get("CDSE_S3_ACCESS_KEY",""); secret=os.environ.get("CDSE_S3_SECRET_KEY","")
    if not access or not secret: print("Missing CDSE S3 credentials.",file=sys.stderr); return 2
    try:
        token=EXTRACT.CAT.request_access_token(os.environ.get("SENTINEL_HUB_CLIENT_ID",""),
            os.environ.get("SENTINEL_HUB_CLIENT_SECRET",""),timeout=30)
        features=EXTRACT.collect_catalog_items(token,"2025-01-01T00:00:00Z","2025-02-20T00:00:00Z")
        products=EXTRACT.extract_all(features,access,secret)
        if len(products)!=8: raise ValueError(f"Expected 8 source products; found {len(products)}")
        report=build_report(products,a.output_dir)
    except Exception as exc:
        print(f"Incidence-angle interpolation failed: {type(exc).__name__}: {exc}",file=sys.stderr); return 2
    a.report.parent.mkdir(parents=True,exist_ok=True); a.report.write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    print(f"Interpolated products: {report['product_count']}; analysis_ready=false; report={a.report}")
    return 0
if __name__=="__main__": raise SystemExit(main())
