import pytest
from pawpal_system import Task, Pet, TaskCategory


def test_task_completion():
    """
    Test the functionality of the `mark_completed` method in the `Task` class.
    This test ensures that:
    1. A newly created task has its `completed` status set to `False` by default.
    2. Calling the `mark_completed` method updates the `completed` status to `True`.
    """
    """Verify that calling mark_completed() actually changes the task's status."""
    # Create a task with default completed status (False)
    task = Task(
        name="Feed the dog",
        duration=10,
        priority=3,
        category=TaskCategory.FEEDING
    )
    
    # Verify initial status is False
    assert task.completed == False
    
    # Mark task as completed
    task.mark_completed()
    
    # Verify status changed to True
    assert task.completed == True


def test_task_addition():
    """Verify that adding a task to a Pet increases that pet's task count."""
    # Create a pet
    pet = Pet(name="Buddy", species="Dog", age=3)
    
    # Verify pet starts with no tasks
    assert len(pet.tasks) == 0
    
    # Create and add a task
    task = Task(
        name="Walk the dog",
        duration=30,
        priority=4,
        category=TaskCategory.WALKING
    )
    pet.add_task(task)
    
    # Verify task count increased to 1
    assert len(pet.tasks) == 1
    
    # Add another task and verify count increases again
    task2 = Task(
        name="Play fetch",
        duration=20,
        priority=2,
        category=TaskCategory.PLAY
    )
    pet.add_task(task2)
    
    # Verify task count is now 2
    assert len(pet.tasks) == 2
