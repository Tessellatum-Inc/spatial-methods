# Connection Scan Algorithm baseline

This dependency-free CSA reference scans a departure-sorted list of timetable
connections once. It maintains separate initial-access and transit-arrival labels, plus a set of
trips the passenger has boarded. This separation ensures interchange penalties
apply only to a vehicle-to-vehicle transfer and never invalidate an independent
access path. A connection is usable if its departure is
reachable after the stop's minimum transfer time, or if it continues a trip
already boarded. This supports same-vehicle continuation even when the
interchange penalty at the stop is positive.

Times use a common service-day clock. Connections must be globally sorted by
departure. The implementation is a single-criterion earliest-arrival baseline;
it does not parse GTFS, model calendars, frequency-based services, footpaths,
overtaking/vehicle block semantics, real-time updates, fares or accessibility.
For large feeds, production implementations require indexed connection
storage and careful trip/transfer semantics.

Run `python -m pytest -q` in this directory.
