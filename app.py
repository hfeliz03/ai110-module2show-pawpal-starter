import streamlit as st
from pawpal_system import *
from ai_reviewer import PawPalAIReviewer

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to PawPal+! A pet care planning assistant that helps you organize and schedule 
care tasks for your pet(s) based on time, priority, and your preferences.
"""
)

with st.expander("Scenario", expanded=False):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.
"""
    )

# Initialize session state for owner and current pet
if "owner" not in st.session_state:
    st.session_state.owner = None

if "current_pet" not in st.session_state:
    st.session_state.current_pet = None

if "ai_review_result" not in st.session_state:
    st.session_state.ai_review_result = None

st.divider()

# OWNER SETUP SECTION
st.subheader("👤 Owner Setup")

col1, col2 = st.columns(2)
with col1:
    owner_name = st.text_input("Your name", value="Jordan", key="owner_name_input")
with col2:
    daily_time = st.number_input(
        "Available time per day (minutes)", 
        min_value=30, 
        max_value=480, 
        value=120,
        key="daily_time_input"
    )

if st.button("Create/Update Owner Profile", key="create_owner_btn"):
    st.session_state.owner = Owner(
        name=owner_name,
        daily_time_available=daily_time,
        preferences={}
    )
    st.success(f"✓ Owner profile created: {owner_name} ({daily_time} min/day available)")

# Show owner status
if st.session_state.owner:
    st.info(f"📌 Current Owner: **{st.session_state.owner.name}** | Available: {st.session_state.owner.daily_time_available} min/day")
else:
    st.warning("Please create an owner profile first.")

st.divider()

# PET SETUP SECTION
if st.session_state.owner:
    st.subheader("🐾 Pet Setup")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        pet_name = st.text_input("Pet name", value="Mochi", key="pet_name_input")
    with col2:
        species = st.selectbox("Species", ["dog", "cat", "rabbit", "bird", "other"], key="species_input")
    with col3:
        pet_age = st.number_input("Pet age (years)", min_value=0, max_value=25, value=3, key="pet_age_input")
    
    if st.button("Add Pet", key="add_pet_btn"):
        new_pet = Pet(name=pet_name, species=species, age=pet_age)
        st.session_state.owner.add_pet(new_pet)
        st.session_state.current_pet = new_pet
        st.success(f"✓ Added pet: {pet_name} ({species}, age {pet_age})")
    
    # Show existing pets
    if st.session_state.owner.pets:
        st.markdown("#### Your Pets:")
        for i, pet in enumerate(st.session_state.owner.pets):
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"**{pet.name}** - {pet.species.capitalize()}, age {pet.age}")
            with col2:
                if st.button("Select", key=f"select_pet_{i}"):
                    st.session_state.current_pet = pet

st.divider()

# TASKS SECTION
if st.session_state.current_pet:
    st.subheader(f"📋 Tasks for {st.session_state.current_pet.name}")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        task_name = st.text_input("Task name", value="Morning walk", key="task_name_input")
    with col2:
        task_duration = st.number_input("Duration (min)", min_value=1, max_value=240, value=20, key="task_duration_input")
    with col3:
        priority_str = st.selectbox("Priority", ["low", "medium", "high"], key="task_priority_input")
    with col4:
        category_str = st.selectbox(
            "Category",
            ["Walking", "Feeding", "Medication", "Grooming", "Play", "Other"],
            key="task_category_input"
        )
    with col5:
        frequency_str = st.selectbox(
            "Frequency",
            ["Once", "Daily", "Weekly"],
            key="task_frequency_input"
        )
    
    if st.button("Add Task", key="add_task_btn"):
        # Convert priority string to numeric (1-5)
        priority_map = {"low": 2, "medium": 3, "high": 5}
        priority_num = priority_map[priority_str]
        
        # Convert category string to TaskCategory enum
        category_map = {
            "Walking": TaskCategory.WALKING,
            "Feeding": TaskCategory.FEEDING,
            "Medication": TaskCategory.MEDICATION,
            "Grooming": TaskCategory.GROOMING,
            "Play": TaskCategory.PLAY,
            "Other": TaskCategory.OTHER
        }
        category = category_map[category_str]
        
        # Convert frequency string to TaskFrequency enum
        frequency_map = {
            "Once": TaskFrequency.ONCE,
            "Daily": TaskFrequency.DAILY,
            "Weekly": TaskFrequency.WEEKLY
        }
        frequency = frequency_map[frequency_str]
        
        # Create and add task
        new_task = Task(
            name=task_name,
            duration=task_duration,
            priority=priority_num,
            category=category,
            frequency=frequency
        )
        st.session_state.current_pet.add_task(new_task)
        st.success(f"✓ Added task: {task_name}")
    
    # Global Conflict Warnings
    scheduler = Scheduler(st.session_state.owner)
    conflicts = scheduler.detect_conflicts()
    if conflicts:
        st.warning("⚠️ **Scheduling Conflicts Detected:**")
        for conflict in conflicts:
            st.write(f"- {conflict}")

    # Display current tasks (Sorted chronologically)
    all_tasks = scheduler.generate_plan()
    if all_tasks:
        st.markdown(f"#### All Scheduled Tasks (Sorted Chronologically):")
        
        task_table_data = []
        for i, task in enumerate(all_tasks):
            # Find which pet this task belongs to (for display)
            pet_name = "Unknown"
            for pet in st.session_state.owner.pets:
                if task in pet.tasks:
                    pet_name = pet.name
                    break
            
            task_table_data.append({
                "Status": "✅" if task.completed else "⏳",
                "Pet": pet_name,
                "Task": task.name,
                "Time": task.due_date.strftime('%H:%M'),
                "Duration": f"{task.duration} min",
                "Repeat": task.frequency.value,
                "ID": i # Just for reference
            })
        
        # Display as a table for professional look
        st.table(task_table_data)
        
        # Actions (Mark Complete)
        st.markdown("#### Actions:")
        cols = st.columns(4)
        for i, task in enumerate(all_tasks):
            if not task.completed:
                with cols[i % 4]:
                    if st.button(f"Done: {task.name}", key=f"complete_btn_{i}_{task.name}"):
                        # We need to find the pet to call complete_task
                        for pet in st.session_state.owner.pets:
                            if task in pet.tasks:
                                pet.complete_task(task)
                                break
                        st.rerun()
    else:
        st.info("No tasks scheduled yet. Add tasks above!")

