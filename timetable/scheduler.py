"""Steps 3 & 4 - Order courses (Welsh-Powell) and assign slots greedily."""
from __future__ import annotations
from datetime import date, datetime, time, timedelta
from typing import Dict, List, Optional

from .graph import ConflictGraph


def welsh_powell(graph: ConflictGraph) -> Dict[str, int]:
    """Greedy graph colouring in decreasing-degree order.

    Returns {course: slot_index} where slot_index starts at 0.
    Adjacent (conflicting) courses never get the same slot.
    Ties in degree are broken alphabetically so results are reproducible.
    """
    order = sorted(graph.vertices, key=lambda c: (-graph.degree(c), c))
    slot_of: Dict[str, int] = {}

    for course in order:
        used = {slot_of[n] for n in graph.adj[course] if n in slot_of}
        slot = 0
        while slot in used:          # lowest slot not used by any neighbour
            slot += 1
        slot_of[course] = slot
    return slot_of


def make_slot_labels(num_slots: int, start: date,
                     times: Optional[List[time]] = None) -> List[str]:
    """Turn slot indices 0..n-1 into 'Tue 01 Dec 2026 09:00' style labels.

    Weekends are skipped. `times` = exam sessions per day.
    """
    times = times or [time(9, 0), time(14, 0)]
    labels: List[str] = []
    day = start
    while len(labels) < num_slots:
        if day.weekday() < 5:
            for t in times:
                if len(labels) < num_slots:
                    labels.append(datetime.combine(day, t).strftime("%a %d %b %Y %H:%M"))
        day += timedelta(days=1)
    return labels


def assign_slots(graph: ConflictGraph, start: date,
                 times: Optional[List[time]] = None):
    """Returns (slot_of_course, slot_labels)."""
    slot_of = welsh_powell(graph)
    num_slots = (max(slot_of.values()) + 1) if slot_of else 0
    return slot_of, make_slot_labels(num_slots, start, times)
