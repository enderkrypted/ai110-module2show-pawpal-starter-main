from datetime import datetime, timedelta


class Owner:
    def __init__(self, name, available_minutes, preferences):
        """Initialize an Owner with a name, daily available minutes, and preferences."""
        self.name = name
        self.available_minutes = available_minutes
        self.preferences = preferences


class Pet:
    def __init__(self, name, species, tasks):
        """Initialize a Pet with a name, species, and list of tasks."""
        self.name = name
        self.species = species
        self.tasks = tasks

    def add_task(self, task):
        """Add a new task to this pet's task list."""
        self.tasks.append(task)


class Task:
    def __init__(self, name, duration, priority, category, preferred_time, is_required, recurring=False):
        """Initialize a Task with scheduling details and completion status."""
        self.name = name
        self.duration = duration
        self.priority = priority
        self.category = category
        self.preferred_time = preferred_time
        self.is_required = is_required
        self.recurring = recurring
        self.completed = False

    def mark_complete(self):
        """Mark this task as completed."""
        self.completed = True

    def create_next_occurrence(self):
        """Return a new identical Task if this is a recurring task, otherwise return None."""
        if self.recurring:
            return Task(
                self.name,
                self.duration,
                self.priority,
                self.category,
                self.preferred_time,
                self.is_required,
                self.recurring,
            )
        return None


class Plan:
    def __init__(self, scheduled_tasks, skipped_tasks, explanations):
        """Initialize a Plan with scheduled tasks, skipped tasks, and explanations."""
        self.scheduled_tasks = scheduled_tasks
        self.skipped_tasks = skipped_tasks
        self.explanations = explanations


class Scheduler:
    def __init__(self, default_start_time):
        """Initialize the Scheduler with a default start time in HH:MM format."""
        self.default_start_time = default_start_time

    def generate_plan(self, pet, owner):
        """Generate a daily schedule for a pet based on task priority and owner's available time."""
        sorted_tasks = sorted(pet.tasks, key=lambda task: task.priority)

        scheduled_tasks = []
        skipped_tasks = []
        explanations = {}
        time_used = 0

        current_time = datetime.strptime(self.default_start_time, "%H:%M")

        for task in sorted_tasks:
            if time_used + task.duration <= owner.available_minutes:
                task.start_time = current_time.strftime("%H:%M")
                scheduled_tasks.append(task)
                time_used += task.duration
                current_time += timedelta(minutes=task.duration)

                if task.is_required:
                    explanations[task.name] = "Scheduled — required task."
                else:
                    explanations[task.name] = f"Scheduled — priority {task.priority}, fit within available time."
            else:
                skipped_tasks.append(task)
                explanations[task.name] = "Skipped — not enough time remaining."

        return Plan(scheduled_tasks, skipped_tasks, explanations)

    def sort_by_time(self, tasks):
        """Return tasks sorted by their assigned start time in chronological order."""
        return sorted(
            [t for t in tasks if hasattr(t, 'start_time')],
            key=lambda task: datetime.strptime(task.start_time, "%H:%M")
        )

    def filter_tasks(self, tasks, completed=None, pet_name=None):
        """Filter tasks by completion status and/or pet name."""
        result = tasks
        if completed is not None:
            result = [t for t in result if t.completed == completed]
        if pet_name is not None:
            result = [t for t in result if hasattr(t, 'pet_name') and t.pet_name == pet_name]
        return result

    def find_conflicts(self, plan):
        """Detect and return pairs of tasks scheduled at the same start time."""
        conflicts = []
        seen_times = {}

        for task in plan.scheduled_tasks:
            if task.start_time in seen_times:
                conflicts.append((seen_times[task.start_time], task))
            else:
                seen_times[task.start_time] = task

        return conflicts