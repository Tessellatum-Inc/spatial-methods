"""Deterministic streaming sketches for spatial tile and event streams."""
from __future__ import annotations

import hashlib
import math
import random


def _encode_key(value):
    if isinstance(value, bytes):
        return b"bytes:" + value
    if isinstance(value, str):
        return b"str:" + value.encode("utf-8")
    raise TypeError("sketch keys must be str or bytes for stable hashing")


class HyperLogLog:
    """Approximate distinct-key counter with mergeable registers."""

    def __init__(self, precision=10):
        if not isinstance(precision, int) or not 4 <= precision <= 16:
            raise ValueError("precision must be an integer from 4 through 16")
        self.precision = precision
        self.register_count = 1 << precision
        self.registers = [0] * self.register_count

    def add(self, value):
        hashed = int.from_bytes(
            hashlib.blake2b(_encode_key(value), digest_size=8, person=b"spatial-hll").digest(),
            "big",
        )
        index = hashed >> (64 - self.precision)
        remainder = hashed & ((1 << (64 - self.precision)) - 1)
        rank = (64 - self.precision - remainder.bit_length() + 1) if remainder else (64 - self.precision + 1)
        self.registers[index] = max(self.registers[index], rank)

    def merge(self, other):
        if not isinstance(other, HyperLogLog) or other.precision != self.precision:
            raise ValueError("HyperLogLog sketches must have the same precision")
        self.registers = [max(a, b) for a, b in zip(self.registers, other.registers)]
        return self

    def estimate(self):
        m = self.register_count
        alpha = {16: 0.673, 32: 0.697, 64: 0.709}.get(m, 0.7213 / (1 + 1.079 / m))
        raw = alpha * m * m / sum(2.0 ** (-rank) for rank in self.registers)
        zero_registers = self.registers.count(0)
        if raw <= 2.5 * m and zero_registers:
            return m * math.log(m / zero_registers)
        return raw


class CountMinSketch:
    """One-sided frequency estimator; estimates never fall below true counts."""

    def __init__(self, width, depth, seed=0):
        if not isinstance(width, int) or width < 1:
            raise ValueError("width must be a positive integer")
        if not isinstance(depth, int) or depth < 1:
            raise ValueError("depth must be a positive integer")
        if not isinstance(seed, int):
            raise ValueError("seed must be an integer")
        self.width = width
        self.depth = depth
        self.seed = seed
        self.table = [[0.0] * width for _ in range(depth)]
        self._key = hashlib.blake2b(str(seed).encode("ascii"), digest_size=16).digest()

    def _indices(self, value):
        key = _encode_key(value)
        for row in range(self.depth):
            person = b"cms" + row.to_bytes(8, "little")
            digest = hashlib.blake2b(key, digest_size=8, key=self._key, person=person).digest()
            yield int.from_bytes(digest, "big") % self.width

    def add(self, value, count=1):
        if not math.isfinite(count) or count < 0:
            raise ValueError("count must be finite and non-negative")
        for row, index in enumerate(self._indices(value)):
            self.table[row][index] += count

    def estimate(self, value):
        return min(self.table[row][index] for row, index in enumerate(self._indices(value)))


class BloomFilter:
    """Probabilistic set-membership filter with no false negatives."""

    def __init__(self, expected_items, false_positive_rate=0.01):
        if not isinstance(expected_items, int) or expected_items < 1:
            raise ValueError("expected_items must be a positive integer")
        if not math.isfinite(false_positive_rate) or not 0 < false_positive_rate < 1:
            raise ValueError("false_positive_rate must be strictly between 0 and 1")
        self.bit_count = max(
            8, math.ceil(-expected_items * math.log(false_positive_rate) / (math.log(2) ** 2))
        )
        self.hash_count = max(1, round(self.bit_count / expected_items * math.log(2)))
        self.bits = bytearray((self.bit_count + 7) // 8)

    def _indices(self, value):
        digest = hashlib.blake2b(_encode_key(value), digest_size=16, person=b"spatial-bloom").digest()
        first = int.from_bytes(digest[:8], "big")
        second = int.from_bytes(digest[8:], "big") | 1
        for i in range(self.hash_count):
            yield (first + i * second) % self.bit_count

    def add(self, value):
        for index in self._indices(value):
            self.bits[index // 8] |= 1 << (index % 8)

    def might_contain(self, value):
        return all(self.bits[index // 8] & (1 << (index % 8)) for index in self._indices(value))


class ReservoirSampler:
    """Uniform size-k sample from a stream of unknown or unbounded length."""

    def __init__(self, capacity, seed=None):
        if not isinstance(capacity, int) or capacity < 1:
            raise ValueError("capacity must be a positive integer")
        self.capacity = capacity
        self.seen = 0
        self._rng = random.Random(seed)
        self._sample = []

    def add(self, value):
        self.seen += 1
        if len(self._sample) < self.capacity:
            self._sample.append(value)
            return
        replacement = self._rng.randrange(self.seen)
        if replacement < self.capacity:
            self._sample[replacement] = value

    def add_many(self, values):
        for value in values:
            self.add(value)
        return self

    @property
    def sample(self):
        return tuple(self._sample)
