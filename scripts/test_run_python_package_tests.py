import unittest

from run_python_package_tests import packages_for_shard


class PackageShardingTests(unittest.TestCase):
    def test_shards_partition_every_package_exactly_once(self):
        packages = [{"directory": f"package-{i}"} for i in range(17)]
        shards = [
            packages_for_shard(packages, index, 5)
            for index in range(5)
        ]
        flattened = [entry["directory"] for shard in shards for entry in shard]
        self.assertEqual(sorted(flattened), sorted(entry["directory"] for entry in packages))
        self.assertEqual(len(flattened), len(set(flattened)))

    def test_invalid_shard_coordinates_are_rejected(self):
        packages = [{"directory": "one"}]
        for index, count in [(-1, 2), (2, 2), (0, 0)]:
            with self.subTest(index=index, count=count):
                with self.assertRaises(ValueError):
                    packages_for_shard(packages, index, count)

    def test_more_shards_than_packages_produces_empty_shards(self):
        packages = [{"directory": "one"}, {"directory": "two"}]
        self.assertEqual(packages_for_shard(packages, 2, 3), [])


if __name__ == "__main__":
    unittest.main()
