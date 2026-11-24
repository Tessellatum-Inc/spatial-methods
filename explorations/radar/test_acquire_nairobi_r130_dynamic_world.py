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

if __name__=="__main__":unittest.main()
