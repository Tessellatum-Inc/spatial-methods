import unittest
from urllib.error import HTTPError
from email.message import Message
from io import BytesIO
from explorations.radar.acquire_nairobi_r130_dynamic_world import date_window, DATES, PROBABILITY_BANDS, BBOX, make_download_tiles

class DynamicWorldWindowTests(unittest.TestCase):
    def test_acquisition_windows_are_symmetric_calendar_windows(self):
        self.assertEqual(date_window("2026-10-06"),("2026-09-21","2026-10-22"))
        self.assertEqual(date_window("2026-11-23"),("2026-11-08","2026-12-09"))

    def test_all_five_r130_dates_are_configured(self):
        self.assertEqual(len(DATES),5)
        self.assertEqual(len(PROBABILITY_BANDS),9)
        self.assertIn("built",PROBABILITY_BANDS)
        self.assertIn("shrub_and_scrub",PROBABILITY_BANDS)

    def test_download_tiles_cover_full_bbox_without_gaps_or_overlaps(self):
        tiles=make_download_tiles(BBOX,4,4)
        self.assertEqual(len(tiles),16)
        self.assertAlmostEqual(min(t[0] for t in tiles),BBOX[0])
        self.assertAlmostEqual(min(t[1] for t in tiles),BBOX[1])
        self.assertAlmostEqual(max(t[2] for t in tiles),BBOX[2])
        self.assertAlmostEqual(max(t[3] for t in tiles),BBOX[3])
        for i,a in enumerate(tiles):
            for b in tiles[i+1:]:
                ox=max(0,min(a[2],b[2])-max(a[0],b[0]))
                oy=max(0,min(a[3],b[3])-max(a[1],b[1]))
                self.assertFalse(ox>1e-12 and oy>1e-12)

    def test_download_tiles_reject_invalid_dimensions_and_bounds(self):
        with self.assertRaises(ValueError):make_download_tiles(BBOX,0,4)
        with self.assertRaises(ValueError):make_download_tiles([1,2,0,3],2,2)

    def test_project_identity_normalizes_resource_manager_path_and_reports_match(self):
        from explorations.radar.acquire_nairobi_r130_dynamic_world import diagnose_project_identity
        project = diagnose_project_identity(
            {"project_id": "sample-project-123"}, "projects/sample-project-123"
        )
        self.assertEqual(project, "sample-project-123")

    def test_project_identity_keeps_explicit_project_when_service_account_differs(self):
        from explorations.radar.acquire_nairobi_r130_dynamic_world import diagnose_project_identity
        project = diagnose_project_identity(
            {"project_id": "service-account-project"}, "earth-engine-project"
        )
        self.assertEqual(project, "earth-engine-project")

    def test_project_identity_rejects_missing_configured_project(self):
        from explorations.radar.acquire_nairobi_r130_dynamic_world import diagnose_project_identity
        with self.assertRaises(ValueError):
            diagnose_project_identity({"project_id": "sample-project"}, "   ")

    def test_download_http_error_includes_bounded_response_and_safe_request_context(self):
        from explorations.radar.acquire_nairobi_r130_dynamic_world import format_download_http_error
        headers=Message()
        headers["Content-Type"]="application/json"
        headers["Content-Length"]="42"
        error=HTTPError("https://example.invalid/token=do-not-log",400,"Bad Request",headers,BytesIO(b'{"error":"request too large"}'))
        message=format_download_http_error(error,"2026-11-23",{
            "name":"dynamic-world-nairobi-r130-2026-11-23",
            "scale":30,"crs":"EPSG:4326","format":"GEO_TIFF"
        })
        self.assertIn("HTTP 400",message)
        self.assertIn("request too large",message)
        self.assertIn("scale_m=30",message)
        self.assertNotIn("do-not-log",message)

if __name__=="__main__":unittest.main()
