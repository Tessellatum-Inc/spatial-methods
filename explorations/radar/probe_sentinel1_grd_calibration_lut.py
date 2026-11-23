#!/usr/bin/env python3
"""Derive ellipsoid incidence angles independently from Sentinel-1 GRD calibration LUTs."""
from __future__ import annotations
import argparse, importlib.util, json, os, sys
from pathlib import Path
from urllib.parse import urlparse
from xml.etree import ElementTree as ET
import numpy as np

RADAR=Path(__file__).resolve().parent
SPEC=importlib.util.spec_from_file_location("extract_sentinel1_grd_incidence_grids",RADAR/"extract_sentinel1_grd_incidence_grids.py")
if SPEC is None or SPEC.loader is None: raise RuntimeError("Cannot load Sentinel-1 GRD source catalogue helper")
SRC=importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(SRC)
PRODUCT_IDS=sorted(SRC.PRODUCT_IDS)

def local_name(tag): return tag.rsplit("}",1)[-1]

def parse_calibration_lut(xml_bytes:bytes)->dict:
    root=ET.fromstring(xml_bytes); vectors=[]
    for node in root.iter():
        if local_name(node.tag)!="calibrationVector": continue
        values={local_name(child.tag):(child.text or "").strip() for child in node}
        try:
            line=float(values["line"])
            pixels=np.fromstring(values["pixel"],sep=" ",dtype=np.float64)
            sigma=np.fromstring(values["sigmaNought"],sep=" ",dtype=np.float64)
            beta=np.fromstring(values["betaNought"],sep=" ",dtype=np.float64)
            gamma=np.fromstring(values["gamma"],sep=" ",dtype=np.float64)
        except (KeyError,ValueError): continue
        if not (len(pixels)==len(sigma)==len(beta)==len(gamma)) or len(pixels)==0:
            raise ValueError(f"Calibration vector at line {line} has inconsistent array lengths")
        valid=np.isfinite(pixels)&np.isfinite(sigma)&np.isfinite(beta)&np.isfinite(gamma)&(sigma>0)&(beta>0)&(gamma>0)
        if not valid.all(): raise ValueError(f"Calibration vector at line {line} contains invalid or non-positive LUT values")
        cos_theta=(gamma/sigma)**2
        sin_theta=(beta/sigma)**2
        if np.any((cos_theta<=0)|(cos_theta>1)) or np.any((sin_theta<=0)|(sin_theta>1)):
            raise ValueError(f"Calibration ratios outside physical incidence-angle domain at line {line}")
        theta_cos=np.rad2deg(np.arccos(cos_theta))
        theta_sin=np.rad2deg(np.arcsin(sin_theta))
        difference=np.abs(theta_cos-theta_sin)
        vectors.append({"line":line,"pixel_min":float(pixels.min()),"pixel_max":float(pixels.max()),
            "sample_count":int(len(pixels)),"incidence_angle_min_degrees":float(theta_cos.min()),
            "incidence_angle_median_degrees":float(np.median(theta_cos)),
            "incidence_angle_max_degrees":float(theta_cos.max()),
            "max_identity_difference_degrees":float(difference.max()),
            "pixels":pixels.tolist(),"incidence_angle_degrees":theta_cos.tolist()})
    if not vectors: raise ValueError("No usable calibrationVector records found")
    lines=np.asarray([v["line"] for v in vectors],dtype=np.float64)
    all_angles=np.concatenate([np.asarray(v["incidence_angle_degrees"]) for v in vectors])
    return {"vector_count":len(vectors),"sample_count":int(len(all_angles)),
        "unique_line_count":int(len(np.unique(lines))),"line_min":float(lines.min()),"line_max":float(lines.max()),
        "incidence_angle_degrees":{"min":float(all_angles.min()),"median":float(np.median(all_angles)),"max":float(all_angles.max())},
        "max_beta_sigma_vs_gamma_sigma_identity_difference_degrees":float(max(v["max_identity_difference_degrees"] for v in vectors)),
        "vectors":vectors}

