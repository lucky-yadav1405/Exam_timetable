"""Optional: allot rooms inside each slot (largest course -> smallest room that fits).

Conflict-freedom is guaranteed by the colouring; rooms are a bonus feature.
Courses that don't fit are reported, not silently dropped.
"""
from __future__ import annotations
from collections import defaultdict
from typing import Dict, List, Optional, Tuple


def allocate_rooms(slot_of: Dict[str, int], students_by_course: Dict[str, set],
                   rooms: List[Tuple[str, int]]):
    """rooms: [(room_name, capacity)]. Returns ({course: room or None}, [warnings])."""
    rooms = sorted(rooms, key=lambda r: r[1])
    by_slot = defaultdict(list)
    for course, slot in slot_of.items():
        by_slot[slot].append(course)

    room_of: Dict[str, Optional[str]] = {}
    warnings: List[str] = []
    for slot, courses in by_slot.items():
        free = list(rooms)
        for course in sorted(courses, key=lambda c: -len(students_by_course[c])):
            need = len(students_by_course[course])
            pick = next((r for r in free if r[1] >= need), None)
            if pick is None:
                room_of[course] = None
                warnings.append(f"{course} ({need} students) has no free room large enough in slot {slot + 1}")
            else:
                room_of[course] = pick[0]
                free.remove(pick)
    return room_of, warnings
