# RAPTOR public-transport routing baseline

This dependency-free teaching implementation computes earliest arrivals in rounds.
Round 0 is the supplied access-time map; round 1 permits one vehicle boarding;
each additional round permits one more boarding, so `max_transfers=1` allows
two vehicle legs. Route trips share an ordered stop sequence. Optional directed
footpaths are relaxed before the first boarding and after every transit round,
including chained walks. Segment chronology is validated: a vehicle cannot depart
a stop after the scheduled arrival at the next stop.

The implementation explicitly scans all trips at each reachable boarding
position. It is a correctness-oriented reference, not the optimized route-scan
RAPTOR data structure. It assumes a common service-day time axis, trips sorted
by first-stop departure, and non-overtaking trips with a fixed stop sequence.
It does not parse GTFS, service calendars, frequency-based trips, real-time
updates, fare constraints, accessibility, overtaking patterns or interlining.

Run `python -m pytest -q` in this directory.
