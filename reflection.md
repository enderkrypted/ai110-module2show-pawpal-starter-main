# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

My initial UML design had five classes: Owner, Pet, Task, Scheduler, and Plan. Owner held the person's name, available minutes per day, and preferences. Pet held basic info plus a list of Task objects. Task was the biggest class — it held the name, duration, priority, category, preferred time, and whether it was required (like meds vs. optional stuff like playtime). Scheduler was the only class with real logic — its job was to take a Pet and Owner and spit out a Plan. Plan just held the results: which tasks got scheduled, which got skipped, and why.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

Yes, it changed a bit once I actually started building. The biggest change was adding a completed attribute and mark_complete() method to Task, and an add_task() method to Pet — neither of those were in my original diagram. I added them because my tests specifically needed to check that marking a task complete actually changed its status, and that adding a task to a pet increased the task count. My first draft treated Task and Pet as pretty static — just data holders — but once I needed to test behavior, not just structure, I realized they needed actual methods, not just attributes.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

My scheduler considers two main things: priority and time. Every task has a priority number (1 = highest), and the scheduler sorts tasks by priority first. Then it walks through the sorted list and keeps a running total of minutes used, only adding a task if it still fits under the owner's available time for the day. I decided priority mattered most because in real life, if you're short on time, you skip the walk before you skip the meds — not the other way around.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?
One tradeoff: my scheduler is greedy — it just takes the highest priority tasks first and keeps going until time runs out, instead of trying every possible combination to find the "best" mathematically optimal schedule. That means it could technically skip a task that would've fit better if the order were slightly different. But for this use case, that's a fine tradeoff — a pet owner doesn't need a perfectly optimized schedule, they need something fast, predictable, and easy to explain. A more "optimal" algorithm would probably be overkill and harder to explain to a user anyway.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

I used AI mainly for three things: building out the UML diagram, debugging syntax errors as I wrote the classes (I made a lot of small typos — missing spaces in def __init__, mismatched variable names, stuff like that), and getting unstuck on file/folder issues in VS Code that had nothing to do with the actual code logic. The most helpful thing was asking it to explain why something was broken instead of just fixing it for me — like when I asked what lambda actually does instead of just copying it in blind.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?
One moment I didn't just accept a suggestion blindly: after building models.py and Scheduler.py as two separate files, the actual assignment instructions said to use one combined file called pawpal_system.py. Instead of just deleting my old files right away, I asked to test that the new combined file actually worked the same way first — running main.py and comparing the output to what I'd already confirmed worked — before deleting anything. That way I knew nothing broke in the process of restructuring.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

I tested seven specific behaviors: that calling mark_complete() on a task actually changes its completed status from False to True; that calling add_task() on a Pet correctly increases the length of its task list; that the scheduler returns tasks sorted correctly by priority order; that a recurring task creates a fresh, uncompleted copy of itself when create_next_occurrence() is called; that the conflict detector correctly reports zero conflicts when no two tasks share the same start time; that the conflict detector correctly catches and flags a real conflict when two tasks are forced onto the same start time; and that a pet with zero tasks produces an empty schedule without crashing. These mattered because they cover three different levels of the system — small object-level state changes (does marking complete actually update the attribute), algorithmic correctness (does the scheduler sort and schedule in the right order), and edge cases (does the system handle unusual inputs gracefully without breaking) — all of which could silently fail without a test catching them, since the app might still run and look fine on the surface while quietly returning wrong results underneath.



**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?
I'm fairly confident the scheduler works correctly for the core cases — priority sorting, time-limit enforcement, start-time assignment, recurrence, and basic conflict detection are all covered by passing tests, and I also manually verified the output multiple times with different task orders and tight time budgets. That said, my conflict detection test only checks that it correctly reports zero conflicts on a normal schedule — I haven't actually tested a case where two tasks are forced onto the same start time to confirm the detector correctly flags a real conflict, which is a gap.
If I had more time, I'd test:

A pet with zero tasks (does it return an empty schedule cleanly, or error out?)
An owner with zero available minutes (everything should get skipped)
Two tasks with the exact same priority (does the sort stay stable, or does the order become unpredictable?)
A forced conflict case, to confirm find_conflicts() actually catches a duplicate time instead of just correctly reporting none
A recurring task that's never marked complete (should create_next_occurrence() still be callable, or should it require completion first?)

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

I'm most satisfied with the fact that the scheduling logic actually works end-to-end from raw task data all the way to a clear, explained schedule shown in the UI. Getting the priority sorting and time-limit logic right, and being able to see it actually reflected correctly in the terminal output, felt like the moment the project clicked.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?
If I did another pass, I'd clean up my project structure earlier instead of building it as two files and then having to merge everything into one later. I'd also add more edge-case tests before moving on to the UI, instead of after.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

The biggest thing I learned is that small typos and file-structure mistakes (wrong folder, unsaved files, mismatched filenames) caused way more of my actual problems than the logic itself did. Writing the scheduling algorithm was honestly more straightforward than getting my files and imports set up correctly.
