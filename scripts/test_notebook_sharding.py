import unittest

from notebook_sharding import select_notebooks


class NotebookShardingTests(unittest.TestCase):
    def test_shards_partition_every_notebook_once_in_original_order(self):
        notebooks = [(f"lab-{index}.ipynb", 180) for index in range(23)]
        shards = [select_notebooks(notebooks, 5, index) for index in range(5)]
        flattened = [item for shard in shards for item in shard]
        self.assertEqual(sorted(flattened), sorted(notebooks))
        self.assertEqual(len(flattened), len(set(flattened)))
        self.assertLessEqual(max(map(len, shards)) - min(map(len, shards)), 1)

    def test_single_shard_preserves_full_manifest_order(self):
        notebooks = [("a.ipynb", 10), ("b.ipynb", 20)]
        self.assertEqual(select_notebooks(notebooks), notebooks)

    def test_rejects_invalid_shard_controls(self):
        with self.assertRaises(ValueError): select_notebooks([], 0, 0)
        with self.assertRaises(ValueError): select_notebooks([], 2, 2)
        with self.assertRaises(ValueError): select_notebooks([], True, 0)


if __name__ == "__main__":
    unittest.main()