st.divider()

# SCHEDULE GENERATION SECTION
if st.session_state.owner and st.session_state.owner.pets:
    st.subheader("📅 Generate Daily Schedule")
    st.caption("Creates an optimized plan based on priorities and available time")
    
    if st.button("Generate Schedule", key="generate_schedule_btn"):
        # Create scheduler
        scheduler = Scheduler(st.session_state.owner)
        
        # Generate plan
        daily_plan = scheduler.generate_plan()
        
        if daily_plan:
            st.success("✓ Schedule generated!")
            
            # Display the plan
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Total Tasks", len(daily_plan))
            with col2:
                total_time = sum(task.duration for task in daily_plan)
                st.metric("Total Time Required", f"{total_time} min")
            
            # Show plan table
            st.markdown("#### Your Daily Chronological Schedule:")
            plan_list = []
            for i, task in enumerate(daily_plan, 1):
                plan_list.append({
                    "Time": task.due_date.strftime('%H:%M'),
                    "Task": task.name,
                    "Duration": f"{task.duration} min",
                    "Priority": f"{task.priority}/5",
                    "Category": task.category.value
                })
            st.table(plan_list)
            
            # Show explanation and warnings
            st.markdown("#### Schedule Analysis:")
            explanation = scheduler.explain_plan()
            st.info(explanation)
            
            # Time availability warning
            total_time = sum(task.duration for task in daily_plan)
            if total_time > st.session_state.owner.daily_time_available:
                st.warning(
                    f"⚠️ Total time ({total_time} min) exceeds available time "
                    f"({st.session_state.owner.daily_time_available} min) by "
                    f"{total_time - st.session_state.owner.daily_time_available} minutes"
                )
            else:
                st.success(
                    f"✓ All tasks fit! {st.session_state.owner.daily_time_available - total_time} "
                    f"minutes available after tasks"
                )
        else:
            st.info("Add some tasks to your pet(s) to generate a schedule.")

    st.divider()
    st.subheader("🤖 AI Schedule Review")
    st.caption("Retrieves local pet-care guidance before reviewing the schedule")

    ai_question = st.text_area(
        "Optional question for PawPal AI Care Coach",
        value="Review this schedule and tell me what care coverage might be missing.",
        key="ai_question_input"
    )

    if st.button("Run AI Review", key="run_ai_review_btn"):
        scheduler = Scheduler(st.session_state.owner)
        reviewer = PawPalAIReviewer()
        try:
            st.session_state.ai_review_result = reviewer.review_schedule(
                st.session_state.owner,
                scheduler,
                ai_question
            )
        except Exception as exc:
            st.session_state.ai_review_result = None
            st.error(f"AI review failed safely: {exc}")

    result = st.session_state.ai_review_result
    if result:
        mode_label = "Fallback grounded reviewer" if result.used_fallback else "OpenAI reviewer"
        st.success(f"AI review completed using: {mode_label}")
        st.metric("Confidence", f"{result.confidence:.2f}")

        st.markdown("#### Summary")
        st.write(result.summary)

        st.markdown("#### Recommendations")
        for recommendation in result.recommendations:
            st.write(f"- {recommendation}")

        if result.warnings:
            st.markdown("#### Guardrails and Warnings")
            for warning in result.warnings:
                st.warning(warning)

        if result.citations:
            st.markdown("#### Retrieved Evidence")
            for citation in result.citations:
                st.write(f"- {citation}")
else:
    st.info("Create an owner profile and add a pet to generate a schedule.")
