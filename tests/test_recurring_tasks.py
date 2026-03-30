import pytest
from datetime import datetime, timedelta
from pawpal_system import Task, Pet, TaskCategory, TaskFrequency

def test_daily_recurrence():
    """Verify that completing a daily task creates a new one for the next day."""
    pet = Pet(name="Buddy", species="Dog", age=3)
    due_date = datetime(2026, 3, 29, 10, 0) # Fixed date for testing
    task = Task(
        name="Morning Walk",
        duration=30,
        priority=5,
        category=TaskCategory.WALKING,
        frequency=TaskFrequency.DAILY,
        due_date=due_date
    )
    pet.add_task(task)
    
    assert len(pet.tasks) == 1
    
    # Complete the task
    pet.complete_task(task)
    
    # Check that task is completed
    assert task.completed == True
    
    # Check that a new task was created
    assert len(pet.tasks) == 2
    
    # Find the new task
    new_task = [t for t in pet.tasks if t != task][0]
    assert new_task.name == "Morning Walk"
    assert new_task.frequency == TaskFrequency.DAILY
    assert new_task.due_date == due_date + timedelta(days=1)
    assert new_task.completed == False

def test_weekly_recurrence():
    """Verify that completing a weekly task creates a new one for the next week."""
    pet = Pet(name="Buddy", species="Dog", age=3)
    due_date = datetime(2026, 3, 29, 10, 0)
    task = Task(
        name="Bath",
        duration=60,
        priority=3,
        category=TaskCategory.GROOMING,
        frequency=TaskFrequency.WEEKLY,
        due_date=due_date
    )
    pet.add_task(task)
    
    pet.complete_task(task)
    
    assert len(pet.tasks) == 2
    new_task = [t for t in pet.tasks if t != task][0]
    assert new_task.due_date == due_date + timedelta(weeks=1)

def test_once_not_recurring():
    """Verify that completing a 'once' task does not create a new one."""
    pet = Pet(name="Buddy", species="Dog", age=3)
    task = Task(
        name="Vet Visit",
        duration=45,
        priority=5,
        category=TaskCategory.OTHER,
        frequency=TaskFrequency.ONCE
    )
    pet.add_task(task)
    
    pet.complete_task(task)
    
    assert len(pet.tasks) == 1
    assert task.completed == True

def test_task_duration_multi_step():
    """Verify multiple completions work correctly."""
    pet = Pet(name="Buddy", species="Dog", age=3)
    current_date = datetime.now()
    task = Task("Feed", 10, 5, TaskCategory.FEEDING, TaskFrequency.DAILY, current_date)
    pet.add_task(task)
    
    # Complete 3 times
    for i in range(1, 4):
        # Find the current incomplete task
        active_task = [t for t in pet.tasks if not t.completed][0]
        expected_date = current_date + timedelta(days=i-1)
        assert active_task.due_date.date() == expected_date.date()
        
        pet.complete_task(active_task)
        assert len(pet.tasks) == i + 1
