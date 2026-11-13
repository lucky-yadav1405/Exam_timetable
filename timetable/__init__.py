"""Student Examination Timetable Generator (conflict-free, Welsh-Powell graph colouring)."""
from .graph import ConflictGraph, build_conflict_graph
from .scheduler import welsh_powell, assign_slots
from .validator import find_conflicts, validate

__all__ = [
    "ConflictGraph", "build_conflict_graph",
    "welsh_powell", "assign_slots",
    "find_conflicts", "validate",
]
