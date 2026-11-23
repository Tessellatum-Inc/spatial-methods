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

def calibration_lut_bilinear_at(vectors,line,pixel):
    ordered=sorted(vectors,key=lambda v:v["line"])
    lines=np.asarray([v["line"] for v in ordered],dtype=np.float64)
    if line<lines[0] or line>lines[-1]: return float("nan")
    hi=int(np.searchsorted(lines,line,side="left"))
    if hi<len(lines) and lines[hi]==line: lo=hi
    else: lo=hi-1
    def interpolate_row(index):
        px=np.asarray(ordered[index]["pixels"],dtype=np.float64)
        values=np.asarray(ordered[index]["incidence_angle_degrees"],dtype=np.float64)
        if pixel<px[0] or pixel>px[-1]: return float("nan")
        return float(np.interp(pixel,px,values))
    low=interpolate_row(lo)
    if not np.isfinite(low): return float("nan")
    if lo==hi: return low
    high=interpolate_row(hi)
    if not np.isfinite(high): return float("nan")
    fraction=(line-lines[lo])/(lines[hi]-lines[lo])
    return float(low*(1.0-fraction)+high*fraction)

def _angle_difference_metrics(predicted,expected):
    valid=np.isfinite(predicted)&np.isfinite(expected)
    if not valid.any(): raise ValueError("No matched angle samples for calibration comparison")
    error=predicted[valid]-expected[valid]; absolute=np.abs(error)
    return {"matched_tie_points":int(valid.sum()),"coverage_fraction":float(valid.mean()),
        "mean_signed_difference_degrees":float(np.mean(error)),
        "mae_degrees":float(np.mean(absolute)),
        "rmse_degrees":float(np.sqrt(np.mean(error**2))),
        "p95_absolute_error_degrees":float(np.percentile(absolute,95)),
        "max_absolute_error_degrees":float(np.max(absolute))}

def compare_calibration_to_annotation(calibration_lut:dict,annotation_grid:dict)->dict:
    from scipy.interpolate import LinearNDInterpolator
    from scipy.spatial import Delaunay, QhullError
    source_xy=[]; source_angles=[]
    for vector in calibration_lut["vectors"]:
        for pixel,angle in zip(vector["pixels"],vector["incidence_angle_degrees"]):
            source_xy.append((vector["line"],pixel)); source_angles.append(angle)
    xy=np.asarray(source_xy,dtype=np.float64); values=np.asarray(source_angles,dtype=np.float64)
    target=np.asarray([(p["line"],p["pixel"]) for p in annotation_grid["points"]],dtype=np.float64)
    expected=np.asarray([p["incidenceAngle"] for p in annotation_grid["points"]],dtype=np.float64)
    try:
        triangulation=Delaunay(xy)
        predicted=np.asarray(LinearNDInterpolator(triangulation,values,fill_value=np.nan)(target),dtype=np.float64)
    except QhullError as exc:
        raise ValueError(f"Could not triangulate calibration LUT source coordinates: {exc}") from exc
    valid=np.isfinite(predicted)&np.isfinite(expected)
    if not valid.any(): raise ValueError("No annotation geolocation points fall inside calibration LUT hull")
    bilinear=np.asarray([calibration_lut_bilinear_at(calibration_lut["vectors"],p["line"],p["pixel"]) for p in annotation_grid["points"]],dtype=np.float64)
    delaunay_metrics=_angle_difference_metrics(predicted,expected)
    bilinear_metrics=_angle_difference_metrics(bilinear,expected)
    return {"method":"Delaunay and bilinear interpolation of calibration LUT samples in source line/pixel coordinates",
        "annotation_tie_points":int(len(expected)),
        "matched_tie_points":delaunay_metrics["matched_tie_points"],
        "annotation_tie_point_coverage_fraction":delaunay_metrics["coverage_fraction"],
        "mean_signed_difference_degrees":delaunay_metrics["mean_signed_difference_degrees"],
        "median_signed_difference_degrees":float(np.median(predicted[valid]-expected[valid])),
        "mae_degrees":delaunay_metrics["mae_degrees"],"rmse_degrees":delaunay_metrics["rmse_degrees"],
        "p95_absolute_error_degrees":delaunay_metrics["p95_absolute_error_degrees"],
        "max_absolute_error_degrees":delaunay_metrics["max_absolute_error_degrees"],
        "delaunay":delaunay_metrics,"bilinear":bilinear_metrics}

