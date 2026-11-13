"""Step 2 - Build the conflict graph.

Vertex  = a course
Edge    = two courses that share at least one enrolled student
Stored as an adjacency list  ->  space O(V + E)
"""
from __future__ import annotations
from collections import defaultdict
from itertools import combinations
from typing import Dict, Iterable, Set, Tuple


class ConflictGraph:
    def __init__(self) -> None:
        self.adj: Dict[str, Set[str]] = defaultdict(set)

    def add_vertex(self, course: str) -> None:
        _ = self.adj[course]  # touch to create

    def add_edge(self, a: str, b: str) -> None:
        if a == b:
            return
        self.adj[a].add(b)
        self.adj[b].add(a)

    @property
    def vertices(self):
        return list(self.adj.keys())

    def degree(self, course: str) -> int:
        return len(self.adj[course])

    @property
    def num_vertices(self) -> int:
        return len(self.adj)

    @property
    def num_edges(self) -> int:
        return sum(len(n) for n in self.adj.values()) // 2


def build_conflict_graph(enrollments: Iterable[Tuple[str, str]]):
    """enrollments: iterable of (student_id, course_code).

    Returns (graph, students_by_course, courses_by_student).
    """
    courses_by_student: Dict[str, Set[str]] = defaultdict(set)
    students_by_course: Dict[str, Set[str]] = defaultdict(set)
    graph = ConflictGraph()

    for student, course in enrollments:
        courses_by_student[student].add(course)
        students_by_course[course].add(student)
        graph.add_vertex(course)

    # every pair of courses taken by the same student is a conflict
    for courses in courses_by_student.values():
        for a, b in combinations(sorted(courses), 2):
            graph.add_edge(a, b)

    return graph, dict(students_by_course), dict(courses_by_student)
