#!/usr/bin/env python3
"""Probe one Sentinel-1 GRD annotation geolocation grid without downloading imagery."""
from __future__ import annotations
import argparse, importlib.util, json, os, sys
from collections import Counter
from pathlib import Path
from statistics import median
from xml.etree import ElementTree as ET

RADAR=Path(__file__).resolve().parent
SPEC=importlib.util.spec_from_file_location("query_sentinelhub_sentinel1",RADAR/"query_sentinelhub_sentinel1.py")
if SPEC is None or SPEC.loader is None: raise RuntimeError("Cannot load Sentinel Hub catalogue client")
CAT=importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(CAT)
PRODUCT_ID="S1A_IW_GRDH_1SDV_20250101T155624_20250101T155649_057252_070AFB_CF43_COG.SAFE"

def local_name(tag:str)->str:
    return tag.rsplit("}",1)[-1]

def summarize_geolocation_grid(xml_bytes:bytes)->dict:
    root=ET.fromstring(xml_bytes)
    points=[]
    for node in root.iter():
        if local_name(node.tag)!="geolocationGridPoint": continue
        values={local_name(child.tag):(child.text or "").strip() for child in node}
        try:
            point={key:float(values[key]) for key in ("line","pixel","latitude","longitude","incidenceAngle","elevationAngle")}
        except (KeyError,ValueError):
            continue
        points.append(point)
    if not points: raise ValueError("No complete geolocationGridPoint records with incidenceAngle found")
    lines=sorted({p["line"] for p in points}); pixels=sorted({p["pixel"] for p in points})
    angles=[p["incidenceAngle"] for p in points]
    return {"geolocation_point_count":len(points),"unique_line_count":len(lines),
        "unique_pixel_count":len(pixels),"grid_complete":len(points)==len(lines)*len(pixels),
        "line_min":min(lines),"line_max":max(lines),"pixel_min":min(pixels),"pixel_max":max(pixels),
        "latitude_min":min(p["latitude"] for p in points),"latitude_max":max(p["latitude"] for p in points),
        "longitude_min":min(p["longitude"] for p in points),"longitude_max":max(p["longitude"] for p in points),
        "incidence_angle_degrees":{"min":min(angles),"median":median(angles),"max":max(angles)},
        "elevation_angle_degrees":{"min":min(p["elevationAngle"] for p in points),
            "median":median(p["elevationAngle"] for p in points),"max":max(p["elevationAngle"] for p in points)},
        "grid_line_values":lines,"grid_pixel_values":pixels}

def fetch_probe(access_key:str,secret_key:str)->dict:
    import boto3
    from botocore.config import Config
    token=CAT.request_access_token(os.environ.get("SENTINEL_HUB_CLIENT_ID",""),
        os.environ.get("SENTINEL_HUB_CLIENT_SECRET",""),timeout=30)
    features={}
    payload=CAT.build_search_payload("2025-01-01T00:00:00Z","2025-02-20T00:00:00Z",100)
    for _ in range(50):
        page=CAT.search_catalog(token,payload,timeout=60)
        for feature in page["features"]:
            if feature.get("id")==PRODUCT_ID: features[PRODUCT_ID]=feature
        nxt=page.get("context",{}).get("next")
        if nxt is None: break
        payload={**payload,"next":nxt}
    feature=features.get(PRODUCT_ID)
    if feature is None: raise RuntimeError("Probe product not found in Sentinel Hub catalogue")
    href=(feature.get("assets") or {}).get("data",{}).get("href")
    if not isinstance(href,str) or not href.startswith("s3://"): raise RuntimeError("Product has no usable S3 data asset")
    from urllib.parse import urlparse
    parsed=urlparse(href); bucket_name=parsed.netloc; prefix=parsed.path.lstrip("/").rstrip("/")+"/"
    resource=boto3.resource("s3",endpoint_url="https://eodata.dataspace.copernicus.eu",
        aws_access_key_id=access_key,aws_secret_access_key=secret_key,region_name="default",
        config=Config(signature_version="s3v4"))
    bucket=resource.Bucket(bucket_name)
    candidates=[obj.key for obj in bucket.objects.filter(Prefix=prefix)
        if "/annotation/" in obj.key.lower() and "/annotation/calibration/" not in obj.key.lower()
        and "/annotation/rfi/" not in obj.key.lower() and obj.key.lower().endswith(".xml")
        and "iw-grd-vv-" in obj.key.lower()]
    if len(candidates)!=1: raise RuntimeError(f"Expected one VV annotation XML, found {len(candidates)}")
    key=candidates[0]
    body=bucket.Object(key).get()["Body"].read()
    result=summarize_geolocation_grid(body)
    return {"product_id":PRODUCT_ID,"annotation_key":key,"annotation_size_bytes":len(body),
        "annotation_grid":result,"analysis_ready":False,
        "limitations":["Single-product metadata probe only; no raster interpolation performed.",
            "The grid must be compared against source image geometry and independently validated before interpolation."]}

def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--output",type=Path,default=Path("data/sentinelhub/nairobi/sentinel1_grd_geolocation_grid_probe.json"))
    a=p.parse_args(argv)
    access=os.environ.get("CDSE_S3_ACCESS_KEY",""); secret=os.environ.get("CDSE_S3_SECRET_KEY","")
    if not access or not secret: print("Missing CDSE S3 secrets.",file=sys.stderr); return 2
    try: report=fetch_probe(access,secret)
    except Exception as exc:
        print(f"Geolocation-grid probe failed: {type(exc).__name__}: {exc}",file=sys.stderr); return 2
    a.output.parent.mkdir(parents=True,exist_ok=True); a.output.write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    grid=report["annotation_grid"]
    print(f"Annotation XML: {report['annotation_key']} ({report['annotation_size_bytes']} bytes)")
    print(f"Geolocation points: {grid['geolocation_point_count']}; grid={grid['unique_line_count']} lines x {grid['unique_pixel_count']} pixels; complete={grid['grid_complete']}")
    print(f"Incidence angle degrees: min={grid['incidence_angle_degrees']['min']:.6f}, median={grid['incidence_angle_degrees']['median']:.6f}, max={grid['incidence_angle_degrees']['max']:.6f}")
    print(f"Latitude range: {grid['latitude_min']:.6f} to {grid['latitude_max']:.6f}; longitude range: {grid['longitude_min']:.6f} to {grid['longitude_max']:.6f}")
    print(f"Report: {a.output}; analysis_ready=false")
    return 0
if __name__=="__main__": raise SystemExit(main())
