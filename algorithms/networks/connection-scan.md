# Connection Scan Algorithm

The Connection Scan Algorithm (CSA) solves timetable-based earliest-arrival
routing by scanning public-transport connections in departure-time order.
A connection is a directed movement from one stop to another with a departure,
arrival and trip identity. The scan maintains the earliest reachable arrival
at each stop and remembers trips already boarded, allowing a passenger to
remain aboard across consecutive connections without paying a transfer penalty.

## Runnable implementation

The [CSA package](../../implementations/python/csa/README.md) implements a
single-pass, departure-sorted connection scan with stop-specific minimum
transfer times and same-trip continuation.

A runnable [RAPTOR and Connection Scan lab](../../notebooks/transit-routing-lab.ipynb) compares departure scans, same-trip continuation and minimum transfer constraints.

## Assumptions and limitations

- All times share one service-day clock and connections are sorted by departure.
- The model is single-criterion earliest arrival.
- Same-trip continuation is represented by trip identity; vehicle blocks,
  interlining and overtaking alternatives are not modelled.
- GTFS calendars, frequency services, footpaths, realtime updates, fares,
  accessibility and production feed indexing remain out of scope.

## References

- Dibbelt, J., Pajor, T., Strasser, B. and Wagner, D. (2013), [Connection
  Scan Algorithm](https://doi.org/10.1007/978-3-319-01790-7_2), JEA.
- [OpenTripPlanner documentation](https://docs.opentripplanner.org/).

**Scope:** a tested one-pass timetable scan is implemented; production feed
semantics and multimodal extensions remain separate work.
