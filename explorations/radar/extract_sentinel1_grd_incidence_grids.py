#!/usr/bin/env python3
"""Extract Sentinel-1 GRD VV geolocation-grid tie points from CDSE S3 metadata."""
from __future__ import annotations
import argparse, importlib.util, json, os, sys
from datetime import datetime, timezone
from pathlib import Path
from statistics import median
from urllib.parse import urlparse
from xml.etree import ElementTree as ET

RADAR=Path(__file__).resolve().parent
SPEC=importlib.util.spec_from_file_location("query_sentinelhub_sentinel1",RADAR/"query_sentinelhub_sentinel1.py")
if SPEC is None or SPEC.loader is None: raise RuntimeError("Cannot load Sentinel Hub catalogue client")
CAT=importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(CAT)
PRODUCT_IDS={
"S1A_IW_GRDH_1SDV_20250108T154826_20250108T154851_057354_070F02_69BA_COG.SAFE",
"S1A_IW_GRDH_1SDV_20250120T154825_20250120T154850_057529_0715F0_AEAD_COG.SAFE",
"S1A_IW_GRDH_1SDV_20250201T154824_20250201T154849_057704_071CDD_B2FC_COG.SAFE",
"S1A_IW_GRDH_1SDV_20250213T154824_20250213T154849_057879_0723E0_AE16_COG.SAFE",
"S1A_IW_GRDH_1SDV_20250101T155624_20250101T155649_057252_070AFB_CF43_COG.SAFE",
"S1A_IW_GRDH_1SDV_20250113T155623_20250113T155648_057427_0711E7_D8F0_COG.SAFE",
"S1A_IW_GRDH_1SDV_20250125T155622_20250125T155647_057602_0718DC_43D7_COG.SAFE",
"S1A_IW_GRDH_1SDV_20250206T155622_20250206T155647_057777_071FCA_BA90_COG.SAFE",
}

def local_name(tag): return tag.rsplit("}",1)[-1]

def parse_geolocation_grid(xml_bytes:bytes)->dict:
    root=ET.fromstring(xml_bytes); points=[]
    for node in root.iter():
        if local_name(node.tag)!="geolocationGridPoint": continue
        values={local_name(child.tag):(child.text or "").strip() for child in node}
        try:
            point={key:float(values[key]) for key in ("line","pixel","latitude","longitude","height","incidenceAngle","elevationAngle")}
        except (KeyError,ValueError): continue
        points.append(point)
    if not points: raise ValueError("No complete geolocationGridPoint records with incidenceAngle found")
    lines=sorted({p["line"] for p in points}); pixels=sorted({p["pixel"] for p in points})
    angles=[p["incidenceAngle"] for p in points]
    return {"point_count":len(points),"unique_line_count":len(lines),"unique_pixel_count":len(pixels),
        "grid_complete":len(points)==len(lines)*len(pixels),
        "line_min":min(lines),"line_max":max(lines),"pixel_min":min(pixels),"pixel_max":max(pixels),
        "latitude_min":min(p["latitude"] for p in points),"latitude_max":max(p["latitude"] for p in points),
        "longitude_min":min(p["longitude"] for p in points),"longitude_max":max(p["longitude"] for p in points),
        "incidence_angle_degrees":{"min":min(angles),"median":median(angles),"max":max(angles)},
        "points":points}

def collect_catalog_items(token,start,end):
    payload=CAT.build_search_payload(start,end,100); found={}
    for _ in range(50):
        page=CAT.search_catalog(token,payload,timeout=60)
        for feature in page["features"]:
            if feature.get("id") in PRODUCT_IDS: found[feature["id"]]=feature
        nxt=page.get("context",{}).get("next")
        if nxt is None: return found
        payload={**payload,"next":nxt}
    raise RuntimeError("Catalogue pagination exceeded 50 pages")

