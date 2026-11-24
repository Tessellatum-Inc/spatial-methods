import unittest
from explorations.radar.acquire_nairobi_r130_dynamic_world import date_window, DATES, PROBABILITY_BANDS

class DynamicWorldWindowTests(unittest.TestCase):
    def test_acquisition_windows_are_symmetric_calendar_windows(self):
        self.assertEqual(date_window("2026-10-06"),("2026-09-21","2026-10-22"))
        self.assertEqual(date_window("2026-11-23"),("2026-11-08","2026-12-09"))

    def test_all_five_r130_dates_are_configured(self):
        self.assertEqual(len(DATES),5)
        self.assertEqual(len(PROBABILITY_BANDS),9)
        self.assertIn("built",PROBABILITY_BANDS)
        self.assertIn("shrub_and_scrub",PROBABILITY_BANDS)

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

if __name__=="__main__":unittest.main()
