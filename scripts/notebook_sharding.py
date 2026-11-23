"""Deterministic partitioning for parallel notebook execution."""


def select_notebooks(notebooks, shard_count=1, shard_index=0):
    """Return one stable modulo shard of a sequence of (filename, timeout) pairs."""
    if isinstance(shard_count, bool) or not isinstance(shard_count, int) or shard_count < 1:
        raise ValueError("shard_count must be a positive integer")
    if isinstance(shard_index, bool) or not isinstance(shard_index, int):
        raise ValueError("shard_index must be an integer")
    if not 0 <= shard_index < shard_count:
        raise ValueError("shard_index must be in [0, shard_count)")
    return [item for index, item in enumerate(notebooks) if index % shard_count == shard_index]
