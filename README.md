# Student Examination Timetable Generator (Conflict-Free)

Thematic Assessment - Reg. No. 251347077 - Lucky

Builds an exam timetable in which **no student ever has two exams in the same slot**,
using a conflict graph and greedy **Welsh-Powell** graph colouring.

## How it works (maps to the PPT methodology)

| PPT step              | Code                                   |
|-----------------------|----------------------------------------|
| 1. Collect input      | `timetable/io_utils.py` (CSV in)       |
| 2. Build conflict graph | `timetable/graph.py`                 |
| 3. Order courses      | `timetable/scheduler.py` (degree desc) |
| 4. Assign slots       | `timetable/scheduler.py` (lowest free colour) |
| 5. Validate & publish | `timetable/validator.py`, `main.py` -> `output/timetable.csv` |
| (extra) Rooms         | `timetable/rooms.py`                   |

## Run

```bash
python generate_sample_data.py 400 8        # optional: makes data/enrollments.csv + data/rooms.csv
python main.py -r data/rooms.csv --start 2026-12-01
python -m pytest                            # pip install pytest first
```

Input `enrollments.csv`: `student_id,course_code` (one row per enrolment).
Input `rooms.csv` (optional): `room,capacity`.
Output: `output/timetable.csv` + a console report (V, E, slots used, run time, clash count).

## Complexity

- Graph building: O(sum of k^2) over students, where k = courses per student (small in practice).
- Welsh-Powell ordering: O(V log V) for the sort, then colouring in O(V + E).
  Overall **O(V log V + E)**. The slide's O(V + E) is the colouring pass itself.
- Space: O(V + E) (adjacency list + one slot per course).

## Notes / limits

- Greedy colouring guarantees **no clashes**, but not the **minimum** number of slots.
- Rooms are allocated per slot by capacity; courses that don't fit are reported as warnings.
