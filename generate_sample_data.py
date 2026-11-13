"""Create realistic sample data: python generate_sample_data.py [students] [programmes]

Each programme has its own pool of courses; students take most courses from
their programme plus an occasional elective from another one. That produces a
sparse-ish conflict graph, like a real university.
"""
import csv, random, sys

n_students = int(sys.argv[1]) if len(sys.argv) > 1 else 400
n_programmes = int(sys.argv[2]) if len(sys.argv) > 2 else 8
random.seed(42)

programmes = {p: [f"P{p}C{i}" for i in range(1, 8)] for p in range(1, n_programmes + 1)}
all_courses = [c for cs in programmes.values() for c in cs]

with open("data/enrollments.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["student_id", "course_code"])
    for s in range(1, n_students + 1):
        prog = random.choice(list(programmes))
        chosen = set(random.sample(programmes[prog], random.randint(4, 5)))
        if random.random() < 0.25:                       # occasional cross-programme elective
            chosen.add(random.choice(all_courses))
        for c in sorted(chosen):
            w.writerow([f"S{s:04d}", c])

with open("data/rooms.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["room", "capacity"])
    for name, cap in [("Hall-A", 120), ("Hall-B", 100), ("Room-101", 60), ("Room-102", 60),
                      ("Room-201", 40), ("Room-202", 40), ("Room-301", 30), ("Room-302", 30)]:
        w.writerow([name, cap])
print("Wrote data/enrollments.csv and data/rooms.csv")
