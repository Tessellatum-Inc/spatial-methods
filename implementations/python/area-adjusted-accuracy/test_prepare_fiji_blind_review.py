import csv,json,tempfile,unittest
from pathlib import Path
from prepare_fiji_blind_review import prepare

class PrepareBlindReviewTests(unittest.TestCase):
 def test_quality_rank_and_cross_catalogue_rgb_match(self):
  with tempfile.TemporaryDirectory() as d:
   root=Path(d); points=root/"points.csv"
   points.write_text("sample_id,longitude,latitude\nP1,179,-18\n",encoding="utf-8")
   spectral=root/"spectral.csv"; fields=["sample_id","item_id","collection","datetime","cloud_cover_percent","platform","status","bands_read","missing_bands","indices"]
   with spectral.open("w",newline="",encoding="utf-8") as f:
    w=csv.DictWriter(f,fieldnames=fields); w.writeheader()
    for item,valid in (("cloudy",.25),("clear",.95)):
     w.writerow({"sample_id":"P1","item_id":item,"collection":"test","datetime":"2021-06-01T00:00:00Z","cloud_cover_percent":1,"platform":"sentinel-2a","status":"core_bands_read","bands_read":json.dumps(["B02","B03","B04","B08","SCL"]),"missing_bands":"[]","indices":json.dumps({"SCL_QA_20m":{"analysis_valid_fraction":valid,"cloud_shadow_fraction":1-valid,"analysis_valid_pixel_count":int(valid*256),"pixel_count":256}})})
   rgb=root/"rgb.csv"
   rgb.write_text("sample_id,item_id,platform,datetime,status,chip_file,chip_sha256\nP1,alias,sentinel-2a,2021-06-01T00:00:01Z,chip_created,/tmp/P1.png,abc\n",encoding="utf-8")
   result=prepare(spectral,points,root/"out",rgb)
   with Path(result["ranking_csv"]).open(newline="",encoding="utf-8") as f: ranked=list(csv.DictReader(f))
   self.assertEqual(ranked[0]["item_id"],"clear")
   self.assertEqual(ranked[0]["rgb_match_method"],"same_platform_datetime_within_2s")
   self.assertEqual(ranked[0]["rgb_chip_file"],"chips/P1.png")
   with Path(result["review_worksheet_csv"]).open(newline="",encoding="utf-8") as f: row=next(csv.DictReader(f))
   self.assertIn("interpreted_class",row); self.assertIn("rgb_chip_inventory",row)
   self.assertNotIn("transition",row); self.assertNotIn("fiji_class",row)
   self.assertEqual(row["primary_rgb_match_status"],"same_platform_datetime_within_2s")
 def test_never_attach_unrelated_scene_as_candidate_chip(self):
  with tempfile.TemporaryDirectory() as d:
   root=Path(d); points=root/"points.csv"; points.write_text("sample_id,longitude,latitude\nP1,179,-18\n")
   spectral=root/"spectral.csv"; fields=["sample_id","item_id","collection","datetime","cloud_cover_percent","platform","status","bands_read","missing_bands","indices"]
   with spectral.open("w",newline="") as f:
    w=csv.DictWriter(f,fieldnames=fields); w.writeheader()
    w.writerow({"sample_id":"P1","item_id":"scene-a","collection":"test","datetime":"2021-06-01T00:00:00Z","platform":"sentinel-2a","status":"core_bands_read","bands_read":'["B02","B03","B04","B08"]',"missing_bands":"[]","indices":"{}"})
   rgb=root/"rgb.csv"; rgb.write_text("sample_id,item_id,platform,datetime,status,chip_file\nP1,other,sentinel-2a,2021-07-01T00:00:00Z,chip_created,/tmp/other.png\n")
   result=prepare(spectral,points,root/"out",rgb)
   with Path(result["review_worksheet_csv"]).open(newline="",encoding="utf-8") as f: row=next(csv.DictReader(f))
   self.assertEqual(row["primary_rgb_chip_file"],"")
   self.assertEqual(row["primary_rgb_match_status"],"no_same_acquisition_rgb_chip")
   self.assertIn("other.png",row["rgb_chip_inventory"])

if __name__=="__main__": unittest.main()
