"""Edge-based turn-aware and FIFO time-dependent routing baselines."""
from __future__ import annotations

from heapq import heappop, heappush
from itertools import count
from math import isfinite
from typing import Callable, Hashable, Iterable, Mapping, Sequence

Node = Hashable
EdgeId = Hashable


def turn_aware_shortest_path(
    edges: Iterable[tuple[EdgeId, Node, Node, float]],
    start: Node,
    goal: Node,
    *,
    prohibited_turns: Iterable[tuple[EdgeId, EdgeId]] = (),
    turn_penalties: Mapping[tuple[EdgeId, EdgeId], float] | None = None,
) -> tuple[list[EdgeId] | None, float]:
    """Dijkstra over incoming-edge states.

    Each edge is (edge_id, tail, head, travel_cost). A transition from edge
    e1 to e2 can be prohibited or assigned an additional non-negative cost.
    """
    outgoing: dict[Node, list[tuple[EdgeId, Node, float]]] = {}
    edge_ids: set[EdgeId] = set()
    for edge_id, tail, head, cost in edges:
        if edge_id in edge_ids:
            raise ValueError("edge identifiers must be unique")
        if not isfinite(cost) or cost < 0:
            raise ValueError("edge costs must be finite and non-negative")
        edge_ids.add(edge_id)
        outgoing.setdefault(tail, []).append((edge_id, head, float(cost)))

    prohibited = set(prohibited_turns)
    penalties = dict(turn_penalties or {})
    for turn, penalty in penalties.items():
        if not isfinite(penalty) or penalty < 0:
            raise ValueError("turn penalties must be finite and non-negative")
    if any(a not in edge_ids or b not in edge_ids for a, b in prohibited):
        raise ValueError("prohibited turn references an unknown edge")
    if any(a not in edge_ids or b not in edge_ids for a, b in penalties):
        raise ValueError("turn penalty references an unknown edge")

    if start == goal:
        return [], 0.0

    serial = count()
    # State is the edge used to enter the current node. None is the start state.
    distance: dict[EdgeId | None, float] = {None: 0.0}
    previous: dict[EdgeId, EdgeId | None] = {}
    state_node: dict[EdgeId | None, Node] = {None: start}
    queue = [(0.0, next(serial), None)]

    while queue:
        cost_so_far, _order, incoming = heappop(queue)
        if cost_so_far != distance.get(incoming):
            continue
        node = state_node[incoming]
        if node == goal:
            path: list[EdgeId] = []
            state = incoming
            while state is not None:
                path.append(state)
                state = previous[state]
            path.reverse()
            return path, cost_so_far

        for edge_id, head, edge_cost in outgoing.get(node, ()):
            if incoming is not None and (incoming, edge_id) in prohibited:
                continue
            candidate = cost_so_far + edge_cost
            if incoming is not None:
                candidate += penalties.get((incoming, edge_id), 0.0)
            if candidate < distance.get(edge_id, float("inf")):
                distance[edge_id] = candidate
                previous[edge_id] = incoming
                state_node[edge_id] = head
                heappush(queue, (candidate, next(serial), edge_id))

    return None, float("inf")


def earliest_arrival(
    graph: Mapping[Node, Sequence[tuple[Node, EdgeId]]],
    start: Node,
    goal: Node,
    departure_time: float,
    travel_time: Callable[[EdgeId, float], float],
) -> tuple[list[Node] | None, float]:
    """FIFO time-dependent Dijkstra; returns path and absolute arrival time.

    The caller must supply a FIFO edge-arrival function: departing an edge
    later must never produce an earlier arrival on that same edge. The
    function validates finite non-negative travel times but cannot prove the
    FIFO property for an arbitrary callable.
    """
    if not isfinite(departure_time):
        raise ValueError("departure_time must be finite")
    if start == goal:
        return [start], float(departure_time)

    serial = count()
    arrival = {start: float(departure_time)}
    previous: dict[Node, Node] = {}
    queue = [(float(departure_time), next(serial), start)]

    while queue:
        current_arrival, _order, node = heappop(queue)
        if current_arrival != arrival.get(node):
            continue
        if node == goal:
            path = [goal]
            while path[-1] != start:
                path.append(previous[path[-1]])
            path.reverse()
            return path, current_arrival

        for neighbor, edge_id in graph.get(node, ()):
            duration = float(travel_time(edge_id, current_arrival))
            if not isfinite(duration) or duration < 0:
                raise ValueError("travel times must be finite and non-negative")
            candidate = current_arrival + duration
            if candidate < arrival.get(neighbor, float("inf")):
                arrival[neighbor] = candidate
                previous[neighbor] = node
                heappush(queue, (candidate, next(serial), neighbor))

    return None, float("inf")



