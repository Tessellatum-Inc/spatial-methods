# RAPTOR round-based transit routing

RAPTOR (Round-bAsed Public Transit Routing) organises transit journeys by
number of vehicle boardings. Round zero contains access-stop arrival times.
Each subsequent round considers journeys with one additional boarding. This
separates transfer count from elapsed time and avoids reducing a timetable to
a static edge-weight graph.

## Core recurrence

For a route with an ordered stop sequence and trips sharing that sequence,
a reachable stop can be a boarding point when the passenger can arrive no
later than a trip's departure. Riding that trip relaxes downstream stop
arrival times. The next round combines these ride improvements with the
previous round's labels. Walking transfer links can be relaxed between rounds.

## Runnable baseline

The [RAPTOR package](../../implementations/python/raptor/README.md) implements
round-indexed earliest-arrival labels, timetable feasibility, transfer rounds
and chained directed footpaths. Its reference scan examines trips explicitly
at each reachable boarding position; it is not the optimized RAPTOR route
scan used for large production feeds.

A runnable [RAPTOR and Connection Scan lab](../../notebooks/transit-routing-lab.ipynb) compares direct journeys, transfers and walking links.

## Assumptions and limitations

- Times are finite minutes on one common service-day clock.
- Each route has a fixed, non-repeating stop sequence.
- Trips are ordered by first-stop departure and assumed non-overtaking.
- Footpaths are directed, non-negative walking durations.
- GTFS parsing, calendars, frequency-based services, real-time updates,
  fares, accessibility constraints and multimodal transfer rules are outside
  this implementation.

## References

- Delling, D., Pajor, T. and Werneck, R. F. (2012), [Round-based public
  transit routing](https://doi.org/10.1007/978-3-642-33090-2_11), ALENEX.
- [OpenTripPlanner documentation](https://docs.opentripplanner.org/).

**Scope:** a tested timetable-based round-routing baseline is implemented;
feed ingestion, optimized route scans and production service semantics remain
separate tasks.
