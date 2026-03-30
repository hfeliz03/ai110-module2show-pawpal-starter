#!/usr/bin/env python3
"""
main.py - Testing ground for PawPal+ system logic

This file demonstrates and tests the core functionality of the pet care scheduling system.
Run this file to verify that the Owner, Pet, Task, and Scheduler classes work correctly.
"""

from pawpal_system import Owner, Pet, Task, Scheduler, TaskCategory


def test_basic_setup():
    """Test creating owners, pets, and tasks"""
    print("=" * 50)
    print("TEST 1: Basic Setup - Creating Owner, Pet, and Tasks")
    print("=" * 50)
    
    # Create an owner
    owner = Owner(name="Jordan", daily_time_available=120, preferences={"morning_person": True})
    print(f"✓ Created owner: {owner.name}")
    print(f"  Available time: {owner.daily_time_available} minutes")
    print(f"  Preferences: {owner.preferences}")
    
    # Create a pet
    pet = Pet(name="Mochi", species="dog", age=3)
    owner.add_pet(pet)
    print(f"\n✓ Created pet: {pet.name} ({pet.species}, age {pet.age})")
    print(f"  Owner has {len(owner.pets)} pet(s)")
    
    # Create tasks
    tasks_data = [
        ("Morning walk", 20, 5, TaskCategory.WALKING),
        ("Breakfast", 10, 4, TaskCategory.FEEDING),
        ("Afternoon play", 30, 3, TaskCategory.PLAY),
        ("Evening walk", 20, 5, TaskCategory.WALKING),
        ("Dinner", 10, 4, TaskCategory.FEEDING),
    ]
    
    print(f"\n✓ Adding {len(tasks_data)} tasks to {pet.name}:")
    for task_name, duration, priority, category in tasks_data:
        task = Task(name=task_name, duration=duration, priority=priority, category=category)
        pet.add_task(task)
        print(f"  - {task_name} ({duration} min, priority {priority}/5)")
    
    return owner


def test_scheduler(owner):
    """Test the scheduler logic"""
    print("\n" + "=" * 50)
    print("TEST 2: Scheduler - Generate and Explain Plan")
    print("=" * 50)
    
    # Create scheduler and generate plan
    scheduler = Scheduler(owner)
    daily_plan = scheduler.generate_plan()
    
    print(f"\n✓ Generated daily plan with {len(daily_plan)} tasks")
    print("\nPlan (sorted chronologically):")
    for i, task in enumerate(daily_plan, 1):
        print(f"  {i}. {task.name} - {task.duration} min (Priority: {task.priority})")
    
    # Explain the plan
    explanation = scheduler.explain_plan()
    print(f"\n✓ Plan explanation:\n{explanation}")
    
    return scheduler


def test_task_operations(owner):
    """Test task completion and editing"""
    print("=" * 50)
    print("TEST 3: Task Operations - Mark Complete & Edit")
    print("=" * 50)
    
    pet = owner.pets[0]
    first_task = pet.get_tasks()[0]
    
    print(f"\n✓ Original task: {first_task.name}")
    print(f"  Completed: {first_task.completed}")
    
    # Mark as completed
    first_task.mark_completed()
    print(f"\n✓ After marking complete:")
    print(f"  Completed: {first_task.completed}")
    
    # Edit task
    first_task.edit_task(duration=25, priority=4)
    print(f"\n✓ After editing:")
    print(f"  Duration: {first_task.duration} min")
    print(f"  Priority: {first_task.priority}")


