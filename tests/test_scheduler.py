import random
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from timetable import build_conflict_graph, welsh_powell, find_conflicts


def run(enrollments):
    g, sbc, cbs = build_conflict_graph(enrollments)
    slot = welsh_powell(g)
    return g, slot, cbs


def test_shared_student_gets_different_slots():
    g, slot, _ = run([("s1", "A"), ("s1", "B")])
    assert slot["A"] != slot["B"]


def test_independent_courses_share_a_slot():
    g, slot, _ = run([("s1", "A"), ("s2", "B")])
    assert slot["A"] == slot["B"] == 0
    assert g.num_edges == 0


def test_triangle_needs_three_slots():
    e = [("s1", "A"), ("s1", "B"), ("s1", "C")]
    _, slot, _ = run(e)
    assert len(set(slot.values())) == 3


def test_no_clashes_on_random_data():
    random.seed(1)
    courses = [f"C{i}" for i in range(30)]
    e = [(f"S{s}", c) for s in range(200) for c in random.sample(courses, random.randint(2, 6))]
    _, slot, cbs = run(e)
    assert find_conflicts(slot, cbs) == []


def test_validator_detects_a_bad_timetable():
    bad = {"A": 0, "B": 0}
    assert find_conflicts(bad, {"s1": {"A", "B"}}) != []


def test_deterministic():
    e = [("s1", "A"), ("s1", "B"), ("s2", "B"), ("s2", "C")]
    assert run(e)[1] == run(e)[1]
