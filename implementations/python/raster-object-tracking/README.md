# Raster object tracking

Overlap-based association of labeled objects across consecutive raster frames. Supports 2-D masks and 3-D labeled volumes, preserves all qualifying overlap edges, exposes split/merge events, and assigns deterministic persistent track IDs through greedy one-to-one maximum-IoU continuations.

Run with NumPy and pytest:

    pip install -r requirements.txt
    pytest -q

Input frames must be equal-shaped integer label arrays with zero as background and positive IDs for objects. Segmentation is a separate step; this package does not threshold the source data or create labels. Non-overlapping objects are not linked, so large displacements, gaps, and occlusions require a motion model or a more advanced assignment method.
