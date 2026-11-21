import csv,json,tempfile,unittest
from pathlib import Path
from prepare_fiji_blind_review import prepare

class PrepareBlindReviewTests(unittest.TestCase):
 def test_local_quality_ranking_and_label_isolation(self):
  with tempfile.TemporaryDirectory() as d:
   root=Path(d); points=root/"points.csv"
   with points.open("w",newline="") as f:
    w=csv.DictWriter(f,fieldnames=["sample_id","longitude","latitude"]); w.writeheader()
    w.writerow({"sample_id":"P1","longitude":"179","latitude":"-18"})
   spectral=root/"spectral.csv"; fields=["sample_id","item_id","collection","datetime","cloud_cover_percent","platform","status","bands_read","missing_bands","indices"]
   with spectral.open("w",newline="") as f:
    w=csv.DictWriter(f,fieldnames=fields); w.writeheader()
    for item,valid in (("cloudy",.25),("clear",.95)):
     w.writerow({"sample_id":"P1","item_id":item,"collection":"test","datetime":"2021-06-01T00:00:00Z","cloud_cover_percent":1,"platform":"S2","status":"core_bands_read","bands_read":json.dumps(["B02","B03","B04","B08","SCL"]),"missing_bands":"[]","indices":json.dumps({"SCL_QA_20m":{"analysis_valid_fraction":valid,"cloud_shadow_fraction":1-valid,"analysis_valid_pixel_count":int(valid*256),"pixel_count":256}})})
   result=prepare(spectral,points,root/"out")
   with Path(result["ranking_csv"]).open() as f: ranked=list(csv.DictReader(f))
   self.assertEqual(ranked[0]["item_id"],"clear")
   with Path(result["review_worksheet_csv"]).open() as f: row=next(csv.DictReader(f))
   self.assertIn("interpreted_class",row); self.assertNotIn("transition",row); self.assertNotIn("fiji_class",row)

if __name__=="__main__": unittest.main()
