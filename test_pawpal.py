import unittest
from pawpal_system import Task, Pet, Owner, Scheduler


class TestPawPal(unittest.TestCase):

    def test_task_completion(self):
        """Test that mark_complete() correctly updates completed status."""
        task = Task("Walk", 30, priority=1, category="walk", preferred_time="morning", is_required=False)
        self.assertFalse(task.completed)
        task.mark_complete()
        self.assertTrue(task.completed)

    def test_task_addition(self):
        """Test that add_task() increases the pet's task count."""
        task1 = Task("Walk", 30, priority=1, category="walk", preferred_time="morning", is_required=False)
        pet = Pet("Rex", "dog", [task1])
        self.assertEqual(len(pet.tasks), 1)

        task2 = Task("Feeding", 10, priority=2, category="feeding", preferred_time="morning", is_required=True)
        pet.add_task(task2)
        self.assertEqual(len(pet.tasks), 2)

    def test_sorting_correctness(self):
        """Test that generate_plan() returns tasks sorted by priority."""
        task_low = Task("Playtime", 20, priority=3, category="enrichment", preferred_time=None, is_required=False)
        task_high = Task("Meds", 5, priority=1, category="meds", preferred_time=None, is_required=True)
        task_mid = Task("Walk", 30, priority=2, category="walk", preferred_time=None, is_required=False)

        pet = Pet("Rex", "dog", [task_low, task_high, task_mid])
        owner = Owner("Alex", available_minutes=120, preferences="")
        scheduler = Scheduler(default_start_time="08:00")

        plan = scheduler.generate_plan(pet, owner)
        priorities = [task.priority for task in plan.scheduled_tasks]
        self.assertEqual(priorities, sorted(priorities))

    def test_recurrence_creates_next_occurrence(self):
        """Test that a recurring task creates a fresh uncompleted copy of itself."""
        task = Task(
            "Feeding", 10, priority=1, category="feeding",
            preferred_time=None, is_required=True, recurring=True
        )
        task.mark_complete()

        next_task = task.create_next_occurrence()

        self.assertIsNotNone(next_task)
        self.assertEqual(next_task.name, "Feeding")
        self.assertFalse(next_task.completed)

    def test_no_conflicts_detected(self):
        """Test that no conflicts are flagged on a clean non-overlapping schedule."""
        task1 = Task("Meds", 5, priority=1, category="meds", preferred_time=None, is_required=True)
        task2 = Task("Walk", 30, priority=2, category="walk", preferred_time=None, is_required=False)

        pet = Pet("Rex", "dog", [task1, task2])
        owner = Owner("Alex", available_minutes=120, preferences="")
        scheduler = Scheduler(default_start_time="08:00")

        plan = scheduler.generate_plan(pet, owner)
        conflicts = scheduler.find_conflicts(plan)
        self.assertEqual(len(conflicts), 0)

    def test_conflict_is_detected(self):
        """Test that find_conflicts() correctly flags two tasks at the same start time."""
        task1 = Task("Bath", 20, priority=1, category="grooming", preferred_time=None, is_required=False)
        task2 = Task("Brush", 10, priority=2, category="grooming", preferred_time=None, is_required=False)

        pet = Pet("Buddy", "dog", [task1, task2])
        owner = Owner("Alex", available_minutes=120, preferences="")
        scheduler = Scheduler(default_start_time="08:00")

        plan = scheduler.generate_plan(pet, owner)

        # Force both tasks to the same start time to simulate a conflict
        plan.scheduled_tasks[0].start_time = "08:00"
        plan.scheduled_tasks[1].start_time = "08:00"

        conflicts = scheduler.find_conflicts(plan)
        self.assertEqual(len(conflicts), 1)

    def test_pet_with_no_tasks(self):
        """Test that a pet with no tasks produces an empty schedule without errors."""
        pet = Pet("Ghost", "cat", [])
        owner = Owner("Alex", available_minutes=120, preferences="")
        scheduler = Scheduler(default_start_time="08:00")

        plan = scheduler.generate_plan(pet, owner)
        self.assertEqual(len(plan.scheduled_tasks), 0)
        self.assertEqual(len(plan.skipped_tasks), 0)


if __name__ == "__main__":
    unittest.main()