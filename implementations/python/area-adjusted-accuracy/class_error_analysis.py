"""Class-specific design-weighted error decomposition for Fiji–WorldCover."""
from __future__ import annotations
import argparse, csv, hashlib, json, math
from collections import Counter, defaultdict
from pathlib import Path

REQUIRED = {"sample_id", "sampling_stratum", "map_class", "reference_class"}

def load_observations(path):
    raw = Path(path).read_bytes()
    rows = list(csv.DictReader(raw.decode("utf-8-sig").splitlines()))
    if not rows or not REQUIRED.issubset(rows[0]):
        raise ValueError("CSV must include sample_id, sampling_stratum, map_class and reference_class.")
    seen=set(); out=[]
    for i,r in enumerate(rows,1):
        sid=r["sample_id"].strip(); h=r["sampling_stratum"].strip(); m=r["map_class"].strip(); ref=r["reference_class"].strip()
        if not sid or sid in seen: raise ValueError(f"Row {i}: sample_id must be unique and non-empty.")
        if not h or not m or not ref: raise ValueError(f"Row {i}: class labels must be non-empty.")
        seen.add(sid); out.append({"sample_id":sid,"sampling_stratum":h,"map_class":m,"reference_class":ref})
    return out, hashlib.sha256(raw).hexdigest()

def _map_summary(rows, weights, map_name, prediction):
    nh=Counter(r["sampling_stratum"] for r in rows)
    labels=sorted({r["reference_class"] for r in rows}|{prediction(r) for r in rows})
    matrix=defaultdict(float); sample_matrix=Counter(); mapped_area=Counter(); reference_area=Counter()
    for r in rows:
        h=r["sampling_stratum"]; pred=prediction(r); ref=r["reference_class"]
        contribution=weights[h]/nh[h]
        matrix[(pred,ref)]+=contribution; sample_matrix[(pred,ref)]+=1
        mapped_area[pred]+=contribution; reference_area[ref]+=contribution
    overall=sum(matrix[(c,c)] for c in labels)
    class_rows=[]
    for c in labels:
        diag=matrix[(c,c)]
        pa=diag/reference_area[c] if reference_area[c] else None
        ua=diag/mapped_area[c] if mapped_area[c] else None
        ref_n=sum(sample_matrix[(m,c)] for m in labels)
        map_n=sum(sample_matrix[(c,ref)] for ref in labels)
        class_rows.append({"class":c,"reference_sample_count":ref_n,"mapped_sample_count":map_n,
          "estimated_reference_area_percent":100*reference_area[c],"estimated_mapped_area_percent":100*mapped_area[c],
          "producers_accuracy_percent":None if pa is None else 100*pa,
          "users_accuracy_percent":None if ua is None else 100*ua,
          "omission_error_contribution_pp":100*(reference_area[c]-diag),
          "commission_error_contribution_pp":100*(mapped_area[c]-diag)})
    transitions=[]
    for (pred,ref),v in matrix.items():
        if pred!=ref and v>0:
            transitions.append({"map_class":pred,"reference_class":ref,"sample_count":sample_matrix[(pred,ref)],
                                "weighted_error_contribution_pp":100*v})
    transitions.sort(key=lambda x:(-x["weighted_error_contribution_pp"],x["map_class"],x["reference_class"]))
    matrix_rows=[]
    for pred in labels:
        matrix_rows.append({"map_class":pred,"cells":[{"reference_class":ref,"estimated_area_percent":100*matrix[(pred,ref)],"sample_count":sample_matrix[(pred,ref)]} for ref in labels]})
    return {"map":map_name,"overall_accuracy_percent":100*overall,"class_metrics":class_rows,
            "area_adjusted_error_matrix":matrix_rows,"largest_error_transitions":transitions,
            "mapped_area_estimates_percent":{c:100*mapped_area[c] for c in labels},
            "reference_area_estimates_percent":{c:100*reference_area[c] for c in labels}}

