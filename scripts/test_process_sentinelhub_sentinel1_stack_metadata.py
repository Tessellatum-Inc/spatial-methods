"""Tests for retained Sentinel-1 catalogue acquisition metadata."""
import importlib.util
from pathlib import Path
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "explorations/radar/process_sentinelhub_sentinel1_stack.py"
spec = importlib.util.spec_from_file_location("sentinel1_stack_processor", SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class CatalogueAcquisitionMetadataTests(unittest.TestCase):
    def test_retains_orbit_and_sensor_properties(self):
        feature = {"properties": {
            "datetime": "2026-11-14T03:11:11Z",
            "platform": "sentinel-1c",
            "sat:orbit_state": "descending",
            "sat:relative_orbit": 79,
            "sat:absolute_orbit": 10327,
            "sar:instrument_mode": "IW",
            "sar:polarizations": ["VV", "VH"],
            "s1:timeliness": "Fast24h",
            "unrelated": "discarded",
        }}
        result = module.catalogue_acquisition_metadata(feature)
        self.assertEqual(result["sat:relative_orbit"], 79)
        self.assertEqual(result["sat:orbit_state"], "descending")
        self.assertEqual(result["sar:instrument_mode"], "IW")
        self.assertEqual(result["sar:polarizations"], ["VV", "VH"])
        self.assertNotIn("unrelated", result)

    def test_missing_metadata_is_not_inferred(self):
        self.assertEqual(module.catalogue_acquisition_metadata({"properties": {"datetime": "x"}}), {"datetime": "x"})
        self.assertEqual(module.catalogue_acquisition_metadata({"properties": None}), {})

    def test_non_dictionary_properties_are_ignored(self):
        self.assertEqual(module.catalogue_acquisition_metadata({"properties": []}), {})


if __name__ == "__main__":
    unittest.main()