def extract_calibration_files(features,annotation_products,access_key,secret_key):
    import boto3
    from botocore.config import Config
    resource=boto3.resource("s3",endpoint_url="https://eodata.dataspace.copernicus.eu",
        aws_access_key_id=access_key,aws_secret_access_key=secret_key,region_name="default",
        config=Config(signature_version="s3v4"))
    annotations={p["product_id"]:p["geolocation_grid"] for p in annotation_products}
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
        annotation=annotations.get(product_id)
        if annotation is None: raise RuntimeError(f"Annotation geolocation grid missing for {product_id}")
        comparison=compare_calibration_to_annotation(parsed_lut,annotation)
        props=feature.get("properties",{})
        output.append({"product_id":product_id,"datetime_utc":props.get("datetime"),
            "relative_orbit":props.get("sat:relative_orbit"),"calibration_key":key,
            "calibration_xml_size_bytes":len(body),"calibration_lut":parsed_lut,
            "calibration_vs_annotation_angle_qa":comparison})
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
        annotations=SRC.extract_all(features,access,secret)
        products=extract_calibration_files(features,annotations,access,secret)
        if len(products)!=8: raise ValueError(f"Expected 8 calibration files; found {len(products)}")
    except Exception as exc:
        print(f"Calibration LUT extraction failed: {type(exc).__name__}: {exc}",file=sys.stderr); return 2
    report={"schema":"tessellatum.sentinel1.grd-calibration-lut-incidence-qa.v1",
        "products":products,"product_count":len(products),"analysis_ready":False,
        "derivation":{"theta_from_gamma_sigma_degrees":"arccos((gamma / sigmaNought)^2)",
            "theta_from_beta_sigma_degrees":"arcsin((betaNought / sigmaNought)^2)",
            "source":"ESA Sentinel-1 Radiometric Calibration technical note; calibration LUT area relationships"},
        "limitations":["This checks internal consistency of the source calibration LUT identities.",
            "Calibration LUT angles are linearly interpolated in source line/pixel coordinates and compared with annotation geolocationGridPoint incidenceAngle; this is an internal product-metadata cross-check, not an independent geodetic reference.",
            "No radiometric normalization or change detection is performed."]}
    a.output.parent.mkdir(parents=True,exist_ok=True); a.output.write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    for product in products:
        lut=product["calibration_lut"]; a0=lut["incidence_angle_degrees"]; qa=product["calibration_vs_annotation_angle_qa"]
        print(f"R{product['relative_orbit']:03d} {product['datetime_utc']}: vectors={lut['vector_count']}, samples={lut['sample_count']}, angle={a0['min']:.5f}/{a0['median']:.5f}/{a0['max']:.5f} degrees, LUT identity max diff={lut['max_beta_sigma_vs_gamma_sigma_identity_difference_degrees']:.6g} degrees, annotation matched={qa['matched_tie_points']}/{qa['annotation_tie_points']}, cross-source bias/MAE/RMSE/P95={qa['mean_signed_difference_degrees']:.5f}/{qa['mae_degrees']:.5f}/{qa['rmse_degrees']:.5f}/{qa['p95_absolute_error_degrees']:.5f} degrees")
    print(f"Products extracted: {len(products)}; report={a.output}; analysis_ready=false")
    return 0
if __name__=="__main__": raise SystemExit(main())
