# Topology-preserving ring simplification — verification

Implementation: implementations/python/topology-preserving-simplification/topology_simplification.py

Tests cover closed/open ring conventions, collinear-vertex removal, concave
ring simplicity, orientation preservation, invalid/self-intersecting/zero-area
inputs, invalid thresholds, non-finite coordinates, and the three-vertex
minimum.

Verification status: tests authored; execution and independent reference
comparison pending. Scope is a single simple ring, not polygon coverage.
