import argparse
import time as clock
from collections import defaultdict
from datetime import date

from timetable import build_conflict_graph, assign_slots, find_conflicts
from timetable.io_utils import read_enrollments, read_rooms, write_timetable
from timetable.rooms import allocate_rooms


def main() -> int:
    p = argparse.ArgumentParser(description="Conflict-free exam timetable generator")
    p.add_argument("-e", "--enrollments", default="data/enrollments.csv")
    p.add_argument("-r", "--rooms", default=None, help="optional rooms CSV (room,capacity)")
    p.add_argument("-o", "--output", default="output/timetable.csv")
    p.add_argument("--start", default=date.today().isoformat(), help="first exam date YYYY-MM-DD")
    args = p.parse_args()

    # 1. collect input
    enrollments = read_enrollments(args.enrollments)

    t0 = clock.perf_counter()
    # 2. conflict graph   3+4. order + assign
    graph, students_by_course, courses_by_student = build_conflict_graph(enrollments)
    slot_of, labels = assign_slots(graph, date.fromisoformat(args.start))
    elapsed = (clock.perf_counter() - t0) * 1000

    # 5. validate
    clashes = find_conflicts(slot_of, courses_by_student)

    room_of, warnings = (None, [])
    if args.rooms:
        room_of, warnings = allocate_rooms(slot_of, students_by_course, read_rooms(args.rooms))

    write_timetable(args.output, slot_of, labels, students_by_course, room_of)

    # report
    by_slot = defaultdict(list)
    for c, s in slot_of.items():
        by_slot[s].append(c)
    print("=" * 60)
    print(" EXAM TIMETABLE")
    print("=" * 60)
    for s in sorted(by_slot):
        print(f"Slot {s + 1:>2}  {labels[s]}")
        print("          " + ", ".join(sorted(by_slot[s])))
    print("-" * 60)
    print(f"Courses (V)            : {graph.num_vertices}")
    print(f"Conflicting pairs (E)  : {graph.num_edges}")
    print(f"Students               : {len(courses_by_student)}")
    print(f"Slots used             : {len(by_slot)}")
    print(f"Max conflicts (degree) : {max((graph.degree(c) for c in graph.vertices), default=0)}")
    print(f"Run time               : {elapsed:.2f} ms")
    print(f"Student clashes found  : {len(clashes)}  ->  {'VALID' if not clashes else 'INVALID'}")
    for w in warnings:
        print("WARNING:", w)
    print(f"Saved to {args.output}")
    return 0 if not clashes else 1


if __name__ == "__main__":
    raise SystemExit(main())
