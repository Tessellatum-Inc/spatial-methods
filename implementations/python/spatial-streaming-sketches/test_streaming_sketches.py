import pytest

from streaming_sketches import BloomFilter, CountMinSketch, HyperLogLog, ReservoirSampler


def test_hyperloglog_empty_and_distinct_estimate():
    sketch = HyperLogLog(precision=11)
    assert sketch.estimate() == pytest.approx(0.0)
    for i in range(10000):
        sketch.add(f"tile-{i}")
    assert sketch.estimate() == pytest.approx(10000, rel=0.12)


def test_hyperloglog_merge_matches_union_estimate():
    left, right = HyperLogLog(10), HyperLogLog(10)
    for i in range(5000):
        left.add(str(i))
    for i in range(5000, 10000):
        right.add(str(i))
    left.merge(right)
    assert left.estimate() == pytest.approx(10000, rel=0.15)


def test_hyperloglog_merge_rejects_different_precision():
    with pytest.raises(ValueError, match="same precision"):
        HyperLogLog(4).merge(HyperLogLog(5))


def test_count_min_sketch_never_underestimates_and_supports_weights():
    sketch = CountMinSketch(width=1000, depth=5, seed=7)
    for _ in range(100):
        sketch.add("tile-a")
    sketch.add("tile-b", count=2.5)
    assert sketch.estimate("tile-a") >= 100
    assert sketch.estimate("tile-b") >= 2.5
    assert sketch.estimate("unseen") >= 0


def test_count_min_sketch_validation():
    with pytest.raises(ValueError):
        CountMinSketch(0, 3)
    with pytest.raises(ValueError):
        CountMinSketch(10, 0)
    with pytest.raises(ValueError):
        CountMinSketch(10, 3).add("tile", -1)


def test_bloom_filter_has_no_false_negatives_and_bounded_observed_fp_rate():
    bloom = BloomFilter(expected_items=300, false_positive_rate=0.01)
    inserted = [f"tile-{i}" for i in range(300)]
    for value in inserted:
        bloom.add(value)
    assert all(bloom.might_contain(value) for value in inserted)
    false_positives = sum(bloom.might_contain(f"other-{i}") for i in range(1000))
    assert false_positives / 1000 < 0.05


def test_bloom_filter_validation_and_bytes_keys():
    with pytest.raises(ValueError):
        BloomFilter(0)
    with pytest.raises(ValueError):
        BloomFilter(100, 1.0)
    bloom = BloomFilter(10)
    bloom.add(b"tile")
    assert bloom.might_contain(b"tile")
    with pytest.raises(TypeError):
        bloom.add(123)


def test_reservoir_sampler_is_bounded_and_seed_reproducible():
    a = ReservoirSampler(20, seed=19).add_many(range(1000))
    b = ReservoirSampler(20, seed=19).add_many(range(1000))
    assert a.seen == 1000
    assert len(a.sample) == 20
    assert a.sample == b.sample
    assert len(set(a.sample)) == 20


def test_reservoir_sampler_handles_short_stream_and_validation():
    sampler = ReservoirSampler(5, seed=1).add_many(["a", "b"])
    assert sampler.sample == ("a", "b")
    with pytest.raises(ValueError):
        ReservoirSampler(0)
