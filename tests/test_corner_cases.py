import pytest
from datetime import datetime, timedelta
from pawpal_system import Owner, Pet, Task, Scheduler, TaskCategory

def test_on_time_overlap():
    """Verify that tasks starting at the exact same time trigger a conflict."""
    owner = Owner("Test Owner")
    pet = Pet("Pet", "cat", 2)
    owner.add_pet(pet)
    
    now = datetime(2026, 4, 1, 12, 0)
    task1 = Task("Task 1", 30, 5, TaskCategory.FEEDING, due_date=now)
    task2 = Task("Task 2", 15, 3, TaskCategory.WALKING, due_date=now)
    
    pet.add_task(task1)
    pet.add_task(task2)
    
    scheduler = Scheduler(owner)
    conflicts = scheduler.detect_conflicts()
    
    assert len(conflicts) == 1
    assert "Task 1" in conflicts[0]
    assert "Task 2" in conflicts[0]

def test_back_to_back_no_overlap():
    """Verify that tasks scheduled back-to-back do NOT trigger a conflict."""
    owner = Owner("Test Owner")
    pet = Pet("Pet", "cat", 2)
    owner.add_pet(pet)
    
    start1 = datetime(2026, 4, 1, 12, 0)
    task1 = Task("Task 1", 30, 5, TaskCategory.FEEDING, due_date=start1)
    
    # Task 2 starts exactly when Task 1 ends
    start2 = start1 + timedelta(minutes=30)
    task2 = Task("Task 2", 15, 3, TaskCategory.WALKING, due_date=start2)
    
    pet.add_task(task1)
    pet.add_task(task2)
    
    scheduler = Scheduler(owner)
    conflicts = scheduler.detect_conflicts()
    
    assert len(conflicts) == 0

def test_empty_plan_behavior():
    """Verify scheduler handles owners/pets with no tasks."""
    owner = Owner("Empty")
    pet = Pet("Lonely", "hamster", 1)
    owner.add_pet(pet)
    
    scheduler = Scheduler(owner)
    plan = scheduler.generate_plan()
    explanation = scheduler.explain_plan()
    
    assert len(plan) == 0
    assert "No tasks scheduled" in explanation

def test_zero_duration_task():
    """Verify that a 0-duration task is handled correctly."""
    # Note: 0-duration should not conflict with something starting at its start time
    owner = Owner("Test")
    pet = Pet("Pet", "dog", 5)
    owner.add_pet(pet)
    
    now = datetime.now()
    task1 = Task("Quick Check", 0, 5, TaskCategory.OTHER, due_date=now)
    task2 = Task("Main Task", 10, 4, TaskCategory.FEEDING, due_date=now + timedelta(seconds=1))
    
    pet.add_task(task1)
    pet.add_task(task2)
    
    scheduler = Scheduler(owner)
    conflicts = scheduler.detect_conflicts()
    assert len(conflicts) == 0

def test_overbooked_owner_warning():
    """Verify explain_plan includes time warning if tasks exceed availability."""
    owner = Owner("Busy", daily_time_available=10) # Only 10 mins
    pet = Pet("BusyPet", "dog", 5)
    owner.add_pet(pet)
    
    pet.add_task(Task("Long Walk", 30, 5, TaskCategory.WALKING))
    
    scheduler = Scheduler(owner)
    scheduler.generate_plan()
    explanation = scheduler.explain_plan()
    
    # Check that explanation mentions the total time vs available time
    assert "Total time required: 30 minutes" in explanation
    assert "Available time: 10 minutes" in explanation

def test_chronological_sorting():
    """Verify that the scheduler returns tasks in chronological order."""
    owner = Owner("Test")
    pet = Pet("Pet", "dog", 5)
    owner.add_pet(pet)
    
    # Add tasks out of order
    now = datetime.now()
    t2 = Task("Late Task", 10, 5, TaskCategory.FEEDING, due_date=now + timedelta(hours=2))
    t1 = Task("Early Task", 10, 5, TaskCategory.WALKING, due_date=now + timedelta(hours=1))
    t3 = Task("Very Late", 10, 5, TaskCategory.PLAY, due_date=now + timedelta(hours=3))
    
    pet.add_task(t2)
    pet.add_task(t1)
    pet.add_task(t3)
    
    scheduler = Scheduler(owner)
    plan = scheduler.generate_plan()
    
    # Should be sorted chronologically
    assert plan[0].name == "Early Task"
    assert plan[1].name == "Late Task"
    assert plan[2].name == "Very Late"
