#!/usr/bin/env python3
"""Extract GRD incidence geolocation and calibration LUT metadata for Surat R009 scenes."""
from __future__ import annotations
import argparse, importlib.util, json, os, sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

RADAR=Path(__file__).resolve().parent
def load_module(name,filename):
    spec=importlib.util.spec_from_file_location(name,RADAR/filename)
    if spec is None or spec.loader is None: raise RuntimeError(f"Cannot load {filename}")
    module=importlib.util.module_from_spec(spec); spec.loader.exec_module(module); return module
SOURCE=load_module("extract_sentinel1_grd_incidence_grids","extract_sentinel1_grd_incidence_grids.py")
LUT=load_module("probe_sentinel1_grd_calibration_lut","probe_sentinel1_grd_calibration_lut.py")
CAT=SOURCE.CAT
PRODUCT_IDS=[
"S1A_IW_GRDH_1SDV_20251219T084112_20251219T084137_062381_07D052_4725_COG.SAFE",
"S1A_IW_GRDH_1SDV_20251231T084111_20251231T084136_062556_07D710_2940_COG.SAFE",
"S1A_IW_GRDH_1SDV_20260112T084110_20260112T084135_062731_07DDCA_F1E5_COG.SAFE",
"S1A_IW_GRDH_1SDV_20260124T084108_20260124T084133_062906_07E425_80AF_COG.SAFE",
]
BBOX=[150.244625,-27.273849,150.500114,-27.070649]

def collect_features(token):
    payload=CAT.build_search_payload("2025-12-18T00:00:00Z","2026-01-25T23:59:59Z",100)
    payload["bbox"]=BBOX; found={}
    for _ in range(30):
        page=CAT.search_catalog(token,payload,timeout=60)
        for feature in page["features"]:
            if feature.get("id") in PRODUCT_IDS: found[feature["id"]]=feature
        nxt=page.get("context",{}).get("next")
        if nxt is None: break
        payload={**payload,"next":nxt}
    missing=sorted(set(PRODUCT_IDS)-set(found))
    if missing: raise RuntimeError(f"Missing catalogue products: {missing}")
    return found

def object_key(bucket,prefix,kind):
    if kind=="annotation":
        keys=[o.key for o in bucket.objects.filter(Prefix=prefix)
            if "/annotation/" in o.key.lower() and "/annotation/calibration/" not in o.key.lower()
            and "/annotation/rfi/" not in o.key.lower() and o.key.lower().endswith(".xml")
            and "iw-grd-vv-" in o.key.lower()]
    else:
        keys=[o.key for o in bucket.objects.filter(Prefix=prefix)
            if "/annotation/calibration/" in o.key.lower() and o.key.lower().endswith(".xml")
            and "calibration-" in o.key.lower() and "iw-grd-vv-" in o.key.lower()]
    if len(keys)!=1: raise RuntimeError(f"Expected one {kind} VV XML under {prefix}; found {len(keys)}")
    return keys[0]

def extract(features,access,secret):
    import boto3
    from botocore.config import Config
    s3=boto3.resource("s3",endpoint_url="https://eodata.dataspace.copernicus.eu",
        aws_access_key_id=access,aws_secret_access_key=secret,region_name="default",
        config=Config(signature_version="s3v4"))
    products=[]
    for product_id in PRODUCT_IDS:
        feature=features[product_id]; href=(feature.get("assets") or {}).get("data",{}).get("href")
        parsed=urlparse(href or "")
        if parsed.scheme!="s3" or not parsed.netloc: raise RuntimeError(f"Invalid S3 asset for {product_id}")
        bucket=s3.Bucket(parsed.netloc); prefix=parsed.path.lstrip("/").rstrip("/")+"/"
        annotation_key=object_key(bucket,prefix,"annotation")
        calibration_key=object_key(bucket,prefix,"calibration")
        annotation=SOURCE.parse_geolocation_grid(bucket.Object(annotation_key).get()["Body"].read())
        calibration=LUT.parse_calibration_lut(bucket.Object(calibration_key).get()["Body"].read())
        crosscheck=LUT.compare_calibration_to_annotation(calibration,annotation)
        props=feature.get("properties",{})
        products.append({"product_id":product_id,"datetime_utc":props.get("datetime"),
            "relative_orbit":props.get("sat:relative_orbit"),"annotation_key":annotation_key,
            "calibration_key":calibration_key,"annotation_grid":annotation,
            "calibration_lut":calibration,"calibration_vs_annotation":crosscheck})
    return products

def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--output",type=Path,default=Path("data/sentinelhub/surat_basin/surat_r009_source_incidence_metadata.json"))
    a=p.parse_args(argv)
    access=os.environ.get("CDSE_S3_ACCESS_KEY",""); secret=os.environ.get("CDSE_S3_SECRET_KEY","")
    if not access or not secret: print("Missing CDSE S3 credentials.",file=sys.stderr); return 2
    try:
        token=CAT.request_access_token(os.environ.get("SENTINEL_HUB_CLIENT_ID",""),
            os.environ.get("SENTINEL_HUB_CLIENT_SECRET",""),timeout=30)
        features=collect_features(token); products=extract(features,access,secret)
    except Exception as exc:
        print(f"Surat source incidence extraction failed: {type(exc).__name__}: {exc}",file=sys.stderr); return 2
    report={"schema":"tessellatum.sentinel1.surat-r009-source-incidence-metadata.v1",
        "products":products,"product_count":len(products),"analysis_ready":False,
        "purpose":"Source GRD geolocation incidence angles plus independent calibration-LUT metadata cross-check for the four R009 validation scenes.",
        "limitations":["Calibration LUT and annotation are two metadata paths from the same source product, not independent geodetic control.",
            "The annotation grid is sparse and must be interpolated without extrapolation.",
            "No RTC normalization or change detection is performed."]}
    a.output.parent.mkdir(parents=True,exist_ok=True); a.output.write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    for product in products:
        g=product["annotation_grid"]; qa=product["calibration_vs_annotation"]
        print(f"{product['datetime_utc']}: annotation points={g['point_count']}; grid={g['unique_line_count']}x{g['unique_pixel_count']}; angle median={g['incidence_angle_degrees']['median']:.5f} degrees; LUT-vs-annotation MAE={qa['mae_degrees']:.5f} degrees; P95={qa['p95_absolute_error_degrees']:.5f} degrees")
    print(f"Extracted {len(products)} products; report={a.output}; analysis_ready=false")
    return 0
if __name__=="__main__": raise SystemExit(main())
