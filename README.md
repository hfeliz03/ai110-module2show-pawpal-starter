# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Smarter Scheduling (New Features)

PawPal+ now includes advanced scheduling logic to help you manage recurring tasks and avoid planning conflicts:

- **Recurring Tasks**: Mark a task as "Daily" or "Weekly", and the system will automatically create the next instance with the correct due date as soon as you complete the current one.
- **Conflict Detection**: The Scheduler now scans your entire plan across all pets and alerts you if any tasks overlap in time, ensuring you never double-book your pet care duties.
- **Pythonic Optimization**: Core algorithms have been refactored for better performance and readability using modern Python patterns like `zip()` and `timedelta`.

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## Testing PawPal+

To ensure the reliability of the scheduling and recurrence logic, a comprehensive test suite is included.

### Running Tests
Use the following command to run all automated tests:
```bash
python -m pytest
```

### Coverage
The test suite covers 12 core behaviors and edge cases, including:
- **Recurring Tasks**: Verifying that DAILY/WEEKLY tasks spawn next-day occurrences.
- **Conflict Detection**: Ensuring overlapping task windows trigger warnings.
- **Chronological Sorting**: Confirming the Daily Plan is ordered by due date.
- **Edge Cases**: Handling empty task lists, 0-minute tasks, and overbooked schedules.

### Confidence Level
**⭐⭐⭐⭐⭐ (5/5 Stars)**
With 100% pass rate on unit and integration tests covering all critical functional paths and edge cases, the system is highly reliable for pet care planning.
