import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import sample_worldcover


class PinnedFijiPointReaderTests(unittest.TestCase):
    def make_geojson(self):
        features = [
            {
                "type": "Feature",
                "properties": {"strata": 3, "ref_class": 1},
                "geometry": {"type": "Point", "coordinates": [177.5, -16.7]},
            },
            {
                "type": "Feature",
                "properties": {"strata": 8, "ref_class": 8},
                "geometry": {"type": "Point", "coordinates": [178.0, -17.0]},
            },
        ]
        return json.dumps({"type": "FeatureCollection", "features": features}).encode()

    def test_reader_assigns_stable_order_ids_and_preserves_design_labels(self):
        data = self.make_geojson()
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "points.geojson"
            path.write_bytes(data)
            with patch.object(
                sample_worldcover, "EXPECTED_GIT_BLOB_SHA1",
                sample_worldcover.git_blob_sha1(data)
            ), patch.object(sample_worldcover, "EXPECTED_SAMPLE_COUNT", 2):
                points, blob_sha = sample_worldcover.read_pinned_points(str(path))

        self.assertEqual(blob_sha, sample_worldcover.git_blob_sha1(data))
        self.assertEqual(points[0]["sample_id"], "FJI2021-000001")
        self.assertEqual(points[0]["sampling_stratum"], "bare_soil_rock")
        self.assertEqual(points[0]["reference_class"], "water")
        self.assertEqual(points[1]["sample_id"], "FJI2021-000002")
        self.assertEqual(points[1]["sampling_stratum"], "tree")

    def test_reader_rejects_unpinned_geojson(self):
        data = self.make_geojson()
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "points.geojson"
            path.write_bytes(data)
            with patch.object(sample_worldcover, "EXPECTED_SAMPLE_COUNT", 2):
                with self.assertRaises(ValueError):
                    sample_worldcover.read_pinned_points(str(path))

    def test_reader_rejects_nonpoint_features(self):
        data = json.loads(self.make_geojson())
        data["features"][0]["geometry"]["type"] = "Polygon"
        encoded = json.dumps(data).encode()
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "points.geojson"
            path.write_bytes(encoded)
            with patch.object(
                sample_worldcover, "EXPECTED_GIT_BLOB_SHA1",
                sample_worldcover.git_blob_sha1(encoded)
            ), patch.object(sample_worldcover, "EXPECTED_SAMPLE_COUNT", 2):
                with self.assertRaises(ValueError):
                    sample_worldcover.read_pinned_points(str(path))


if __name__ == "__main__":
    unittest.main()