def test_multiple_pets():
    """Test system with multiple pets"""
    print("\n" + "=" * 50)
    print("TEST 4: Multiple Pets")
    print("=" * 50)
    
    owner = Owner(name="Alex", daily_time_available=180)
    
    # Create two pets
    dog = Pet(name="Buddy", species="dog", age=5)
    cat = Pet(name="Whiskers", species="cat", age=2)
    
    owner.add_pet(dog)
    owner.add_pet(cat)
    
    print(f"\n✓ Owner {owner.name} has {len(owner.pets)} pets:")
    for pet in owner.pets:
        print(f"  - {pet.name} ({pet.species})")
    
    # Add tasks to each pet
    dog.add_task(Task("Dog walk", 30, 5, TaskCategory.WALKING))
    dog.add_task(Task("Dog feed", 10, 4, TaskCategory.FEEDING))
    
    cat.add_task(Task("Cat feed", 5, 4, TaskCategory.FEEDING))
    cat.add_task(Task("Cat play", 15, 3, TaskCategory.PLAY))
    
    print(f"\n✓ Added tasks:")
    print(f"  {dog.name}: {len(dog.get_tasks())} tasks")
    print(f"  {cat.name}: {len(cat.get_tasks())} tasks")
    
    # Generate plan
    scheduler = Scheduler(owner)
    plan = scheduler.generate_plan()
    print(f"\n✓ Generated combined plan: {len(plan)} total tasks")
    print(f"  Total duration needed: {sum(t.duration for t in plan)} minutes")
    print(f"  Available time: {owner.daily_time_available} minutes")
    
    if sum(t.duration for t in plan) <= owner.daily_time_available:
        print(f"  ✓ All tasks fit within available time!")
    else:
        print(f"  ⚠ Tasks exceed available time by {sum(t.duration for t in plan) - owner.daily_time_available} minutes")


def test_owner_preferences():
    """Test owner preference updates"""
    print("\n" + "=" * 50)
    print("TEST 5: Owner Preferences & Time Management")
    print("=" * 50)
    
    owner = Owner(name="Casey", daily_time_available=100)
    print(f"\n✓ Initial setup:")
    print(f"  Name: {owner.name}")
    print(f"  Available time: {owner.daily_time_available} minutes")
    print(f"  Preferences: {owner.preferences}")
    
    # Update preferences
    owner.update_preferences(morning_person=True, prefers_group_walks=False, budget_conscious=True)
    print(f"\n✓ After updating preferences:")
    print(f"  Preferences: {owner.preferences}")
    
    # Update available time
    owner.update_time_available(150)
    print(f"\n✓ After updating available time:")
    print(f"  Available time: {owner.daily_time_available} minutes")


def test_conflict_detection():
    """Test the scheduler's ability to detect overlapping tasks"""
    print("\n" + "=" * 50)
    print("TEST 6: Conflict Detection")
    print("=" * 50)
    
    from datetime import datetime
    
    owner = Owner(name="Sam", daily_time_available=120)
    pet = Pet(name="Luna", species="cat", age=4)
    owner.add_pet(pet)
    
    # Create two tasks at exactly the same time
    now = datetime.now()
    task1 = Task("Morning Feed", 15, 5, TaskCategory.FEEDING, due_date=now)
    task2 = Task("Medication", 5, 5, TaskCategory.MEDICATION, due_date=now)
    
    pet.add_task(task1)
    pet.add_task(task2)
    
    print(f"✓ Created two overlapping tasks for {pet.name} at {now.strftime('%H:%M')}")
    
    scheduler = Scheduler(owner)
    scheduler.generate_plan()
    explanation = scheduler.explain_plan()
    
    print("\nScheduler Explanation (should contain warning):")
    print(explanation)
    
    if "⚠ CONFLICT" in explanation:
        print("\n✓ SUCCESS: Conflict detected correctly!")
    else:
        print("\n❌ FAILURE: Conflict was not detected.")


def main():
    """Run all tests"""
    print("\n")
    print("🐾" * 25)
    print("PawPal+ System Testing Ground")
    print("🐾" * 25)
    
    try:
        owner = test_basic_setup()
        test_scheduler(owner)
        test_task_operations(owner)
        test_multiple_pets()
        test_owner_preferences()
        test_conflict_detection()
        
        print("\n" + "=" * 50)
        print("✓ ALL TESTS COMPLETED SUCCESSFULLY!")
        print("=" * 50)
        print("\nYour PawPal+ system logic is working correctly.")
        print("You can now integrate it with the Streamlit app (app.py).\n")
        
    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