def extract_all(features,access_key,secret_key):
    import boto3
    from botocore.config import Config
    resource=boto3.resource("s3",endpoint_url="https://eodata.dataspace.copernicus.eu",
        aws_access_key_id=access_key,aws_secret_access_key=secret_key,region_name="default",
        config=Config(signature_version="s3v4"))
    results=[]
    for product_id in sorted(PRODUCT_IDS):
        feature=features.get(product_id)
        if feature is None: raise RuntimeError(f"Catalogue item missing: {product_id}")
        href=(feature.get("assets") or {}).get("data",{}).get("href")
        if not isinstance(href,str): raise RuntimeError(f"Missing data asset for {product_id}")
        parsed=urlparse(href)
        if parsed.scheme!="s3" or not parsed.netloc: raise RuntimeError(f"Invalid S3 URI for {product_id}")
        bucket=resource.Bucket(parsed.netloc); prefix=parsed.path.lstrip("/").rstrip("/")+"/"
        keys=[obj.key for obj in bucket.objects.filter(Prefix=prefix)
            if "/annotation/" in obj.key.lower() and "/annotation/calibration/" not in obj.key.lower()
            and "/annotation/rfi/" not in obj.key.lower() and obj.key.lower().endswith(".xml")
            and "iw-grd-vv-" in obj.key.lower()]
        if len(keys)!=1: raise RuntimeError(f"Expected exactly one VV annotation XML for {product_id}; found {len(keys)}")
        key=keys[0]; body=bucket.Object(key).get()["Body"].read()
        grid=parse_geolocation_grid(body)
        props=feature.get("properties",{})
        results.append({"product_id":product_id,"datetime_utc":props.get("datetime"),
            "relative_orbit":props.get("sat:relative_orbit"),"annotation_key":key,
            "annotation_size_bytes":len(body),"geolocation_grid":grid})
    return results

def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--output",type=Path,default=Path("data/sentinelhub/nairobi/sentinel1_grd_incidence_geolocation_grids.json"))
    a=p.parse_args(argv); access=os.environ.get("CDSE_S3_ACCESS_KEY",""); secret=os.environ.get("CDSE_S3_SECRET_KEY","")
    if not access or not secret: print("Missing CDSE S3 credentials.",file=sys.stderr); return 2
    try:
        token=CAT.request_access_token(os.environ.get("SENTINEL_HUB_CLIENT_ID",""),os.environ.get("SENTINEL_HUB_CLIENT_SECRET",""),timeout=30)
        features=collect_catalog_items(token,"2025-01-01T00:00:00Z","2025-02-20T00:00:00Z")
        products=extract_all(features,access,secret)
    except Exception as exc:
        print(f"Geolocation-grid extraction failed: {type(exc).__name__}: {exc}",file=sys.stderr); return 2
    report={"schema":"tessellatum.sentinel1.grd-incidence-geolocation-grids.v1",
        "products":products,"product_count":len(products),"analysis_ready":False,
        "purpose":"Source GRD geolocation-grid tie points for independent incidence-angle interpolation QA.",
        "limitations":["The tie points are sparse source-grid samples, not an interpolated output raster.",
            "Interpolation must be validated on held-out tie points and checked for spatial coverage.",
            "The annotation incidenceAngle field is retained as supplied; no terrain-angle substitution is made."]}
    a.output.parent.mkdir(parents=True,exist_ok=True); a.output.write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    print(f"Products extracted: {len(products)}; total tie points: {sum(x['geolocation_grid']['point_count'] for x in products)}")
    for x in products:
        g=x["geolocation_grid"]; ang=g["incidence_angle_degrees"]
        print(f"R{x['relative_orbit']:03d} {x['datetime_utc']}: {g['point_count']} points ({g['unique_line_count']}x{g['unique_pixel_count']}); incidence={ang['min']:.6f}/{ang['median']:.6f}/{ang['max']:.6f}; complete={g['grid_complete']}")
    print(f"Report: {a.output}; analysis_ready=false")
    return 0
if __name__=="__main__": raise SystemExit(main())
