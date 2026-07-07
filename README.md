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

## 🖥️ Sample Output

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:

```
# e.g.:
# Daily plan for Biscuit (Golden Retriever):
#   08:00 — Morning walk (30 min) [priority: high]
#   09:00 — Feeding (10 min) [priority: high]
#   ...

Today's Schedule for Biscuit
Scheduled (sorted by time):

🕐 08:00 — Morning walk (21 min)

Scheduled — priority 1, fit within available time.

🕐 08:21 — Feeding (10 min)

Scheduled — priority 1, fit within available time.

🕐 08:31 — medication (5 min)

Scheduled — priority 1, fit within available time.

🕐 08:36 — Playtime (45 min)

Skipped — not enough time remaining.

Skipped:

⏭️ Playtime (53 min)

Skipped — not enough time remaining.
```

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
pytest

# Run with coverage:
pytest --cov
```

Sample test output:

```
# Paste your pytest output here
test_pawpal.py::TestPawPal::test_conflict_is_detected PASSED                                      [ 14%]
test_pawpal.py::TestPawPal::test_no_conflicts_detected PASSED                                     [ 28%]
test_pawpal.py::TestPawPal::test_pet_with_no_tasks PASSED                                         [ 42%]
test_pawpal.py::TestPawPal::test_recurrence_creates_next_occurrence PASSED                        [ 57%]
test_pawpal.py::TestPawPal::test_sorting_correctness PASSED                                       [ 71%]
test_pawpal.py::TestPawPal::test_task_addition PASSED                                             [ 85%]
test_pawpal.py::TestPawPal::test_task_completion PASSED                                           [100%]

========================================== 7 passed in 0.14s ===========================================


```

## 📐 Smarter Scheduling

> Fill in once you've implemented scheduling logic.

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `Scheduler.generate_plan()` | Sorts tasks by priority (1 = highest) using `sorted(pet.tasks, key=lambda task: task.priority)` |
| Filtering | `Scheduler.generate_plan()` | Tracks running time used and skips any task that would push the total over `owner.available_minutes` |
| Conflict handling | `Scheduler.find_conflicts()` | Checks scheduled tasks for duplicate `start_time` values and returns any conflicting pairs found |
| Recurring tasks | `Task.create_next_occurrence()` | If a task has `recurring=True`, calling this after completion generates a fresh, uncompleted copy of the task for the next day |


## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. Open the app and enter the owner's name and the pet's name and species at the top of the page.
2. In the Tasks section, fill in a task title, duration (in minutes), and priority (low/medium/high), then click Add task. Repeat this for each task you want to schedule.
3. Review the task list shown in the table to confirm everything was added correctly.
4. Click Generate schedule to run the scheduler on the tasks you entered.
5. View the results under "Today's Schedule" — each scheduled task shows its assigned start time and a short explanation of why it was included. Any tasks that didn't fit within the available time appear in a separate "Skipped" list, each with a reason.

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
