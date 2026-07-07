from pawpal_system import Owner, Pet, Task, Scheduler

owner = Owner("Alex", available_minutes=120, preferences="mornings")

task1 = Task("Walk", 30, priority=2, category="walk", preferred_time="morning", is_required=False)
task2 = Task("Meds", 5, priority=1, category="meds", preferred_time="morning", is_required=True)
pet1 = Pet("Rex", "dog", [task1, task2])

task3 = Task("Feeding", 10, priority=1, category="feeding", preferred_time="morning", is_required=True)
task4 = Task("Playtime", 20, priority=3, category="enrichment", preferred_time="afternoon", is_required=False)
pet2 = Pet("Whiskers", "cat", [task3, task4])

scheduler = Scheduler(default_start_time="08:00")

print("=== TODAY'S SCHEDULE ===")

for pet in [pet1, pet2]:
    print(f"\n{pet.name}'s schedule:")
    plan = scheduler.generate_plan(pet, owner)

    for task in plan.scheduled_tasks:
        print(f"  {task.start_time} - {task.name} ({task.duration} min) — {plan.explanations[task.name]}")

    for task in plan.skipped_tasks:
        print(f"  SKIPPED: {task.name} ({task.duration} min) — {plan.explanations[task.name]}")

# Demonstrate sort_by_time
print("\n=== SORTED BY TIME (Rex) ===")
plan_rex = scheduler.generate_plan(pet1, owner)
sorted_tasks = scheduler.sort_by_time(plan_rex.scheduled_tasks)
for task in sorted_tasks:
    print(f"  {task.start_time} - {task.name}")

# Demonstrate filter_tasks (incomplete tasks only)
print("\n=== INCOMPLETE TASKS (Rex) ===")
incomplete = scheduler.filter_tasks(plan_rex.scheduled_tasks, completed=False)
for task in incomplete:
    print(f"  {task.name} — completed: {task.completed}")

# Demonstrate conflict detection (force two tasks at same time)
print("\n=== CONFLICT DETECTION TEST ===")
conflict_task1 = Task("Bath", 20, priority=1, category="grooming", preferred_time="morning", is_required=False)
conflict_task2 = Task("Brush", 10, priority=1, category="grooming", preferred_time="morning", is_required=False)
conflict_pet = Pet("Buddy", "dog", [conflict_task1, conflict_task2])
conflict_plan = scheduler.generate_plan(conflict_pet, owner)

# Manually force same start time to simulate a conflict
conflict_plan.scheduled_tasks[0].start_time = "08:00"
conflict_plan.scheduled_tasks[1].start_time = "08:00"

conflicts = scheduler.find_conflicts(conflict_plan)
if conflicts:
    for t1, t2 in conflicts:
        print(f"  ⚠️ Conflict detected: '{t1.name}' and '{t2.name}' both scheduled at {t1.start_time}")
else:
    print("  No conflicts detected.")