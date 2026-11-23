#!/usr/bin/env python3
"""Interpolate Surat R009 source GRD incidence angles to the paired raster grid."""
from __future__ import annotations
import argparse, importlib.util, json, sys
from pathlib import Path
import numpy as np

RADAR=Path(__file__).resolve().parent
def load_module(name,filename):
    spec=importlib.util.spec_from_file_location(name,RADAR/filename)
    if spec is None or spec.loader is None: raise RuntimeError(f"Cannot load {filename}")
    module=importlib.util.module_from_spec(spec); spec.loader.exec_module(module); return module
SOURCE=load_module("extract_sentinel1_grd_incidence_grids","extract_sentinel1_grd_incidence_grids.py")
INTERP=load_module("interpolate_sentinel1_ellipsoid_incidence","interpolate_sentinel1_ellipsoid_incidence.py")
BBOX=[150.244625,-27.273849,150.500114,-27.070649]
WIDTH=2500; HEIGHT=2200

def build_report(source_report,output_dir):
    products=[]
    for product in source_report["products"]:
        points=product["annotation_grid"]["points"]
        cv=INTERP.cross_validate(points)
        raster,grid=INTERP.interpolate_to_grid(points,width=WIDTH,height=HEIGHT,bbox=BBOX)
        name=f"surat_r009_{product['datetime_utc'][:10]}_ellipsoid_incidence_angle.tif"
        path=output_dir/name
        INTERP.write_geotiff(raster,path,bbox=BBOX)
        valid=raster[np.isfinite(raster)]
        products.append({"product_id":product["product_id"],"datetime_utc":product["datetime_utc"],
            "relative_orbit":product["relative_orbit"],"source_annotation":product["annotation_key"],
            "source_tie_points":len(points),"cross_validation":cv,"target_grid":grid,
            "interpolated_angle_degrees":{"min":float(valid.min()),"median":float(np.median(valid)),"max":float(valid.max())},
            "output_file":name})
        print(f"{product['datetime_utc']}: coverage={grid['coverage_fraction']:.4f}; CV MAE/RMSE/P95={cv['mae_degrees']:.5f}/{cv['rmse_degrees']:.5f}/{cv['p95_absolute_error_degrees']:.5f} degrees")
    return {"schema":"tessellatum.sentinel1.surat-r009-ellipsoid-incidence-grids.v1",
        "bbox_crs84":BBOX,"width":WIDTH,"height":HEIGHT,"crs":"EPSG:4326",
        "products":products,"product_count":len(products),"analysis_ready":False,
        "limitations":["Interpolation uses sparse annotation geolocation-grid tie points and no extrapolation.",
            "Five-fold tie-point validation is internal to the source product metadata, not independent geodetic control.",
            "Calibration-LUT agreement is a second metadata path from the same source product, not an external reference."]}

def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--input",type=Path,default=Path("data/sentinelhub/surat_basin/surat_r009_source_incidence_metadata.json"))
    p.add_argument("--output-dir",type=Path,default=Path("data/sentinelhub/surat_basin/processed/ellipsoid_incidence"))
    p.add_argument("--report",type=Path,default=Path("data/sentinelhub/surat_basin/processed/surat_r009_incidence_interpolation_qa.json"))
    a=p.parse_args(argv)
    try:
        source=json.loads(a.input.read_text(encoding="utf-8"))
        if source.get("product_count")!=4: raise ValueError("Expected four source incidence metadata products")
        a.output_dir.mkdir(parents=True,exist_ok=True)
        report=build_report(source,a.output_dir)
        a.report.parent.mkdir(parents=True,exist_ok=True)
        a.report.write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    except Exception as exc:
        print(f"Surat incidence interpolation failed: {type(exc).__name__}: {exc}",file=sys.stderr); return 2
    print(f"Interpolated {report['product_count']} products; report={a.report}; analysis_ready=false")
    return 0
if __name__=="__main__": raise SystemExit(main())
