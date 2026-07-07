import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown("""
Welcome to PawPal+ — a smart daily planner for your pet's care tasks.
""")

with st.expander("Scenario", expanded=True):
    st.markdown("""
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.
""")

with st.expander("What you need to build", expanded=True):
    st.markdown("""
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
""")

st.divider()

# --- Owner + Pet stored in session state ---
st.subheader("Owner & Pet Info")

owner_name = st.text_input("Owner name", value="Jordan")
available_minutes = st.number_input("Available minutes today", min_value=10, max_value=480, value=180)
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])

if "owner" not in st.session_state or st.session_state.owner.name != owner_name:
    st.session_state.owner = Owner(owner_name, available_minutes, preferences="")

if "pet" not in st.session_state or st.session_state.pet.name != pet_name:
    st.session_state.pet = Pet(pet_name, species, [])

# --- Task form ---
st.markdown("### Tasks")
st.caption("Add tasks below. They feed directly into your scheduler.")

if "tasks" not in st.session_state:
    st.session_state.tasks = []

col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

if st.button("Add task"):
    st.session_state.tasks.append(
        {"title": task_title, "duration_minutes": int(duration), "priority": priority}
    )

if st.session_state.tasks:
    st.write("Current tasks:")
    st.table(st.session_state.tasks)
else:
    st.info("No tasks yet. Add one above.")

# --- Filter ---
st.divider()
st.subheader("Filter Tasks")
filter_choice = st.radio(
    "Show tasks by status:",
    ["All", "Incomplete only", "Completed only"],
    horizontal=True
)

st.divider()

# --- Generate schedule ---
st.subheader("Build Schedule")

if st.button("Generate schedule"):
    if not st.session_state.tasks:
        st.warning("Add at least one task before generating a schedule.")
    else:
        priority_map = {"high": 1, "medium": 2, "low": 3}

        task_objects = []
        for t in st.session_state.tasks:
            task_objects.append(
                Task(
                    name=t["title"],
                    duration=t["duration_minutes"],
                    priority=priority_map[t["priority"]],
                    category="general",
                    preferred_time=None,
                    is_required=False,
                )
            )

        # Update the existing session-state Owner and Pet instead of rebuilding them
        st.session_state.owner.available_minutes = available_minutes
        st.session_state.pet.tasks = task_objects

        scheduler = Scheduler(default_start_time="08:00")
        plan = scheduler.generate_plan(st.session_state.pet, st.session_state.owner)

        st.success(f"Schedule generated for {st.session_state.pet.name}!")
        st.subheader(f"Today's Schedule for {st.session_state.pet.name}")

        # Apply filter
        if filter_choice == "Incomplete only":
            display_tasks = scheduler.filter_tasks(plan.scheduled_tasks, completed=False)
        elif filter_choice == "Completed only":
            display_tasks = scheduler.filter_tasks(plan.scheduled_tasks, completed=True)
        else:
            display_tasks = plan.scheduled_tasks

        # Sort by time before displaying
        display_tasks = scheduler.sort_by_time(display_tasks)

        if display_tasks:
            st.markdown("**Scheduled (sorted by time):**")
            for task in display_tasks:
                st.write(f"🕐 {task.start_time} — **{task.name}** ({task.duration} min)")
                st.caption(plan.explanations[task.name])
        else:
            st.info("No tasks match this filter.")

        if plan.skipped_tasks:
            st.markdown("**Skipped:**")
            for task in plan.skipped_tasks:
                st.write(f"⏭️ **{task.name}** ({task.duration} min)")
                st.caption(plan.explanations[task.name])

        # Conflict check
        conflicts = scheduler.find_conflicts(plan)
        if conflicts:
            st.warning("⚠️ Conflicts detected:")
            for t1, t2 in conflicts:
                st.write(f"'{t1.name}' and '{t2.name}' are both scheduled at {t1.start_time}")
        else:
            st.success("✅ No scheduling conflicts detected.")