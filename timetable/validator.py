"""Step 5 - Validate: no student may have two exams in the same slot.

This check is independent of the graph: it works straight from the
student->courses data, so it really verifies the final timetable.
"""
from __future__ import annotations
from collections import defaultdict
from typing import Dict, List, Set, Tuple


def find_conflicts(slot_of: Dict[str, int],
                   courses_by_student: Dict[str, Set[str]]) -> List[Tuple[str, int, List[str]]]:
    """Return [(student, slot, [courses in that slot]), ...] for every clash."""
    clashes = []
    for student, courses in courses_by_student.items():
        by_slot = defaultdict(list)
        for c in courses:
            by_slot[slot_of[c]].append(c)
        for slot, cs in by_slot.items():
            if len(cs) > 1:
                clashes.append((student, slot, sorted(cs)))
    return clashes


def validate(slot_of, courses_by_student) -> bool:
    return not find_conflicts(slot_of, courses_by_student)