def non_fifo_earliest_arrival(
    graph: Mapping[Node, Sequence[tuple[Node, EdgeId]]],
    departure_profiles: Mapping[EdgeId, Mapping[int, int]],
    start: Node,
    goal: Node,
    start_time: int,
    horizon: int,
    *,
    max_wait: int | None = None,
) -> dict:
    """Exact finite-horizon non-FIFO routing with optional per-visit wait cap.

    Each edge profile maps allowed integer departure ticks to non-negative
    integer travel durations. Waiting one tick is allowed at every node.
    max_wait=None means unrestricted waiting; otherwise no visit to a node
    may include more than max_wait consecutive waiting ticks. Travel resets
    the local waiting counter. The expanded state is (node, tick, waited).
    """
    from numbers import Integral

    def integer(value, label, *, minimum=0):
        if isinstance(value, bool) or not isinstance(value, Integral) or value < minimum:
            raise ValueError(f"{label} must be an integer >= {minimum}")
        return int(value)

    start_time = integer(start_time, "start_time")
    horizon = integer(horizon, "horizon")
    if horizon < start_time:
        raise ValueError("horizon must be >= start_time")
    if max_wait is not None:
        max_wait = integer(max_wait, "max_wait")
    edge_ids = {edge_id for outgoing in graph.values() for _neighbor, edge_id in outgoing}
    if set(departure_profiles) - edge_ids:
        raise ValueError("departure profile references an unknown edge")
    profiles = {}
    for edge_id, profile in departure_profiles.items():
        if not isinstance(profile, Mapping):
            raise ValueError("each edge profile must map departure ticks to durations")
        clean = {}
        for raw_departure, raw_duration in profile.items():
            departure = integer(raw_departure, "profile departure")
            duration = integer(raw_duration, "travel duration")
            clean[departure] = duration
        profiles[edge_id] = clean

    initial = (start, start_time, 0)
    serial = count()
    queue = [(start_time, next(serial), initial)]
    best = {initial: start_time}
    previous = {}
    terminal = None
    while queue:
        current_time, _order, state = heappop(queue)
        if current_time != best.get(state):
            continue
        node, tick, waited = state
        if node == goal:
            terminal = state
            break
        transitions = []
        wait_allowed = tick < horizon and (max_wait is None or waited < max_wait)
        if wait_allowed:
            transitions.append(((node, tick + 1, waited + 1),
                                ("wait", node, tick, tick + 1)))
        for neighbor, edge_id in graph.get(node, ()):
            duration = profiles.get(edge_id, {}).get(tick)
            if duration is None:
                continue
            arrival = tick + duration
            if arrival <= horizon:
                transitions.append(((neighbor, arrival, 0),
                                    ("travel", edge_id, node, neighbor, tick, arrival)))
        for next_state, action in transitions:
            arrival = next_state[1]
            if arrival < best.get(next_state, float("inf")):
                best[next_state] = arrival
                previous[next_state] = (state, action)
                heappush(queue, (arrival, next(serial), next_state))

    if terminal is None:
        return {"path": None, "arrival_time": None, "legs": [], "waits": [],
                "start_time": start_time, "horizon": horizon, "max_wait": max_wait}
    actions = []
    state = terminal
    while state != initial:
        prior, action = previous[state]
        actions.append(action)
        state = prior
    actions.reverse()
    legs, waits, path = [], [], [start]
    for action in actions:
        if action[0] == "travel":
            _, edge_id, tail, head, depart, arrive = action
            legs.append({"edge_id": edge_id, "from": tail, "to": head,
                         "departure_time": depart, "arrival_time": arrive})
            path.append(head)
        else:
            _, node, begin, end = action
            if waits and waits[-1]["node"] == node and waits[-1]["end"] == begin:
                waits[-1]["end"] = end
            else:
                waits.append({"node": node, "start": begin, "end": end})
    return {"path": path, "arrival_time": terminal[1], "legs": legs,
            "waits": waits, "start_time": start_time, "horizon": horizon,
            "max_wait": max_wait}