def analyse(rows, weights):
    weights={str(k):float(v) for k,v in weights.items()}
    if not weights or any(not math.isfinite(v) or v<=0 for v in weights.values()) or not math.isclose(sum(weights.values()),1,abs_tol=1e-9):
        raise ValueError("Stratum area weights must be positive and sum to one.")
    nh=Counter(r["sampling_stratum"] for r in rows)
    if set(nh)!=set(weights): raise ValueError("Observed sampling strata must exactly match supplied weight keys.")
    fiji=_map_summary(rows,weights,"Fiji 2021 map",lambda r:r["sampling_stratum"])
    wc=_map_summary(rows,weights,"ESA WorldCover 2021 v200",lambda r:r["map_class"])
    ref_classes=sorted({r["reference_class"] for r in rows})
    byclass=[]
    fidx={x["class"]:x for x in fiji["class_metrics"]}; wcidx={x["class"]:x for x in wc["class_metrics"]}
    for c in ref_classes:
        a=fidx[c];b=wcidx[c]
        byclass.append({"reference_class":c,"reference_sample_count":a["reference_sample_count"],
          "reference_area_estimate_percent":a["estimated_reference_area_percent"],
          "fiji_producers_accuracy_percent":a["producers_accuracy_percent"],
          "worldcover_producers_accuracy_percent":b["producers_accuracy_percent"],
          "worldcover_minus_fiji_producers_accuracy_pp":b["producers_accuracy_percent"]-a["producers_accuracy_percent"],
          "fiji_omission_error_contribution_pp":a["omission_error_contribution_pp"],
          "worldcover_omission_error_contribution_pp":b["omission_error_contribution_pp"],
          "worldcover_minus_fiji_omission_error_pp":b["omission_error_contribution_pp"]-a["omission_error_contribution_pp"]})
    byclass.sort(key=lambda x:-x["worldcover_omission_error_contribution_pp"])
    transition=defaultdict(lambda:[0,0.0])
    for r in rows:
        h=r["sampling_stratum"];key=(h,r["map_class"]);transition[key][0]+=1;transition[key][1]+=weights[h]/nh[h]
    stratum_to_wc=[{"original_fiji_stratum":h,"worldcover_class":c,"sample_count":n,"weighted_area_contribution_percent":100*v}
      for (h,c),(n,v) in transition.items()]
    stratum_to_wc.sort(key=lambda x:(x["original_fiji_stratum"],-x["weighted_area_contribution_percent"]))
    return {"title":"Class-specific error decomposition: Fiji 2021 and ESA WorldCover 2021 v200",
      "sample_size":len(rows),"design":"Stratified simple random sample without replacement within original Fiji mapped-class strata.",
      "estimator":"Each matrix cell is the sum over original sampling strata of W_h times its within-stratum sample proportion. Class accuracy ratios use design-weighted matrix margins.",
      "sampling_stratum_area_weights":weights,"sample_counts_by_stratum":dict(nh),
      "fiji":fiji,"worldcover":wc,"reference_class_comparison":byclass,
      "original_fiji_stratum_to_worldcover_transitions":stratum_to_wc,
      "dominant_worldcover_error_transitions":wc["largest_error_transitions"][:15],
      "limitations":["Results apply to the eligible Fiji sampling frame, excluding Tikinas used for training samples.",
       "Reference labels are supplied visual interpretations and were not independently field-verified here.",
       "WorldCover is sampled from the single raster cell containing each point; positional tolerance and mixed-pixel effects are not modelled.",
       "Class-specific accuracy ratios are descriptive point estimates; no confidence intervals are provided for these ratios.",
       "Very small or empty predicted classes produce unstable or undefined user's accuracy. In particular, WorldCover agriculture has only two sample predictions, bare/sparse vegetation seven, and no shrubland predictions.",
       "Error transitions describe observed class confusions, not their causes. They cannot by themselves distinguish legend mismatch, mixed pixels, temporal change, reference-label uncertainty or classifier behaviour.",
       "The strict working class crosswalk is provisional; crosswalk sensitivity is analysed separately."]}

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument("observations_csv");p.add_argument("--stratum-area-weights",required=True);p.add_argument("--json-out",required=True);a=p.parse_args()
    try:
        rows,digest=load_observations(a.observations_csv);weights=json.loads(a.stratum_area_weights)
        if not isinstance(weights,dict):raise ValueError("Weights must be a JSON object.")
        result=analyse(rows,weights);result["input_csv_sha256"]=digest
        Path(a.json_out).write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf-8")
        print(json.dumps({"sample_size":result["sample_size"],"fiji_oa_percent":result["fiji"]["overall_accuracy_percent"],
          "worldcover_oa_percent":result["worldcover"]["overall_accuracy_percent"],
          "largest_worldcover_error_transitions":result["dominant_worldcover_error_transitions"][:8]},indent=2))
    except (OSError,ValueError,TypeError,json.JSONDecodeError) as exc:p.error(str(exc))
    return 0
if __name__=="__main__":raise SystemExit(main())
