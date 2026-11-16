"""Deferred-acceptance stable matching for strict, incomplete preferences."""
from __future__ import annotations

from collections import deque
from collections.abc import Mapping, Sequence
from typing import Hashable

Agent = Hashable


def _ranking(preferences, *, owners, choices, label):
    if not isinstance(preferences, Mapping):
        raise ValueError(f"{label} preferences must be a mapping")
    if set(preferences) != owners:
        raise ValueError(f"{label} preference keys must match the participant set")
    result = {}
    for owner, choices_in_order in preferences.items():
        if isinstance(choices_in_order, (str, bytes)):
            raise ValueError(f"{label} preferences must be sequences, not strings")
        try:
            ordered = list(choices_in_order)
        except TypeError as exc:
            raise ValueError(f"{label} preferences must be sequences") from exc
        if len(ordered) != len(set(ordered)):
            raise ValueError(f"{label} preferences contain a duplicate choice")
        if not set(ordered) <= choices:
            raise ValueError(f"{label} preferences contain an unknown participant")
        result[owner] = {choice: rank for rank, choice in enumerate(ordered)}
    return result


def _capacities(hospitals, capacities):
    if capacities is None:
        return {hospital: 1 for hospital in hospitals}
    if not isinstance(capacities, Mapping) or not set(capacities) <= hospitals:
        raise ValueError("capacities must be a mapping keyed by known hospitals")
    result = {hospital: capacities.get(hospital, 1) for hospital in hospitals}
    for hospital, value in result.items():
        if isinstance(value, bool) or not isinstance(value, int) or value < 0:
            raise ValueError(f"capacity for {hospital!r} must be a non-negative integer")
    return result


def stable_matching(resident_preferences, hospital_preferences, capacities=None):
    """Return a resident-proposing stable matching for a many-to-one market.

    Preferences are strict ordered sequences. Omitted pairs are unacceptable.
    Omitted hospital capacities default to one. The result maps every resident
    to a hospital or None. Mapping insertion order determines queue order.
    """
    residents = set(resident_preferences)
    hospitals = set(hospital_preferences)
    _ranking(resident_preferences, owners=residents, choices=hospitals, label="resident")
    hospital_rank = _ranking(
        hospital_preferences, owners=hospitals, choices=residents, label="hospital"
    )
    capacity = _capacities(hospitals, capacities)

    next_choice = {resident: 0 for resident in resident_preferences}
    assigned = {resident: None for resident in resident_preferences}
    held = {hospital: [] for hospital in hospitals}
    free = deque(resident_preferences)

    while free:
        resident = free.popleft()
        choices = resident_preferences[resident]
        if next_choice[resident] >= len(choices):
            continue
        hospital = choices[next_choice[resident]]
        next_choice[resident] += 1

        ranking = hospital_rank[hospital]
        if resident not in ranking or capacity[hospital] == 0:
            if next_choice[resident] < len(choices):
                free.append(resident)
            continue

        incumbents = held[hospital]
        if len(incumbents) < capacity[hospital]:
            incumbents.append(resident)
            assigned[resident] = hospital
            continue

        worst = max(incumbents, key=ranking.__getitem__)
        if ranking[resident] < ranking[worst]:
            incumbents.remove(worst)
            assigned[worst] = None
            incumbents.append(resident)
            assigned[resident] = hospital
            if next_choice[worst] < len(resident_preferences[worst]):
                free.append(worst)
        elif next_choice[resident] < len(choices):
            free.append(resident)

    return assigned


def blocking_pairs(resident_preferences, hospital_preferences, matching, capacities=None):
    """Return mutually acceptable resident-hospital pairs that block matching."""
    residents = set(resident_preferences)
    hospitals = set(hospital_preferences)
    resident_rank = _ranking(
        resident_preferences, owners=residents, choices=hospitals, label="resident"
    )
    hospital_rank = _ranking(
        hospital_preferences, owners=hospitals, choices=residents, label="hospital"
    )
    capacity = _capacities(hospitals, capacities)
    if set(matching) != residents:
        raise ValueError("matching keys must match the resident set")

    incumbents = {hospital: [] for hospital in hospitals}
    for resident, hospital in matching.items():
        if hospital is not None:
            if hospital not in hospitals or resident not in hospital_rank[hospital]:
                raise ValueError("matching contains an unacceptable or unknown assignment")
            incumbents[hospital].append(resident)
    for hospital, members in incumbents.items():
        if len(members) > capacity[hospital]:
            raise ValueError("matching exceeds a hospital capacity")

    blocks = []
    for resident in resident_preferences:
        current = matching[resident]
        current_rank = resident_rank[resident].get(current, float("inf"))
        for hospital in resident_preferences[resident]:
            if resident_rank[resident][hospital] >= current_rank:
                break
            ranking = hospital_rank[hospital]
            if resident not in ranking:
                continue
            members = incumbents[hospital]
            if len(members) < capacity[hospital]:
                blocks.append((resident, hospital))
            elif members and ranking[resident] < max(ranking[m] for m in members):
                blocks.append((resident, hospital))
    return blocks
