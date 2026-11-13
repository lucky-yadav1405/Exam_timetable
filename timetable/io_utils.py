"""Step 1 - Collect input, and write the final timetable."""
from __future__ import annotations
import csv
from typing import Dict, List, Optional, Set, Tuple


def read_enrollments(path: str) -> List[Tuple[str, str]]:
    """CSV with header: student_id,course_code"""
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return [(r["student_id"].strip(), r["course_code"].strip())
                for r in reader if r["student_id"].strip() and r["course_code"].strip()]


def read_rooms(path: str) -> List[Tuple[str, int]]:
    """CSV with header: room,capacity"""
    with open(path, newline="", encoding="utf-8") as f:
        return [(r["room"].strip(), int(r["capacity"])) for r in csv.DictReader(f)]


def write_timetable(path: str, slot_of: Dict[str, int], labels: List[str],
                    students_by_course: Dict[str, Set[str]],
                    room_of: Optional[Dict[str, Optional[str]]] = None) -> None:
    rows = sorted(slot_of, key=lambda c: (slot_of[c], c))
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["slot_no", "date_time", "course", "students", "room"])
        for c in rows:
            room = "" if room_of is None else (room_of.get(c) or "UNASSIGNED")
            w.writerow([slot_of[c] + 1, labels[slot_of[c]], c, len(students_by_course[c]), room])
