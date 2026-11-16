# Staypoints, home/work inference and activity spaces

Install and test with `python -m pip install -r requirements.txt && python -m pytest -q`.

- `detect_staypoints` extracts sequential dwell episodes using a radius from the first fix and a minimum elapsed duration. Timestamps are seconds and must be strictly increasing.
- `infer_home_work` clusters staypoint centroids separately in night and day windows, selecting the cluster with the greatest accumulated dwell time. Supply the fixed UTC offset for timestamp interpretation.
- `activity_space_metrics` returns radius of gyration and planar convex-hull area.

These outputs are exploratory candidates. The simple detector is sensitive to sampling frequency, GPS noise, gaps and its first-fix radius rule. Home/work roles require longer longitudinal observation and user-specific schedules; this baseline does not infer co-location/contact events, handle irregular time zones/DST, or provide privacy protection and disclosure control.
