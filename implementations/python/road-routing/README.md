# Turn-aware and time-dependent routing baselines

This package adds three road-network modelling examples beyond a node-only
shortest-path graph.

## Run

```bash
python -m pip install -r requirements.txt
python -m pytest -q
```

## Turn-aware shortest path

Edges are explicit records: `(edge_id, tail, head, cost)`. The search state is
the incoming edge, so a transition can be prohibited or assigned a turn
penalty. This is the basic reason a turn-restricted road router often needs an
edge-based graph rather than one state per intersection.

## Time-dependent earliest arrival

The time-dependent function receives an edge ID and the actual departure time
from that edge. It returns the travel duration. The search returns an absolute
arrival time, not an elapsed duration.

The label-setting algorithm requires FIFO edge-arrival functions: leaving later
must not result in arriving earlier on the same edge. The code validates that
travel times are finite and non-negative, but it cannot prove FIFO for an
arbitrary Python callable. The caller must document and test that contract.

## Non-FIFO earliest arrival

`non_fifo_earliest_arrival` uses a finite integer time-expanded state graph. Each edge has a mapping of allowed departure ticks to non-negative integer travel durations. A one-tick waiting transition is available at every node, so the algorithm can deliberately wait for a faster later departure even when edge arrival functions are non-FIFO. It returns the node path, absolute arrival time, traversed legs and collapsed waiting intervals.

This is exact only for the supplied discrete departure profiles, integer time domain and finite horizon. The state space is bounded by O(|V|H) and each state scans outgoing edges; this is a reference algorithm, not a continuous-time or large-network production router. Waiting is unrestricted and has zero cost.

## Limits

These are small teaching baselines. They do not parse GTFS, model waiting
choices or service calendars, support multimodal transfers, infer turn
restrictions from source data, or provide production-grade network snapping
and route geometry.


Restricted waiting is supported by passing `max_wait` to `non_fifo_earliest_arrival`. The limit is the maximum number of consecutive one-tick waits during a single visit to a node; taking an edge resets the counter. `max_wait=0` means no waiting, while `None` preserves unrestricted waiting. This remains a finite integer-time, finite-horizon solver.