def extract_calibration_files(features,access_key,secret_key):
    import boto3
    from botocore.config import Config
    resource=boto3.resource("s3",endpoint_url="https://eodata.dataspace.copernicus.eu",
        aws_access_key_id=access_key,aws_secret_access_key=secret_key,region_name="default",
        config=Config(signature_version="s3v4"))
    output=[]
    for product_id in PRODUCT_IDS:
        feature=features.get(product_id)
        if feature is None: raise RuntimeError(f"Catalogue item missing: {product_id}")
        href=(feature.get("assets") or {}).get("data",{}).get("href")
        parsed=urlparse(href or "")
        if parsed.scheme!="s3" or not parsed.netloc: raise RuntimeError(f"Invalid S3 data asset for {product_id}")
        bucket=resource.Bucket(parsed.netloc); prefix=parsed.path.lstrip("/").rstrip("/")+"/"
        keys=[o.key for o in bucket.objects.filter(Prefix=prefix)
            if "/annotation/calibration/" in o.key.lower() and o.key.lower().endswith(".xml")
            and "calibration-" in o.key.lower() and "iw-grd-vv-" in o.key.lower()]
        if len(keys)!=1: raise RuntimeError(f"Expected one calibration XML for {product_id}; found {len(keys)}")
        key=keys[0]; body=bucket.Object(key).get()["Body"].read()
        parsed_lut=parse_calibration_lut(body)
        props=feature.get("properties",{})
        output.append({"product_id":product_id,"datetime_utc":props.get("datetime"),
            "relative_orbit":props.get("sat:relative_orbit"),"calibration_key":key,
            "calibration_xml_size_bytes":len(body),"calibration_lut":parsed_lut})
    return output

def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--output",type=Path,default=Path("data/sentinelhub/nairobi/sentinel1_grd_calibration_lut_incidence_qa.json"))
    a=p.parse_args(argv); access=os.environ.get("CDSE_S3_ACCESS_KEY",""); secret=os.environ.get("CDSE_S3_SECRET_KEY","")
    if not access or not secret: print("Missing CDSE S3 credentials.",file=sys.stderr); return 2
    try:
        token=SRC.CAT.request_access_token(os.environ.get("SENTINEL_HUB_CLIENT_ID",""),
            os.environ.get("SENTINEL_HUB_CLIENT_SECRET",""),timeout=30)
        features=SRC.collect_catalog_items(token,"2025-01-01T00:00:00Z","2025-02-20T00:00:00Z")
        products=extract_calibration_files(features,access,secret)
        if len(products)!=8: raise ValueError(f"Expected 8 calibration files; found {len(products)}")
    except Exception as exc:
        print(f"Calibration LUT extraction failed: {type(exc).__name__}: {exc}",file=sys.stderr); return 2
    report={"schema":"tessellatum.sentinel1.grd-calibration-lut-incidence-qa.v1",
        "products":products,"product_count":len(products),"analysis_ready":False,
        "derivation":{"theta_from_gamma_sigma_degrees":"arccos((gamma / sigmaNought)^2)",
            "theta_from_beta_sigma_degrees":"arcsin((betaNought / sigmaNought)^2)",
            "source":"ESA Sentinel-1 Radiometric Calibration technical note; calibration LUT area relationships"},
        "limitations":["This checks internal consistency of the source calibration LUT identities.",
            "The calibration-derived angle samples have not yet been spatially interpolated or compared with annotation geolocationGridPoint incidenceAngle.",
            "No radiometric normalization or change detection is performed."]}
    a.output.parent.mkdir(parents=True,exist_ok=True); a.output.write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    for product in products:
        lut=product["calibration_lut"]; a0=lut["incidence_angle_degrees"]
        print(f"R{product['relative_orbit']:03d} {product['datetime_utc']}: vectors={lut['vector_count']}, samples={lut['sample_count']}, angle={a0['min']:.5f}/{a0['median']:.5f}/{a0['max']:.5f} degrees, identity max diff={lut['max_beta_sigma_vs_gamma_sigma_identity_difference_degrees']:.6g} degrees")
    print(f"Products extracted: {len(products)}; report={a.output}; analysis_ready=false")
    return 0
if __name__=="__main__": raise SystemExit(main())
